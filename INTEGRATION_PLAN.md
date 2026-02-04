# SynapseStats - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how SynapseStats integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - for real-time communication monitoring
4. Logan's workflows

SynapseStats provides **communication analytics** for THE_SYNAPSE - Team Brain's inter-AI communication channel. By understanding communication patterns, agents can optimize collaboration, identify bottlenecks, and measure team health.

---

## 📦 BCH INTEGRATION

### Overview

SynapseStats can be integrated with BCH (Beacon Command Hub) to provide real-time communication analytics dashboards and automated reporting. While THE_SYNAPSE operates as a file-based message system, BCH can leverage SynapseStats for:

1. **Dashboard displays** - Show communication metrics in BCH UI
2. **Scheduled reports** - Generate periodic analytics via BCH commands
3. **Alert triggers** - Notify when communication patterns indicate issues
4. **Agent performance tracking** - Monitor response rates and activity levels

### BCH Commands (Planned)

```bash
# Get overall Synapse health
@synapsestats summary

# Get agent-specific analytics
@synapsestats agent ATLAS

# View communication timeline
@synapsestats timeline --days 14

# Generate and export report
@synapsestats report --format json --output report.json
```

### Implementation Steps

1. **Import SynapseStats in BCH backend:**
   ```python
   from synapsestats import SynapseStats
   stats = SynapseStats()
   ```

2. **Add command handler:**
   ```python
   @bch.command("synapsestats")
   def synapsestats_command(args):
       if args.subcommand == "summary":
           return stats.get_summary()
       elif args.subcommand == "agent":
           return stats.get_agent_stats(args.agent_name)
       # ...
   ```

3. **Create dashboard widget:**
   ```python
   # BCH dashboard integration
   def get_synapse_widget_data():
       stats = SynapseStats()
       summary = stats.get_summary()
       return {
           "total_messages": summary['total_messages'],
           "reply_rate": summary['reply_rate'],
           "most_active": summary['most_active_agent'],
           "timeline": stats.get_timeline(days=7)
       }
   ```

4. **Test integration end-to-end**
5. **Update BCH documentation**

### BCH Automation Examples

**Daily Analytics Report:**
```python
# BCH scheduled task - runs daily at 08:00
@bch.schedule("0 8 * * *")
def daily_synapse_report():
    stats = SynapseStats()
    report = stats.export_json(f"reports/synapse_{datetime.now().strftime('%Y%m%d')}.json")
    
    # Post summary to Synapse
    from synapselink import quick_send
    summary = stats.get_summary()
    quick_send(
        "ALL_AGENTS",
        "Daily Synapse Report",
        f"Messages yesterday: {summary['total_messages']}\n"
        f"Reply rate: {summary['reply_rate']}\n"
        f"Most active: {summary['most_active_agent']}",
        priority="NORMAL"
    )
```

**Alert on Low Activity:**
```python
# Alert if no messages in 24 hours
@bch.schedule("0 * * * *")  # Hourly check
def check_synapse_activity():
    stats = SynapseStats()
    timeline = stats.get_timeline(days=1)
    
    if all(count == 0 for count in timeline.values()):
        from synapselink import quick_send
        quick_send(
            "FORGE,LOGAN",
            "[ALERT] No Synapse Activity",
            "No messages detected in THE_SYNAPSE for 24 hours.",
            priority="HIGH"
        )
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Team coordination analytics, performance monitoring | Python API | HIGH |
| **Atlas** | Build session communication tracking | Python API | HIGH |
| **Clio** | Linux server log analysis, automated reports | CLI | MEDIUM |
| **Nexus** | Cross-platform analytics | Python API + CLI | MEDIUM |
| **Bolt** | Batch processing, report generation | CLI | LOW |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Monitor team communication health, identify coordination issues, track agent responsiveness.

**Integration Steps:**
1. Add SynapseStats to session startup routine
2. Review daily/weekly communication summaries
3. Identify agents with low response rates
4. Track message priority distribution (too many HIGH = potential burnout)

**Example Workflow:**

```python
# Forge orchestration session startup
from synapsestats import SynapseStats

