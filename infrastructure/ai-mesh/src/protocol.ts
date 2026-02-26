// AI Mesh — Agent-to-Agent Messaging Protocol

export enum MessageType {
  TASK_REQUEST = 'task_request',
  TASK_RESPONSE = 'task_response',
  STATUS_UPDATE = 'status_update',
  CAPABILITY_QUERY = 'capability_query',
}

export interface Message {
  id: string;
  type: MessageType;
  sender: string;
  receiver: string;
  timestamp: number;
  payload: unknown;
  correlationId: string;
  acknowledged: boolean;
}

let idCounter = 0;

export function createMessage(
  type: MessageType,
  sender: string,
  receiver: string,
  payload: unknown,
  correlationId?: string
): Message {
  return {
    id: `msg_${++idCounter}_${Date.now()}`,
    type,
    sender,
    receiver,
    timestamp: Date.now(),
    payload,
    correlationId: correlationId ?? `corr_${idCounter}_${Date.now()}`,
    acknowledged: false,
  };
}

export class MessageQueue {
  private queues: Map<string, Message[]> = new Map();

  send(message: Message): void {
    const q = this.queues.get(message.receiver) ?? [];
    q.push(message);
    this.queues.set(message.receiver, q);
  }

  receive(agentId: string): Message | undefined {
    const q = this.queues.get(agentId);
    if (!q || q.length === 0) return undefined;
    return q[0];
  }

  acknowledge(agentId: string, messageId: string): boolean {
    const q = this.queues.get(agentId);
    if (!q) return false;
    const idx = q.findIndex((m) => m.id === messageId);
    if (idx === -1) return false;
    q[idx].acknowledged = true;
    q.splice(idx, 1);
    return true;
  }

  pending(agentId: string): number {
    return this.queues.get(agentId)?.length ?? 0;
  }

  drain(agentId: string): Message[] {
    const q = this.queues.get(agentId) ?? [];
    this.queues.set(agentId, []);
    return q;
  }
}
