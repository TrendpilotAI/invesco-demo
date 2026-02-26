import { AgentRegistry } from '../src/registry';

describe('AgentRegistry', () => {
  let registry: AgentRegistry;

  beforeEach(() => { registry = new AgentRegistry(100); }); // 100ms timeout for tests

  test('register and get agent', () => {
    registry.register('bot1', ['summarize', 'translate'], 'http://bot1');
    const agent = registry.get('bot1');
    expect(agent?.name).toBe('bot1');
    expect(agent?.capabilities).toContain('summarize');
    expect(agent?.status).toBe('online');
  });

  test('query by capability', () => {
    registry.register('bot1', ['summarize'], 'http://bot1');
    registry.register('bot2', ['translate'], 'http://bot2');
    registry.register('bot3', ['summarize', 'translate'], 'http://bot3');
    const results = registry.queryByCapability('summarize');
    expect(results.map(r => r.name).sort()).toEqual(['bot1', 'bot3']);
  });

  test('deregister removes agent', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    expect(registry.deregister('bot1')).toBe(true);
    expect(registry.get('bot1')).toBeUndefined();
  });

  test('heartbeat updates timestamp', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    const before = registry.get('bot1')!.lastHeartbeat;
    // small delay
    const start = Date.now(); while (Date.now() - start < 5) {}
    registry.heartbeat('bot1');
    expect(registry.get('bot1')!.lastHeartbeat).toBeGreaterThan(before);
  });

  test('timed-out agents go offline and are excluded from queries', async () => {
    registry.register('bot1', ['x'], 'http://bot1');
    await new Promise(r => setTimeout(r, 150));
    const results = registry.queryByCapability('x');
    expect(results.length).toBe(0);
    expect(registry.get('bot1')!.status).toBe('offline');
  });
});
