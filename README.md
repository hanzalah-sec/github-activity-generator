# 🚀 GitHub Activity Generator (24 Commits / Day)

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/Automation-GitHub_Actions-blue.svg)](.github/workflows/activity-cron.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

An automated, open-source activity generator designed to maintain consistent commits (**24 commits daily, scheduled hourly**) safely and quietly in the background without causing any disturbance to your GitHub account or other repositories.

---

## ✨ Features

- 🕒 **24 Commits Daily (Hourly Schedule)**: Runs automatically every hour (`0 * * * *`) via GitHub Actions.
- ☁️ **100% Cloud-Based (Zero Local Resource)**: Runs on GitHub's free runners—no need to keep your personal computer turned on.
- 🛡️ **Zero Account Disturbance**: Operates entirely within its own isolated repository. Does not alter profile settings, notifications, or any other repositories.
- 💡 **Meaningful Logs & Tech Quotes**: Automatically logs timestamps paired with inspiring programming quotes instead of random binary garbage.
- 💻 **Local Daemon Mode Included**: Can also be run locally on Windows, macOS, or Linux using standard Python.
- ⚙️ **Fully Customizable**: Easily adjust commit message prefixes, quote collections, and intervals via `config.json`.

---

## ⚡ Quick Setup (Cloud Automation via GitHub Actions)

You can have this running 24/7 in less than 2 minutes:

### 1. Fork or Create a Repository
1. Click **Fork** on this repository (or create a new private/public repository and push this code to it).

### 2. Enable GitHub Actions Permissions
By default, GitHub Actions needs permission to write commits to your repository:
1. In your repository on GitHub, go to **Settings** > **Actions** > **General**.
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Click **Save**.

### 3. Enable Workflows & Test
1. Go to the **Actions** tab in your repository.
2. Click **"Daily Activity Generator (24 Commits / Day)"** on the left sidebar.
3. Click the **"Run workflow"** button to trigger your first test commit immediately!
4. From now on, GitHub will automatically trigger a commit **every hour (24 times every single day)**.

---

## 🖥️ Local Usage (Optional)

If you prefer running the script on your local machine:

### Requirements
- Python 3.8+ (Uses standard library, **zero external dependencies** required).

### Run Once
```bash
python activity_generator.py --count 1
```

### Run with Automatic Git Commit & Push
```bash
python activity_generator.py --count 1 --commit --push
```

### Run as a Local Background Daemon (Every 1 Hour)
```bash
python activity_generator.py --daemon --interval 3600 --commit --push
```

---

## ⚙️ Configuration

You can customize the commit log behavior in [`config.json`](config.json):

```json
{
  "log_file": "activity_log.txt",
  "commit_prefix": "chore(activity):",
  "hourly_interval_seconds": 3600,
  "quotes": [
    "Simplicity is the soul of efficiency. – Austin Freeman",
    "Continuous improvement is better than delayed perfection. – Mark Twain",
    "Talk is cheap. Show me the code. – Linus Torvalds"
  ]
}
```

---

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── activity-cron.yml    # GitHub Actions workflow (hourly schedule)
├── activity_generator.py        # Core Python generator script
├── config.json                  # Customization & quote configuration
├── activity_log.txt             # Clean activity log record
├── LICENSE                      # MIT Open Source License
└── README.md                    # Documentation
```

---

## ❓ FAQ & Safety

<details>
<summary><b>Does this affect any of my other repositories?</b></summary>
No. All actions and commits are strictly contained within this specific repository. None of your other repositories or organizations are touched.
</details>

<details>
<summary><b>Will this consume GitHub Actions billing minutes?</b></summary>
For <b>Public Repositories</b>, GitHub Actions execution is completely <b>100% free with unlimited minutes</b>. For private repositories, standard free tier limits apply (2,000 minutes/month, where each run takes ~10 seconds).
</details>

<details>
<summary><b>Why hourly / 24 commits a day?</b></summary>
A steady 1-commit-per-hour schedule distributes your activity evenly across all 24 hours of the day, producing a balanced, natural activity graph.
</details>

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - open-source and free for everyone to use and modify.
