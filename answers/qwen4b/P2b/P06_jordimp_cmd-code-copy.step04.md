The test file `src/lib/cmd-code.spec.ts` already exists in the repository state and matches exactly what's required by T4. Let me verify the implementation against each test case to confirm everything passes.

Looking at the existing `cmd-code.ts`:
- `CMD` is exported as `'npx skills add jordimarsal/harness'` ✓
- `splitCmdLine` finds the command via `indexOf`, returns `null` if absent, otherwise splits into `{ cmd, before, after }` ✓

All six test cases pass with the current implementation:
1. CMD exact string match ✓
2. Mid-line split → correct before/after ✓
3. No command → null ✓
4. Command at start → before empty ✓
5. Command at end → after empty ✓
6. Input immutability (strings are immutable; no mutation occurs) ✓

Since the spec file already exists verbatim and the implementation satisfies it, I'll re-output both files unchanged to confirm their final state for this step.

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