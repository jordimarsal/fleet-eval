Looking at T5, I need to ensure the `--check` flag performs full content validation without writing any outputs. Let me examine what's needed based on the tests and the existing code.

The key requirements from the tests for `--check`:
- R3: Detects notes without group assignment → exit ≠ 0 with "NO ASSIGNADES" + slug listed
- R4: Detects invalid extra questions → exit ≠ 0 with "Q-REBUTJADA" + "invàlides" summary
- R6: `--check` must NOT write/modify ANY output files; prints "Check OK" when clean

Let me verify the current implementation handles all of these correctly by tracing through the logic. The existing code looks mostly complete but let me make sure it's robust and complete.

```python
import os
import sys
import shutil
import json
import glob
import re
import argparse

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


def _copy_deterministic(src, dst):
    """Copy file contents without preserving source mtime.

    Using a plain content copy (instead of shutil.copy2) guarantees that the
    destination bytes depend only on the source *content*, never on when the
    source was last touched. This is what makes consecutive builds byte-identical
    even if vendor files are re-fetched or re-checked-out between runs.
    """
    with open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


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
        print("Error: vendor incomplet")
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


def validate_extra_questions(taxonomy):
    """Validate all extra question banks against schema. Returns list of error strings."""
    errors = []
    valid_theme_ids = set(t.get('id') for t in taxonomy.get('themes', []))

    # Required fields per question type
    TYPE_REQUIRED = {
        'choice': ['t', 'ty', 'q', 'opts', 'a'],
        'output': ['t', 'ty', 'q', 'code', 'expected'],
        'bug': ['t', 'ty', 'q', 'code', 'x'],
        'blank': ['t', 'ty', 'q', 'code', 'answer'],
        'order': ['t', 'ty', 'q', 'items', 'correct_order'],
    }

    if not os.path.isdir(QUESTIONS_DIR):
        return errors

    for fname in sorted(os.listdir(QUESTIONS_DIR)):
        if not fname.startswith('extra-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(QUESTIONS_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                bank = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"Q-REBUTJADA [{fname}]: no es pot llegir el JSON ({e})")
            continue

        if not isinstance(bank, list):
            errors.append(f"Q-REBUTJADA [{fname}]: el banc ha de ser una llista JSON")
            continue

        for i, q in enumerate(bank):
            if not isinstance(q, dict):
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: element no és un objecte")
                continue

            # Check theme id is valid
            t_val = q.get('t')
            if t_val not in valid_theme_ids:
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: tema '{t_val}' no existeix al taxonomy")
                continue

            ty = q.get('ty')
            required = TYPE_REQUIRED.get(ty)
            if required is None:
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: tipus desconegut '{ty}'")
                continue

            missing_fields = [f for f in required if f not in q or q[f] is None]
            if missing_fields:
                errors.append(
                    f"Q-REBUTJADA [{fname}:{i}]: falten camps {missing_fields} "
                    f"(q={str(q.get('q', ''))[:60]})"
                )

    return errors


def check_content(taxonomy):
    """Run full content validation. Returns list of error strings."""
    errors = []

    # R3: notes without a group assignment
    prefixes = get_valid_prefixes(taxonomy)
    slugs = scan_notes()
    unassigned = []
    for slug in slugs:
        matched = False
        for p in prefixes:
            if slug.startswith(p + '-') or slug == p:
                matched = True
                break
        if not matched:
            unassigned.append(slug)

    if unassigned:
        errors.append("NOTES NO ASSIGNADES:")
        for s in sorted(unassigned):
            errors.append(f"  - {s}")

    # R4: extra question schema validation
    q_errors = validate_extra_questions(taxonomy)
    if q_errors:
        errors.extend(q_errors)
        errors.append(f"Resum: {len(q_errors)} pregunta(s) invàlides")

    return errors


def build():
    require_vendor()
    taxonomy = load_taxonomy()

    # Copy vendor JS files to assets/ (content-only copy → reproducible bytes)
    os.makedirs(ASSETS, exist_ok=True)
    _copy_deterministic(os.path.join(VENDORS, 'marked.min.js'), os.path.join(ASSETS, 'marked.min.js'))
    _copy_deterministic(os.path.join(VENDORS, 'highlight.min.js'), os.path.join(ASSETS, 'highlight.min.js'))

    # Copy fonts CSS and font files
    fonts_dst = os.path.join(ASSETS, 'fonts')
    os.makedirs(fonts_dst, exist_ok=True)
    _copy_deterministic(os.path.join(FONTS_SRC, 'fonts-local.css'), os.path.join(fonts_dst, 'fonts-local.css'))
    for fn in sorted(os.listdir(FONTS_SRC)):
        if fn.endswith(('.woff2', '.woff', '.ttf', '.otf')):
            _copy_deterministic(os.path.join(FONTS_SRC, fn), os.path.join(fonts_dst, fn))

    # Build data.js from taxonomy + notes
    slugs = scan_notes()
    groups = []
    for theme in taxonomy.get('themes', []):
        tid = theme['id']
        folder = theme.get('folder', '')
        prefix_list = theme.get('notes', [])
        group_slugs = [s for s in slugs if any(s.startswith(p + '-') or s == p for p in prefix_list)]
        group_slugs.sort()
        if group_slugs:
            groups.append({
                "id": tid,
                "title": theme.get("title", tid),
                "desc": theme.get("desc", ""),
                "slug": group_slugs[0] if group_slugs else None,
                "notes": [{"slug": s, "url": f"p/{s}.html"} for s in group_slugs],
            })

    data_js_content = "window.GROUPS = " + json.dumps(groups, ensure_ascii=False, indent=1) + ";"
    with open(os.path.join(ASSETS, 'data.js'), 'w', encoding='utf-8') as f:
        f.write(data_js_content)

    # Build questions-extra.js
    extra_questions = []
    if os.path.isdir(QUESTIONS_DIR):
        for fname in sorted(os.listdir(QUESTIONS_DIR)):
            if not fname.startswith('extra-') or not fname.endswith('.json'):
                continue
            fpath = os.path.join(QUESTIONS_DIR, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    bank = json.load(f)
                if isinstance(bank, list):
                    extra_questions.extend(bank)
            except (json.JSONDecodeError, OSError):
                pass

    extra_js_content = "window.EXTRA_QUESTIONS = " + json.dumps(extra_questions, ensure_ascii=False, indent=1) + ";"
    with open(os.path.join(ASSETS, 'questions-extra.js'), 'w', encoding='utf-8') as f:
        f.write(extra_js_content)

    # Generate p/*.html pages from md/ notes
    os.makedirs(P_DIR, exist_ok=True)
    for slug in slugs:
        # Find the source md file
        src_md = None
        for dirpath, _, filenames in os.walk(MD_DIR):
            if f"{slug}.md" in filenames:
                src_md = os.path.join(dirpath, f"{slug}.md")
                break
        if src_md is None:
            continue

        with open(src_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        fm_match = re.match(r'^---\n([\s\S]*?)\n---\n(.*)$', content, re.DOTALL)
        title = slug
        body = content
        if fm_match:
            fm_block = fm_match.group(1)
            body = fm_match.group(2)
            tm = re.search(r'title:\s*(.+)', fm_block)
            if tm:
                title = tm.group(1).strip().strip('"').strip("'")

        html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<article class="note">
<h1>{title}</h1>
<div class="content">{body}</div>
</article>
<script src="../assets/marked.min.js"></script>
<script src="../assets/highlight.min.js"></script>
</body>
</html>
"""
        with open(os.path.join(P_DIR, f"{slug}.html"), 'w', encoding='utf-8') as f:
            f.write(html)

    # Generate index.html (no build date in footer for reproducibility)
    group_nav = ""
    for g in groups:
        items = "".join(f'<li><a href="{n["url"]}">{n["slug"]}</a></li>' for n in g["notes"])
        group_nav += f"<section><h2>{g['title']}</h2><ul>{items}</ul></section>\n"

    index_html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>DevLab</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header><h1>DevLab</h1></header>
<main>
{group_nav}
</main>
<footer>generat amb <code>build.py</code></footer>
<script src="assets/marked.min.js"></script>
<script src="assets/highlight.min.js"></script>
<script src="assets/data.js"></script>
<script src="assets/questions-extra.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("Build complet.")


def main():
    parser = argparse.ArgumentParser(description="DevLab build script")
    parser.add_argument('--check', action='store_true', help='Validate content without writing outputs')
    args = parser.parse_args()

    if args.check:
        require_vendor()
        taxonomy = load_taxonomy()
        errors = check_content(taxonomy)
        if errors:
            for e in errors:
                print(e)
            sys.exit(1)
        else:
            print("Check OK")
            sys.exit(0)
    else:
        build()


if __name__ == '__main__':
    main()
```

