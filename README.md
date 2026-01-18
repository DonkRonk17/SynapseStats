# SynapseStats

**Communication Analytics for THE_SYNAPSE**

Comprehensive analytics and insights into Team Brain communication patterns. Track message volume, response times, most active agents, trends over time, and export detailed reports.

---

## ⚡ Features

- **Summary Statistics** - Total messages, reply rates, activity levels
- **Agent Analytics** - Per-agent stats (sent, received, response rates)
- **Timeline Analysis** - Message trends over days/weeks
- **Priority Tracking** - Distribution by priority level
- **Communication Matrix** - Who messages whom
- **Response Time Analysis** - Average, fastest, slowest responses
- **Export Reports** - CSV and JSON export
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Works on Windows, Linux, macOS

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download
cd AutoProjects/SynapseStats

# Use immediately (no installation required!)
python synapsestats.py summary
```

### First Analysis

```bash
# Get overall summary
python synapsestats.py summary

# Analyze specific agent
python synapsestats.py agent --agent ATLAS

# View 7-day timeline
python synapsestats.py timeline --days 7

# Export full report
python synapsestats.py export --output report.json
```

---

## 💻 Usage

### Command Line Interface

```bash
# Summary statistics
python synapsestats.py summary

# Agent-specific stats
python synapsestats.py agent --agent FORGE

# Timeline (last N days)
python synapsestats.py timeline --days 14

# Export to CSV
python synapsestats.py export --output stats.csv --format csv

# Export to JSON
python synapsestats.py export --output stats.json --format json
```

### Python API

```python
from synapsestats import SynapseStats

# Initialize
stats = SynapseStats()

# Get summary
summary = stats.get_summary()
print(f"Total messages: {summary['total_messages']}")
print(f"Reply rate: {summary['reply_rate']}")
print(f"Most active: {summary['most_active_agent']}")

# Agent stats
atlas_stats = stats.get_agent_stats("ATLAS")
print(f"ATLAS sent: {atlas_stats['messages_sent']}")
print(f"ATLAS response rate: {atlas_stats['response_rate']}")

# Timeline (last 7 days)
timeline = stats.get_timeline(days=7)
for date, count in timeline.items():
    print(f"{date}: {count} messages")

# Priority trends
trends = stats.get_priority_trends()
print(f"HIGH priority: {trends['HIGH']:.1f}%")

# Communication matrix
matrix = stats.get_communication_matrix()
print(f"FORGE -> ATLAS: {matrix['FORGE']['ATLAS']} messages")

# Response times
response_times = stats.get_response_times()
print(f"Average response: {response_times['average_minutes']} minutes")

# Export
stats.export_json("full_report.json")
stats.export_csv("summary.csv")
```

---

## 📊 What You Get

### Summary Statistics

```
Total messages: 221
Reply rate: 45.2%
Most active: FORGE (85 messages)

By sender:
  FORGE: 85
  ATLAS: 67
  CLIO: 42
  NEXUS: 27

By priority:
  NORMAL: 156
  HIGH: 48
  CRITICAL: 17
```

### Agent Statistics

```
=== STATS FOR ATLAS ===
Sent: 67
Received: 89
Replied to: 42
Response rate: 47.2%
```

### Timeline

```
=== MESSAGE TIMELINE (Last 7 days) ===
2026-01-12: 18 messages
2026-01-13: 24 messages
2026-01-14: 31 messages
2026-01-15: 28 messages
2026-01-16: 35 messages
2026-01-17: 42 messages
2026-01-18: 43 messages
```

### Communication Matrix

```json
{
  "FORGE": {
    "ATLAS": 25,
    "ALL_AGENTS": 15,
    "CLIO": 12
  },
  "ATLAS": {
    "FORGE": 18,
    "ALL_AGENTS": 8
  }
}
```

### Response Time Analysis

```json
{
  "messages_analyzed": 85,
  "average_minutes": "45.3",
  "fastest_minutes": "2.1",
  "slowest_minutes": "1440.5"
}
```

---

## 🎯 Use Cases

**For Team Leaders:**
- Monitor team communication health
- Identify bottlenecks (slow responders)
- Track message volume trends
- Measure collaboration effectiveness

**For Individual Agents:**
- Track your own activity levels
- See who you communicate with most
- Monitor your response rate
- Compare your activity to team

**For System Analysis:**
- Identify communication patterns
- Spot unusual activity
- Track priority distribution
- Measure system health

---

## 📈 Advanced Features

### Time-Series Analysis

```python
# Get daily message counts for last 30 days
timeline = stats.get_timeline(days=30)

# Identify trends
daily_counts = list(timeline.values())
avg = sum(daily_counts) / len(daily_counts)
print(f"Average daily messages: {avg:.1f}")
```

### Priority Distribution

```python
trends = stats.get_priority_trends()

print("Priority Distribution:")
for priority, percent in sorted(trends.items(), key=lambda x: x[1], reverse=True):
    print(f"  {priority}: {percent:.1f}%")
```

### Export for External Analysis

```python
# Export to JSON for data science tools
stats.export_json("synapse_data.json")

# Export to CSV for Excel/Sheets
stats.export_csv("synapse_report.csv")
```

---

## 🔗 Integration with Team Brain

### With TokenTracker

```python
from synapsestats import SynapseStats
from tokentracker import TokenTracker

stats = SynapseStats()
tracker = TokenTracker()

# Correlate communication with cost
summary = stats.get_summary()
usage = tracker.get_usage_summary("month")

print(f"Messages: {summary['total_messages']}")
print(f"Cost: ${usage['total_cost']:.2f}")
print(f"Cost per message: ${usage['total_cost'] / summary['total_messages']:.4f}")
```

### With SynapseWatcher

```python
from synapsewatcher import SynapseWatcher
from synapsestats import SynapseStats

# Generate daily report when new message arrives
def generate_daily_report(message):
    if "daily report" in message.subject.lower():
        stats = SynapseStats()
        stats.export_json(f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")

watcher = SynapseWatcher()
watcher.register_callback(generate_daily_report)
watcher.start()
```

---

## 📖 Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **API Documentation** - Full API reference above

---

## 🐛 Troubleshooting

### No data showing

**Cause:** Synapse path incorrect  
**Fix:** Check `DEFAULT_SYNAPSE_PATH` in code or pass custom path:
```python
stats = SynapseStats(synapse_path=Path("/custom/path"))
```

### Malformed JSON errors

**Cause:** Some Synapse messages have invalid JSON  
**Fix:** Tool automatically skips malformed files (logged but not fatal)

### Timeline shows no data

**Cause:** Messages don't have valid timestamps  
**Fix:** Ensure messages follow standard Synapse schema with ISO timestamps

---

## 🙏 Credits

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (Q-Mode Tool Requests)  
**For:** Logan Smith / Metaphy LLC  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Methodology:** Test-Break-Optimize (20/20 tests passed)

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🔗 Links

- **GitHub:** https://github.com/DonkRonk17/SynapseStats
- **Issues:** https://github.com/DonkRonk17/SynapseStats/issues
- **Team Brain:** Part of the AutoProjects collection

---

**SynapseStats** - Because communication patterns reveal team health! 📊
