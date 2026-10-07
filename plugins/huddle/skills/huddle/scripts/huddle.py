#!/usr/bin/env python3
"""huddle — ask the user a rich question in an agterm HTML overlay and print the answer as JSON.

  huddle SPEC.json | huddle - < spec.json      ask from a JSON spec (see SKILL.md for the schema)
  huddle q "Prompt" "Label|subtitle" "*Recommended|subtitle" ... [--multi] [--context MD]
  huddle wait PAGE_ID                          resume waiting after a timeout (exit 4)
  huddle demo [NAME ...]                       open bundled demos (no name: list them)
  huddle templates                             list templates with their one-line purpose
  huddle render SPEC -o FILE                   build the page only, open nothing

Common flags: --follow (pull the user to this session), --size N (floating panel, % of the
session), --timeout SEC (default 570, under the Bash tool's 600 s cap), --browser (force the
local-browser fallback), --no-status (leave the sidebar glyph alone).

Exit codes: 0 answered or "chat" (user wants to discuss in the terminal), 2 dismissed (closed
unanswered), 3 no way to show it, 4 still pending after --timeout (run `huddle wait ID`), 1 error.
"""
import argparse
import base64
import glob
import http.server
import json
import mimetypes
import os
import secrets
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import webbrowser

HERE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RUNTIME = os.path.join(HERE, "runtime")
TEMPLATES = os.path.join(HERE, "templates")
DEMOS = os.path.join(HERE, "demos")
CACHE = os.path.expanduser("~/.cache/huddle")
DEFAULTS = os.path.join(HERE, "defaults.json")
OUTDIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "huddle")
MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.min.js"
MERMAID_FILE = os.path.join(CACHE, "mermaid-11.12.0.min.js")
ASKING = ["blocked", "--blink", "--color", "#f59e0b", "--shape", "triangle"]  # agent-lights "asking"
WORKING = ["active", "--blink", "--color", "#3b82f6"]                         # agent-lights "working"
MAX_IMAGE = 8 * 1024 * 1024


def die(msg, code=1):
    print(json.dumps({"status": "error", "error": msg}))
    sys.exit(code)


# ---------- spec loading ----------

def load_spec(arg):
    if arg in (None, "-"):
        if sys.stdin.isatty():
            die("no spec: pass a JSON file or pipe one on stdin")
        raw = sys.stdin.read()
    else:
        with open(os.path.expanduser(arg), encoding="utf-8") as f:
            raw = f.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"spec is not valid JSON: {e}")


def check_spec(spec):
    qs = spec.get("questions") or [spec]
    if not isinstance(qs, list) or not qs:
        die("spec needs `questions` (a list) or top-level question fields")
    ids = set()
    for i, q in enumerate(qs):
        qid = q.get("id") or (f"q{i + 1}" if spec.get("questions") else "answer")
        if qid in ids:
            die(f"duplicate question id {qid!r}")
        ids.add(qid)
        opts = q.get("options") or []
        if len(opts) > 9:
            die(f"question {qid!r} has {len(opts)} options; keys 1-9 cover at most 9 (aim for 6)")
        oids = [o if isinstance(o, str) else o.get("id") for o in opts]
        if len([x for x in oids if x]) != len(set(x for x in oids if x)):
            die(f"question {qid!r} has duplicate option ids")
        if not q.get("prompt") and not spec.get("title"):
            die(f"question {qid!r} has no prompt")


def embed_images(node, base):
    """Replace local `image` paths with data URIs: a page without --cwd has no file access."""
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k == "image" and isinstance(v, str) and not v.startswith(("http://", "https://", "data:")):
                p = os.path.expanduser(v)
                if not os.path.isabs(p):
                    p = os.path.join(base, p)
                if not os.path.isfile(p):
                    node[k] = ""
                    node.setdefault("alt", f"missing image: {v}")
                    continue
                if os.path.getsize(p) > MAX_IMAGE:
                    die(f"image too large to embed (>8MB): {v}")
                mime = mimetypes.guess_type(p)[0] or "image/png"
                with open(p, "rb") as f:
                    node[k] = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
            else:
                embed_images(v, base)
    elif isinstance(node, list):
        for v in node:
            embed_images(v, base)


