The user wants to implement **T1: Implement pure segmentation helper and unit tests**.

**Analysis of Requirements:**
1.  **File**: `src/lib/cmd-code.ts`
2.  **Exports**:
    *   `CMD`: A string constant `'npx skills add jordimarsal/harness'`.
    *   `splitCmdLine`: A function that takes a string `line` and returns an object `{ before, cmd, after }` or `null`.
3.  **Logic for `splitCmdLine`**:
    *   It must find the exact substring `CMD` within the input line.
    *   If found, it splits the line into three parts:
        *   `before`: The text preceding the command.
        *   `cmd`: The command itself (should be exactly `CMD`).
        *   `after`: The text following the command.
    *   If the command is not found, return `null`.
    *   It must not mutate the input.

**Test Cases Analysis (`src/lib/cmd-code.spec.ts`):**
*   `CMD` should be `'npx skills add jordimarsal/harness'`.
*   Case 1: Mid-line occurrence.
    *   Input: `'Its process ships as six standalone skills, installable with npx skills add jordimarsal/harness.'`
    *   Expected `before`: `'Its process ships as six standalone skills, installable with '`
    *   Expected `cmd`: `'npx skills add jordimarsal/harness'`
    *   Expected `after`: `'.'`
*   Case 2: No command.
    *   Input: `'Born from daily use across personal projects.'`
    *   Expected: `null`
*   Case 3: Command at start.
    *   Input: `'npx skills add jordimarsal/harness and then some'`
    *   Expected `before`: `''`
    *   Expected `cmd`: `'npx skills add jordimarsal/harness'`
    *   Expected `after`: `' and then some'`
*   Case 4: Command at end.
    *   Input: `'Installable with npx skills add jordimarsal/harness'`
    *   Expected `before`: `'Installable with '`
    *   Expected `cmd`: `'npx skills add jordimarsal/harness'`
    *   Expected `after`: `''`
*   Case 5: Immutability check (standard JS string behavior).

**Implementation Plan:**
1.  Define `CMD` constant.
2.  Implement `splitCmdLine(line: string)`.
    *   Use `line.indexOf(CMD)` to find the position.
    *   If `-1`, return `null`.
    *   Otherwise, slice the string into `before`, `cmd`, `after`.
    *   Return `{ before, cmd, after }`.

Let's write the code.

```typescript
export const CMD = 'npx skills add jordimarsal/harness';

export interface SplitResult {
  before: string;
  cmd: string;
  after: string;
}

export function splitCmdLine(line: string): SplitResult | null {
  const index = line.indexOf(CMD);
  if (index === -1) {
    return null;
  }
  
  const before = line.slice(0, index);
  const cmd = line.slice(index, index + CMD.length);
  const after = line.slice(index + CMD.length);
  
  return { before, cmd, after };
}
```

This looks correct and satisfies all test cases. I will create the file `src/lib/cmd-code.ts`. The spec file is already provided in the prompt context as "TESTS THE FINAL RESULT MUST PASS", so I don't need to generate it, but the task says "Implement pure segmentation helper and unit tests". Usually, this means creating both files if they don't exist. However, the prompt says "CURRENT REPOSITORY STATE ... (none yet)" for previous work, but lists `src/lib/cmd-code.spec.ts` under FILES. And then provides its content under "TESTS THE FINAL RESULT MUST PASS". This implies the spec file might already be there or I should ensure it exists. Given the instruction "Output ONLY the files this step needs... at the paths the plan gives", and T1 includes "unit tests", I should probably output both files to be safe, ensuring the spec matches what's expected. Wait, looking closely: "TESTS THE FINAL RESULT MUST PASS" usually implies these are existing constraints. But since "YOUR PREVIOUS WORK IN THIS TASK" is "(none yet)", I am starting from scratch. I will provide both files to ensure the gate passes. Actually, often in these tasks, if the spec is provided in the prompt, I just need to implement the source. But to be thorough and follow "Implement ... unit tests", I will include the spec file as well, matching the provided content exactly.

Wait, looking at the structure:
FILES
src/lib/cmd-code.ts
src/lib/cmd-code.spec.ts

I will generate both.

=== FILE: src/lib/cmd-code.ts ===
export const CMD = 'npx skills add jordimarsal/harness';

export interface SplitResult {
  before: string;
  cmd: string;
  after: string;
}

/**
 * Splits a line of text into segments around the known install command.
 * Returns null if the command is not present in the line.
 */
export function splitCmdLine(line: string): SplitResult | null {
  const index = line.indexOf(CMD);
  if (index === -1) {
    return null;
  }

  const before = line.slice(0, index);
  const cmd = line.slice(index, index + CMD.length);
  const after = line.slice(index + CMD.length);

  return { before, cmd, after };
}
=== END FILE ===

=== FILE: src/lib/cmd-code.spec.ts ===
import { describe, expect, it } from 'vitest';
import { CMD, splitCmdLine } from './cmd-code';

describe('splitCmdLine', () => {
  it('exposes the exact install command as CMD', () => {
    expect(CMD).toBe('npx skills add jordimarsal/harness');
  });

  it('splits a mid-line occurrence into before/cmd/after', () => {
    const line =
      'Its process ships as six standalone skills, installable with npx skills add jordimarsal/harness.';
    const r = splitCmdLine(line);
    expect(r).not.toBeNull();
    expect(r?.cmd).toBe('npx skills add jordimarsal/harness');
    expect(r?.before).toBe('Its process ships as six standalone skills, installable with ');
    expect(r?.after).toBe('.');
  });

  it('returns null when the line has no command', () => {
    expect(splitCmdLine('Born from daily use across personal projects.')).toBeNull();
  });

  it('handles the command at line start (before is empty)', () => {
    const r = splitCmdLine('npx skills add jordimarsal/harness and then some');
    expect(r?.before).toBe('');
    expect(r?.cmd).toBe('npx skills add jordimarsal/harness');
    expect(r?.after).toBe(' and then some');
  });

  it('handles the command at line end (after is empty)', () => {
    const r = splitCmdLine('Installable with npx skills add jordimarsal/harness');
    expect(r?.before).toBe('Installable with ');
    expect(r?.after).toBe('');
  });

  it('does not mutate the input', () => {
    const line = 'with npx skills add jordimarsal/harness inside';
    splitCmdLine(line);
    expect(line).toBe('with npx skills add jordimarsal/harness inside');
  });
});
=== END FILE ===