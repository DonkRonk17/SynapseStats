# SynapseStats - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Monitor team communication health and agent responsiveness

### Step 1: Installation Check

```bash
# Navigate to SynapseStats
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SynapseStats

# Verify installation
python synapsestats.py --version
# Expected: SynapseStats 1.0.0
```

### Step 2: First Use - Team Health Check

```bash
# Get overall communication summary
python synapsestats.py summary
```

**Expected Output:**
```
============================================================
SYNAPSE COMMUNICATION SUMMARY
============================================================
Total messages: 221
Reply rate: 45.2%
Most active: FORGE (85 messages)

By sender: {'FORGE': 85, 'ATLAS': 67, 'CLIO': 42, 'NEXUS': 27}
By priority: {'NORMAL': 156, 'HIGH': 48, 'CRITICAL': 17}
============================================================
```

### Step 3: Agent Performance Check

```python
# In your Forge session
from synapsestats import SynapseStats

stats = SynapseStats()

# Check each agent's responsiveness
for agent in ['ATLAS', 'CLIO', 'NEXUS', 'BOLT']:
    agent_stats = stats.get_agent_stats(agent)
    print(f"{agent}: Response rate {agent_stats['response_rate']}")
```

### Step 4: Common Forge Commands

```bash
# Quick summary
python synapsestats.py summary

# Check specific agent
python synapsestats.py agent --agent ATLAS

# View weekly timeline
python synapsestats.py timeline --days 7

# Export for analysis
python synapsestats.py export --output weekly_report.json
```

### Step 5: Integrate into Orchestration

```python
# Add to your session startup
def forge_startup():
    from synapsestats import SynapseStats
    
    stats = SynapseStats()
    summary = stats.get_summary()
    
    # Quick health check
    reply_rate = float(summary['reply_rate'].rstrip('%'))
    if reply_rate < 40:
        print("[!] Low reply rate - check team coordination")
    else:
        print(f"[OK] Team health: {reply_rate}% reply rate")
```

### Next Steps for Forge
1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge orchestration section
2. Set up weekly communication reviews
3. Create team health dashboard

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Track communication during tool builds

### Step 1: Installation Check

```python
# Quick verification
from synapsestats import SynapseStats
print("SynapseStats loaded successfully!")
```

### Step 2: First Use - Activity Check

```python
from synapsestats import SynapseStats

stats = SynapseStats()

# Check your own stats
my_stats = stats.get_agent_stats("ATLAS")
print(f"Messages sent: {my_stats['messages_sent']}")
print(f"Messages received: {my_stats['messages_received']}")
print(f"Response rate: {my_stats['response_rate']}")
```

### Step 3: Build Session Tracking

```python
from synapsestats import SynapseStats
from datetime import datetime

# At start of build session
def start_build(tool_name):
    stats = SynapseStats()
    initial_count = stats.get_summary()['total_messages']
    print(f"[Build Start] {tool_name} - Synapse baseline: {initial_count} messages")
    return initial_count

# At end of build session
def end_build(tool_name, initial_count):
    stats = SynapseStats()
    final_count = stats.get_summary()['total_messages']
    messages_during = final_count - initial_count
    print(f"[Build End] {tool_name} - {messages_during} coordination messages")
```

### Step 4: Common Atlas Commands

```bash
# Check your stats
python synapsestats.py agent --agent ATLAS

# See who you communicate with most
python -c "
from synapsestats import SynapseStats
stats = SynapseStats()
matrix = stats.get_communication_matrix()
if 'ATLAS' in matrix:
    print('ATLAS sends to:', matrix['ATLAS'])
"
```

### Step 5: CLI Usage

```bash
# Full summary
python synapsestats.py summary

# Agent comparison
for agent in FORGE ATLAS CLIO NEXUS BOLT; do
    python synapsestats.py agent --agent $agent
done

# Export JSON for analysis
python synapsestats.py export --output build_session_stats.json --format json
```

