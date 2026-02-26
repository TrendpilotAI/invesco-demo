// AI Mesh — Agent Capability Registry

export type AgentStatus = 'online' | 'offline' | 'busy';

export interface AgentRecord {
  name: string;
  capabilities: string[];
  endpoint: string;
  status: AgentStatus;
  registeredAt: number;
  lastHeartbeat: number;
}

export class AgentRegistry {
  private agents: Map<string, AgentRecord> = new Map();
  private heartbeatTimeout: number;

  constructor(heartbeatTimeoutMs: number = 30_000) {
    this.heartbeatTimeout = heartbeatTimeoutMs;
  }

  register(name: string, capabilities: string[], endpoint: string): AgentRecord {
    const record: AgentRecord = {
      name,
      capabilities,
      endpoint,
      status: 'online',
      registeredAt: Date.now(),
      lastHeartbeat: Date.now(),
    };
    this.agents.set(name, record);
    return record;
  }

  deregister(name: string): boolean {
    return this.agents.delete(name);
  }

  heartbeat(name: string): boolean {
    const agent = this.agents.get(name);
    if (!agent) return false;
    agent.lastHeartbeat = Date.now();
    agent.status = 'online';
    return true;
  }

  queryByCapability(capability: string): AgentRecord[] {
    this.pruneTimedOut();
    const results: AgentRecord[] = [];
    for (const agent of this.agents.values()) {
      if (agent.capabilities.includes(capability) && agent.status === 'online') {
        results.push(agent);
      }
    }
    return results;
  }

  get(name: string): AgentRecord | undefined {
    return this.agents.get(name);
  }

  all(): AgentRecord[] {
    return [...this.agents.values()];
  }

  pruneTimedOut(): string[] {
    const now = Date.now();
    const pruned: string[] = [];
    for (const [name, agent] of this.agents) {
      if (now - agent.lastHeartbeat > this.heartbeatTimeout) {
        agent.status = 'offline';
        pruned.push(name);
      }
    }
    return pruned;
  }
}