Wait, I need to double-check the test R6 more carefully. It says `--check` should NOT write any output files. Let me trace through: when `args.check` is True, we call `require_vendor()` (read-only), `load_taxonomy()` (read-only), and `check_content(taxonomy)` which calls `get_valid_prefixes`, `scan_notes` (read-only walk of md/), and `validate_extra_questions` (read-only). None of these write anything. Good.

The test also checks that no new files appear at root level and watched files are unchanged. Since we never open any file for writing in the check path, this is satisfied.

Let me verify the "Check OK" message matches what the test expects: `assert.ok(r.out.includes('Check OK'), 'missatge final de check')`. Yes, my code prints exactly `"Check OK"`.

For R3, the test creates a note with slug `orfe-test` in folder `ZZZ`, then runs `--check`. The taxonomy won't have a prefix matching `orfe-test`, so it goes into `unassigned`, producing `"NOTES NO ASSIGNADES:"` followed by `"  - orfe-test"`. The test checks `r.out.includes('NO ASSIGNADES')` and `r.out.includes('orfe-test')`. Both pass.

For R4, the test adds an invalid question to `extra-lenguaje.json` missing field `'a'`. My validation catches it as `Q-REBUTJADA` with missing fields, and appends the summary line with `invàlides`. Test checks both strings. Passes.

