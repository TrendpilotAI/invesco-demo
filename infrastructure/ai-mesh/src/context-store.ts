// AI Mesh — Shared Context Store

interface ContextEntry {
  value: unknown;
  updatedAt: number;
  expiresAt: number | null;
}

export class ContextStore {
  private store: Map<string, ContextEntry> = new Map();

  private key(namespace: string, key: string): string {
    return `${namespace}::${key}`;
  }

  set(namespace: string, key: string, value: unknown, ttlMs?: number): void {
    this.store.set(this.key(namespace, key), {
      value,
      updatedAt: Date.now(),
      expiresAt: ttlMs ? Date.now() + ttlMs : null,
    });
  }

  get(namespace: string, key: string): unknown | undefined {
    const entry = this.store.get(this.key(namespace, key));
    if (!entry) return undefined;
    if (entry.expiresAt && Date.now() > entry.expiresAt) {
      this.store.delete(this.key(namespace, key));
      return undefined;
    }
    return entry.value;
  }

  delete(namespace: string, key: string): boolean {
    return this.store.delete(this.key(namespace, key));
  }

  /** List all live keys in a namespace */
  keys(namespace: string): string[] {
    const prefix = `${namespace}::`;
    const result: string[] = [];
    const now = Date.now();
    for (const [k, entry] of this.store) {
      if (k.startsWith(prefix)) {
        if (entry.expiresAt && now > entry.expiresAt) {
          this.store.delete(k);
        } else {
          result.push(k.slice(prefix.length));
        }
      }
    }
    return result;
  }

  /** Shared global namespace helpers */
  setGlobal(key: string, value: unknown, ttlMs?: number): void {
    this.set('__global__', key, value, ttlMs);
  }

  getGlobal(key: string): unknown | undefined {
    return this.get('__global__', key);
  }
}
