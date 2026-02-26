import { ContextStore } from '../src/context-store';

describe('ContextStore', () => {
  let store: ContextStore;

  beforeEach(() => { store = new ContextStore(); });

  test('set and get within namespace', () => {
    store.set('agent1', 'key1', 'value1');
    expect(store.get('agent1', 'key1')).toBe('value1');
  });

  test('namespaces are isolated', () => {
    store.set('agent1', 'key', 'a');
    store.set('agent2', 'key', 'b');
    expect(store.get('agent1', 'key')).toBe('a');
    expect(store.get('agent2', 'key')).toBe('b');
  });

  test('TTL expiration', async () => {
    store.set('ns', 'temp', 'data', 50);
    expect(store.get('ns', 'temp')).toBe('data');
    await new Promise(r => setTimeout(r, 80));
    expect(store.get('ns', 'temp')).toBeUndefined();
  });

  test('global namespace helpers', () => {
    store.setGlobal('shared', 42);
    expect(store.getGlobal('shared')).toBe(42);
  });

  test('keys lists non-expired keys', () => {
    store.set('ns', 'a', 1);
    store.set('ns', 'b', 2);
    store.set('other', 'c', 3);
    expect(store.keys('ns').sort()).toEqual(['a', 'b']);
  });

  test('delete removes entry', () => {
    store.set('ns', 'k', 'v');
    expect(store.delete('ns', 'k')).toBe(true);
    expect(store.get('ns', 'k')).toBeUndefined();
  });

  test('last-write-wins', () => {
    store.set('ns', 'k', 'first');
    store.set('ns', 'k', 'second');
    expect(store.get('ns', 'k')).toBe('second');
  });
});