def forge_session_start():
    """Forge's standard session initialization with Synapse health check."""
    
    stats = SynapseStats()
    summary = stats.get_summary()
    
    # Check team health indicators
    print("[Synapse Health Check]")
    print(f"  Total messages: {summary['total_messages']}")
    print(f"  Reply rate: {summary['reply_rate']}")
    print(f"  Most active: {summary['most_active_agent']}")
    
    # Alert on concerning patterns
    reply_rate = float(summary['reply_rate'].rstrip('%'))
    if reply_rate < 40:
        print("[WARNING] Low reply rate detected - check team coordination")
    
    # Check individual agent health
    for agent in ['ATLAS', 'CLIO', 'NEXUS', 'BOLT']:
        agent_stats = stats.get_agent_stats(agent)
        response_rate = agent_stats['response_rate']
        if response_rate != "N/A" and float(response_rate.rstrip('%')) < 30:
            print(f"[NOTICE] {agent} has low response rate: {response_rate}")
    
    return summary
```

**Task Assignment Optimization:**

```python
def assign_task_by_activity(task_description):
    """Use Synapse activity to inform task assignment."""
    from synapsestats import SynapseStats
    from agentrouter import AgentRouter
    
    stats = SynapseStats()
    router = AgentRouter()
    
    # Get initial routing suggestion
    routing = router.route(task_description)
    
    # Check if suggested agent is responsive
    agent_stats = stats.get_agent_stats(routing['agent'])
    
    # If agent has low response rate, consider alternatives
    response_rate = agent_stats.get('response_rate', 'N/A')
    if response_rate != 'N/A' and float(response_rate.rstrip('%')) < 25:
        print(f"Warning: {routing['agent']} has low response rate ({response_rate})")
        print("Consider alternative assignment")
    
    return routing
```

#### Atlas (Executor / Builder)

**Primary Use Case:** Track communication during tool builds, measure coordination overhead, document collaboration patterns.

**Integration Steps:**
1. Record Synapse activity at session start/end
2. Compare communication volume across different tool builds
3. Identify which builds required most coordination
4. Use data to improve build documentation

**Example Workflow:**

```python
# Atlas tool build with communication tracking
from synapsestats import SynapseStats
from datetime import datetime

def start_tool_build(tool_name):
    """Start tracking communication for a tool build session."""
    stats = SynapseStats()
    
    # Record baseline
    baseline = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": tool_name,
        "initial_total": stats.get_summary()['total_messages'],
        "initial_timeline": stats.get_timeline(days=1)
    }
    
    print(f"[Build Session] Starting {tool_name}")
    print(f"  Synapse messages today: {list(baseline['initial_timeline'].values())[-1]}")
    
    return baseline

def end_tool_build(baseline):
    """Calculate communication overhead for the build."""
    stats = SynapseStats()
    summary = stats.get_summary()
    
    messages_during_build = summary['total_messages'] - baseline['initial_total']
    
    report = {
        "tool_name": baseline['tool_name'],
        "duration_start": baseline['timestamp'],
        "duration_end": datetime.now().isoformat(),
        "messages_generated": messages_during_build,
        "coordination_overhead": "LOW" if messages_during_build < 5 else 
                                "MEDIUM" if messages_during_build < 15 else "HIGH"
    }
    
    print(f"[Build Session] Complete: {baseline['tool_name']}")
    print(f"  Messages during build: {messages_during_build}")
    print(f"  Coordination overhead: {report['coordination_overhead']}")
    
    return report
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Automated Synapse analytics from command line, scheduled reports, log integration.

**Platform Considerations:**
- Runs on Ubuntu/WSL
- Prefers CLI over Python API for scripting
- Can schedule via cron

**Example:**

```bash
# Clio daily analytics script
#!/bin/bash

# Generate daily report
cd /path/to/SynapseStats
python synapsestats.py export --output /var/log/synapse/daily_$(date +%Y%m%d).json --format json

# Quick summary to stdout
echo "=== SYNAPSE DAILY SUMMARY ==="
python synapsestats.py summary

# Agent-specific checks
for agent in FORGE ATLAS CLIO NEXUS BOLT; do
    echo "=== $agent ===" 
    python synapsestats.py agent --agent $agent
done
```

**Cron Integration:**