def uses_mermaid(node):
    if isinstance(node, dict):
        return "mermaid" in node or any(uses_mermaid(v) for v in node.values())
    if isinstance(node, list):
        return any(uses_mermaid(v) for v in node)
    return False


def mermaid_js():
    if os.path.isfile(MERMAID_FILE) and os.path.getsize(MERMAID_FILE) > 100_000:
        with open(MERMAID_FILE, encoding="utf-8") as f:
            return f.read()
    try:
        os.makedirs(CACHE, exist_ok=True)
        with urllib.request.urlopen(MERMAID_URL, timeout=20) as r:
            data = r.read().decode("utf-8")
        with open(MERMAID_FILE, "w", encoding="utf-8") as f:
            f.write(data)
        return data
    except Exception as e:  # diagrams fall back to their source text
        print(f"huddle: mermaid unavailable ({e}); diagrams show as source", file=sys.stderr)
        return ""


def build_html(spec, base):
    embed_images(spec, base)
    def read(name):
        with open(os.path.join(RUNTIME, name), encoding="utf-8") as f:
            return f.read()
    css, js = read("huddle.css"), read("huddle.js")
    mm = mermaid_js() if uses_mermaid(spec) else ""
    data = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\u0021--")
    title = spec.get("title") or (spec.get("questions") or [spec])[0].get("prompt") or "Question"
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{esc(title)[:120]}</title><style>{css}</style></head>"
        f"<body><div id=\"app\"></div><script type=\"application/json\" id=\"hd-spec\">{data}</script>"
        + (f"<script>{mm}</script>" if mm else "")
        + f"<script>{js}</script></body></html>"
    )


def write_page(html):
    os.makedirs(OUTDIR, exist_ok=True)
    now = time.time()
    for old in glob.glob(os.path.join(OUTDIR, "*.html")):  # keep a day for debugging
        try:
            if now - os.path.getmtime(old) > 86400:
                os.remove(old)
        except OSError:
            pass
    path = os.path.join(OUTDIR, time.strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(3) + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def defaults():
    try:
        with open(DEFAULTS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def apply_defaults(spec):
    d = defaults()
    spec.setdefault("style", d.get("style", "refined"))
    spec.setdefault("review", d.get("review", "auto"))
    return spec


def auto_size(spec):
    """Pick the floating-panel percent from how much the page has to show."""
    qs = spec.get("questions") or [spec]
    blob = json.dumps(spec)
    visual = any(k in blob for k in ('"preview"', '"mermaid"', '"chart"', '"image"', '"stats"', '"table"'))
    compare = any(q.get("layout") == "compare" for q in qs)
    nopts = max((len(q.get("options") or []) for q in qs), default=0)
    if visual or compare or len(qs) > 2:
        return 90
    if spec.get("width") == "narrow" and nopts <= 4 and len(blob) < 1500:
        return 66
    return 78


# ---------- agterm ----------

def agtermctl():
    return shutil.which("agtermctl") or next((p for p in ("/opt/homebrew/bin/agtermctl", "/Applications/agterm.app/Contents/MacOS/agtermctl") if os.path.exists(p)), None)


def ctl(*args, check=True):
    exe = agtermctl()
    cmd = [exe, *args]
    if os.environ.get("AGTERM_SOCKET"):
        cmd += ["--socket", os.environ["AGTERM_SOCKET"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode not in (0, 2):
        raise RuntimeError((r.stderr or r.stdout).strip() or f"agtermctl exited {r.returncode}")
    return r


def in_agterm():
    return os.environ.get("AGTERM_ENABLED") == "1" and os.environ.get("AGTERM_SESSION_ID") and agtermctl()


def set_status(args):
    sid, pid = os.environ.get("AGTERM_SESSION_ID"), os.environ.get("AGTERM_PANE_ID")
    extra = ["--pane-id", pid] if pid else []
    try:
        ctl("session", "status", *args, "--target", sid, *extra, check=False)
    except Exception:
        pass


def open_overlay(path, a, spec):
    args = ["session", "overlay", "open", "--html", path, "--js", "--target", os.environ["AGTERM_SESSION_ID"], "--json"]
    if a.follow:
        args.append("--follow")
    size = a.size or spec.get("size") or defaults().get("size", "auto")
    if a.full or size == "full":
        size = None
    elif size == "auto":
        size = auto_size(spec)
    if size:
        args += ["--size-percent", str(int(size))]
    if a.chromeless:
        args.append("--chromeless")
    r = ctl(*args, check=False)
    try:
        reply = json.loads(r.stdout)
    except json.JSONDecodeError:
        die((r.stderr or r.stdout).strip() or "overlay open failed")
    if not reply.get("ok", True) or r.returncode != 0:
        die(reply.get("error") or (r.stderr or r.stdout).strip())
    res = reply.get("result", reply)
    return res.get("pageID") or res.get("id")


def wait_page(page_id, timeout, status=True):
    deadline = time.time() + timeout
    if status:
        set_status(ASKING)
    still_open = False
    try:
        while True:
            r = ctl("session", "overlay", "result", "--page", page_id, "--json", check=False)
            try:
                o = json.loads(r.stdout).get("result", {}).get("pageOutcome", {})
            except json.JSONDecodeError:
                o = {}
            out = o.get("outcome")
            if out == "submitted":
                try:
                    ans = json.loads(o.get("value") or "{}")
                except json.JSONDecodeError:
                    ans = {"status": "answered", "answers": {"answer": {"selected": [], "labels": [], "text": o.get("value")}}}
                ans["pageID"] = page_id
                print(json.dumps(ans, ensure_ascii=False, indent=1))
                return 0
            if out == "dismissed":
                print(json.dumps({"status": "dismissed", "pageID": page_id}))
                return 2
            if not out and "no such page" in (r.stderr + r.stdout):
                die(f"no such page {page_id}")
            if time.time() > deadline:
                still_open = True  # the question is still up: keep the "asking" glyph
                print(json.dumps({"status": "pending", "pageID": page_id,
                                  "hint": f"still open; run `huddle wait {page_id}` to keep waiting"}))
                return 4
            time.sleep(0.4)
    finally:
        if status and not still_open:
            set_status(WORKING)


# ---------- browser fallback ----------

def ask_in_browser(html, timeout):
    answer = {}
    done = threading.Event()

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            body = html.encode()
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            n = int(self.headers.get("content-length", 0))
            try:
                answer.update(json.loads(self.rfile.read(n)))
            except json.JSONDecodeError:
                pass
            self.send_response(204)
            self.end_headers()
            done.set()

    srv = socketserver.TCPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"huddle: opened {url}", file=sys.stderr)
    webbrowser.open(url)
    ok = done.wait(timeout)
    srv.shutdown()
    if not ok:
        print(json.dumps({"status": "timeout", "url": url}))
        return 4
    print(json.dumps(answer, ensure_ascii=False, indent=1))
    return 0


# ---------- commands ----------

def ask(spec, a, base):
    check_spec(spec)
    apply_defaults(spec)
    if a.style:
        spec["style"] = a.style
    if a.review:
        spec["review"] = a.review
    html = build_html(spec, base)
    if a.browser or not in_agterm():
        if not a.browser and os.environ.get("HUDDLE_NO_BROWSER"):
            die("not inside agterm and HUDDLE_NO_BROWSER is set", 3)
        return ask_in_browser(html, a.timeout)
    path = write_page(html)
    page = open_overlay(path, a, spec)
    if a.no_wait:
        print(json.dumps({"status": "open", "pageID": page, "file": path}))
        return 0
    return wait_page(page, a.timeout, status=not a.no_status)


def quick_spec(a):
    opts = []
    for i, raw in enumerate(a.options):
        rec = raw.startswith("*")
        label, _, sub = raw.lstrip("*").partition("|")
        o = {"id": f"o{i + 1}", "label": label.strip()}
        if sub.strip():
            o["subtitle"] = sub.strip()
        if rec:
            o["recommended"] = True
        opts.append(o)
    spec = {"prompt": a.prompt, "options": opts}
    if a.multi:
        spec["mode"] = "multi"
    if a.context:
        spec["context"] = a.context
    if a.title:
        spec["title"] = a.title
    if opts:
        spec["width"] = "narrow"
    return spec


def list_dir(d):
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            with open(p, encoding="utf-8") as f:
                s = json.load(f)
            rows.append((os.path.basename(p)[:-5], s.get("_about", "")))
        except Exception as e:
            rows.append((os.path.basename(p)[:-5], f"(unreadable: {e})"))
    return rows


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--follow", action="store_true", help="select this session so the user sees it now")
    common.add_argument("--size", type=int, help="floating panel, percent of the session (1-100); default auto")
    common.add_argument("--full", action="store_true", help="cover the whole session instead of a floating panel")
    common.add_argument("--style", choices=["refined", "minimal", "bold", "terminal"], help="visual style (default from defaults.json)")
    common.add_argument("--review", choices=["auto", "always", "never"], help="show the answer review before sending")
    common.add_argument("--chromeless", action="store_true", help="hide the overlay's title strip")
    common.add_argument("--timeout", type=float, default=570, help="seconds to wait (default 570)")
    common.add_argument("--no-wait", action="store_true", help="open and print the page id; read it later with `huddle wait`")
    common.add_argument("--no-status", action="store_true", help="leave the sidebar status glyph alone")
    common.add_argument("--browser", action="store_true", help="use the local browser fallback even inside agterm")

    argv = sys.argv[1:]
    sub = argv[0] if argv and argv[0] in ("q", "wait", "demo", "templates", "render", "ask") else None
    if sub is None:
        argv = ["ask", *argv]
        sub = "ask"

    p = argparse.ArgumentParser(prog="huddle", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd")
    s_ask = sp.add_parser("ask", parents=[common]); s_ask.add_argument("spec", nargs="?")
    s_q = sp.add_parser("q", parents=[common]); s_q.add_argument("prompt"); s_q.add_argument("options", nargs="*")
    s_q.add_argument("--multi", action="store_true"); s_q.add_argument("--context"); s_q.add_argument("--title")
    s_w = sp.add_parser("wait", parents=[common]); s_w.add_argument("page_id")
    s_d = sp.add_parser("demo", parents=[common]); s_d.add_argument("names", nargs="*")
    sp.add_parser("templates")
    s_r = sp.add_parser("render"); s_r.add_argument("spec"); s_r.add_argument("-o", "--out", required=True)
    a = p.parse_args(argv)

    if a.cmd == "ask":
        base = os.path.dirname(os.path.abspath(a.spec)) if a.spec not in (None, "-") else os.getcwd()
        sys.exit(ask(load_spec(a.spec), a, base))
    if a.cmd == "q":
        sys.exit(ask(quick_spec(a), a, os.getcwd()))
    if a.cmd == "wait":
        if not in_agterm():
            die("not inside agterm", 3)
        sys.exit(wait_page(a.page_id, a.timeout, status=not a.no_status))
    if a.cmd == "templates":
        for name, about in list_dir(TEMPLATES):
            print(f"{name:18} {about}")
        print(f"\n{TEMPLATES}")
        return
    if a.cmd == "demo":
        if not a.names:
            for name, about in list_dir(DEMOS) + list_dir(TEMPLATES):
                print(f"{name:18} {about}")
            return
        code = 0
        for name in a.names:
            path = next((os.path.join(d, name + ".json") for d in (DEMOS, TEMPLATES) if os.path.isfile(os.path.join(d, name + ".json"))), None)
            if not path:
                die(f"no demo or template named {name!r}")
            code = ask(load_spec(path), a, os.path.dirname(path))
            if code not in (0, 2):
                break
        sys.exit(code)
    if a.cmd == "render":
        spec = apply_defaults(load_spec(a.spec))
        check_spec(spec)
        base = os.path.dirname(os.path.abspath(a.spec)) if a.spec != "-" else os.getcwd()
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(build_html(spec, base))
        print(a.out)


if __name__ == "__main__":
    main()
