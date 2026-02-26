// registry.ts - Agent capability registry

export interface AgentInfo {
  name: string;
  capabilities: string[];
  endpoint: string;
  status: 'online' | 'offline' | 'busy';
  last_seen: number;
}

const AGENT_TIMEOUT = 60_000; // ms

class Registry {
  private agents: Map<string, AgentInfo> = new Map();

  register(agent: AgentInfo) {
    this.agents.set(agent.name, { ...agent, last_seen: Date.now() });
  }

  updateHeartbeat(agentName: string) {
    const agent = this.agents.get(agentName);
    if (agent) agent.last_seen = Date.now();
  }

  queryByCapability(capability: string): AgentInfo[] {
    return Array.from(this.agents.values()).filter(
      a => a.capabilities.includes(capability) && a.status === 'online'
    );
  }

  get(name: string): AgentInfo | undefined {
    return this.agents.get(name);
  }

  all(): AgentInfo[] {
    return Array.from(this.agents.values());
  }

  cleanup() {
    // Deregister agents with expired heartbeat
    const now = Date.now();
    for (const [name, agent] of this.agents) {
      if (agent.status !== 'offline' && now - agent.last_seen > AGENT_TIMEOUT) {
        this.agents.delete(name);
      }
    }
  }
}

export const registry = new Registry();