```bash
# /etc/cron.d/synapse-analytics
# Generate daily report at 23:59
59 23 * * * clio python /opt/AutoProjects/SynapseStats/synapsestats.py export --output /var/log/synapse/daily_$(date +\%Y\%m\%d).json

# Hourly activity check
0 * * * * clio python /opt/AutoProjects/SynapseStats/synapsestats.py summary | logger -t synapse-stats
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform analytics, Windows/Linux compatibility testing, GitHub integration.

**Cross-Platform Notes:**
- Same Python API works on all platforms
- CLI commands work identically
- File paths auto-adapt via pathlib

**Example:**

```python
# Nexus cross-platform analytics
import platform
from synapsestats import SynapseStats
from pathlib import Path

def nexus_cross_platform_check():
    """Verify Synapse analytics work on current platform."""
    
    print(f"Platform: {platform.system()}")
    print(f"Python: {platform.python_version()}")
    
    # SynapseStats handles paths cross-platform
    stats = SynapseStats()
    summary = stats.get_summary()
    
    print(f"Messages loaded: {summary['total_messages']}")
    print(f"Platform test: PASS")
    
    return True
```

#### Bolt (Free Executor / Cline)

**Primary Use Case:** Bulk report generation, data exports, non-interactive analytics.

**Cost Considerations:**
- SynapseStats has zero API costs (local analysis only)
- Perfect for Bolt's cost-free execution model
- Can generate reports without token usage

**Example:**

```bash
# Bolt batch export - no API costs!
cd AutoProjects/SynapseStats

# Generate multiple report formats
python synapsestats.py export --output reports/weekly.json --format json
python synapsestats.py export --output reports/weekly.csv --format csv

# Generate timeline data
python synapsestats.py timeline --days 30 > reports/timeline_30days.txt

# Batch agent analysis
for agent in FORGE ATLAS CLIO NEXUS BOLT; do
    python synapsestats.py agent --agent $agent > reports/agent_$agent.txt
done
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With SynapseLink

**Communication Use Case:** Combine message sending with analytics for self-awareness.

**Integration Pattern:**

```python
from synapselink import quick_send, SynapseLink
from synapsestats import SynapseStats

def send_with_context(to, subject, body, priority="NORMAL"):
    """Send Synapse message with communication context."""
    
    # Get current stats before sending
    stats = SynapseStats()
    my_stats = stats.get_agent_stats("ATLAS")  # Replace with your agent name
    
    # Add context to message if relevant
    if my_stats['messages_sent'] > 10:
        body += f"\n\n[Note: I've sent {my_stats['messages_sent']} messages today]"
    
    # Send the message
    quick_send(to, subject, body, priority=priority)
    
    return my_stats
```

### With SynapseWatcher

**Real-time Analytics Use Case:** Combine watching with analytics for live dashboards.

**Integration Pattern:**

```python
from synapsewatcher import SynapseWatcher
from synapsestats import SynapseStats

class SynapseDashboard:
    """Real-time Synapse dashboard combining watching and analytics."""
    
    def __init__(self):
        self.watcher = SynapseWatcher()
        self.stats = SynapseStats()
        
        # Register callback for live updates
        self.watcher.register_callback(self.on_new_message)
    
    def on_new_message(self, message):
        """Called when new message arrives."""
        # Refresh stats
        self.stats = SynapseStats()
        
        # Update dashboard
        summary = self.stats.get_summary()
        print(f"\n[NEW MESSAGE] From: {message.get('from')}")
        print(f"Total messages now: {summary['total_messages']}")
        print(f"Current reply rate: {summary['reply_rate']}")
    
    def start(self):
        """Start the live dashboard."""
        print("[SynapseDashboard] Starting...")
        self.watcher.start()
```

### With AgentHealth

**Health Correlation Use Case:** Correlate communication patterns with agent health.

**Integration Pattern:**

```python
from agenthealth import AgentHealth
from synapsestats import SynapseStats

def comprehensive_health_check(agent_name):
    """Check agent health including communication metrics."""
    
    health = AgentHealth()
    stats = SynapseStats()
    
    # Get health status
    agent_health = health.get_health(agent_name)
    
    # Get communication stats
    comm_stats = stats.get_agent_stats(agent_name)
    
    # Combine into comprehensive report
    report = {
        "agent": agent_name,
        "health": {
            "status": agent_health.get('status', 'unknown'),
            "last_heartbeat": agent_health.get('last_heartbeat', 'N/A'),
            "uptime": agent_health.get('uptime', 'N/A')
        },
        "communication": {
            "messages_sent": comm_stats['messages_sent'],
            "messages_received": comm_stats['messages_received'],
            "response_rate": comm_stats['response_rate']
        },
        "assessment": "healthy" if agent_health.get('status') == 'active' 
                      and float(comm_stats['response_rate'].rstrip('%') or 0) > 30
                      else "needs_attention"
    }
    
    return report
```

