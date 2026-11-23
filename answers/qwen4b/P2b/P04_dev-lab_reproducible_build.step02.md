Looking at T2, I need to understand what "missing file validation with error reporting" means beyond the existing `require_vendor()`. Let me examine the test expectations and current state more carefully.

The key insight from the tests:
- **R2** (`vendor incomple` + no traceback): Already handled by `require_vendor()` — but it only checks 3 files, not the `.woff2` fonts. The gate requires all `.woff2` files to be validated too.
- **R3** (`NO ASSIGNADES` + slug listing): This is content validation via `--check`, which belongs to T5.

So for T2 specifically, I should make `require_vendor()` robust: validate the vendor JS/CSS files **and** the font files referenced by `fonts-local.css`, report each missing path cleanly, and exit non-zero without a traceback.

Let me verify my understanding of the existing code before writing. The current `require_vendor()` hardcodes 3 paths. I'll extend it to also discover `.woff2` files from the CSS so the gate's requirement ("all `.woff2` files exist in assets/") is enforced during validation.

=== FILE: build.py ===
import os
import sys
import shutil
import json
import glob
import re
import argparse
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(VENDORS, 'fonts')
ASSETS = os.path.join(ROOT, 'assets')
MD_DIR = os.path.join(ROOT, 'md')
TAXONOMY_FILE = os.path.join(ROOT, 'taxonomy.json')
QUESTIONS_DIR = os.path.join(ROOT, 'src', 'questions')
P_DIR = os.path.join(ROOT, 'p')


def _font_files_from_css(css_path):
    """Return absolute paths of .woff2/.woff/.ttf/.otf files referenced by url() in a CSS file."""
    if not os.path.exists(css_path):
        return []
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
    except OSError:
        return []
    refs = re.findall(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', css)
    found = []
    for ref in refs:
        # Skip remote / data URIs and protocol-relative URLs.
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', ref) or ref.startswith('//'):
            continue
        base_dir = os.path.dirname(os.path.abspath(css_path))
        candidate = os.path.normpath(os.path.join(base_dir, ref.split('?')[0]))
        if candidate.endswith(('.woff2', '.woff', '.ttf', '.otf')):
            found.append(candidate)
    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for c in found:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def require_vendor():
    """Check that all required vendor files (JS/CSS + referenced fonts) exist.

    Exits cleanly with a readable error message when anything is missing; never
    raises a traceback.
    """
    required_files = [
        os.path.join(VENDORS, 'marked.min.js'),
        os.path.join(VENDORS, 'highlight.min.js'),
        os.path.join(FONTS_SRC, 'fonts-local.css'),
    ]

    # Also validate every font file the local CSS references so an incomplete
    # vendor/fonts directory is caught up front.
    css_path = os.path.join(FONTS_SRC, 'fonts-local.css')
    if os.path.exists(css_path):
        required_files.extend(_font_files_from_css(css_path))

    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)

    if missing:
        print("Error: vendor incomple")
        for m in missing:
            rel_path = os.path.relpath(m, ROOT)
            print(f"  falta: {rel_path}")
        sys.exit(1)

def load_taxonomy():
    with open(TAXONOMY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_valid_prefixes(taxonomy):
    prefixes = set()
    for theme in taxonomy.get('themes', []):
        notes = theme.get('notes', [])
        for n in notes:
            prefixes.add(n)
    return prefixes

def scan_notes():
    """Returns list of slugs found in md/"""
    slugs = []
    if not os.path.exists(MD_DIR):
        return slugs
    for dirpath, _, filenames in os.walk(MD_DIR):
        for fn in sorted(filenames):
            if fn.endswith('.md'):
                slug = fn[:-3]
                slugs.append(slug)
    return slugs
=== END FILE ===