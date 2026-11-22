FILES
src/components/site/DeptPanel.astro
src/styles/site.css
tests/fixtures/parity.json

TASKS
T1: Update DeptPanel markup to position CTA before body content
    depends_on: (none)
    refs: R1
T2: Add scoped CSS for filled CTA and disabled fill-sweep overlay
    depends_on: T1
    refs: R2
T3: Add scoped CSS to disable card hover/focus overlays and reduce sizing within panels
    depends_on: T1
    refs: R3, R4
T4: Regenerate parity fixture to match new panel markup order
    depends_on: T1
    refs: R5

GATES
npm run build && node -e "const fs=require('fs'); const locales=['en','es','ca']; locales.forEach(l => { const html = fs.readFileSync(`dist/${l}/index.html`, 'utf8'); const regex = /<div class=\"dept-panel\"[^>]*>([\s\S]*?)<\/div>\s*(?=<div class=\"dept-panel\"|<\/main>|$)/g; let m; while((m=regex.exec(html))!==null){ const panel=m[0]; const btnIdx=panel.indexOf('.btn'); const bodySelectors=['.cards','.ledger','.prose','.pills','.q-plaque-copy']; let minBodyIdx=Infinity; bodySelectors.forEach(s=>{const i=panel.indexOf(s); if(i>-1&&i<minBodyIdx)minBodyIdx=i;}); if(btnIdx===-1||minBodyIdx===Infinity) continue; if(btnIdx>=minBodyIdx) throw new Error('CTA not before body in '+l); }); console.log('R1 Gate Passed'); }"
grep -q ".dept-panel__cta .btn { background: var(--y1)" src/styles/site.css && grep -q ".dept-panel__cta .btn::before { display: none" src/styles/site.css || (echo "R2 Gate Failed"; exit 1)
grep -q ".dept-panel .card::before { display: none" src/styles/site.css && grep -q ".dept-panel .card:hover { transform: translateY(-2px)" src/styles/site.css || (echo "R3/R4 Gate Failed"; exit 1)
npx vitest run
npm run distill:parity
git diff --name-only | grep -vE "^(src/components/site/DeptPanel.astro|src/styles/site.css|tests/fixtures/parity.json)$" && echo "Unexpected files changed" && exit 1