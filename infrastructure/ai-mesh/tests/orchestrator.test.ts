import { Orchestrator } from '../src/orchestrator';
import { AgentRegistry } from '../src/registry';
import { MessageQueue } from '../src/protocol';

describe('Orchestrator', () => {
  let registry: AgentRegistry;
  let mq: MessageQueue;
  let orch: Orchestrator;

  beforeEach(() => {
    registry = new AgentRegistry(60_000);
    mq = new MessageQueue();
    orch = new Orchestrator(registry, mq, 2);
  });

  test('submit creates pending task', () => {
    const task = orch.submit('summarize', { text: 'hi' });
    expect(task.state).toBe('pending');
    expect(task.capability).toBe('summarize');
  });

  test('processPending assigns to available agent', () => {
    registry.register('bot1', ['summarize'], 'http://bot1');
    const task = orch.submit('summarize', {});
    const assigned = orch.processPending();
    expect(assigned.length).toBe(1);
    expect(orch.getTask(task.id)!.state).toBe('assigned');
    expect(orch.getTask(task.id)!.assignedTo).toBe('bot1');
    expect(mq.pending('bot1')).toBe(1);
  });

  test('processPending skips if no capable agent', () => {
    orch.submit('translate', {});
    const assigned = orch.processPending();
    expect(assigned.length).toBe(0);
  });

  test('priority ordering', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    const low = orch.submit('x', {}, 1);
    const high = orch.submit('x', {}, 10);
    const assigned = orch.processPending();
    expect(assigned.length).toBe(2);
    // High priority should be first
    expect(assigned[0].id).toBe(high.id);
    expect(assigned[1].id).toBe(low.id);
  });

  test('complete sets result', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    const task = orch.submit('x', {});
    orch.processPending();
    orch.markInProgress(task.id);
    expect(orch.getTask(task.id)!.state).toBe('in_progress');
    orch.complete(task.id, { answer: 42 });
    expect(orch.getTask(task.id)!.state).toBe('completed');
    expect(orch.getTask(task.id)!.result).toEqual({ answer: 42 });
  });

  test('fail retries then permanently fails', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    const task = orch.submit('x', {});
    // Attempt 1
    orch.processPending();
    orch.fail(task.id, 'err1');
    expect(orch.getTask(task.id)!.state).toBe('pending');
    // Attempt 2 (max=2)
    orch.processPending();
    orch.fail(task.id, 'err2');
    expect(orch.getTask(task.id)!.state).toBe('failed');
  });

  test('backoff increases exponentially', () => {
    registry.register('bot1', ['x'], 'http://bot1');
    const task = orch.submit('x', {});
    orch.processPending();
    expect(orch.backoffMs(task.id)).toBe(1000); // 2^0 * 1000
    orch.fail(task.id, 'e');
    orch.processPending();
    expect(orch.backoffMs(task.id)).toBe(2000); // 2^1 * 1000
  });
});
