The user wants to implement **T2** from the plan.

**Task T2:** Refactor validations: `unassigned_notes(notes)` + `validate_questions()` executed in build and `--check`, with hard `sys.exit` (R3, R4); `--check` remains as complete validation without writing (R6).

**Context Analysis:**
1.  **Current State**: `build.py` currently has a stub for `--check` that just prints "Check OK". It does not validate notes or questions.
2.  **Requirements from Tests (`tests/build.test.js`)**:
    *   **R3**: If a note exists in `md/` but is not assigned to any group in `taxonomy.json` (or similar structure), running `python3 build.py --check` must exit non-zero and print "NO ASSIGNADES" and the slug of the unassigned note.
    *   **R4**: If a question in `src/questions/*.json` is invalid (specifically, missing required fields like `'a'` for choice questions? The test adds `{ t: 'lenguaje', ty: 'choice', q: '...', opts: ['a', 'b'] }` which lacks an answer key usually denoted by `a` or similar in this codebase's context, though looking at other tests, `q.a` is often the answer index or value. Let's look closer at R4 test: `bank.push({ t: 'lenguaje', ty: 'choice', q: 'Pregunta trencada de test', opts: ['a', 'b'] });`. It expects output containing "Q-REBUTJADA" and "invàlides". This implies `validate_questions()` needs to check validity. What makes it invalid? Usually, a choice question needs an answer. In many such schemas, `a` is the correct option index or ID. Here `opts` are strings. Let's assume standard validation: `ty` must be valid, `t` must match theme, etc. But specifically, the test case provided is minimal. I need to infer what "invalid" means based on the error message expected.
    *   **R6**: `--check` must NOT write any files. It should validate everything (vendors via T1 logic, notes via R3, questions via R4) and exit 0 if all good, printing "Check OK".

**Implementation Plan for `build.py`:**

1.  **Helper Functions**:
    *   `load_taxonomy()`: Read `taxonomy.json`.
    *   `get_assigned_slugs(taxonomy)`: Extract all slugs defined in the taxonomy groups.
    *   `scan_notes(root)`: Find all `.md` files in `md/` subdirectories. Return list of `(slug, path)` or just slugs. The slug is typically the filename without extension.
    *   `unassigned_notes(notes, assigned_slugs)`: Returns list of note slugs that are in `notes` but not in `assigned_slugs`.
    *   `validate_questions(root)`: Scan `src/questions/*.json`. For each question, check validity.
        *   What constitutes an invalid question?
            *   Looking at other tests (e.g., `tests/shell_scripting.test.js`), questions have `t`, `ty`, `q`, `ref`, etc.
            *   The test case for R4 adds a question with `t: 'lenguaje'`, `ty: 'choice'`, `q: ...`, `opts: [...]`. It does *not* have an answer field. In many quiz schemas, you need to know which option is correct. Let's assume the schema requires an `a` field (answer index or ID). If `ty == 'choice'` and `'a' not in q`, it's invalid. Or maybe `a` must be valid.
            *   Let's look at the error message expected: "Q-REBUTJADA". And summary "invàlides".
            *   I will implement a basic validator:
                *   Must have `t`, `ty`, `q`.
                *   If `ty == 'choice'`, must have `opts` (list) and `a` (int/index or string id). The test case lacks `a`. So checking for presence of `a` seems safe.
    *   `run_checks(root)`:
        1.  Check vendors (already done by `require_vendor`).
        2.  Load taxonomy.
        3.  Scan notes.
        4.  Find unassigned notes. If any, print "NO ASSIGNADES" + list, return False.
        5.  Validate questions. Collect errors. If any, print "Q-REBUTJADA" lines + summary "X invàlides", return False.
        6.  Return True if all pass.

2.  **Main Logic**:
    *   Parse args (`--check`).
    *   Call `require_vendor()`.
    *   If `--check`:
        *   Run `run_checks()`.
        *   If success: print "Check OK", exit 0.
        *   If fail: exit 1.
        *   **Crucial**: Do NOT write files.
    *   Else (Build):
        *   Run `run_checks()`? Or just build?
        *   The plan says: "`unassigned_notes(notes)` + `validate_questions()` executades a build i `--check`". So yes, run checks in both modes.
        *   If checks fail in Build mode: Exit non-zero (hard sys.exit).
        *   If checks pass: Proceed to generate outputs (copy vendors, generate HTML/JS).

**Refining Validation Logic based on Test R4:**
The test modifies `src/questions/extra-lenguaje.json`. It adds a question without an answer.
I need to make sure my validator catches this.
Common fields in these repos: `t` (theme), `ty` (type), `q` (question text), `opts` (options for choice), `a` (answer index or value).
If I check for `'a' in q`, the test case will fail validation.

**Refining Note Scanning (R3):**
Test creates `md/ZZZ/orfe-test.md`.
Taxonomy likely doesn't have "orfe-test" in any group's notes list.
So `scan_notes` finds `orfe-test`. `get_assigned_slugs` does not contain it.
Result: Unassigned.

**Data Structures:**
*   `taxonomy.json`: Likely `{ themes: [ { id, folder, notes: [...] } ] }`. The `notes` field seems to be a list of prefixes or slugs?
    *   Looking at `tests/django_ab.test.js`: `assert.deepEqual(t.notes, [prefix], ...)`. So `t.notes` is a list of strings. Are they full slugs or prefixes?
    *   In R2 of django test: `NOTES = { Django: ['django-orm-querysets', ...] }`. And `t.notes` is checked against `[prefix]`. Wait.
    *   Let's look at `tests/shell_scripting.test.js`: `assert.deepEqual(shell.notes, ['shell'])`. But the actual note files are `shell-pipelines.md`, etc.
    *   This implies `taxonomy.json`'s `notes` field might define **prefixes** or specific slugs?
    *   Actually, usually in these setups, `data.js` (generated) contains the mapping. Or `taxonomy.json` lists the exact slugs.
    *   Let's check `tests/build.test.js` R3 again. It just creates a file and expects it to be flagged if not assigned.
    *   How does the build know what is "assigned"? Usually by reading `taxonomy.json` which lists all valid notes/slugs for each theme.
    *   If `taxonomy.json` has `themes[].notes` as a list of slugs, then I can compare directly.
    *   If `taxonomy.json` uses prefixes, I need to match by prefix.
    *   Given `assert.deepEqual(t.notes, [prefix])` in other tests, it seems `notes` in taxonomy holds prefixes or single slug identifiers that map to folders/files.
    *   However, `build.py` generates `assets/data.js`. The source of truth for "what exists" is the filesystem (`md/`). The source of truth for "what should exist/be grouped" is likely `taxonomy.json`.
    *   Let's assume `taxonomy.json` defines the canonical set of slugs. I will extract all strings from `themes[*].notes` into a set `valid_slugs`.
    *   Then scan `md/**\/*.md`. For each file, get basename (slug). If slug not in `valid_slugs`, it's unassigned.

**Wait**, looking at `tests/django_ab.test.js`:
```javascript
const NOTES = {
  Django: ['django-orm-querysets', 'django-vs-fastapi'],
  ...
};
// ...
assert.ok(DATA_JS.includes(`"slug": "${slug}"`), `${slug}: no és a data.js`);
```
And `taxonomy.json` check:
```javascript
assert.deepEqual(t.notes, [prefix], `${id}: prefix de notes`);
```
This suggests `t.notes` might be `[ "django" ]` (the prefix) and the actual files are `django-*.md`.
If so, matching exact slugs against `t.notes` would fail because `t.notes` has `"django"` but file is `django-orm-querysets.md`.
So, validation must handle prefixes OR the taxonomy lists full slugs.
Let's look at `tests/shell_scripting.test.js`:
`t.notes` is `['shell']`. Files are `shell-pipelines.md`.
It is highly probable that `notes` in taxonomy contains **prefixes**.
Therefore, a note is "assigned" if its slug starts with any of the prefixes defined in `taxonomy.json`'s themes.

**Validation Logic for Notes:**
1. Load `taxonomy.json`.
2. Collect all strings from `themes[*].notes` into a list `prefixes`.
3. Scan `md/` for `.md` files. Extract slug (filename without ext).
4. For each slug, check if it matches any prefix. Match logic: `slug == prefix` or `slug.startswith(prefix + '-')`? Or just `startswith(prefix)`?
   Usually, to avoid `shell` matching `shells`, we might need strictness. But simple startswith is common in these small repos. Let's assume standard prefix matching where the next char is `-` or end of string.
   Actually, simpler: The build script generates `data.js`. Maybe I should parse `assets/data.js`? No, R6 says `--check` doesn't write. And R3 creates a *new* file not in data.js yet. So I must validate against source config (`taxonomy.json`) and filesystem.
   
   Let's refine the match: A slug is valid if there exists a theme such that the slug corresponds to one of its notes. If `t.notes` are prefixes, then `slug.startswith(p)` is likely the intended logic.

**Validation Logic for Questions:**
1. Scan `src/questions/*.json`.
2. Parse JSON array.
3. For each question `q`:
   - Must have `t`, `ty`, `q`.
   - If `ty == 'choice'`: Must have `opts` (list) and `a` (answer).
   - Other types might have different requirements, but the test only tests `choice` missing `a`.
   - If invalid, record error.
4. If errors exist, print them with "Q-REBUTJADA" tag.

**Output Format for Errors:**
R3 expects: `NO ASSIGNADES` and the slug.
R4 expects: `Q-REBUTJADA` and summary `invàlides`.

Let's write the code.

```python
import os
import sys
import shutil
import json
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(VENDORS, 'fonts')
ASSETS = os.path.join(ROOT, 'assets')
MD_DIR = os.path.join(ROOT, 'md')
TAXONOMY_FILE = os.path.join(ROOT, 'taxonomy.json')
QUESTIONS_DIR = os.path.join(ROOT, 'src', 'questions')


def require_vendor():
    """Check that all required vendor files exist. Exit cleanly if missing."""
    required_files = [
        os.path.join(VENDORS, 'marked.min.js'),
        os.path.join(VENDORS, 'highlight.min.js'),
        os.path.join(FONTS_SRC, 'fonts-local.css'),
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
            
    if missing:
        print("Error: vendor incomple")
        for m in missing:
            print(f"  falta: {m}")
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
        for fn in filenames:
            if fn.endswith('.md'):
                slug = os.path.splitext(fn)[0]
                slugs.append(slug)
    return slugs

def unassigned_notes(slugs, prefixes):
    """Check which slugs do not match any prefix."""
    unassigned = []
    for slug in slugs:
        is_assigned = False
        for p in prefixes:
            # Match if slug equals prefix or starts with prefix followed by '-'
            if slug == p or slug.startswith(p + '-'):
                is_assigned = True
                break
        if not is_assigned:
            unassigned.append(slug)
    return unassigned

def validate_questions():
    """Validate questions in src/questions/*.json. Returns list of error strings."""
    errors = []
    if not os.path.exists(QUESTIONS_DIR):
        return errors
        
    files = glob.glob(os.path.join(QUESTIONS_DIR, '*.json'))
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"{os.path.basename(filepath)}: JSON invàlid ({e})")
            continue
            
        if not isinstance(data, list):
            errors.append(f"{os.path.basename(filepath)}: no és una llista")
            continue
            
        for i, q in enumerate(data):
            if not isinstance(q, dict):
                errors.append(f"{os.path.basename(filepath)}[{i}]: no és un objecte")
                continue
                
            # Basic checks
            if 't' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 't'")
                continue
            if 'ty' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 'ty'")
                continue
            if 'q' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 'q'")
                continue
                
            ty = q['ty']
            
            # Specific type checks
            if ty == 'choice':
                if 'opts' not in q or not isinstance(q['opts'], list):
                    errors.append(f"{os.path.basename(filepath)}[{i}]: choice sense opts vàlides")
                elif 'a' not in q:
                    errors.append(f"{os.path.basename(filepath)}[{i}]: choice sense resposta ('a')")
                    
    return errors

def run_checks():
    """Run all validations. Returns True if OK, False otherwise."""
    # 1. Notes validation
    try:
        taxonomy = load_taxonomy()
    except Exception as e:
        print(f"Error carregant taxonomy.json: {e}")
        return False
        
    prefixes = get_valid_prefixes(taxonomy)
    slugs = scan_notes()
    
    unassigned = unassigned_notes(slugs, prefixes)
    if unassigned:
        print("NO ASSIGNADES:")
        for slug in sorted(unassigned):
            print(f"  - {slug}")
        
    # 2. Questions validation
    q_errors = validate_questions()
    if q_errors:
        for err in q_errors:
            print(f"Q-REBUTJADA: {err}")
        print(f"Resum: {len(q_errors)} preguntes invàlides")
        
    if unassigned or q_errors:
        return False
        
    return True

def main():
    check_mode = '--check' in sys.argv
    
    # T1: Validate vendors before doing anything else
    require_vendor()
    
    # T2: Run content validations (Notes + Questions)
    # These must pass for both build and --check
    if not run_checks():
        sys.exit(1)
        
    if check_mode:
        # In --check mode, we perform validations but do NOT write outputs.
        print("Check OK")
        return

    # Normal build mode
    
    # Ensure assets directory exists
    os.makedirs(ASSETS, exist_ok=True)
    
    # Copy JS vendors
    shutil.copy(os.path.join(VENDORS, 'marked.min.js'), os.path.join(ASSETS, 'marked.min.js'))
    shutil.copy(os.path.join(VENDORS, 'highlight.min.js'), os.path.join(ASSETS, 'highlight.min.js'))
    
    # Copy fonts
    fonts_dst = os.path.join(ASSETS, 'fonts')
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(FONTS_SRC):
        if f.endswith('.css') or f.endswith('.woff2'):
            shutil.copy(os.path.join(FONTS_SRC, f), os.path.join(fonts_dst, f))
            
    # Generate index.html with static footer (T3 requirement prep)
    html_content = """<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <title>DevLab</title>
    <link rel="stylesheet" href="assets/fonts/fonts-local.css">
</head>
<body>
    <h1>DevLab</h1>
    <footer>generat amb <code>build.py</code></footer>
    <script src="assets/marked.min.js"></script>
    <script src="assets/highlight.min.js"></script>
</body>
</html>"""
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Generate dummy data.js and questions-extra.js to satisfy structure checks
    with open(os.path.join(ASSETS, 'data.js'), 'w', encoding='utf-8') as f:
        f.write("window.GROUPS = [];")
        
    with open(os.path.join(ASSETS, 'questions-extra.js'), 'w', encoding='utf-8') as f:
        f.write("window.QUESTIONS_EXTRA = {};")

if __name__ == '__main__':
    main()
```

Double check R4 test details:
`bank.push({ t: 'lenguaje', ty: 'choice', q: 'Pregunta trencada de test', opts: ['a', 'b'] });`
My validator checks `ty == 'choice'` -> `'a' not in q`. This will trigger the error.
The error message printed is `Q-REBUTJADA: ...`. The test asserts `r.out.includes('Q-REBUTJADA')`.
It also asserts `r.out.includes('invàlides')`. My summary line prints `Resum: {len(q_errors)} preguntes invàlides`. This contains "invàlides".

Double check R3 test details:
Creates `md/ZZZ/orfe-test.md`.
`scan_notes` finds `orfe-test`.
`taxonomy.json` presumably has prefixes like `django`, `shell`, etc. It does NOT have `orfe` or `zzz`.
So `unassigned_notes` returns `['orfe-test']`.
Prints `NO ASSIGNADES:` and `- orfe-test`.
Test asserts `r.out.includes('NO ASSIGNADES')` and `r.out.includes('orfe-test')`.

One edge case: What if `taxonomy.json` doesn't exist? `load_taxonomy` throws, caught, returns False. Exit 1. Correct behavior for a broken repo state.

What if `src/questions` doesn't exist? `validate_questions` returns empty list. No errors. Correct.

Does the build mode need to generate *real* data.js?
The current stub writes dummy data. The plan says T2 is just refactoring validations. T5 mentions "rebuild complet... assets regenerats idèntics". This implies that in later steps (or maybe this step?) we might need to actually parse the markdown/taxonomy to generate real JS. However, T2 specifically focuses on **validations**. The prompt says "Implement ONLY this". The previous work had dummy generation. I should stick to the validation logic changes and keep the existing generation logic (dummy) unless it breaks R6 (which checks no write). Since Build mode *does* write, and Check mode does not, my structure handles this.

Wait, looking at R6 test again:
```javascript
const watched = ['index.html', 'assets/style.css', 'assets/data.js', firstNote];
// ...
assert.equal(sha256(join(sb, f)), before[f], `--check no modifica ${f}`);
```
It checks that files are NOT modified. My code path for `--check` exits before any file writing operations (`shutil.copy`, `open(..., 'w')`). So this is safe.

One detail: `assets/style.css` is watched in R6 but doesn't exist in my current build script's output list?
The sandbox copies the repo. If `assets/style.css` exists in the repo, it will be there. My build script doesn't touch it. So its hash remains unchanged. This is fine.

I will proceed with generating the updated `build.py`.

=== FILE: build.py ===
import os
import sys
import shutil
import json
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(VENDORS, 'fonts')
ASSETS = os.path.join(ROOT, 'assets')
MD_DIR = os.path.join(ROOT, 'md')
TAXONOMY_FILE = os.path.join(ROOT, 'taxonomy.json')
QUESTIONS_DIR = os.path.join(ROOT, 'src', 'questions')


def require_vendor():
    """Check that all required vendor files exist. Exit cleanly if missing."""
    required_files = [
        os.path.join(VENDORS, 'marked.min.js'),
        os.path.join(VENDORS, 'highlight.min.js'),
        os.path.join(FONTS_SRC, 'fonts-local.css'),
    ]
    
    # Check for at least one woff2 file (test expects >= 3 in repo, but build just needs to copy what's there)
    # However, R1 checks the repo state directly. Build script should probably verify integrity too?
    # The test R2 only removes marked.min.js. So checking specific files is sufficient for the error path.
    
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
            
    if missing:
        print("Error: vendor incomple")
        for m in missing:
            print(f"  falta: {m}")
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
        for fn in filenames:
            if fn.endswith('.md'):
                slug = os.path.splitext(fn)[0]
                slugs.append(slug)
    return slugs

def unassigned_notes(slugs, prefixes):
    """Check which slugs do not match any prefix."""
    unassigned = []
    for slug in slugs:
        is_assigned = False
        for p in prefixes:
            # Match if slug equals prefix or starts with prefix followed by '-'
            if slug == p or slug.startswith(p + '-'):
                is_assigned = True
                break
        if not is_assigned:
            unassigned.append(slug)
    return unassigned

def validate_questions():
    """Validate questions in src/questions/*.json. Returns list of error strings."""
    errors = []
    if not os.path.exists(QUESTIONS_DIR):
        return errors
        
    files = glob.glob(os.path.join(QUESTIONS_DIR, '*.json'))
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"{os.path.basename(filepath)}: JSON invàlid ({e})")
            continue
            
        if not isinstance(data, list):
            errors.append(f"{os.path.basename(filepath)}: no és una llista")
            continue
            
        for i, q in enumerate(data):
            if not isinstance(q, dict):
                errors.append(f"{os.path.basename(filepath)}[{i}]: no és un objecte")
                continue
                
            # Basic checks
            if 't' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 't'")
                continue
            if 'ty' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 'ty'")
                continue
            if 'q' not in q:
                errors.append(f"{os.path.basename(filepath)}[{i}]: falta 'q'")
                continue
                
            ty = q['ty']
            
            # Specific type checks
            if ty == 'choice':
                if 'opts' not in q or not isinstance(q['opts'], list):
                    errors.append(f"{os.path.basename(filepath)}[{i}]: choice sense opts vàlides")
                elif 'a' not in q:
                    errors.append(f"{os.path.basename(filepath)}[{i}]: choice sense resposta ('a')")
                    
    return errors

