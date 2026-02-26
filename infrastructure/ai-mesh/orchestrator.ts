// orchestrator.ts - Task delegation orchestrator
import {registry, AgentInfo} from './registry.js'
import {messageQueue, AgentMessage} from './protocol.js'

type TaskState = 'pending' | 'assigned' | 'in_progress' | 'completed' | 'failed';

interface Task {
  id: string;
  type: string;
  payload: any;
  state: TaskState;
  assignedTo?: string;
  priority: number;
  retries: number;
  lastAttempt: number;
  correlation_id: string;
}

const MAX_RETRIES = 3;
const BASE_BACKOFF = 2000;

class PriorityTaskQueue {
  private queue: Task[] = [];

  enqueue(task: Task) {
    this.queue.push(task);
    this.queue.sort((a, b) => b.priority - a.priority || a.lastAttempt - b.lastAttempt);
  }
  dequeue(): Task|undefined {
    return this.queue.shift();
  }
  all() {
    return this.queue;
  }
  remove(id: string) {
    this.queue = this.queue.filter(t => t.id !== id);
  }
}

class Orchestrator {
  private tasks: Map<string, Task> = new Map();
  private taskQueue = new PriorityTaskQueue();

  submitTask(type: string, payload: any, priority=1): string {
    const id = `task-${Date.now()}-${Math.random().toString(36).slice(2,8)}`;
    const correlation_id = id;
    const task: Task = {id, type, payload, state: 'pending', priority, retries: 0, lastAttempt: 0, correlation_id};
    this.tasks.set(id, task);
    this.taskQueue.enqueue(task);
    this.tryAssignTasks();
    return id;
  }

  tryAssignTasks() {
    for (const task of this.taskQueue.all()) {
      if (task.state !== 'pending' && task.state !== 'failed') continue;
      const agent = this.findBestAgent(task.type);
      if (!agent) continue;
      task.assignedTo = agent.name;
      task.state = 'assigned';
      task.lastAttempt = Date.now();
      // Send request
      const message: AgentMessage = {
        type: 'task_request',
        sender: 'orchestrator',
        receiver: agent.name,
        timestamp: Date.now(),
        payload: task.payload,
        correlation_id: task.correlation_id
      };
      messageQueue.send(message);
    }
  }

  handleResponse(msg: AgentMessage) {
    const task = [...this.tasks.values()].find(t => t.correlation_id === msg.correlation_id);
    if (!task) return;
    if (msg.type === 'task_response') {
      task.state = (msg.payload && msg.payload.success) ? 'completed' : 'failed';
      if (task.state === 'failed') {
        this.retryTask(task);
      } else {
        this.taskQueue.remove(task.id);
      }
    }
  }

  private retryTask(task: Task) {
    if (task.retries >= MAX_RETRIES) {
      this.taskQueue.remove(task.id);
      return;
    }
    task.retries++;
    task.state = 'pending';
    setTimeout(() => {
      this.taskQueue.enqueue(task);
      this.tryAssignTasks();
    }, BASE_BACKOFF * Math.pow(2, task.retries - 1));
  }

  findBestAgent(capability: string): AgentInfo|undefined {
    const agents = registry.queryByCapability(capability);
    // Choose least busy/by load, or random if all are equal
    return agents[0];
  }

  getTask(id: string): Task|undefined {
    return this.tasks.get(id);
  }

  getAllTasks(): Task[] {
    return Array.from(this.tasks.values());
  }
}

export const orchestrator = new Orchestrator();