### Next Steps for Atlas
1. Add communication tracking to Holy Grail automation
2. Compare coordination overhead across tool builds
3. Use data to improve build documentation

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Automated Synapse analytics and scheduled reports

### Step 1: Linux Installation

```bash
# Clone or access SynapseStats
cd ~/AutoProjects/SynapseStats  # Or your path

# Verify Python
python3 --version

# Test run
python3 synapsestats.py --version
```

### Step 2: First Use - CLI Summary

```bash
# Get summary
python3 synapsestats.py summary

# Check your own stats
python3 synapsestats.py agent --agent CLIO

# View timeline
python3 synapsestats.py timeline --days 7
```

### Step 3: Shell Integration

```bash
# Add to your .bashrc or .zshrc
alias synstats='python3 ~/AutoProjects/SynapseStats/synapsestats.py'

# Now use:
synstats summary
synstats agent --agent CLIO
synstats timeline --days 14
```

### Step 4: Automated Reports Script

```bash
#!/bin/bash
# synapse_daily_report.sh

REPORT_DIR="/var/log/synapse_reports"
DATE=$(date +%Y%m%d)

mkdir -p $REPORT_DIR

# Generate daily report
python3 ~/AutoProjects/SynapseStats/synapsestats.py export \
    --output "$REPORT_DIR/synapse_$DATE.json" \
    --format json

# Generate summary to syslog
python3 ~/AutoProjects/SynapseStats/synapsestats.py summary | \
    logger -t synapse-analytics

echo "Daily report generated: $REPORT_DIR/synapse_$DATE.json"
```

### Step 5: Cron Setup

```bash
# Edit crontab
crontab -e

# Add daily report at 11:59 PM
59 23 * * * /home/clio/scripts/synapse_daily_report.sh

# Add hourly summary to logs
0 * * * * python3 /home/clio/AutoProjects/SynapseStats/synapsestats.py summary | logger -t synapse-stats
```

### Linux-Specific Tips

```bash
# Watch for changes (combine with watch)
watch -n 60 "python3 synapsestats.py summary"

# Pipeline with other tools
python3 synapsestats.py export --output - --format json | jq '.summary.reply_rate'

# Quick one-liner check
python3 -c "from synapsestats import SynapseStats; s=SynapseStats(); print(s.get_summary()['reply_rate'])"
```

### Next Steps for Clio
1. Set up cron jobs for automated reporting
2. Integrate with system monitoring
3. Create ABIOS startup check for Synapse health

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Cross-platform Synapse analytics

### Step 1: Platform Verification

```python
import platform
print(f"Platform: {platform.system()}")
print(f"Python: {platform.python_version()}")

# SynapseStats works identically on all platforms
from synapsestats import SynapseStats
stats = SynapseStats()
print(f"Messages loaded: {len(stats.messages)}")
```

### Step 2: First Use - Cross-Platform

```python
from synapsestats import SynapseStats
from pathlib import Path

# Path handling is automatic via pathlib
stats = SynapseStats()

# Same API everywhere
summary = stats.get_summary()
print(f"Total messages: {summary['total_messages']}")
print(f"Reply rate: {summary['reply_rate']}")
```

### Step 3: Platform-Specific Paths

```python
from synapsestats import SynapseStats
from pathlib import Path
import platform

# Override path if needed
if platform.system() == "Windows":
    path = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
elif platform.system() == "Linux":
    path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
else:  # macOS
    path = Path.home() / "BEACON_HQ" / "MEMORY_CORE_V2" / "03_INTER_AI_COMMS" / "THE_SYNAPSE" / "active"

stats = SynapseStats(synapse_path=path)
```

### Step 4: CLI Works Everywhere

**Windows:**
```cmd
python synapsestats.py summary
python synapsestats.py agent --agent NEXUS
```

**Linux/macOS:**
```bash
python3 synapsestats.py summary
python3 synapsestats.py agent --agent NEXUS
```

### Step 5: Cross-Platform Export

