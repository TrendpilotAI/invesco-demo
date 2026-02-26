// protocol.ts - Agent-to-agent messaging protocol

export type MessageType = 'task_request' | 'task_response' | 'status_update' | 'capability_query';

export interface AgentMessage {
  type: MessageType;
  sender: string;
  receiver: string;
  timestamp: number;
  payload: any;
  correlation_id: string;
}

interface QueueMessage {
  message: AgentMessage;
  acknowledged: boolean;
}

class MessageQueue {
  private queues: Map<string, QueueMessage[]> = new Map();

  send(message: AgentMessage) {
    if (!this.queues.has(message.receiver)) {
      this.queues.set(message.receiver, []);
    }
    this.queues.get(message.receiver)!.push({ message, acknowledged: false });
  }

  receive(agent: string): AgentMessage | undefined {
    const queue = this.queues.get(agent);
    if (!queue) return undefined;
    const msg = queue.find(q => !q.acknowledged);
    if (msg) msg.acknowledged = true;
    return msg?.message;
  }

  acknowledge(agent: string, correlation_id: string) {
    const queue = this.queues.get(agent);
    if (!queue) return;
    const msg = queue.find(q => q.message.correlation_id === correlation_id);
    if (msg) msg.acknowledged = true;
  }

  getQueue(agent: string): AgentMessage[] {
    return (this.queues.get(agent) || []).map(q => q.message);
  }
}

export const messageQueue = new MessageQueue();
