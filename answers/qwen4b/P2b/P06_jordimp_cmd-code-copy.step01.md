The user wants to implement **T1: Implement command extraction and segmentation helper**.

**Analysis of Requirements:**
1.  **File Path**: `src/lib/cmd-code.ts`
2.  **Dependencies**: None.
3.  **References**: R1, R4 (likely referring to requirements about rendering commands and copy behavior, but T1 is just the logic).
4.  **Test File**: `src/lib/cmd-code.spec.ts` defines the exact API.

**API Definition from Tests (`src/lib/cmd-code.spec.ts`):**
*   Export constant `CMD`: `'npx skills add jordimarsal/harness'`.
*   Export function `splitCmdLine(line: string): { cmd: string; before: string; after: string } | null`.
    *   If `line` contains `CMD`, return an object with `cmd` set to `CMD`, `before` as the substring before it, and `after` as the substring after it.
    *   If `line` does not contain `CMD`, return `null`.
    *   Must handle start/end cases correctly (empty strings for before/after).
    *   Must not mutate input (strings are immutable in JS anyway, but good to keep in mind).

**Implementation Plan:**
1.  Define `export const CMD = 'npx skills add jordimarsal/harness';`.
2.  Implement `splitCmdLine`:
    *   Check if `line.includes(CMD)`.
    *   If false, return `null`.
    *   Find index of `CMD`.
    *   Slice `before` and `after`.
    *   Return `{ cmd: CMD, before, after }`.

Let's double check edge cases from tests:
- `splitCmdLine('Its process ships as six standalone skills, installable with npx skills add jordimarsal/harness.')` -> `before: '...with '`, `cmd: ...`, `after: '.'`. Correct.
- `splitCmdLine('Born from daily use across personal projects.')` -> `null`. Correct.
- `splitCmdLine('npx skills add jordimarsal/harness and then some')` -> `before: ''`, `cmd: ...`, `after: ' and then some'`. Correct.
- `splitCmdLine('Installable with npx skills add jordimarsal/harness')` -> `before: 'Installable with '`, `cmd: ...`, `after: ''`. Correct.

The implementation is straightforward.

```typescript
export const CMD = 'npx skills add jordimarsal/harness';

export interface SplitResult {
  cmd: string;
  before: string;
  after: string;
}

export function splitCmdLine(line: string): SplitResult | null {
  const index = line.indexOf(CMD);
  if (index === -1) {
    return null;
  }
  
  return {
    cmd: CMD,
    before: line.slice(0, index),
    after: line.slice(index + CMD.length),
  };
}
```

Wait, looking at the test file again:
```typescript
import { describe, expect, it } from 'vitest';
import { CMD, splitCmdLine } from './cmd-code';
```
It imports `CMD` and `splitCmdLine`. It does not import a type `SplitResult`, but returning an object literal is fine. I will define the interface for clarity or just let TS infer it. The prompt asks to output files needed. Only `src/lib/cmd-code.ts` is needed for T1.

Let's verify against "GATES" later steps might rely on this.
- T2 adds copy affordance.
- T3 verifies rendering parity.
- T4 updates tests.

The current step is strictly T1.

One detail: `line.indexOf(CMD)` vs `includes`. `indexOf` gives position which is needed for slicing.

Final check of the code structure.
File: `src/lib/cmd-code.ts`

```typescript
export const CMD = 'npx skills add jordimarsal/harness';

export function splitCmdLine(line: string): { cmd: string; before: string; after: string } | null {
  const idx = line.indexOf(CMD);
  if (idx === -1) return null;
  
  return {
    cmd: CMD,
    before: line.slice(0, idx),
    after: line.slice(idx + CMD.length),
  };
}
```
This looks correct and minimal.

=== FILE: src/lib/cmd-code.ts ===
export const CMD = 'npx skills add jordimarsal/harness';

export interface SplitResult {
  cmd: string;
  before: string;
  after: string;
}

export function splitCmdLine(line: string): SplitResult | null {
  const index = line.indexOf(CMD);
  if (index === -1) {
    return null;
  }

  return {
    cmd: CMD,
    before: line.slice(0, index),
    after: line.slice(index + CMD.length),
  };
}
=== END FILE ===