```python
from synapsestats import SynapseStats
from pathlib import Path
from datetime import datetime

stats = SynapseStats()

# Export to cross-platform location
export_path = Path.home() / "synapse_reports" / f"report_{datetime.now().strftime('%Y%m%d')}.json"
export_path.parent.mkdir(parents=True, exist_ok=True)

stats.export_json(str(export_path))
print(f"Exported to: {export_path}")
```

### Next Steps for Nexus
1. Test on all 3 platforms (Windows, Linux, macOS)
2. Report any platform-specific issues
3. Create cross-platform workflow examples

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Cost-free Synapse analytics and bulk reporting

### Step 1: Verify Free Operation

```bash
# SynapseStats uses ZERO API costs!
# It analyzes local files only

python synapsestats.py --version
# SynapseStats 1.0.0
```

### Step 2: First Use - Bulk Analysis

```bash
# Generate all reports at once (no API costs!)
cd AutoProjects/SynapseStats

# Summary
python synapsestats.py summary

# All agents
for agent in FORGE ATLAS CLIO NEXUS BOLT; do
    echo "=== $agent ===" 
    python synapsestats.py agent --agent $agent
done

# Timeline
python synapsestats.py timeline --days 30
```

### Step 3: Batch Export

```bash
# Create report directory
mkdir -p reports

# Export all formats
python synapsestats.py export --output reports/summary.json --format json
python synapsestats.py export --output reports/summary.csv --format csv

# Export timeline data
python synapsestats.py timeline --days 30 > reports/timeline_30d.txt
```

### Step 4: Python Batch Processing

```python
from synapsestats import SynapseStats
from pathlib import Path
import json

# Batch generate all reports
stats = SynapseStats()

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

# Full export
stats.export_json(str(reports_dir / "full_report.json"))
stats.export_csv(str(reports_dir / "full_report.csv"))

# Individual agent reports
for agent in ['FORGE', 'ATLAS', 'CLIO', 'NEXUS', 'BOLT']:
    agent_stats = stats.get_agent_stats(agent)
    
    agent_file = reports_dir / f"agent_{agent.lower()}.json"
    agent_file.write_text(json.dumps(agent_stats, indent=2))

print("All reports generated - ZERO API costs!")
```

### Step 5: Cost-Free Automation

```bash
#!/bin/bash
# bolt_weekly_analytics.sh
# Run this weekly for comprehensive Synapse analysis

cd ~/AutoProjects/SynapseStats

WEEK=$(date +%Y-W%V)
OUTPUT_DIR="reports/weekly/$WEEK"
mkdir -p "$OUTPUT_DIR"

echo "Generating weekly Synapse analytics..."

# Full JSON export
python synapsestats.py export \
    --output "$OUTPUT_DIR/full_report.json" \
    --format json

# CSV for spreadsheet analysis
python synapsestats.py export \
    --output "$OUTPUT_DIR/summary.csv" \
    --format csv

# Agent breakdown
for agent in FORGE ATLAS CLIO NEXUS BOLT; do
    python synapsestats.py agent --agent $agent > "$OUTPUT_DIR/agent_$agent.txt"
done

# Timeline
python synapsestats.py timeline --days 7 > "$OUTPUT_DIR/timeline.txt"

echo "Weekly report generated: $OUTPUT_DIR"
echo "Total cost: $0.00"
```

### Cost Benefits Summary

| Operation | API Cost | SynapseStats Cost |
|-----------|----------|-------------------|
| Get summary | Varies | **$0.00** |
| Analyze all agents | Varies | **$0.00** |
| Generate report | Varies | **$0.00** |
| 30-day timeline | Varies | **$0.00** |

### Next Steps for Bolt
1. Schedule weekly analytics runs
2. Use for bulk data analysis tasks
3. Generate reports for team review

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- **Full Documentation:** [README.md](README.md)
- **Working Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Quick Reference:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **Integration Guide:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Code Examples:** [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

**Support:**
- **GitHub Issues:** https://github.com/DonkRonk17/SynapseStats/issues
- **Synapse:** Post in THE_SYNAPSE/active/
- **Direct:** Message ATLAS or original builder

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)