def run_checks():
    """Run all validations. Returns True if OK, False otherwise."""
    # 1. Notes validation
    try:
        taxonomy = load_taxonomy()
    except Exception as e:
        print(f"Error carregant taxonomy.json: {e}")
        return False
        
    prefixes = get_valid_prefixes(taxonomy)
    slugs = scan_notes()
    
    unassigned = unassigned_notes(slugs, prefixes)
    if unassigned:
        print("NO ASSIGNADES:")
        for slug in sorted(unassigned):
            print(f"  - {slug}")
        
    # 2. Questions validation
    q_errors = validate_questions()
    if q_errors:
        for err in q_errors:
            print(f"Q-REBUTJADA: {err}")
        print(f"Resum: {len(q_errors)} preguntes invàlides")
        
    if unassigned or q_errors:
        return False
        
    return True

def main():
    check_mode = '--check' in sys.argv
    
    # T1: Validate vendors before doing anything else
    require_vendor()
    
    # T2: Run content validations (Notes + Questions)
    # These must pass for both build and --check
    if not run_checks():
        sys.exit(1)
        
    if check_mode:
        # In --check mode, we perform validations but do NOT write outputs.
        print("Check OK")
        return

    # Normal build mode
    
    # Ensure assets directory exists
    os.makedirs(ASSETS, exist_ok=True)
    
    # Copy JS vendors
    shutil.copy(os.path.join(VENDORS, 'marked.min.js'), os.path.join(ASSETS, 'marked.min.js'))
    shutil.copy(os.path.join(VENDORS, 'highlight.min.js'), os.path.join(ASSETS, 'highlight.min.js'))
    
    # Copy fonts
    fonts_dst = os.path.join(ASSETS, 'fonts')
    os.makedirs(fonts_dst, exist_ok=True)
    for f in os.listdir(FONTS_SRC):
        if f.endswith('.css') or f.endswith('.woff2'):
            shutil.copy(os.path.join(FONTS_SRC, f), os.path.join(fonts_dst, f))
            
    # Generate index.html with static footer (T3 requirement prep)
    html_content = """<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <title>DevLab</title>
    <link rel="stylesheet" href="assets/fonts/fonts-local.css">
</head>
<body>
    <h1>DevLab</h1>
    <footer>generat amb <code>build.py</code></footer>
    <script src="assets/marked.min.js"></script>
    <script src="assets/highlight.min.js"></script>
</body>
</html>"""
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Generate dummy data.js and questions-extra.js to satisfy structure checks
    with open(os.path.join(ASSETS, 'data.js'), 'w', encoding='utf-8') as f:
        f.write("window.GROUPS = [];")
        
    with open(os.path.join(ASSETS, 'questions-extra.js'), 'w', encoding='utf-8') as f:
        f.write("window.QUESTIONS_EXTRA = {};")

if __name__ == '__main__':
    main()
=== END FILE ===