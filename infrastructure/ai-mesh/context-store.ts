// context-store.ts - Shared context store for agents

interface StoreEntry {
  value: any;
  expires_at?: number;
  updated_at: number;
}

type Namespace = 'global' | `agent:${string}`;

class ContextStore {
  private store: Map<string, StoreEntry> = new Map();

  private key(namespace: Namespace, key: string) {
    return `${namespace}:${key}`;
  }

  set(namespace: Namespace, key: string, value: any, ttlMs?: number) {
    const now = Date.now();
    const expires_at = ttlMs ? now + ttlMs : undefined;
    this.store.set(this.key(namespace, key), {
      value,
      expires_at,
      updated_at: now
    });
  }

  get(namespace: Namespace, key: string): any {
    this.cleanup();
    const entry = this.store.get(this.key(namespace, key));
    return entry ? entry.value : undefined;
  }

  delete(namespace: Namespace, key: string) {
    this.store.delete(this.key(namespace, key));
  }

  // Last-write-wins conflict resolution (timestamp-based)
  setIfNewer(namespace: Namespace, key: string, value: any, updated_at: number, ttlMs?: number) {
    const k = this.key(namespace, key);
    const existing = this.store.get(k);
    if (!existing || existing.updated_at < updated_at) {
      this.set(namespace, key, value, ttlMs);
    }
  }

  cleanup() {
    const now = Date.now();
    for (const [key, entry] of this.store.entries()) {
      if (entry.expires_at !== undefined && entry.expires_at < now) {
        this.store.delete(key);
      }
    }
  }
}

export const contextStore = new ContextStore();
