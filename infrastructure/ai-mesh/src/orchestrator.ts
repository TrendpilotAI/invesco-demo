// AI Mesh — Task Orchestrator

import { AgentRegistry } from './registry';
import { MessageQueue, MessageType, createMessage } from './protocol';

export type TaskState = 'pending' | 'assigned' | 'in_progress' | 'completed' | 'failed';

export interface Task {
  id: string;
  capability: string;
  payload: unknown;
  priority: number; // higher = more urgent
  state: TaskState;
  assignedTo: string | null;
  attempts: number;
  maxRetries: number;
  createdAt: number;
  updatedAt: number;
  result?: unknown;
  error?: string;
}

let taskCounter = 0;

export class Orchestrator {
  private tasks: Map<string, Task> = new Map();
  private queue: Task[] = []; // sorted by priority desc

  constructor(
    private registry: AgentRegistry,
    private messageQueue: MessageQueue,
    private maxRetries: number = 3
  ) {}

  submit(capability: string, payload: unknown, priority: number = 0): Task {
    const task: Task = {
      id: `task_${++taskCounter}_${Date.now()}`,
      capability,
      payload,
      priority,
      state: 'pending',
      assignedTo: null,
      attempts: 0,
      maxRetries: this.maxRetries,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    this.tasks.set(task.id, task);
    this.enqueue(task);
    return task;
  }

  private enqueue(task: Task): void {
    this.queue.push(task);
    this.queue.sort((a, b) => b.priority - a.priority);
  }

  /** Try to assign pending tasks to available agents */
  processPending(): Task[] {
    const assigned: Task[] = [];
    const remaining: Task[] = [];

    for (const task of this.queue) {
      if (task.state !== 'pending') continue;
      const agents = this.registry.queryByCapability(task.capability);
      const available = agents.find((a) => a.status === 'online');

      if (available) {
        task.state = 'assigned';
        task.assignedTo = available.name;
        task.attempts++;
        task.updatedAt = Date.now();

        const msg = createMessage(
          MessageType.TASK_REQUEST,
          '__orchestrator__',
          available.name,
          { taskId: task.id, ...((task.payload as object) ?? {}) },
          task.id
        );
        this.messageQueue.send(msg);
        assigned.push(task);
      } else {
        remaining.push(task);
      }
    }

    this.queue = remaining;
    return assigned;
  }

  /** Mark task in progress */
  markInProgress(taskId: string): boolean {
    const task = this.tasks.get(taskId);
    if (!task || task.state !== 'assigned') return false;
    task.state = 'in_progress';
    task.updatedAt = Date.now();
    return true;
  }

  /** Complete a task */
  complete(taskId: string, result: unknown): boolean {
    const task = this.tasks.get(taskId);
    if (!task) return false;
    task.state = 'completed';
    task.result = result;
    task.updatedAt = Date.now();
    return true;
  }

  /** Fail a task; retries with backoff if under max */
  fail(taskId: string, error: string): boolean {
    const task = this.tasks.get(taskId);
    if (!task) return false;

    if (task.attempts < task.maxRetries) {
      task.state = 'pending';
      task.assignedTo = null;
      task.error = error;
      task.updatedAt = Date.now();
      this.enqueue(task);
      return true;
    }

    task.state = 'failed';
    task.error = error;
    task.updatedAt = Date.now();
    return true;
  }

  /** Backoff delay in ms for a task's current attempt */
  backoffMs(taskId: string): number {
    const task = this.tasks.get(taskId);
    if (!task) return 0;
    return Math.min(1000 * Math.pow(2, task.attempts - 1), 30_000);
  }

  getTask(taskId: string): Task | undefined {
    return this.tasks.get(taskId);
  }

  allTasks(): Task[] {
    return [...this.tasks.values()];
  }
}
