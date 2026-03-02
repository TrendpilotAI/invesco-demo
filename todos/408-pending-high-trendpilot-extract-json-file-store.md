# 408 — Extract Generic JsonFileStore<T> to Eliminate DRY Violations

**Priority:** HIGH (P1) — Enables clean Supabase migration  
**Repo:** Trendpilot  
**Effort:** S (½ day)  
**Dependencies:** None  
**Unlocks:** 236-pending-p0-trendpilot-wire-supabase-data-store.md

## Problem
The same file-backed JSON store boilerplate is copy-pasted across 6+ services:
- `src/services/storage/index.ts`
- `src/services/email/digest.ts`
- `src/services/theming/index.ts`
- `src/services/teams/index.ts`
- `src/services/tenants/index.ts`
- `src/services/apiKeys/index.ts`

~150 lines of near-identical `read()`/`write()` using `fs.readFileSync`/`fs.writeFileSync`.

## Coding Prompt
```
Create /data/workspace/projects/Trendpilot/src/lib/JsonFileStore.ts:

export class JsonFileStore<T extends { id: string }> {
  private filePath: string;
  
  constructor(filePath: string) {
    this.filePath = filePath;
  }
  
  read(): T[] {
    if (!fs.existsSync(this.filePath)) return [];
    return JSON.parse(fs.readFileSync(this.filePath, 'utf-8'));
  }
  
  write(data: T[]): void {
    fs.mkdirSync(path.dirname(this.filePath), { recursive: true });
    fs.writeFileSync(this.filePath, JSON.stringify(data, null, 2));
  }
  
  getById(id: string): T | undefined {
    return this.read().find(item => item.id === id);
  }
  
  save(item: T): T {
    const all = this.read();
    const idx = all.findIndex(i => i.id === item.id);
    if (idx >= 0) all[idx] = item; else all.push(item);
    this.write(all);
    return item;
  }
  
  delete(id: string): boolean {
    const all = this.read();
    const filtered = all.filter(i => i.id !== id);
    if (filtered.length === all.length) return false;
    this.write(filtered);
    return true;
  }
}

Then refactor all 6 services to use JsonFileStore<T> instead of copy-pasted logic.
Write unit tests for JsonFileStore in tests/lib/jsonFileStore.test.ts.
```

## Acceptance Criteria
- [ ] `JsonFileStore<T>` extracted to `src/lib/JsonFileStore.ts`
- [ ] All 6 services refactored to use it
- [ ] All existing tests still pass
- [ ] Unit tests for the generic class added
