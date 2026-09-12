#!/usr/bin/env python3
"""
GitHub Activity Generator
An open-source, automated activity generator designed to maintain consistent commits
safely without disturbing repository health or account settings.
"""

import argparse
import datetime
import json
import os
import random
import subprocess
import sys
import time

# Fallback quotes if config.json is not found
DEFAULT_QUOTES = [
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "Fix the cause, not the symptom. - Steve Maguire",
    "Optimism is an occupational hazard of programming: feedback is the treatment. - Kent Beck",
    "Simplicity is prerequisite for reliability. - Edsger W. Dijkstra",
    "Make it work, make it right, make it fast. - Kent Beck",
    "Clean code always looks like it was written by someone who cares. - Robert C. Martin",
    "Refactor early, refactor often. - Anonymous",
    "The best error message is the one that never shows up. - Thomas Fuchs",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
    "Java is to JavaScript what car is to Carpet. - Chris Heilmann",
    "Knowledge is power. - Francis Bacon",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Talk is cheap. Show me the code. - Linus Torvalds",
    "Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
    "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
    "Before software can be reusable it first has to be usable. - Ralph Johnson",
    "Deleted code is debugged code. - Jeff Sickel",
    "Simplicity is the soul of efficiency. - Austin Freeman",
    "Quality is not an act, it is a habit. - Aristotle",
    "The most important property of a program is whether it accomplishes the intention of its user. - C.A.R. Hoare",
    "Continuous improvement is better than delayed perfection. - Mark Twain",
    "Small daily improvements over time lead to stunning results. - Robin Sharma"
]

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_LOG_PATH = os.path.join(os.path.dirname(__file__), "activity_log.txt")


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    """Loads configuration from JSON file or returns defaults."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Failed to load config file: {e}. Using defaults.")
    
    return {
        "log_file": "activity_log.txt",
        "commit_prefix": "chore(activity):",
        "quotes": DEFAULT_QUOTES,
        "hourly_interval_seconds": 3600
    }


def update_log_file(log_path: str, quotes: list) -> tuple[str, str]:
    """Appends an activity entry with UTC timestamp and an inspiring tech quote."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    selected_quote = random.choice(quotes) if quotes else "Daily automated commit update."
    
    entry = f"[{timestamp_str}] Activity Record | {selected_quote}\n"
    
    # Ensure parent dir exists
    abs_log_path = os.path.abspath(log_path)
    os.makedirs(os.path.dirname(abs_log_path), exist_ok=True)
    
    with open(abs_log_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return timestamp_str, selected_quote


def execute_git_commit(log_path: str, commit_message: str, auto_push: bool = False) -> bool:
    """Stages the log file and creates a git commit."""
    try:
        # Stage the log file
        subprocess.run(["git", "add", log_path], check=True, capture_output=True, text=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        print(f"[Success] Committed: {commit_message}")
        
        if auto_push:
            subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
            print("[Success] Pushed to remote repository.")
        return True
    except subprocess.CalledProcessError as err:
        stderr_msg = err.stderr.strip() if err.stderr else str(err)
        if "nothing to commit" in stderr_msg.lower():
            print("[Info] Nothing new to commit.")
            return True
        print(f"[Git Error] Failed executing git operation: {stderr_msg}")
        return False
    except FileNotFoundError:
        print("[Notice] Git executable not found in PATH. Log file was updated without creating a git commit.")
        return False


def run_single_iteration(config: dict, git_commit: bool = False, auto_push: bool = False) -> None:
    """Executes a single log generation cycle."""
    log_file = config.get("log_file", "activity_log.txt")
    quotes = config.get("quotes", DEFAULT_QUOTES)
    prefix = config.get("commit_prefix", "chore(activity):")
    
    timestamp, quote = update_log_file(log_file, quotes)
    print(f"[{timestamp}] Activity updated.")
    print(f"Quote: \"{quote}\"")
    
    if git_commit:
        commit_msg = f"{prefix} record activity at {timestamp}"
        execute_git_commit(log_file, commit_msg, auto_push=auto_push)


def run_daemon_mode(config: dict, interval_seconds: int = 3600, git_commit: bool = False, auto_push: bool = False) -> None:
    """Runs a local hourly loop for 24 commits/day continuous generation."""
    print("=" * 60)
    print("GitHub Activity Generator - Local Daemon Mode Started")
    print(f"Interval: {interval_seconds} seconds ({interval_seconds / 3600:.2f} hours)")
    print(f"Git Commit Enabled: {git_commit} | Auto-Push: {auto_push}")
    print("Press Ctrl+C to stop.")
    print("=" * 60)
    
    cycle = 1
    try:
        while True:
            print(f"\n--- Cycle #{cycle} ---")
            run_single_iteration(config, git_commit=git_commit, auto_push=auto_push)
            cycle += 1
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n[Stopped] Daemon terminated by user.")


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Activity Generator - Automate daily commit history smoothly and safely."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help="Path to custom config.json"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of log entries / commits to generate in this run (default: 1)"
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Perform git commit for each entry"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Automatically git push after committing"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuously in background daemon mode (e.g. 1 commit every hour)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Interval in seconds for daemon mode (default: 3600s / 1 hour)"
    )
    
    args = parser.parse_args()
    config = load_config(args.config)
    
    if args.daemon:
        run_daemon_mode(
            config=config,
            interval_seconds=args.interval,
            git_commit=args.commit,
            auto_push=args.push
        )
    else:
        for i in range(args.count):
            if args.count > 1:
                print(f"Running iteration {i + 1}/{args.count}...")
            run_single_iteration(config, git_commit=args.commit, auto_push=args.push)
            if i < args.count - 1:
                time.sleep(1)


if __name__ == "__main__":
    main()
