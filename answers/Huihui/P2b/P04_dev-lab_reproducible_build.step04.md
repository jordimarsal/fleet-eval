The user wants me to implement **T4: Add automated verification tests**.

Looking at the plan and the "TESTS THE FINAL RESULT MUST PASS" section, I see `tests/build.test.js` is provided as the reference implementation for what the tests *should* look like or verify against. However, the task list says:
`T4: Add automated verification tests`
`refs: R1, R2, R3, R4, R5, R6`

And the FILES section lists:
`tests/build_reproducible.test.js`
`tests/validation_errors.test.js`

Wait, looking closely at the prompt structure:
- The "FULL PLAN" lists specific files: `tests/build_reproducible.test.js` and `tests/validation_errors.test.js`.
- The "CURRENT STEP TO IMPLEMENT NOW" is T4.
- The "OTHER SOURCE FILES" shows existing test files like `tests/grader.test.js`, `tests/django_ab.test.js`, etc., but notably does NOT show `tests/build_reproducible.test.js` or `tests/validation_errors.test.js` in the tree (the tree was empty in the prompt's "CURRENT REPOSITORY STATE").
- The "TESTS THE FINAL RESULT MUST PASS" section provides `tests/build.test.js`. This looks like a *reference* or perhaps the actual target file name if the plan's filenames were just placeholders? No, usually in these prompts, the "FILES" section defines exactly which files to create/modify.

Let's re-read carefully.
The plan says:
FILES
...
tests/build_reproducible.test.js
tests/validation_errors.test.js

So I need to create these two files.

However, the content of the tests needs to verify R1-R6.
R1: Vendor assets migration and path update.
R2: Hard validation logic for vendors.
R3: Hard validation logic for groups/orphans.
R4: Hard validation logic for questions.
R5: Reproducible build output.
R6: --check mode.

The provided reference test `tests/build.test.js` covers all these scenarios (R1-R6) in one file. But the plan asks for two specific files. It is likely that `build_reproducible.test.js` should cover R1, R5, R6 (reproducibility/checks) and `validation_errors.test.js` should cover R2, R3, R4 (error handling). Or maybe split differently.

Let's look at the requirements again.
T4 depends on T3 (Reproducible build + check mode).
The gates are:
- `python3 build.py --check` exits 0...
- Sandbox: Remove vendor -> exit != 0, stderr "marked.min.js"
- Sandbox: Orphan note -> exit != 0, stderr "orphan"
- Sandbox: Invalid question -> exit != 0, stderr rejected ID
- Reproducibility: Run twice, compare SHA-256. No date in index.html.
- `npm test` passes.

I will create the two files specified in the plan. I will distribute the tests logically.
`tests/validation_errors.test.js`: Tests for R2 (vendor missing), R3 (orphan note), R4 (invalid question).
`tests/build_reproducible.test.js`: Tests for R1 (vendor presence/paths), R5 (byte-identical builds, no dates), R6 (--check mode behavior).

I need to ensure the tests use the correct helpers (sandboxing, running python). The reference `build.test.js` provides a good template for the sandbox logic. I should replicate that logic or import it if possible, but since these are new files and I don't see a shared helper file in the repo state (only `grader-helpers.mjs` is mentioned in other tests, not build ones), I will inline the necessary utilities in each test file or keep them self-contained as per standard Node.js testing practices when no shared module is explicitly provided for *these* specific tests. Given the small size, inlining is safer to avoid dependency issues with non-existent files.

Wait, looking at `tests/grader.test.js`, it imports from `./grader-helpers.mjs`.
Looking at `tests/build.test.js` (the reference), it defines `sandbox()` and `run()` locally.
Since the plan doesn't list a helper file for build tests, I will define the helpers inside the test files or create a minimal setup. To be safe and follow the "FILES" constraint strictly, I will only output the two requested test files. I will include the necessary utility functions within them.

Let's refine the content of each file based on the Reference Test `build.test.js` which seems to contain the exact assertions required by the Gates.

**File 1: `tests/validation_errors.test.js`**
- R2: Vendor missing check.
- R3: Orphan note check.
- R4: Invalid question check.

**File 2: `tests/build_reproducible.test.js`**
- R1: Vendor assets exist and paths are correct in `build.py`.
- R5: Reproducibility (double build hash match) + No date in footer.
- R6: `--check` mode does not write files.

I need to make sure the Python commands match what `build.py` expects.
The reference test uses:
`execSync(`${PY} build.py ${args}`, ...)`

And checks specific strings:
R2: 'vendor incomple', no 'Traceback'.
R3: 'NO ASSIGNADES', slug name.
R4: 'Q-REBUTJADA', 'invàlides'.
R5: SHA-256 comparison, regex for dates `\d{2}\/\d{2}\/\d{4}`.
R6: File hashes unchanged after `--check`, output contains 'Check OK'.

One detail: The reference test R4 modifies `src/questions/extra-lenguaje.json`. I must ensure this file exists in the sandbox or handle its absence. The reference assumes it exists because it reads it first. In a real repo, if it doesn't exist, the test fails. However, looking at other tests (`django_ab.test.js`), they read specific bank files. It is highly likely `extra-lenguaje.json` exists in the repo context implied by the "Other Source Files" (though not explicitly shown, `extra-shell.json` etc are). Wait, `tests/shell_scripting.test.js` references `extra-shell.json`. `tests/django_ab.test.js` references `extra-django.json`.
Does `extra-lenguaje.json` exist?
The prompt's "CURRENT REPOSITORY STATE" is empty.
However, T1-T3 were implemented. Did they create question banks?
T2 says "Implement hard validation logic...".
Usually, these tasks come with a pre-existing content structure. If `extra-lenguaje.json` does not exist, the test will crash on `readFileSync`.
To be robust, I should check if the file exists before reading, or create a dummy one in the sandbox if missing? No, standard practice for these "verification" tests is to assume the repo state is valid *except* for the mutation being tested.
If `extra-lenguaje.json` is not part of the base repo, R4 cannot run as written in the reference.
Let's look at the Gates again:
"Sandbox test: Inject invalid question schema into `src/questions/extra-dades.json`..."
Ah! The Gate mentions `extra-dades.json`.
But the Reference Test `build.test.js` uses `extra-lenguaje.json`.
There is a conflict between the Gate description and the Reference Test filename.
The Reference Test is labeled "TESTS THE FINAL RESULT MUST PASS (they define the exact API)". This usually takes precedence over the textual description of gates if there's a mismatch, OR the gate description is just an example and the actual test file defines the truth.
However, if `extra-lenguaje.json` doesn't exist, the test fails immediately.
I will assume that either:
1. `extra-lenguaje.json` exists in the repo (created by previous steps or pre-existing).
2. I need to adapt the test to use a file that definitely exists, like one from other themes, OR create it in the sandbox setup.

Actually, looking at `tests/shell_scripting.test.js`, it reads `extra-shell.json`.
If I write the test to read `extra-lenguaje.json` and it's not there, it breaks.
Safe approach: In the sandbox setup for R4, check if a specific bank file exists. If not, pick any existing `.json` in `src/questions/`. Or better, since I am writing the *test*, I can make it robust: find any JSON file in `src/questions/` to mutate.

Let's look at the reference code again:
```javascript
const bank = JSON.parse(readFileSync(join(sb, 'src/questions/extra-lenguaje.json'), 'utf8'));
```
This is hardcoded. If this file isn't in the repo, the provided "Reference" would fail on a clean checkout unless that file was created in T1-T3. Since I don't see evidence of its creation in the "Previous Work" (which only shows vendor files and build.py), it might be missing.
However, often in these prompts, the "Other Source Files" are excerpts. It's possible `extra-lenguaje.json` is part of the base content.
To be safe, I will modify the test logic slightly to be more robust: iterate through available question files or use a known one from other tests (like `extra-shell.json`) if `extra-lenguaje.json` is risky? No, sticking to the reference is usually best for "exact API". But if the file doesn't exist, the test fails.
I'll add a check: if the specific file doesn't exist, create a minimal valid one in the sandbox before mutating? Or just pick the first `.json` found in `src/questions`.
Actually, the prompt says "Implement ONLY this step... preserve their behavior". The previous steps didn't show creating question banks. But T2 implemented validation *logic*. The data must come from somewhere.
Let's assume the standard repo structure includes some question banks. I will write the test to look for `extra-lenguaje.json` but fallback to any existing JSON if it's not there, to prevent false negatives due to missing fixture data.

Wait, looking at the provided `build.py`, it globs `QUESTIONS_DIR = os.path.join(ROOT, 'src', 'questions')`.
If no files are there, `validate_questions` passes trivially.
For R4 to work, we need a file to corrupt.
I will make the test find an existing JSON file in `src/questions/`. If none exists, it creates a dummy one in the sandbox. This makes the test self-contained and robust against the exact filename.

Same for R3 (Orphan note): It creates `md/ZZZ/orfe-test.md`. This is safe.
R2 (Vendor): Removes `vendor/marked.min.js`. Safe.

So, plan for `tests/validation_errors.test.js`:
1. Helper functions (`sandbox`, `run`).
2. Test R2: Remove vendor, expect error.
3. Test R3: Add orphan md, expect error.
4. Test R4: Find/create a question json, inject bad schema, expect error.

Plan for `tests/build_reproducible.test.js`:
1. Helper functions.
2. Test R1: Check vendor files exist in repo root, check `build.py` source strings.
3. Test R5: Run build twice in sandbox, compare hashes of outputs. Check index.html footer for dates.
4. Test R6: Run `--check` in sandbox, ensure no files changed/written.

One detail from Reference R1:
```javascript
assert.ok(src.includes("VENDORS = os.path.join(ROOT, 'vendor')"), 'VENDORS cap a repo');
```
My `build.py` has exactly that string. Good.

Reference R6:
```javascript
const firstNote = `p/${readdirSync(join(sb, 'p'))[0]}`;
```
This assumes `p/` exists and is not empty *before* the check? No, `--check` shouldn't write. But `p/` might be generated by a previous build or committed. The reference test runs on a sandbox copied from ROOT. If ROOT has `p/` (generated artifacts), it works. If not, `readdirSync` throws.
The Gate says: "`python3 build.py --check` exits 0 with no file writes on a clean repo."
If `p/` doesn't exist, does `--check` fail? My `build.py` implementation in "Previous Work" calls `validate_notes`, which scans `md/`. It doesn't seem to require `p/` to exist for validation.
However, the test tries to read `p/[first_file]` to hash it *before* running check. If `p/` is missing, this crashes.
I should handle the case where `p/` might be empty or missing in the test setup, OR ensure the test only watches files that definitely exist (like `index.html` if it's committed, or just skip watching `p/` if it's not there).
Actually, looking at R5, it runs a full build first (`run(sb, '')`). This generates `p/`.
R6 in the reference runs on a *fresh* sandbox?
```javascript
const sb = sandbox(); // Fresh copy
// ...
const firstNote = `p/${readdirSync(join(sb, 'p'))[0]}`; 
```
This implies `p/` must exist in the source repo. Since T3 implemented "Reproducible build output", presumably the artifacts are either committed or generated. The gate says "on a clean repo". Usually "clean repo" means git-clean, but does it include generated files?
If I look at `tests/build.test.js` R1:
`assert.ok(existsSync(join(ROOT, 'assets/marked.min.js')), 'output vendor present a assets/');`
It expects `assets/` to exist in ROOT.
So the repo state includes built artifacts.
Therefore, `p/` should also exist.
I will follow the reference logic closely.

One adjustment for R4 robustness:
Instead of hardcoding `extra-lenguaje.json`, I'll do:
```javascript
let qFile = join(sb, 'src/questions/extra-lenguaje.json');
if (!existsSync(qFile)) {
  const dir = join(sb, 'src/questions');
  if (existsSync(dir)) {
    const files = readdirSync(dir).filter(f => f.endsWith('.json'));
    if (files.length > 0) qFile = join(dir, files[0]);
  } else {
    mkdirSync(dir, {recursive: true});
    writeFileSync(qFile, '[]'); // Create dummy if none exists
  }
}
// Then read and mutate
```
This ensures the test passes regardless of which specific bank file is present, as long as *some* question infrastructure exists or can be created.

Let's write the files.

=== FILE: tests/validation_errors.test.js ===
Content: Node.js test module using `node:test`. Imports fs, path, child_process. Defines sandbox/run helpers. Tests R2, R3, R4.

=== FILE: tests/build_reproducible.test.js ===
Content: Node.js test module. Defines sandbox/run helpers. Tests R1, R5, R6.

I will ensure the code style matches the other tests (ESM imports, strict assert).

One final check on R6 in reference:
`assert.ok(r.out.includes('Check OK'), ...)`
My `build.py` needs to print "Check OK".
Looking at my previous work for `build.py`:
It ends with:
```python
if args.check:
    # ... validation logic ...
    pass # It doesn't explicitly print "Check OK" in the snippet provided?
```
Wait, the snippet for `build.py` in "Previous Work" cuts off at `if args.`.
However, T3 was "Implement reproducible build output and --check mode".
The Gate says: "`python3 build.py --check` exits 0...".
The Reference Test expects `r.out.includes('Check OK')`.
If my current `build.py` implementation (from previous steps) does *not* print "Check OK", the test will fail.
Since I am implementing T4 (Tests), I must assume T3 is complete and correct. If T3 didn't add the print statement, that's a bug in T3. But I can only modify files listed in T4.
Can I modify `build.py`? No, T4 is "Add automated verification tests". The FILES list for T4 only includes the two test files.
Therefore, I must assume `build.py` already prints "Check OK".
(If it doesn't, the test fails, but I cannot fix `build.py` in this step without violating the "FILES" constraint or stepping into T3 territory which is marked as done/dependent).
Actually, looking at the prompt structure, "YOUR PREVIOUS WORK IN THIS TASK" shows `build.py`. It ends abruptly.
But usually, these prompts imply the dependencies are satisfied. I will write the test expecting "Check OK" as per the reference.

One detail: `tests/build.test.js` (reference) uses `import { tmpdir } from 'node:os';`.
I will use the same imports.

Final check on R1 in Reference:
It checks `assets/marked.min.js` exists in ROOT.
My sandbox copies everything except `.git`, `node_modules`, etc. So if it's in ROOT, it's in Sandbox.
The test runs on ROOT directly for R1 (`existsSync(join(ROOT, ...))`). This is fine.

Let's generate the files.

=== FILE: tests/validation_errors.test.js ===
```javascript
// tests/validation_errors.test.js — validation logic (R2–R4)
// Verifies that build.py exits with non-zero code and specific error messages
// when vendor files are missing, notes are orphaned, or question schemas are invalid.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  readFileSync, existsSync, mkdirSync, cpSync, rmSync, readdirSync, writeFileSync,
} from 'node:fs';
import { execSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const PY = 'python3';

function sandbox() {
  const dir = join(tmpdir(), `devlab-sb-${process.pid}-${Math.random().toString(36).slice(2)}`);
  mkdirSync(dir);
  const skip = new Set(['.git', 'node_modules', 'harness', 'tests']);
  for (const entry of readdirSync(ROOT)) {
    if (skip.has(entry)) continue;
    cpSync(join(ROOT, entry), join(dir, entry), { recursive: true });
  }
  return dir;
}

function run(dir, args) {
  try {
    const out = execSync(`${PY} build.py ${args}`, { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { code: 0, out };
  } catch (e) {
    return { code: e.status ?? 1, out: `${e.stdout ?? ''}${e.stderr ?? ''}` };
  }
}

// R2 — vendor incomple → error net, sense traceback
test('R2: falta un vendor → exit != 0 amb missatge net', () => {
  const sb = sandbox();
  try {
    rmSync(join(sb, 'vendor/marked.min.js'));
    const r = run(sb, '');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('vendor incomple'), `missatge net: ${r.out.slice(0, 200)}`);
    assert.ok(!r.out.includes('Traceback'), 'sense traceback');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R3 — nota sense grup → exit != 0 amb slugs
test('R3: nota sense assignar → exit != 0 llistant el slug', () => {
  const sb = sandbox();
  try {
    mkdirSync(join(sb, 'md/ZZZ'), { recursive: true });
    writeFileSync(join(sb, 'md/ZZZ/orfe-test.md'), '---\ntitle: Orfe\ntags: []\n---\n\nCos.\n');
    const r = run(sb, '--check');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('NO ASSIGNADES'), 'missatge NO ASSIGNADES');
    assert.ok(r.out.includes('orfe-test'), 'llista el slug');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R4 — pregunta extra invàlida → exit != 0 amb Q-REBUTJADA
test('R4: pregunta extra invàlida → exit != 0', () => {
  const sb = sandbox();
  try {
    // Find an existing question bank file to mutate, or create a dummy one if none exists
    let qFile = join(sb, 'src/questions/extra-lenguaje.json');
    if (!existsSync(qFile)) {
      const dir = join(sb, 'src/questions');
      if (existsSync(dir)) {
        const files = readdirSync(dir).filter(f => f.endsWith('.json'));
        if (files.length > 0) {
          qFile = join(dir, files[0]);
        } else {
          writeFileSync(qFile, '[]');
        }
      } else {
        mkdirSync(dir, { recursive: true });
        writeFileSync(qFile, '[]');
      }
    }

    let bank;
    try {
      bank = JSON.parse(readFileSync(qFile, 'utf8'));
    } catch {
      bank = [];
    }
    
    // Inject invalid question: missing answer for choice type
    bank.push({ t: 'lenguaje', ty: 'choice', q: 'Pregunta trencada de test', opts: ['a', 'b'] }); 
    writeFileSync(qFile, JSON.stringify(bank, null, 1));
    
    const r = run(sb, '--check');
    assert.notEqual(r.code, 0, 'ha de fallar');
    assert.ok(r.out.includes('Q-REBUTJADA'), 'missatge Q-REBUTJADA');
    assert.ok(r.out.includes('invàlides'), 'resum d’errors');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});
```

=== FILE: tests/build_reproducible.test.js ===
```javascript
// tests/build_reproducible.test.js — reproducible build (R1, R5–R6)
// Verifies vendor paths, byte-identical builds, absence of dates in output,
// and that --check mode does not modify the filesystem.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  readFileSync, existsSync, mkdirSync, cpSync, rmSync, readdirSync,
} from 'node:fs';
import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const PY = 'python3';

const sha256 = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

function sandbox() {
  const dir = join(tmpdir(), `devlab-sb-${process.pid}-${Math.random().toString(36).slice(2)}`);
  mkdirSync(dir);
  const skip = new Set(['.git', 'node_modules', 'harness', 'tests']);
  for (const entry of readdirSync(ROOT)) {
    if (skip.has(entry)) continue;
    cpSync(join(ROOT, entry), join(dir, entry), { recursive: true });
  }
  return dir;
}

function run(dir, args) {
  try {
    const out = execSync(`${PY} build.py ${args}`, { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { code: 0, out };
  } catch (e) {
    return { code: e.status ?? 1, out: `${e.stdout ?? ''}${e.stderr ?? ''}` };
  }
}

// R1 — vendors dins el repo i build.py apuntant-hi
test('R1: vendor/ complet i build.py llegeix del repo', () => {
  for (const f of ['vendor/marked.min.js', 'vendor/highlight.min.js', 'vendor/fonts/fonts-local.css']) {
    assert.ok(existsSync(join(ROOT, f)), `falta ${f}`);
  }
  const woffs = readdirSync(join(ROOT, 'vendor/fonts')).filter((f) => f.endsWith('.woff2'));
  assert.ok(woffs.length >= 3, `fonts woff2 presents (${woffs.length})`);
  
  const src = readFileSync(join(ROOT, 'build.py'), 'utf8');
  assert.ok(src.includes("VENDORS = os.path.join(ROOT, 'vendor')"), 'VENDORS cap a repo');
  assert.ok(src.includes("FONTS_SRC = os.path.join(ROOT, 'vendor', 'fonts')"), 'FONTS_SRC cap a repo');
  assert.ok(!src.includes('/tmp/opencode'), 'cap referència a /tmp/opencode');
  
  // Check that built assets exist in the root (committed or generated previously)
  assert.ok(existsSync(join(ROOT, 'assets/marked.min.js')), 'output vendor present a assets/');
});

// R5 — doble build byte-idèntic + footer sense data
test('R5: doble build byte-idèntic i footer sense data', () => {
  const sb = sandbox();
  try {
    const files = ['index.html', 'assets/data.js', 'assets/questions-extra.js'];
    
    // First build
    const r1 = run(sb, '');
    assert.equal(r1.code, 0, `primer build verd: ${r1.out.slice(-200)}`);
    const h1 = files.map((f) => sha256(join(sb, f)));
    
    // Second build
    const r2 = run(sb, '');
    assert.equal(r2.code, 0, 'segon build verd');
    const h2 = files.map((f) => sha256(join(sb, f)));
    
    assert.deepEqual(h2, h1, 'dos builds consecutius → outputs byte-idèntics');
    
    const idx = readFileSync(join(sb, 'index.html'), 'utf8');
    const footerPart = idx.split('<footer')[1] ?? '';
    assert.ok(!/\d{2}\/\d{2}\/\d{4}/.test(footerPart), 'footer sense data');
    assert.ok(idx.includes('generat amb <code>build.py</code>'), 'footer amb text estàtic');
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});

// R6 — --check valida sense escriure (ni modificar) cap output
test('R6: --check valida sense escriure cap output', () => {
  const sb = sandbox();
  try {
    // Ensure p/ exists and has content for hashing, or handle gracefully if not
    let firstNotePath = null;
    const pDir = join(sb, 'p');
    if (existsSync(pDir)) {
      const files = readdirSync(pDir);
      if (files.length > 0) {
        firstNotePath = `p/${files[0]}`;
      }
    }

    const watched = ['index.html', 'assets/style.css', 'assets/data.js'];
    if (firstNotePath) watched.push(firstNotePath);

    const before = Object.fromEntries(watched.map((f) => [f, sha256(join(sb, f))]));
    const listingBefore = readdirSync(sb).sort();
    
    const r = run(sb, '--check');
    assert.equal(r.code, 0, `check verd sobre contingut net: ${r.out.slice(-200)}`);
    assert.ok(r.out.includes('Check OK'), 'missatge final de check');
    
    assert.deepEqual(readdirSync(sb).sort(), listingBefore, 'cap fitxer nou al root');
    for (const f of watched) {
      assert.equal(sha256(join(sb, f)), before[f], `--check no modifica ${f}`);
    }
  } finally {
    rmSync(sb, { recursive: true, force: true });
  }
});
```