import { messageQueue, AgentMessage } from '../protocol.js';

describe('MessageQueue', () => {
  const agentA = 'agentA', agentB = 'agentB';
  const msg: AgentMessage = {
    type: 'task_request',
    sender: agentA,
    receiver: agentB,
    timestamp: Date.now(),
    payload: { job: 'test' },
    correlation_id: 'abc123'
  };

  it('should send and receive messages', () => {
    messageQueue.send(msg);
    const received = messageQueue.receive(agentB);
    expect(received).toEqual(msg);
  });

  it('should acknowledge messages', () => {
    const msg2 = { ...msg, correlation_id: 'def456'};
    messageQueue.send(msg2);
    messageQueue.acknowledge(agentB, 'def456');
    const queue = messageQueue.getQueue(agentB);
    expect(queue.find(m => m.correlation_id === 'def456')).toBeDefined();
  });
});