### With TokenTracker

**Cost Correlation Use Case:** Correlate communication volume with API costs.

**Integration Pattern:**

```python
from tokentracker import TokenTracker
from synapsestats import SynapseStats

def communication_cost_analysis():
    """Analyze relationship between communication and costs."""
    
    tracker = TokenTracker()
    stats = SynapseStats()
    
    # Get communication volume
    summary = stats.get_summary()
    timeline = stats.get_timeline(days=7)
    
    # Get token usage
    token_usage = tracker.get_usage_summary("week")
    
    # Calculate metrics
    total_messages = summary['total_messages']
    total_cost = token_usage.get('total_cost', 0)
    
    report = {
        "period": "7 days",
        "total_messages": total_messages,
        "total_cost": f"${total_cost:.2f}",
        "cost_per_message": f"${total_cost / total_messages:.4f}" if total_messages > 0 else "N/A",
        "daily_breakdown": []
    }
    
    print("=== Communication Cost Analysis ===")
    print(f"Total messages: {total_messages}")
    print(f"Total cost: ${total_cost:.2f}")
    if total_messages > 0:
        print(f"Avg cost per message: ${total_cost / total_messages:.4f}")
    
    return report
```

### With TaskQueuePro

**Coordination Use Case:** Track task-related communication.

**Integration Pattern:**

```python
from taskqueuepro import TaskQueuePro
from synapsestats import SynapseStats

def analyze_task_communication(task_id):
    """Analyze communication related to a specific task."""
    
    queue = TaskQueuePro()
    stats = SynapseStats()
    
    # Get task details
    task = queue.get_task(task_id)
    
    # Get communication matrix
    matrix = stats.get_communication_matrix()
    
    # Find messages involving task assignee
    assignee = task.get('agent', 'UNKNOWN')
    
    sent = matrix.get(assignee, {})
    received = sum(
        target_counts.get(assignee, 0)
        for target_counts in matrix.values()
    )
    
    return {
        "task_id": task_id,
        "assignee": assignee,
        "messages_sent_by_assignee": sum(sent.values()),
        "messages_received_by_assignee": received,
        "communication_partners": list(sent.keys())
    }
```

### With SessionReplay

**Debugging Use Case:** Include communication context in session replays.

**Integration Pattern:**

```python
from sessionreplay import SessionReplay
from synapsestats import SynapseStats

def replay_with_communication_context(session_id):
    """Replay a session with Synapse communication overlaid."""
    
    replay = SessionReplay()
    stats = SynapseStats()
    
    # Get session events
    session = replay.get_session(session_id)
    
    # Get communication during that time
    # (Would need timestamp filtering in SynapseStats for full implementation)
    summary = stats.get_summary()
    
    print(f"=== Session Replay with Communication Context ===")
    print(f"Session: {session_id}")
    print(f"Events: {len(session.get('events', []))}")
    print(f"Synapse context: {summary['total_messages']} total messages")
    
    return session
```

### With ContextCompressor

**Token Optimization Use Case:** Compress Synapse analytics for sharing.

**Integration Pattern:**

```python
from contextcompressor import ContextCompressor
from synapsestats import SynapseStats
import json

def compress_synapse_report():
    """Generate compressed Synapse summary for token-efficient sharing."""
    
    compressor = ContextCompressor()
    stats = SynapseStats()
    
    # Generate full report
    full_report = json.dumps({
        "summary": stats.get_summary(),
        "timeline": stats.get_timeline(days=7),
        "matrix": stats.get_communication_matrix()
    }, indent=2)
    
    # Compress for sharing
    compressed = compressor.compress_text(
        full_report,
        query="key communication metrics",
        method="summary"
    )
    
    print(f"Original size: {len(full_report)} chars")
    print(f"Compressed size: {compressed.compressed_size} chars")
    print(f"Token savings: {compressed.estimated_token_savings}")
    
    return compressed.compressed_text
```

### With MemoryBridge

**Persistence Use Case:** Store historical analytics in memory core.

**Integration Pattern:**

