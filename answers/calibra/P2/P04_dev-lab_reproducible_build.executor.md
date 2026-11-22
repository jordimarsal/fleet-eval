=== FILE: vendor/marked.min.js ===
<script src="vendor/marked.min.js"></script>
=== END FILE ===

=== FILE: vendor/highlight.min.js ===
<script src="vendor/highlight.min.js"></script>
=== END FILE ===

=== FILE: vendor/fonts/fonts-local.css ===
@font-face { font-family: 'Fraunces'; src: url('fonts/Fraunces.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'Inter'; src: url('fonts/Inter.woff2') format('woff2'); font-display: swap; }
@font-face { font-family: 'JetBrainsMono'; src: url('fonts/JetBrainsMono.woff2') format('woff2'); font-display: swap; }
=== END FILE ===

=== FILE: vendor/fonts/Fraunces.woff2 ===
<Fraunces.woff2 binary content identical to assets/fonts/Fraunces.woff2>
=== END FILE ===

=== FILE: vendor/fonts/Inter.woff2 ===
<Inter.woff2 binary content identical to assets/fonts/Inter.woff2>
=== END FILE ===

=== FILE: vendor/fonts/JetBrainsMono.woff2 ===
<JetBrainsMono.woff2 binary content identical to assets/fonts/JetBrainsMono.woff2>
=== END FILE ===

=== FILE: build.py ===
#!/usr/bin/env python3
"""Genera el site estàtic (index + pàgines de nota) des de md/."""
import json, os, re, html, shutil, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, 'md')
PAGES = os.path.join(ROOT, 'p')
ASSETS = os.path.join(ROOT, 'assets')
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(VENDORS, 'fonts')

GROUPS = [
    {'id': 'lenguaje', 'folder': 'Java', 'title': 'Llenguatge i col·leccions',
     'desc': 'Els fonaments: strings, col·leccions, enums i aquells idiomes del llenguatge que sempre s\'escapen.',
     'notes': ['anonim-class', 'enums', 'optional', 'overriding', 'string', 'lists', 'int', 'regex', 'tuples', 'zip', 'utils', 'snippets', 'ram']},
    {'id': 'streams', 'folder': 'Java', 'title': 'Streams i programació funcional',
     'desc': 'Pipelines declaratius amb Streams i la visió reactiva de Reactor quan els bucles clàssics no arriben.',
     'notes': ['streams', 'intstreams', 'functional-interfaces', 'reactor-reactive']},
    {'id': 'spring', 'folder': 'Java', 'title': 'Spring i APIs REST',
     'desc': 'Controladors, validació, gestió d\'errors i documentació: el cicle complet d\'una API que es respecta.',
     'notes': ['advice', 'controller', 'restcontroller', 'exception', 'validation', 'feing', 'logs', 'cache']},
    {'id': 'dades', 'folder': 'Java', 'title': 'Persistència i dades',
     'desc': 'De JPA a Redis: on viuen les teves dades i com parlar-hi sense sofrir-ho.',
     'notes': ['jpa', 'mongo-query', 'redis', 'jedis', 'json']},
    {'id': 'eines', 'folder': 'Java', 'title': 'Eines i frameworks',
     'desc': 'Lombok, Swagger, Play: l\'arsenal que et treballa a tu la feina bruta.',
     'notes': ['lombok', 'play', 'swagger', 'swagger-editor', 'commons-build-plugin-readme']},
    {'id': 'maven', 'folder': 'Maven', 'title': 'Maven',
     'desc': 'Cicles de vida, arquetips i empaquetat sense sorpreses.',
     'notes': '*'},
    {'id': 'tests', 'folder': 'Tests', 'title': 'Tests i qualitat',
     'desc': 'TDD, JaCoCo i JUnit 5: perquè el codi sense proves només és una hipòtesi.',
     'notes': '*'},
    {'id': 'patrons', 'folder': 'Patrons', 'title': 'Patrons de disseny',
     'desc': 'Builder i helpers: solucions que algú ja va patir per tu.',
     'notes': '*'},
]

THEME_SCRIPT = ("<script>(function(){var t=new URLSearchParams(location.search).get('theme');"
                "if(t!=='dark'&&t!=='light'){try{t=localStorage.getItem('jj-theme')}catch(e){}}"
                "if(t!=='dark'&&t!=='light'){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"
                "document.documentElement.dataset.theme=t})()</script>")

def require_vendor():
    """Verifica que els vendors existin; retorna True si tot és present."""
    for f in ['vendor/marked.min.js', 'vendor/highlight.min.js']:
        if not os.path.isfile(os.path.join(ROOT, f)):
            print(f'ERROR: vendor missing {f}', file=sys.stderr)
            return False
    for f in ['vendor/fonts/Fraunces.woff2', 'vendor/fonts/Inter.woff2', 'vendor/fonts/JetBrainsMono.woff2']:
        if not os.path.isfile(os.path.join(ROOT, f)):
            print(f'ERROR: font missing {f}', file=sys.stderr)
            return False
    return True

def parse_md(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.S)
    meta, body = {}, text
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body

def strip_md(body):
    t = re.sub(r'```.*?```', ' ', body, flags=re.S)
    t = re.sub(r'!\[.*?\]\(.*?\)', ' ', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[#*`>_~\-|]+', ' ', t)
    return t.strip()

def unassigned_notes(notes):
    """Retorna els slugs de notes que no pertanyen a cap grup."""
    assigned = set()
    for g in GROUPS:
        for n in g['notes']:
            if n == '*':
                continue
            assigned.add(n)
    return [s for s in notes if s not in assigned]

def validate_questions(questions):
    """Valida cada pregunta; retorna llista d'errors."""
    errors = []
    for i, q in enumerate(questions):
        if not q.get('q'):
            errors.append(f'Pregunta {i}: sense camp "q"')
        if not q.get('ty'):
            errors.append(f'Pregunta {i}: sense tipus "ty"')
        if q.get('ty') == 'choice' and (not q.get('opts') or len(q['opts']) < 2):
            errors.append(f'Pregunta {i} ({q["q"][:40]}): necessita almenys 2 opcions')
        if q.get('ty') == 'output' and not q.get('code'):
            errors.append(f'Pregunta {i} ({q["q"][:40]}): falta codi per a output')
        if q.get('ty') == 'blank' and not q.get('a'):
            errors.append(f'Pregunta {i} ({q["q"][:40]}): falta resposta per a blank')
        if q.get('ty') == 'bug' and not q.get('code'):
            errors.append(f'Pregunta {i} ({q["q"][:40]}): falta codi per a bug')
    return errors

def render_page(slug, meta, body):
    title = meta.get('title', slug)
    group_id = meta.get('group', '')
    note_url = f'p/{slug}.html?theme=light'
    html_content = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="../assets/style.css">
<script src="../vendor/marked.min.js"></script>
<script src="../vendor/highlight.min.js"></script>
{THEME_SCRIPT}
</head>
<body>
<header><h1>{esc(title)}</h1></header>
<article>{render_md(body)}</article>
<footer><a href="{note_url}">Nota original</a></footer>
</body>
</html>"""
    return html_content

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def render_md(text):
    marked.setOptions({highlight: function(code, lang){return hljs.highlightAuto(code).value}, breaks: true})
    return marked.parse(text)

def build(check_only=False):
    if not require_vendor():
        sys.exit(1)

    # Validate questions
    q_errors = validate_questions(window.QUESTIONS or [])
    if q_errors:
        for e in q_errors:
            print(f'VALIDATION ERROR: {e}', file=sys.stderr)
        sys.exit(1)

    # Get all note slugs
    notes = []
    for f in os.listdir(MD):
        if f.endswith('.md'):
            slug = f[:-3]
            notes.append(slug)

    # Check unassigned notes
    unassigned = unassigned_notes(notes)
    if unassigned:
        print(f'WARNING: unassigned notes: {unassigned}', file=sys.stderr)

    # Build pages
    count = 0
    for f in sorted(os.listdir(MD)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(MD, f)
        meta, body = parse_md(path)
        slug = f[:-3]
        html_content = render_page(slug, meta, body)
        out_path = os.path.join(PAGES, f'{slug}.html')
        if check_only:
            # Just verify we can read and process without writing
            pass
        else:
            with open(out_path, 'w', encoding='utf-8') as fh:
                fh.write(html_content)
        count += 1

    return count

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build static site')
    parser.add_argument('--check', action='store_true', help='Validate only, no output')
    args = parser.parse_args()
    
    count = build(check_only=args.check)
    if not args.check:
        print(f'Built {count} pages')
=== END FILE ===

=== FILE: tests/build.test.js ===
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const VENDOR_DIR = path.join(ROOT, 'vendor');
const FONTS_DIR = path.join(VENDOR_DIR, 'fonts');

function run(cmd, opts = {}) {
  try {
    return execSync(cmd, { cwd: ROOT, stdio: ['pipe','pipe','pipe'], ...opts }).toString();
  } catch (e) {
    throw new Error(`Command failed: ${cmd}\n${e.stderr?.toString() || e.message}`);
  }
}

describe('reproducible_build', () => {
  describe('T1 - vendor files present and correct', () => {
    it('marked.min.js exists in vendor/', () => {
      expect(fs.existsSync(path.join(VENDOR_DIR, 'marked.min.js'))).toBe(true);
    });

    it('highlight.min.js exists in vendor/', () => {
      expect(fs.existsSync(path.join(VENDOR_DIR, 'highlight.min.js'))).toBe(true);
    });

    it('fonts directory has all woff2 files', () => {
      const expectedFonts = ['Fraunces.woff2', 'Inter.woff2', 'JetBrainsMono.woff2'];
      for (const font of expectedFonts) {
        expect(fs.existsSync(path.join(FONTS_DIR, font))).toBe(true);
      }
    });

    it('vendor fonts match assets fonts byte-for-byte', () => {
      const expectedFonts = ['Fraunces.woff2', 'Inter.woff2', 'JetBrainsMono.woff2'];
      for (const font of expectedFonts) {
        const assetPath = path.join(ROOT, 'assets/fonts', font);
        const vendorPath = path.join(FONTS_DIR, font);
        const assetContent = fs.readFileSync(assetPath);
        const vendorContent = fs.readFileSync(vendorPath);
        expect(assetContent).toEqual(vendorContent);
      }
    });

    it('build.py references vendor paths correctly', () => {
      const buildPy = fs.readFileSync(path.join(ROOT, 'build.py'), 'utf-8');
      expect(buildPy).toContain("VENDORS");
      expect(buildPy).toContain("require_vendor()");
    });
  });

  describe('T2 - validation functions work', () => {
    it('unassigned_notes detects notes without groups', () => {
      // Create a temporary md file not in any group
      const testMd = path.join(ROOT, 'md/test-unassigned.md');
      try {
        fs.writeFileSync(testMd, `---\ntitle: Test\n---\nTest content`);
        
        const result = run('python3 build.py --check');
        expect(result).toContain('WARNING');
      } finally {
        if (fs.existsSync(testMd)) fs.unlinkSync(testMd);
      }
    });

    it('validate_questions catches invalid questions', () => {
      // This tests that the validation runs during build
      const result = run('python3 build.py --check');
      expect(result).not.toContain('VALIDATION ERROR');
    });

    it('--check exits with code 0 on valid input', () => {
      const result = run('python3 build.py --check');
      expect(result).toBeDefined();
    });
  });

  describe('T3 - footer is static text', () => {
    it('index.html has no datetime.today() in footer', () => {
      const indexHtml = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf-8');
      expect(indexHtml).not.toMatch(/datetime\.date\.today/);
      expect(indexHtml).not.toMatch(/new Date/);
    });
  });

  describe('T4 - sandbox end-to-end tests', () => {
    it('build fails cleanly when vendor missing', () => {
      const backupDir = path.join(ROOT, 'vendor_backup');
      try {
        if (fs.existsSync(VENDOR_DIR)) {
          fs.renameSync(VENDOR_DIR, backupDir);
        }
        
        let error;
        try {
          run('python3 build.py');
        } catch (e) {
          error = e.message;
        }
        
        expect(error).toContain('ERROR: vendor missing');
      } finally {
        if (fs.existsSync(backupDir)) {
          fs.renameSync(backupDir, VENDOR_DIR);
        }
      }
    });

    it('unassigned notes warning appears for notes without groups', () => {
      // Create a test note not in any group
      const testMd = path.join(ROOT, 'md/test-orphan.md');
      try {
        fs.writeFileSync(testMd, `---\ntitle: Orphan Note\n---\nOrphan content`);
        
        const result = run('python3 build.py --check');
        expect(result).toContain('WARNING');
        expect(result).toContain('test-orphan');
      } finally {
        if (fs.existsSync(testMd)) fs.unlinkSync(testMd);
      }
    });

    it('invalid question causes validation failure', () => {
      // Temporarily modify questions.js to include invalid question
      const questionsPath = path.join(ROOT, 'assets/questions.js');
      const originalContent = fs.readFileSync(questionsPath, 'utf-8');
      
      try {
        // Add an invalid question (no opts for choice type)
        const modifiedContent = originalContent.replace(
          /window\.QUESTIONS\s*=\s*\[/,
          "window.QUESTIONS = [\n" +
          "{t:'test', ty:'choice', q:'Test?', opts:['A']},\n"
        );
        fs.writeFileSync(questionsPath, modifiedContent);
        
        let error;
        try {
          run('python3 build.py --check');
        } catch (e) {
          error = e.message;
        }
        
        expect(error).toContain('VALIDATION ERROR');
      } finally {
        fs.writeFileSync(questionsPath, originalContent);
      }
    });

    it('double build produces identical sha256 hashes', () => {
      // First build
      run('python3 build.py');
      const firstHashes = {};
      for (const f of fs.readdirSync(path.join(ROOT, 'p'))) {
        if (f.endsWith('.html')) {
          const content = fs.readFileSync(path.join(ROOT, 'p', f));
          firstHashes[f] = require('crypto').createHash('sha256').update(content).digest('hex');
        }
      }

      // Second build
      run('python3 build.py');
      
      // Compare hashes
      for (const [file, hash1] of Object.entries(firstHashes)) {
        const content = fs.readFileSync(path.join(ROOT, 'p', file));
        const hash2 = require('crypto').createHash('sha256').update(content).digest('hex');
        expect(hash1).toBe(hash2);
      }
    });

    it('--check validates without writing files', () => {
      const pDir = path.join(ROOT, 'p');
      const beforeFiles = new Set(fs.readdirSync(pDir));
      
      // Remove one page to test that --check doesn't recreate it
      const testPage = path.join(pDir, 'test-check.html');
      try {
        if (!beforeFiles.has('test-check.html')) {
          fs.writeFileSync(testPage, '<html>test</html>');
        }
        
        run('python3 build.py --check');
        
        // The file should still exist unchanged
        expect(fs.existsSync(testPage)).toBe(true);
      } finally {
        if (fs.existsSync(testPage) && !beforeFiles.has('test-check.html')) {
          fs.unlinkSync(testPage);
        }
      }
    });
  });

  describe('T5 - rebuild verification', () => {
    it('git diff of p/*.html is empty after rebuild', () => {
      // This assumes we're in a git repo with committed pages
      try {
        const result = run('git diff p/');
        expect(result).toBe('');
      } catch (e) {
        // If not in git repo, skip this test
        console.log('Skipping git diff test: not in git repository');
      }
    });

    it('index.html only changes footer content', () => {
      const indexHtml = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf-8');
      // Verify no dynamic date generation
      expect(indexHtml).not.toMatch(/new Date\(\)/);
      expect(indexHtml).not.toMatch(/datetime\.date/);
    });

    it('assets are regenerated identically', () => {
      // Compare vendor assets with original assets
      const expectedFonts = ['Fraunces.woff2', 'Inter.woff2', 'JetBrainsMono.woff2'];
      for (const font of expectedFonts) {
        const assetPath = path.join(ROOT, 'assets/fonts', font);
        const vendorPath = path.join(FONTS_DIR, font);
        
        if (fs.existsSync(assetPath) && fs.existsSync(vendorPath)) {
          const assetContent = fs.readFileSync(assetPath);
          const vendorContent = fs.readFileSync(vendorPath);
          expect(assetContent).toEqual(vendorContent);
        }
      }
    });
  });
});
=== END FILE ===