import { MessageQueue, MessageType, createMessage } from '../src/protocol';

describe('Protocol', () => {
  test('createMessage produces valid message', () => {
    const msg = createMessage(MessageType.TASK_REQUEST, 'a1', 'a2', { foo: 1 });
    expect(msg.sender).toBe('a1');
    expect(msg.receiver).toBe('a2');
    expect(msg.type).toBe(MessageType.TASK_REQUEST);
    expect(msg.payload).toEqual({ foo: 1 });
    expect(msg.correlationId).toBeTruthy();
    expect(msg.acknowledged).toBe(false);
  });

  test('createMessage with explicit correlationId', () => {
    const msg = createMessage(MessageType.TASK_RESPONSE, 'a1', 'a2', {}, 'corr-123');
    expect(msg.correlationId).toBe('corr-123');
  });
});

describe('MessageQueue', () => {
  let queue: MessageQueue;

  beforeEach(() => { queue = new MessageQueue(); });

  test('send and receive', () => {
    const msg = createMessage(MessageType.STATUS_UPDATE, 'a1', 'a2', 'hi');
    queue.send(msg);
    expect(queue.pending('a2')).toBe(1);
    const received = queue.receive('a2');
    expect(received?.id).toBe(msg.id);
  });

  test('receive from empty queue returns undefined', () => {
    expect(queue.receive('nobody')).toBeUndefined();
  });

  test('acknowledge removes message', () => {
    const msg = createMessage(MessageType.CAPABILITY_QUERY, 'a1', 'a2', {});
    queue.send(msg);
    expect(queue.acknowledge('a2', msg.id)).toBe(true);
    expect(queue.pending('a2')).toBe(0);
  });

  test('acknowledge unknown message returns false', () => {
    expect(queue.acknowledge('a2', 'nope')).toBe(false);
  });

  test('drain returns all and empties', () => {
    queue.send(createMessage(MessageType.TASK_REQUEST, 'a1', 'a2', 1));
    queue.send(createMessage(MessageType.TASK_REQUEST, 'a1', 'a2', 2));
    const all = queue.drain('a2');
    expect(all.length).toBe(2);
    expect(queue.pending('a2')).toBe(0);
  });
});