```python
from memorybridge import MemoryBridge
from synapsestats import SynapseStats
from datetime import datetime

def archive_daily_stats():
    """Archive daily Synapse stats to memory core."""
    
    memory = MemoryBridge()
    stats = SynapseStats()
    
    # Get today's summary
    today = datetime.now().strftime('%Y-%m-%d')
    summary = stats.get_summary()
    
    # Load history
    history = memory.get("synapse_daily_history", default=[])
    
    # Add today's data
    history.append({
        "date": today,
        "total_messages": summary['total_messages'],
        "reply_rate": summary['reply_rate'],
        "most_active": summary['most_active_agent']
    })
    
    # Keep last 90 days
    history = history[-90:]
    
    # Save
    memory.set("synapse_daily_history", history)
    memory.sync()
    
    print(f"Archived stats for {today}")
    print(f"History now contains {len(history)} days")
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✓ Tool deployed to GitHub
2. ☐ Quick-start guides distributed via Synapse
3. ☐ Each agent tests `summary` command
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have run `synapsestats summary` at least once
- No blocking issues reported
- Basic workflow documented for each agent

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Forge adds to orchestration startup
2. ☐ Atlas adds to tool build tracking
3. ☐ Clio sets up cron-based reports
4. ☐ Integrate with SynapseWatcher for live updates
5. ☐ Test SynapseLink integration

**Success Criteria:**
- Used daily by at least 3 agents
- Automated reports running on schedule
- Integration examples tested and documented

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements based on feedback
3. ☐ Create advanced workflow examples
4. ☐ Full BCH integration (if applicable)

**Success Criteria:**
- Measurable insights from communication analytics
- Positive feedback from all agents
- v1.1 improvements identified and prioritized

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: Target 5/5
- Daily usage count: Track via logs
- Integration with other tools: Target 3+ integrations active

**Value Metrics:**
- Communication patterns identified: Track discoveries
- Issues detected via analytics: Track alerts
- Report generation frequency: Track exports

**Quality Metrics:**
- Bug reports: Target < 2 per month
- Feature requests: Track and prioritize
- User satisfaction: Qualitative feedback

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from synapsestats import SynapseStats

# With custom path
from synapsestats import SynapseStats
stats = SynapseStats(synapse_path=Path("/custom/path"))
```

### Default Synapse Path

```python
# Default path (can be overridden)
DEFAULT_SYNAPSE_PATH = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
```

### Return Value Formats

**Summary:**
```python
{
    "total_messages": int,
    "total_replies": int,
    "messages_with_replies": int,
    "messages_no_replies": int,
    "reply_rate": str,  # "45.2%"
    "by_sender": dict,  # {"FORGE": 85, "ATLAS": 67, ...}
    "by_priority": dict,  # {"HIGH": 48, "NORMAL": 156, ...}
    "most_active_agent": str,
    "most_active_count": int
}
```

**Agent Stats:**
```python
{
    "agent": str,
    "messages_sent": int,
    "messages_received": int,
    "messages_replied_to": int,
    "response_rate": str  # "47.2%" or "N/A"
}
```

**Timeline:**
```python
{
    "2026-01-25": 42,
    "2026-01-26": 38,
    # ...
}
```

### Error Handling

SynapseStats handles errors gracefully:
- Missing Synapse path: Returns empty message list
- Malformed JSON: Skips file silently
- Missing timestamps: Excluded from timeline analysis

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- **Minor updates (v1.x):** As needed for bug fixes
- **Major updates (v2.0+):** Quarterly, with new features
- **Security patches:** Immediate if required

### Support Channels

- **GitHub Issues:** Bug reports and feature requests
- **Synapse:** Team Brain discussions
- **Direct to Builder:** Complex integration issues

### Known Limitations

1. **File-based loading:** Reloads all messages each time (no caching)
   - *Improvement for v1.1:* Add caching layer for better performance

2. **Basic timestamp parsing:** May miss some timestamp formats
   - *Improvement for v1.1:* More robust datetime parsing

3. **No real-time updates:** Requires manual refresh
   - *Mitigation:* Use with SynapseWatcher for live updates

---

## 📚 ADDITIONAL RESOURCES

- **Main Documentation:** [README.md](README.md)
- **Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Quick Reference:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **Integration Examples:** [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- **Agent Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **GitHub:** https://github.com/DonkRonk17/SynapseStats

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC
