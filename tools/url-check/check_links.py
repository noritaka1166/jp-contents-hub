#!/usr/bin/env python3
"""リンク切れチェック - Phase 1: HTTPステータスチェック
200以外をエラーとして報告し、200のURLリストも別途出力する。
"""

import re
import ssl
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
SOURCE = REPO_ROOT / "content" / "index.md"
ERRORS_FILE = SCRIPT_DIR / "errors.tsv"
OK_FILE = SCRIPT_DIR / "ok_urls.txt"


def extract_urls(source_path):
    content = source_path.read_text(encoding="utf-8")
    urls = re.findall(r'href="(https?://[^"]+)"', content)
    return sorted(set(urls))


def check_status(url, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (LinkChecker)"})
    try:
        resp = urlopen(req, timeout=timeout, context=ctx)
        return resp.getcode(), str(resp.url)
    except HTTPError as e:
        return e.code, url
    except (URLError, OSError, Exception):
        return 0, url


def main():
    urls = extract_urls(SOURCE)
    total = len(urls)
    print(f"Checking {total} URLs...\n")

    ok_urls = []
    errors = []

    for i, url in enumerate(urls, 1):
        status, final_url = check_status(url)
        if status == 200:
            ok_urls.append(url)
            sys.stdout.write(f"\r[{i}/{total}] OK: {len(ok_urls)} | Errors: {len(errors)}")
            sys.stdout.flush()
        else:
            errors.append((status, url))
            print(f"\n[{i}/{total}] HTTP {status}: {url}")

    # 保存
    with open(ERRORS_FILE, "w") as f:
        f.write("STATUS\tURL\n")
        for status, url in errors:
            f.write(f"{status}\t{url}\n")

    with open(OK_FILE, "w") as f:
        for url in ok_urls:
            f.write(url + "\n")

    print(f"\n\n===== Summary =====")
    print(f"Total: {total}")
    print(f"OK (200): {len(ok_urls)}")
    print(f"Errors: {len(errors)}")
    print(f"\nError details: {ERRORS_FILE}")
    print(f"OK URLs (for content check): {OK_FILE}")


if __name__ == "__main__":
    main()