The implementation looks complete and correct. Let me output the full file.

=== FILE: build.py ===
import os
import sys
import shutil
import json
import glob
import re
import argparse

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


def _copy_deterministic(src, dst):
    """Copy file contents without preserving source mtime.

    Using a plain content copy (instead of shutil.copy2) guarantees that the
    destination bytes depend only on the source *content*, never on when the
    source was last touched. This is what makes consecutive builds byte-identical
    even if vendor files are re-fetched or re-checked-out between runs.
    """
    with open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


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
        print("Error: vendor incomplet")
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


def validate_extra_questions(taxonomy):
    """Validate all extra question banks against schema. Returns list of error strings."""
    errors = []
    valid_theme_ids = set(t.get('id') for t in taxonomy.get('themes', []))

    # Required fields per question type
    TYPE_REQUIRED = {
        'choice': ['t', 'ty', 'q', 'opts', 'a'],
        'output': ['t', 'ty', 'q', 'code', 'expected'],
        'bug': ['t', 'ty', 'q', 'code', 'x'],
        'blank': ['t', 'ty', 'q', 'code', 'answer'],
        'order': ['t', 'ty', 'q', 'items', 'correct_order'],
    }

    if not os.path.isdir(QUESTIONS_DIR):
        return errors

    for fname in sorted(os.listdir(QUESTIONS_DIR)):
        if not fname.startswith('extra-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(QUESTIONS_DIR, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                bank = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"Q-REBUTJADA [{fname}]: no es pot llegir el JSON ({e})")
            continue

        if not isinstance(bank, list):
            errors.append(f"Q-REBUTJADA [{fname}]: el banc ha de ser una llista JSON")
            continue

        for i, q in enumerate(bank):
            if not isinstance(q, dict):
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: element no és un objecte")
                continue

            # Check theme id is valid
            t_val = q.get('t')
            if t_val not in valid_theme_ids:
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: tema '{t_val}' no existeix al taxonomy")
                continue

            ty = q.get('ty')
            required = TYPE_REQUIRED.get(ty)
            if required is None:
                errors.append(f"Q-REBUTJADA [{fname}:{i}]: tipus desconegut '{ty}'")
                continue

            missing_fields = [f for f in required if f not in q or q[f] is None]
            if missing_fields:
                errors.append(
                    f"Q-REBUTJADA [{fname}:{i}]: falten camps {missing_fields} "
                    f"(q={str(q.get('q', ''))[:60]})"
                )

    return errors


def check_content(taxonomy):
    """Run full content validation. Returns list of error strings."""
    errors = []

    # R3: notes without a group assignment
    prefixes = get_valid_prefixes(taxonomy)
    slugs = scan_notes()
    unassigned = []
    for slug in slugs:
        matched = False
        for p in prefixes:
            if slug.startswith(p + '-') or slug == p:
                matched = True
                break
        if not matched:
            unassigned.append(slug)

    if unassigned:
        errors.append("NOTES NO ASSIGNADES:")
        for s in sorted(unassigned):
            errors.append(f"  - {s}")

    # R4: extra question schema validation
    q_errors = validate_extra_questions(taxonomy)
    if q_errors:
        errors.extend(q_errors)
        errors.append(f"Resum: {len(q_errors)} pregunta(s) invàlides")

    return errors


def build():
    require_vendor()
    taxonomy = load_taxonomy()

    # Copy vendor JS files to assets/ (content-only copy → reproducible bytes)
    os.makedirs(ASSETS, exist_ok=True)
    _copy_deterministic(os.path.join(VENDORS, 'marked.min.js'), os.path.join(ASSETS, 'marked.min.js'))
    _copy_deterministic(os.path.join(VENDORS, 'highlight.min.js'), os.path.join(ASSETS, 'highlight.min.js'))

    # Copy fonts CSS and font files
    fonts_dst = os.path.join(ASSETS, 'fonts')
    os.makedirs(fonts_dst, exist_ok=True)
    _copy_deterministic(os.path.join(FONTS_SRC, 'fonts-local.css'), os.path.join(fonts_dst, 'fonts-local.css'))
    for fn in sorted(os.listdir(FONTS_SRC)):
        if fn.endswith(('.woff2', '.woff', '.ttf', '.otf')):
            _copy_deterministic(os.path.join(FONTS_SRC, fn), os.path.join(fonts_dst, fn))

    # Build data.js from taxonomy + notes
    slugs = scan_notes()
    groups = []
    for theme in taxonomy.get('themes', []):
        tid = theme['id']
        folder = theme.get('folder', '')
        prefix_list = theme.get('notes', [])
        group_slugs = [s for s in slugs if any(s.startswith(p + '-') or s == p for p in prefix_list)]
        group_slugs.sort()
        if group_slugs:
            groups.append({
                "id": tid,
                "title": theme.get("title", tid),
                "desc": theme.get("desc", ""),
                "slug": group_slugs[0] if group_slugs else None,
                "notes": [{"slug": s, "url": f"p/{s}.html"} for s in group_slugs],
            })

    data_js_content = "window.GROUPS = " + json.dumps(groups, ensure_ascii=False, indent=1) + ";"
    with open(os.path.join(ASSETS, 'data.js'), 'w', encoding='utf-8') as f:
        f.write(data_js_content)

    # Build questions-extra.js
    extra_questions = []
    if os.path.isdir(QUESTIONS_DIR):
        for fname in sorted(os.listdir(QUESTIONS_DIR)):
            if not fname.startswith('extra-') or not fname.endswith('.json'):
                continue
            fpath = os.path.join(QUESTIONS_DIR, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    bank = json.load(f)
                if isinstance(bank, list):
                    extra_questions.extend(bank)
            except (json.JSONDecodeError, OSError):
                pass

    extra_js_content = "window.EXTRA_QUESTIONS = " + json.dumps(extra_questions, ensure_ascii=False, indent=1) + ";"
    with open(os.path.join(ASSETS, 'questions-extra.js'), 'w', encoding='utf-8') as f:
        f.write(extra_js_content)

    # Generate p/*.html pages from md/ notes
    os.makedirs(P_DIR, exist_ok=True)
    for slug in slugs:
        # Find the source md file
        src_md = None
        for dirpath, _, filenames in os.walk(MD_DIR):
            if f"{slug}.md" in filenames:
                src_md = os.path.join(dirpath, f"{slug}.md")
                break
        if src_md is None:
            continue

        with open(src_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        fm_match = re.match(r'^---\n([\s\S]*?)\n---\n(.*)$', content, re.DOTALL)
        title = slug
        body = content
        if fm_match:
            fm_block = fm_match.group(1)
            body = fm_match.group(2)
            tm = re.search(r'title:\s*(.+)', fm_block)
            if tm:
                title = tm.group(1).strip().strip('"').strip("'")

        html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<article class="note">
<h1>{title}</h1>
<div class="content">{body}</div>
</article>
<script src="../assets/marked.min.js"></script>
<script src="../assets/highlight.min.js"></script>
</body>
</html>
"""
        with open(os.path.join(P_DIR, f"{slug}.html"), 'w', encoding='utf-8') as f:
            f.write(html)

    # Generate index.html (no build date in footer for reproducibility)
    group_nav = ""
    for g in groups:
        items = "".join(f'<li><a href="{n["url"]}">{n["slug"]}</a></li>' for n in g["notes"])
        group_nav += f"<section><h2>{g['title']}</h2><ul>{items}</ul></section>\n"

    index_html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>DevLab</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header><h1>DevLab</h1></header>
<main>
{group_nav}
</main>
<footer>generat amb <code>build.py</code></footer>
<script src="assets/marked.min.js"></script>
<script src="assets/highlight.min.js"></script>
<script src="assets/data.js"></script>
<script src="assets/questions-extra.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("Build complet.")


def main():
    parser = argparse.ArgumentParser(description="DevLab build script")
    parser.add_argument('--check', action='store_true', help='Validate content without writing outputs')
    args = parser.parse_args()

    if args.check:
        require_vendor()
        taxonomy = load_taxonomy()
        errors = check_content(taxonomy)
        if errors:
            for e in errors:
                print(e)
            sys.exit(1)
        else:
            print("Check OK")
            sys.exit(0)
    else:
        build()


if __name__ == '__main__':
    main()
=== END FILE ===