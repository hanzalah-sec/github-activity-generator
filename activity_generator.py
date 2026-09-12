#!/usr/bin/env python3
"""
=============================================================================
🚀 GitHub Activity Generator
=============================================================================
An open-source, production-grade activity automation engine designed to maintain
a consistent, healthy GitHub commit history (24 commits daily / hourly schedule)
completely in the cloud with zero disturbance to account health or other repositories.

Author: Tauqeer Mustafa
License: MIT
=============================================================================
"""

import argparse
import datetime
import json
import os
import random
import subprocess
import sys
import time

# Ensure safe UTF-8 output across all operating systems and Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

__version__ = "2.0.0"

# Comprehensive collection of curated engineering quotes & wisdom
CURATED_QUOTES = [
    # Clean Code & Craftsmanship
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "Fix the cause, not the symptom. - Steve Maguire",
    "Simplicity is prerequisite for reliability. - Edsger W. Dijkstra",
    "Make it work, make it right, make it fast. - Kent Beck",
    "Clean code always looks like it was written by someone who cares. - Robert C. Martin",
    "Refactor early, refactor often. - Martin Fowler",
    "The best error message is the one that never shows up. - Thomas Fuchs",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
    "Deleted code is debugged code. - Jeff Sickel",
    "Simplicity is the soul of efficiency. - Austin Freeman",
    "Quality is not an act, it is a habit. - Aristotle",
    "Before software can be reusable it first has to be usable. - Ralph Johnson",
    "Good code is its own best documentation. - Steve McConnell",
    "Don't comment bad code - rewrite it. - Brian W. Kernighan",
    
    # Systems & Architecture
    "Talk is cheap. Show me the code. - Linus Torvalds",
    "The only way to go fast is to go well. - Robert C. Martin",
    "Premature optimization is the root of all evil. - Donald Knuth",
    "There are only two hard things in Computer Science: cache invalidation and naming things. - Phil Karlton",
    "Complexity is the enemy of execution. - Tony Robbins",
    "Architecture is about the important stuff. Whatever that is. - Ralph Johnson",
    "Software is a great combination between artistry & engineering. - Bill Gates",
    "The function of good software is to make the complex appear to be simple. - Grady Booch",
    
    # Continuous Growth & Philosophy
    "Continuous improvement is better than delayed perfection. - Mark Twain",
    "Small daily improvements over time lead to stunning results. - Robin Sharma",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Knowledge is power. - Francis Bacon",
    "Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
    "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
    "Mastery is not an accident, it is a process. - Robert Greene",
    "Focus on being productive instead of busy. - Tim Ferriss"
]

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_LOG_PATH = os.path.join(os.path.dirname(__file__), "activity_log.txt")


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    """Loads configuration from JSON file or returns robust defaults."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"⚠️ [Warning] Failed to load {config_path}: {e}. Falling back to default settings.")
    
    return {
        "log_file": "activity_log.txt",
        "commit_prefix": "chore(activity):",
        "quotes": CURATED_QUOTES,
        "hourly_interval_seconds": 3600
    }


def save_config(config: dict, config_path: str = DEFAULT_CONFIG_PATH) -> None:
    """Saves updated configuration to file."""
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"⚠️ [Warning] Failed to save config: {e}")


def read_log_stats(log_path: str) -> dict:
    """Parses activity_log.txt to compute activity statistics."""
    if not os.path.exists(log_path):
        return {
            "total_entries": 0,
            "first_entry": "None",
            "last_entry": "None",
            "unique_days": 0
        }
    
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        
        total = len(lines)
        first = lines[0].split("]")[0].replace("[", "") if total > 0 else "N/A"
        last = lines[-1].split("]")[0].replace("[", "") if total > 0 else "N/A"
        
        # Calculate unique dates
        days = set()
        for line in lines:
            if line.startswith("[") and len(line) >= 11:
                date_part = line[1:11]
                days.add(date_part)
                
        return {
            "total_entries": total,
            "first_entry": first,
            "last_entry": last,
            "unique_days": len(days)
        }
    except Exception as e:
        return {"total_entries": 0, "error": str(e)}


def update_log_file(log_path: str, quotes: list) -> tuple[str, str]:
    """Appends a new activity record with UTC timestamp and quote."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    selected_quote = random.choice(quotes) if quotes else "Daily automated commit update."
    
    entry = f"[{timestamp_str}] Activity Record | {selected_quote}\n"
    
    abs_log_path = os.path.abspath(log_path)
    os.makedirs(os.path.dirname(abs_log_path), exist_ok=True)
    
    with open(abs_log_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return timestamp_str, selected_quote


def write_github_step_summary(timestamp: str, quote: str, stats: dict) -> None:
    """Publishes a rich GitHub Actions Step Summary markdown card if in CI."""
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
        
    markdown = f"""
## 🚀 GitHub Activity Automation Summary

| Metric | Details |
| :--- | :--- |
| 🕒 **Execution Time** | `{timestamp}` |
| 📊 **Total Activity Records** | `{stats.get('total_entries', 1)}` commits |
| 📅 **Active Days Logged** | `{stats.get('unique_days', 1)}` days |
| ⚡ **Frequency** | Hourly (`24 commits/day`) |

### 💬 Wisdom of the Hour
> *"{quote}"*

---
*Generated automatically by [GitHub Activity Generator](https://github.com/TauqeerMustafa/github-activity-generator).*
"""
    try:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(markdown)
    except Exception as e:
        print(f"⚠️ [Warning] Could not write GitHub step summary: {e}")


def execute_git_commit(log_path: str, commit_message: str, auto_push: bool = False) -> bool:
    """Stages the log file and creates a clean git commit."""
    try:
        subprocess.run(["git", "add", log_path], check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        print(f"✅ [Committed] {commit_message}")
        
        if auto_push:
            subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
            print("🚀 [Pushed] Successfully pushed changes to remote repository.")
        return True
    except subprocess.CalledProcessError as err:
        stderr_msg = err.stderr.strip() if err.stderr else str(err)
        if "nothing to commit" in stderr_msg.lower():
            print("ℹ️ [Info] Working tree clean. Nothing to commit.")
            return True
        print(f"❌ [Git Error] {stderr_msg}")
        return False
    except FileNotFoundError:
        print("⚠️ [Notice] Git binary not found in system PATH. Log was updated locally without git commit.")
        return False


def run_single_iteration(config: dict, git_commit: bool = False, auto_push: bool = False, dry_run: bool = False) -> None:
    """Executes a single log generation cycle."""
    log_file = config.get("log_file", "activity_log.txt")
    quotes = config.get("quotes", CURATED_QUOTES)
    prefix = config.get("commit_prefix", "chore(activity):")
    
    if dry_run:
        now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        sample_quote = random.choice(quotes)
        print("🧪 [DRY RUN] Would append entry:")
        print(f"   [{now_utc}] Activity Record | {sample_quote}")
        print(f"   Commit Message: {prefix} record activity at {now_utc}")
        return
        
    timestamp, quote = update_log_file(log_file, quotes)
    stats = read_log_stats(log_file)
    
    print(f"✨ [{timestamp}] Activity record appended.")
    print(f"💬 Quote: \"{quote}\"")
    print(f"📈 Total records in log: {stats.get('total_entries')}")
    
    write_github_step_summary(timestamp, quote, stats)
    
    if git_commit:
        commit_msg = f"{prefix} record activity at {timestamp}"
        execute_git_commit(log_file, commit_msg, auto_push=auto_push)


def print_stats(config: dict) -> None:
    """Displays formatted terminal statistics."""
    log_file = config.get("log_file", "activity_log.txt")
    stats = read_log_stats(log_file)
    quotes = config.get("quotes", CURATED_QUOTES)
    
    print("=" * 60)
    print("📊 GITHUB ACTIVITY GENERATOR - STATS DASHBOARD")
    print("=" * 60)
    print(f"📁 Log File Path      : {os.path.abspath(log_file)}")
    print(f"🔢 Total Records      : {stats.get('total_entries', 0):,}")
    print(f"📅 Active Days Logged : {stats.get('unique_days', 0):,} days")
    print(f"🕒 First Activity     : {stats.get('first_entry', 'N/A')}")
    print(f"🕒 Latest Activity    : {stats.get('last_entry', 'N/A')}")
    print(f"💡 Quote Pool Size    : {len(quotes)} quotes")
    print(f"⚡ Daily Target Rate  : 24 commits / day (Hourly)")
    print("=" * 60)


def run_daemon_mode(config: dict, interval_seconds: int = 3600, git_commit: bool = False, auto_push: bool = False) -> None:
    """Runs a local hourly background daemon for 24 commits/day continuous generation."""
    print("=" * 65)
    print("⚡ GitHub Activity Generator - Local Daemon Mode Started")
    print(f"⏰ Interval: {interval_seconds}s ({interval_seconds / 3600:.2f} hours)")
    print(f"🔄 Git Auto-Commit: {git_commit} | Auto-Push: {auto_push}")
    print("🛑 Press Ctrl+C anytime to cleanly exit.")
    print("=" * 65)
    
    cycle = 1
    try:
        while True:
            print(f"\n--- [Cycle #{cycle}] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            run_single_iteration(config, git_commit=git_commit, auto_push=auto_push)
            cycle += 1
            print(f"⏳ Sleeping for {interval_seconds} seconds until next hourly cycle...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n🛑 [Stopped] Daemon mode stopped cleanly by user.")


def main():
    parser = argparse.ArgumentParser(
        description="🚀 GitHub Activity Generator - 24 Commits/Day Automation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python activity_generator.py --count 1
  python activity_generator.py --commit --push
  python activity_generator.py --stats
  python activity_generator.py --daemon --interval 3600 --commit --push
        """
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH, help="Custom configuration JSON path")
    parser.add_argument("--count", type=int, default=1, help="Number of records to generate in this run (default: 1)")
    parser.add_argument("--commit", action="store_true", help="Automatically git commit generated records")
    parser.add_argument("--push", action="store_true", help="Automatically git push after committing")
    parser.add_argument("--daemon", action="store_true", help="Run in continuous background loop mode")
    parser.add_argument("--interval", type=int, default=3600, help="Interval in seconds for daemon mode (default: 3600s)")
    parser.add_argument("--stats", action="store_true", help="Show activity summary and statistics")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying files or git")
    
    args = parser.parse_args()
    config = load_config(args.config)
    
    if args.stats:
        print_stats(config)
        return
        
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
                print(f"\n[Run {i + 1}/{args.count}]")
            run_single_iteration(config, git_commit=args.commit, auto_push=args.push, dry_run=args.dry_run)
            if i < args.count - 1:
                time.sleep(1)


if __name__ == "__main__":
    main()
