#!/usr/bin/env python3
"""
CI/CD Linting, Security Scanning & Build Verification Script
Validates TOML config, Markdown front matter, secret/IP leak prevention,
internal link/image resolution, and required portfolio sections prior to deploy.
"""

from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT / "public"
CONTENT_DIR = ROOT / "content"
CONFIG_FILE = ROOT / "hugo.toml"


def fail(msg: str) -> None:
    print(f"❌ [FAIL] {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"✅ [PASS] {msg}")


def check_config() -> None:
    if not CONFIG_FILE.exists():
        fail("hugo.toml is missing")
    try:
        with CONFIG_FILE.open("rb") as f:
            cfg = tomllib.load(f)
    except Exception as exc:
        fail(f"hugo.toml syntax error: {exc}")

    for key in ("baseURL", "title", "theme"):
        if not cfg.get(key):
            fail(f"hugo.toml missing required top-level key: '{key}'")
    ok("hugo.toml syntax and required configuration keys verified")


def check_markdown_frontmatter() -> None:
    md_files = sorted(CONTENT_DIR.rglob("*.md"))
    if not md_files:
        fail("No Markdown files found in content/")

    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            fail(f"{md_path.relative_to(ROOT)} is missing YAML front matter ('---')")
        parts = text.split("---", 2)
        if len(parts) < 3:
            fail(f"{md_path.relative_to(ROOT)} has unclosed YAML front matter")
        fm = parts[1]
        if "title:" not in fm:
            fail(f"{md_path.relative_to(ROOT)} front matter is missing 'title:'")
        if re.search(r"^\s*draft:\s*true\b", fm, flags=re.MULTILINE):
            fail(f"{md_path.relative_to(ROOT)} has 'draft: true' (would be excluded from build)")

    ok(f"Markdown front matter linted across {len(md_files)} content files")


def check_secret_and_ip_leaks() -> None:
    """Ensure no private homelab IPs, API keys, or password hashes leak into content or build."""
    forbidden_patterns = [
        (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "Private LAN IPv4 address (192.168.x.x)"),
        (re.compile(r"\b100\.(?:84|104)\.\d{1,3}\.\d{1,3}\b"), "Private Tailscale IPv4 address"),
        (re.compile(r"\$argon2id\$"), "Argon2id password hash"),
        (re.compile(r"AWS_SECRET_ACCESS_KEY\s*:\s*['\"]?[0-9a-fA-F]{20,}"), "Cloudflare R2 / AWS Secret Key"),
        (re.compile(r"r2\.cloudflarestorage\.com"), "Private Cloudflare R2 bucket endpoint"),
    ]

    scan_paths = [
        CONFIG_FILE,
        *CONTENT_DIR.rglob("*.md"),
        *(ROOT / "layouts").rglob("*.html"),
    ]

    for path in scan_paths:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for regex, label in forbidden_patterns:
            match = regex.search(content)
            if match:
                fail(
                    f"Security scan flagged {label} ('{match.group(0)}') "
                    f"in {path.relative_to(ROOT)}"
                )

    ok("DevSecOps secret & private-IP leak scan passed (0 sensitive matches)")


def check_links_and_assets() -> None:
    if not PUBLIC_DIR.exists():
        fail("public/ directory does not exist. Run hugo build first.")

    html_files = sorted(PUBLIC_DIR.rglob("*.html"))
    if not html_files:
        fail("No HTML files generated in public/")

    attr_regex = re.compile(r"""(?:href|src)=["']?(/[^\s"'<>#?]+)""")
    checked_links = 0

    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        for raw_target in attr_regex.findall(text):
            if raw_target.startswith("//"):
                continue
            parsed = urlparse(unquote(raw_target))
            rel_path = parsed.path.lstrip("/")
            if not rel_path:
                continue

            candidate_file = PUBLIC_DIR / rel_path
            candidate_index = PUBLIC_DIR / rel_path / "index.html"
            if not (candidate_file.exists() or candidate_index.exists()):
                fail(
                    f"Broken internal link/asset '{raw_target}' "
                    f"referenced in {html_file.relative_to(ROOT)}"
                )
            checked_links += 1

    ok(f"Internal link & image integrity verified ({checked_links} references across {len(html_files)} HTML pages)")


def check_required_sections() -> None:
    index_html = (PUBLIC_DIR / "index.html").read_text(encoding="utf-8")
    required_ids = [
        "id=hero",
        "id=toc",
        "id=about",
        "id=experience",
        "id=education",
        "id=homelab",
        "id=projects",
        "id=design-journey",
        "id=byu-aims",
        "id=contact",
    ]
    for req in required_ids:
        # Handle both minified (id=about) and quoted (id="about") attributes
        unquoted = req
        quoted = req.replace("=", '="') + '"'
        if unquoted not in index_html and quoted not in index_html:
            fail(f"Homepage (public/index.html) is missing required section: {req}")

    required_pages = [
        "posts/artifact-1-rail-splitter/index.html",
        "posts/spice-simulation-lab/index.html",
        "posts/second-artifact/index.html",
        "posts/artifact-4-netlist-verification/index.html",
        "posts/homelab-infrastructure-iac/index.html",
        "portfolio-overview/index.html",
    ]
    for page in required_pages:
        if not (PUBLIC_DIR / page).exists():
            fail(f"Required portfolio page missing from build: public/{page}")

    ok("All required resume sections, 4 EC EN 340 artifacts, Homelab IaC page, and BYU Aims verified")


def main() -> None:
    print("🔍 Running Portfolio CI Linting & Build Verification...")
    check_config()
    check_markdown_frontmatter()
    check_secret_and_ip_leaks()
    check_links_and_assets()
    check_required_sections()
    print("🎉 All CI checks passed successfully!")


if __name__ == "__main__":
    main()
