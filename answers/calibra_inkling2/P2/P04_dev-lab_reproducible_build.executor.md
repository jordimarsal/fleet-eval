=== FILE: build.py ===
#!/usr/bin/env python3
"""Genera el site estàtic (index + pàgines de nota) des de md/."""
import json, os, re, html, shutil, datetime, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, 'md')
PAGES = os.path.join(ROOT, 'p')
ASSETS = os.path.join(ROOT, 'assets')
VENDORS = os.path.join(ROOT, 'vendor')
FONTS_SRC = os.path.join(ROOT, 'vendor', 'fonts')

GROUPS = [
    {'id': 'lenguaje', 'folder': 'Java', 'title': 'Llenguatge i col·leccions',
     'desc': 'Els fonaments: strings, col·leccions, enums i aquells idiomes del llenguatge que sempre s’escapen.',
     'notes': ['anonim-class', 'enums', 'optional', 'overriding', 'string', 'lists', 'int', 'regex', 'tuples', 'zip', 'utils', 'snippets', 'ram']},
    {'id': 'streams', 'folder': 'Java', 'title': 'Streams i programació funcional',
     'desc': 'Pipelines declaratius amb Streams i la visió reactiva de Reactor quan els bucles clàssics no arriben.',
     'notes': ['streams', 'intstreams', 'functional-interfaces', 'reactor-reactive']},
    {'id': 'spring', 'folder': 'Java', 'title': 'Spring i APIs REST',
     'desc': 'Controladors, validació, gestió d’errors i documentació: el cicle complet d’una API que es respecta.',
     'notes': ['advice', 'controller', 'restcontroller', 'exception', 'validation', 'feing', 'logs', 'cache']},
    {'id': 'dades', 'folder': 'Java', 'title': 'Persistència i dades',
     'desc': 'De JPA a Redis: on viuen les teves dades i com parlar-hi sense sofrir-ho.',
     'notes': ['jpa', 'mongo-query', 'redis', 'jedis', 'json']},
    {'id': 'eines', 'folder': 'Java', 'title': 'Eines i frameworks',
     'desc': 'Lombok, Swagger, Play: l’arsenal que et treballa a tu la feina bruta.',
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
    missing = []
    required_files = ['marked.min.js', 'highlight.min.js', os.path.join('fonts', 'fonts-local.css')]
    for f in required_files:
        if not os.path.isfile(os.path.join(VENDORS, f)):
            missing.append(f)
    try:
        woff2 = [x for x in os.listdir(FONTS_SRC) if x.endswith('.woff2')]
    except Exception:
        woff2 = []
    if len(woff2) < 3:
        missing.append('fonts/*.woff2 (almenys 3; trobats %d)' % len(woff2))
    if missing:
        print('Error: vendor incomple — falta(n) a vendor/: %s' % ', '.join(missing), file=sys.stderr)
        sys.exit(1)


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
    t = re.sub(r'[#*`>_~\\-|]+', ' ', t)
    t = re.sub(r'\\s+', ' ', t)
    return t.strip()


STATIC_FOOTER_TEXT = ("generat amb <code>build.py</code> · Camp de Proves del Java Developer — "
                       "materials d’estudi en català per a qui es prepara el seu salt professional.")


def _notes_index():
    """Llista de dicts {slug, folder} per totes les notes md trobades sota MD."""
    found = []
    for path in sorted(glob.glob(os.path.join(MD, '**', '*.md'), recursive=True)):
        rel = os.path.relpath(path, MD)
        parts = rel.replace(os.sep, '/').split('/')
        if len(parts) != 2:
            continue
        folder, filename = parts
        slug = filename[:-3] if filename.endswith('.md') else filename
        found.append({'slug': slug, 'folder': folder})
    return found


def unassigned_notes(notes):
    unassigned = []
    for n in notes:
        ok = False
        for g in GROUPS:
            if n['folder'] != g['folder']:
                # nota en una carpeta no coneguda mai es assignable
                continue
            wanted = g.get('notes', '*')
            if wanted == '*' or n['slug'] in wanted:
                ok = True
                break
        if not ok:
            unassigned.append(n['slug'] + (' (carpeta \"%s\")' % n['folder'] if n['folder'] not in [g['folder'] for g in GROUPS] else ''))
    return unassigned


VALID_TYPES = {'choice', 'output', 'blank', 'bug', 'order'}
REQUIRED_KEYS = {'t', 'ty', 'q'}


def validate_questions():
    errors = []
    files = sorted(glob.glob(os.path.join(ROOT, 'src', 'questions', '*.json')))
    for path in files:
        name = os.path.basename(path)
        try:
            data = json.load(open(path, encoding='utf-8'))
        except Exception as e:
            errors.append({'file': name, 'idx': None, 'reason': 'JSON invàlid: %s' % e})
            continue
        if isinstance(data, dict) and 'items' in data:  # tolera envoltant { items: [...] }
            data = data['items']
        if not isinstance(data, list):
            errors.append({'file': name, 'idx': None, 'reason': 'no és una llista de preguntes'})
            continue
        for i, q in enumerate(data):
            label = '%s#%d' % (name, i)
            problems = []
            if not isinstance(q, dict):
                problems.append('entrada no és un objecte')
            else:
                missing = sorted(REQUIRED_KEYS - set(q.keys()))
                if missing:
                    problems.append('falten claus obligatòries: ' + ', '.join(missing))
                ty = q.get('ty')
                if ty is not None and str(ty).lower() not in VALID_TYPES:
                    problems.append('tipus desconegut \"%s\"' % ty)
                t = q.get('t')
                known_teams = {g['id'] for g in GROUPS} | {'lenguaje', 'streams', 'spring', 'dades', 'eines', 'maven', 'tests', 'patrons'}
                if t is not None and str(t).lower() not in known_teams:
                    # temes nous permesos? No generat fins que NO ASSIGNADES ho cobreixi; marquem com a suspès però no estris
                    pass
                opts = q.get('opts')
                has_a = ('a' in q) or (q.get('answer') is not None) or (q.get('ans') is not None)
                if ty != 'blank' and not isinstance(opts, list):
                    problems.append('falta una llista \"opts\"')
                elif isinstance(opts, list) and len(opts) < 2:
                    problems.append('una pregunta necessita almenys 2 opcions')
                if ty == 'choice' or ty == 'output' or ty == 'bug' or (ty is None and isinstance(opts, list) and len(opts) >= 2):
                    a = q.get('a', q.get('answer', q.get('ans')))
                    try:
                        ai = int(a)
                        if not isinstance(opts, list) or not (0 <= ai < len(opts)):
                            problems.append('resposta fora de límits')
                    except Exception:
                        problems.append('falta o és invàlida la resposta \"a\"')
                if ty == 'blank' and not (q.get('a') or q.get('answer') or q.get('ans')):
                    problems.append('falta la resposta correcta')
                if ty == 'order' and not (len(q.get('correctOrder') or q.get('correct_order') or []) >= 2):
                    # order pot acceptar simplement opts numerats; no fem bloquejant check aquí
                    pass
            if problems:
                errors.append({'file': name, 'idx': i, 'reason': '; '.join(problems)})
    return errors


def run_checks():
    # validacions dures (exit hard) — exit != 0 si n'hi ha cap
    notes = _notes_index()
    unassigned = unassigned_notes(notes)
   