#!/usr/bin/env python3
"""CLI entry point for the model benchmark framework."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from benchmark_tasks import TASKS
from benchmark_runner import MODELS, run_single, save_result, format_markdown_table, save_combined_results
from benchmark_judge import judge_outputs, save_judgement


def main():
    parser = argparse.ArgumentParser(description="Model Benchmark Runner")
    parser.add_argument("--all", action="store_true", help="Run all tasks on all models")
    parser.add_argument("--task", type=str, help="Specific task key to run")
    parser.add_argument("--model", type=str, help="Specific model key to run")
    parser.add_argument("--judge", action="store_true", help="Run quality judging after benchmarks")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without calling APIs")
    parser.add_argument("--format", choices=["json", "markdown", "html"], default="markdown", help="Output format")
    parser.add_argument("--results-dir", default="results", help="Directory for results")
    args = parser.parse_args()

    # Determine which tasks and models to run
    if args.all:
        task_keys = list(TASKS.keys())
        model_keys = list(MODELS.keys())
    elif args.task and args.model:
        task_keys = [args.task]
        model_keys = [args.model]
    elif args.task:
        task_keys = [args.task]
        model_keys = list(MODELS.keys())
    elif args.model:
        task_keys = list(TASKS.keys())
        model_keys = [args.model]
    else:
        parser.print_help()
        print("\nSpecify --all, --task, --model, or a combination.")
        sys.exit(1)

    # Validate
    for tk in task_keys:
        if tk not in TASKS:
            print(f"❌ Unknown task: {tk}. Available: {list(TASKS.keys())}")
            sys.exit(1)
    for mk in model_keys:
        if mk not in MODELS:
            print(f"❌ Unknown model: {mk}. Available: {list(MODELS.keys())}")
            sys.exit(1)

    total = len(task_keys) * len(model_keys)
    print(f"{'🏃 DRY RUN' if args.dry_run else '🚀 BENCHMARK RUN'}")
    print(f"Tasks: {task_keys}")
    print(f"Models: {model_keys}")
    print(f"Total runs: {total}")
    print("=" * 60)

    all_results = []
    # Group by task for judging
    task_outputs = {tk: {} for tk in task_keys}

    for task_key in task_keys:
        task = TASKS[task_key]
        print(f"\n📋 Task: {task['name']} ({task_key})")
        print("-" * 40)

        for model_key in model_keys:
            model_display = MODELS[model_key]["display_name"]
            print(f"  🤖 {model_display}...", end=" ", flush=True)

            result = run_single(model_key, task_key, task, dry_run=args.dry_run)
            all_results.append(result)

            # Save individual result
            filepath = save_result(result, args.results_dir)

            if args.dry_run:
                print("(dry run)")
            elif result["status"] == "error":
                print(f"❌ Error: {result.get('error', 'unknown')}")
            else:
                print(
                    f"✅ {result['elapsed_ms']:,.0f}ms | "
                    f"{result['output_tokens']:,} tokens | "
                    f"{result['tokens_per_second']:.1f} t/s | "
                    f"${result['cost_usd']:.4f}"
                )
                task_outputs[task_key][model_key] = result["content"]

    # Combined results file
    combined_path = save_combined_results(all_results, args.results_dir)
    print(f"\n💾 Combined results: {combined_path}")

    # Judging
    if args.judge and not args.dry_run:
        print("\n" + "=" * 60)
        print("⚖️  QUALITY JUDGING (via Claude Opus)")
        print("=" * 60)
        for task_key in task_keys:
            outputs = task_outputs[task_key]
            if len(outputs) < 2:
                print(f"  ⏭️  Skipping {task_key} (need ≥2 outputs)")
                continue
            print(f"  📊 Judging: {task_key}...", end=" ", flush=True)
            evaluation = judge_outputs(task_key, TASKS[task_key]["name"], TASKS[task_key]["prompt"], outputs)
            if evaluation:
                save_judgement(evaluation, args.results_dir)
                print(f"✅ Ranking: {evaluation.get('ranking', 'N/A')}")
                for ev in evaluation.get("evaluations", []):
                    print(f"     {ev['model']}: {ev['overall']}/10 — {ev.get('strengths', '')[:60]}")
            else:
                print("❌ Failed")

    # Output
    print("\n" + "=" * 60)
    if args.format == "markdown":
        print(format_markdown_table(all_results))
    elif args.format == "json":
        slim = [{k: v for k, v in r.items() if k != "content"} for r in all_results]
        print(json.dumps(slim, indent=2))
    elif args.format == "html":
        print(f"HTML dashboard available at: {args.results_dir}/dashboard.html")
        print(f"Results JSON at: {combined_path}")

    # Summary
    if not args.dry_run:
        total_cost = sum(r["cost_usd"] for r in all_results)
        total_time = sum(r["elapsed_ms"] for r in all_results)
        print(f"\n💰 Total cost: ${total_cost:.4f}")
        print(f"⏱️  Total time: {total_time/1000:.1f}s")


if __name__ == "__main__":
    main()
