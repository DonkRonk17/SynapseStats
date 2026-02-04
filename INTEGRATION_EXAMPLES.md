# SynapseStats - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

SynapseStats is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

All examples are tested and ready to use in your workflows.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: SynapseStats + SynapseLink](#pattern-1-synapsestats--synapselink)
2. [Pattern 2: SynapseStats + SynapseWatcher](#pattern-2-synapsestats--synapsewatcher)
3. [Pattern 3: SynapseStats + AgentHealth](#pattern-3-synapsestats--agenthealth)
4. [Pattern 4: SynapseStats + TokenTracker](#pattern-4-synapsestats--tokentracker)
5. [Pattern 5: SynapseStats + TaskQueuePro](#pattern-5-synapsestats--taskqueuepro)
6. [Pattern 6: SynapseStats + SessionReplay](#pattern-6-synapsestats--sessionreplay)
7. [Pattern 7: SynapseStats + MemoryBridge](#pattern-7-synapsestats--memorybridge)
8. [Pattern 8: SynapseStats + ContextCompressor](#pattern-8-synapsestats--contextcompressor)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: SynapseStats + SynapseLink

**Use Case:** Send Synapse messages with communication context awareness

**Why:** Be aware of your own communication patterns when sending messages

**Code:**

```python
from synapsestats import SynapseStats
from synapselink import quick_send

def send_message_with_context(to, subject, body, agent_name="ATLAS", priority="NORMAL"):
    """Send a Synapse message with awareness of current communication patterns."""
    
    # Get current stats
    stats = SynapseStats()
    my_stats = stats.get_agent_stats(agent_name)
    summary = stats.get_summary()
    
    # Check if team is overwhelmed
    reply_rate = float(summary['reply_rate'].rstrip('%'))
    if reply_rate < 30 and priority == "NORMAL":
        print(f"[Notice] Low team reply rate ({reply_rate}%). Consider if this message is necessary.")
    
    # Check your own activity
    sent_today = my_stats['messages_sent']
    if sent_today > 20:
        print(f"[Notice] You've sent {sent_today} messages today. Consider batching communications.")
    
    # Send the message
    result = quick_send(to, subject, body, priority=priority)
    
    return {
        "sent": True,
        "team_reply_rate": summary['reply_rate'],
        "your_messages_today": sent_today
    }

# Example usage
result = send_message_with_context(
    to="FORGE",
    subject="Task Complete: SynapseStats Repair",
    body="Phase 7 documentation added. Ready for review.",
    agent_name="ATLAS"
)
print(f"Message sent. Team reply rate: {result['team_reply_rate']}")
```

**Result:** Messages sent with awareness of team communication health

---

## Pattern 2: SynapseStats + SynapseWatcher

**Use Case:** Real-time dashboard combining watching with analytics

**Why:** Get live updates with statistical context

**Code:**

```python
from synapsestats import SynapseStats
from synapsewatcher import SynapseWatcher
from datetime import datetime

class LiveSynapseDashboard:
    """Real-time Synapse dashboard with analytics."""
    
    def __init__(self):
        self.watcher = SynapseWatcher()
        self.message_count_at_start = 0
        self.session_start = datetime.now()
        
        # Register callback
        self.watcher.register_callback(self.on_message)
    
    def on_message(self, message):
        """Called when a new message arrives."""
        # Refresh stats
        stats = SynapseStats()
        summary = stats.get_summary()
        
        # Calculate session metrics
        session_duration = (datetime.now() - self.session_start).seconds / 60
        messages_this_session = summary['total_messages'] - self.message_count_at_start
        
        # Display update
        print(f"\n{'='*50}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] NEW MESSAGE")
        print(f"  From: {message.get('from', 'unknown')}")
        print(f"  Subject: {message.get('subject', 'no subject')}")
        print(f"{'='*50}")
        print(f"Session Stats ({session_duration:.0f} min):")
        print(f"  Messages this session: {messages_this_session}")
        print(f"  Total messages: {summary['total_messages']}")
        print(f"  Reply rate: {summary['reply_rate']}")
        print(f"{'='*50}\n")
    
    def start(self):
        """Start the live dashboard."""
        stats = SynapseStats()
        self.message_count_at_start = stats.get_summary()['total_messages']
        self.session_start = datetime.now()
        
        print("Live Synapse Dashboard Started")
        print(f"Baseline: {self.message_count_at_start} messages")
        print("Watching for new messages...\n")
        
        self.watcher.start()
    
    def stop(self):
        """Stop the dashboard."""
        self.watcher.stop()
        print("Dashboard stopped")

# Example usage
dashboard = LiveSynapseDashboard()
dashboard.start()
# dashboard.stop()  # When done
```

**Result:** Real-time message notifications with statistical context

---

## Pattern 3: SynapseStats + AgentHealth

**Use Case:** Comprehensive agent health including communication metrics

**Why:** Communication patterns are indicators of agent health

**Code:**

```python
from synapsestats import SynapseStats
from agenthealth import AgentHealth

def comprehensive_agent_health(agent_name):
    """Get full health report including communication metrics."""
    
    health = AgentHealth()
    stats = SynapseStats()
    
    # Get health status
    agent_health = health.get_health(agent_name)
    
    # Get communication stats
    comm_stats = stats.get_agent_stats(agent_name)
    summary = stats.get_summary()
    
    # Calculate communication health score
    response_rate_str = comm_stats['response_rate']
    if response_rate_str != "N/A":
        response_rate = float(response_rate_str.rstrip('%'))
    else:
        response_rate = 0
    
    # Communication health indicators
    comm_health = "healthy"
    comm_notes = []
    
    if response_rate < 30:
        comm_health = "low_engagement"
        comm_notes.append(f"Response rate {response_rate}% is below 30% threshold")
    
    if comm_stats['messages_sent'] == 0:
        comm_health = "inactive"
        comm_notes.append("No messages sent")
    
    # Compile report
    report = {
        "agent": agent_name,
        "health_status": {
            "operational": agent_health.get('status', 'unknown'),
            "last_heartbeat": agent_health.get('last_heartbeat', 'N/A'),
            "uptime": agent_health.get('uptime', 'N/A')
        },
        "communication_status": {
            "health": comm_health,
            "messages_sent": comm_stats['messages_sent'],
            "messages_received": comm_stats['messages_received'],
            "response_rate": comm_stats['response_rate'],
            "notes": comm_notes
        },
        "team_context": {
            "team_reply_rate": summary['reply_rate'],
            "most_active_agent": summary['most_active_agent']
        },
        "overall_assessment": "healthy" if comm_health == "healthy" else "needs_attention"
    }
    
    return report

# Example usage
report = comprehensive_agent_health("ATLAS")
print(f"Agent: {report['agent']}")
print(f"Overall: {report['overall_assessment']}")
print(f"Response rate: {report['communication_status']['response_rate']}")
print(f"Messages sent: {report['communication_status']['messages_sent']}")
```

**Result:** Combined health and communication assessment

---

## Pattern 4: SynapseStats + TokenTracker

**Use Case:** Correlate communication volume with API costs

**Why:** Understand the cost of team coordination

**Code:**

```python
from synapsestats import SynapseStats
from tokentracker import TokenTracker
from datetime import datetime

def communication_cost_report(days=7):
    """Analyze communication volume vs API costs."""
    
    stats = SynapseStats()
    tracker = TokenTracker()
    
    # Get communication data
    summary = stats.get_summary()
    timeline = stats.get_timeline(days=days)
    
    # Get token/cost data
    usage = tracker.get_usage_summary("week")
    
    # Calculate metrics
    total_messages = summary['total_messages']
    total_cost = usage.get('total_cost', 0)
    total_tokens = usage.get('total_tokens', 0)
    
    cost_per_message = total_cost / total_messages if total_messages > 0 else 0
    tokens_per_message = total_tokens / total_messages if total_messages > 0 else 0
    
    report = {
        "period": f"{days} days",
        "generated": datetime.now().isoformat(),
        
        "communication": {
            "total_messages": total_messages,
            "reply_rate": summary['reply_rate'],
            "most_active": summary['most_active_agent'],
            "by_sender": summary['by_sender']
        },
        
        "costs": {
            "total_cost": f"${total_cost:.2f}",
            "total_tokens": total_tokens,
            "cost_per_message": f"${cost_per_message:.4f}",
            "tokens_per_message": round(tokens_per_message)
        },
        
        "insights": []
    }
    
    # Add insights
    if cost_per_message > 0.10:
        report['insights'].append("High cost per message - consider batching communications")
    if total_messages > 100 and float(summary['reply_rate'].rstrip('%')) < 30:
        report['insights'].append("Many messages but low reply rate - communication may be inefficient")
    
    return report

# Example usage
report = communication_cost_report(days=7)
print(f"=== Communication Cost Report ({report['period']}) ===")
print(f"Messages: {report['communication']['total_messages']}")
print(f"Total cost: {report['costs']['total_cost']}")
print(f"Cost per message: {report['costs']['cost_per_message']}")
if report['insights']:
    print(f"Insights: {', '.join(report['insights'])}")
```

**Result:** Clear correlation between communication and costs

---

## Pattern 5: SynapseStats + TaskQueuePro

**Use Case:** Track communication related to task management

**Why:** Understand coordination overhead for tasks

**Code:**

```python
from synapsestats import SynapseStats
from taskqueuepro import TaskQueuePro

def analyze_task_communication():
    """Analyze communication patterns around task management."""
    
    queue = TaskQueuePro()
    stats = SynapseStats()
    
    # Get communication matrix
    matrix = stats.get_communication_matrix()
    summary = stats.get_summary()
    
    # Get active tasks
    active_tasks = queue.list_tasks(status="in_progress")
    
    # Analyze communication for each agent with active tasks
    analysis = []
    for task in active_tasks:
        agent = task.get('agent', 'UNKNOWN')
        agent_stats = stats.get_agent_stats(agent)
        
        # Get who this agent communicates with
        sent_to = matrix.get(agent, {})
        
        analysis.append({
            "task_id": task.get('id'),
            "task_title": task.get('title'),
            "agent": agent,
            "messages_sent": agent_stats['messages_sent'],
            "response_rate": agent_stats['response_rate'],
            "communicates_with": list(sent_to.keys())[:3]  # Top 3
        })
    
    return {
        "total_active_tasks": len(active_tasks),
        "team_reply_rate": summary['reply_rate'],
        "task_details": analysis
    }

# Example usage
result = analyze_task_communication()
print(f"Active tasks: {result['total_active_tasks']}")
print(f"Team reply rate: {result['team_reply_rate']}")
for task in result['task_details']:
    print(f"\nTask: {task['task_title']}")
    print(f"  Assigned to: {task['agent']}")
    print(f"  Response rate: {task['response_rate']}")
```

**Result:** Task-level communication analysis

---

## Pattern 6: SynapseStats + SessionReplay

**Use Case:** Include communication context in session recordings

**Why:** Understand communication patterns during sessions

**Code:**

```python
from synapsestats import SynapseStats
from sessionreplay import SessionReplay
from datetime import datetime

def start_recorded_session(agent_name, task_description):
    """Start a session with communication baseline recorded."""
    
    replay = SessionReplay()
    stats = SynapseStats()
    
    # Record baseline
    baseline = stats.get_summary()
    agent_baseline = stats.get_agent_stats(agent_name)
    
    # Start session
    session_id = replay.start_session(agent_name, task=task_description)
    
    # Log communication context
    replay.log_input(session_id, f"[Communication Baseline]")
    replay.log_input(session_id, f"  Total messages: {baseline['total_messages']}")
    replay.log_input(session_id, f"  Agent messages: {agent_baseline['messages_sent']}")
    replay.log_input(session_id, f"  Team reply rate: {baseline['reply_rate']}")
    
    return {
        "session_id": session_id,
        "baseline_messages": baseline['total_messages'],
        "baseline_agent_sent": agent_baseline['messages_sent']
    }

def end_recorded_session(session_info, agent_name, status="COMPLETED"):
    """End session with communication summary."""
    
    replay = SessionReplay()
    stats = SynapseStats()
    
    # Get final stats
    final = stats.get_summary()
    agent_final = stats.get_agent_stats(agent_name)
    
    # Calculate deltas
    messages_during = final['total_messages'] - session_info['baseline_messages']
    sent_during = agent_final['messages_sent'] - session_info['baseline_agent_sent']
    
    # Log to session
    replay.log_output(session_info['session_id'], f"[Communication Summary]")
    replay.log_output(session_info['session_id'], f"  Messages during session: {messages_during}")
    replay.log_output(session_info['session_id'], f"  Messages sent: {sent_during}")
    
    # End session
    replay.end_session(session_info['session_id'], status=status)
    
    return {
        "messages_during_session": messages_during,
        "messages_sent": sent_during
    }

# Example usage
session = start_recorded_session("ATLAS", "Build SynapseStats Phase 7")
# ... do work ...
result = end_recorded_session(session, "ATLAS")
print(f"Session recorded. Messages during: {result['messages_during_session']}")
```

**Result:** Session recordings with communication context

---

## Pattern 7: SynapseStats + MemoryBridge

**Use Case:** Persist historical analytics to memory core

**Why:** Track communication trends over time

**Code:**

```python
from synapsestats import SynapseStats
from memorybridge import MemoryBridge
from datetime import datetime

def archive_daily_synapse_stats():
    """Archive today's Synapse stats to memory core."""
    
    memory = MemoryBridge()
    stats = SynapseStats()
    
    # Get today's data
    today = datetime.now().strftime('%Y-%m-%d')
    summary = stats.get_summary()
    
    # Load or create history
    history = memory.get("synapse_stats_history", default=[])
    
    # Check if today already recorded
    if any(entry['date'] == today for entry in history):
        print(f"Stats for {today} already archived")
        return history
    
    # Create today's entry
    entry = {
        "date": today,
        "total_messages": summary['total_messages'],
        "reply_rate": summary['reply_rate'],
        "most_active": summary['most_active_agent'],
        "by_sender": summary['by_sender'],
        "by_priority": summary['by_priority']
    }
    
    # Add to history
    history.append(entry)
    
    # Keep last 90 days
    history = history[-90:]
    
    # Save
    memory.set("synapse_stats_history", history)
    memory.sync()
    
    print(f"Archived stats for {today}")
    print(f"History now contains {len(history)} days")
    
    return history

def get_trend_report(days=30):
    """Get trend report from archived data."""
    
    memory = MemoryBridge()
    history = memory.get("synapse_stats_history", default=[])
    
    if len(history) < 2:
        return {"error": "Insufficient history data"}
    
    # Get recent entries
    recent = history[-days:]
    
    # Calculate trends
    reply_rates = []
    for entry in recent:
        rate_str = entry.get('reply_rate', '0%')
        rate = float(rate_str.rstrip('%'))
        reply_rates.append(rate)
    
    avg_reply_rate = sum(reply_rates) / len(reply_rates) if reply_rates else 0
    trend = "improving" if reply_rates[-1] > reply_rates[0] else "declining" if reply_rates[-1] < reply_rates[0] else "stable"
    
    return {
        "period": f"{len(recent)} days",
        "average_reply_rate": f"{avg_reply_rate:.1f}%",
        "trend": trend,
        "earliest": recent[0]['date'],
        "latest": recent[-1]['date']
    }

# Example usage
archive_daily_synapse_stats()
trends = get_trend_report(days=30)
print(f"Trend report ({trends['period']}): {trends['trend']}")
```

**Result:** Historical communication data in memory core

---

## Pattern 8: SynapseStats + ContextCompressor

**Use Case:** Compress Synapse reports for token-efficient sharing

**Why:** Save tokens when sharing large reports

**Code:**

```python
from synapsestats import SynapseStats
from contextcompressor import ContextCompressor
import json

def generate_compressed_report():
    """Generate a compressed Synapse report for sharing."""
    
    compressor = ContextCompressor()
    stats = SynapseStats()
    
    # Generate full report
    full_report = {
        "summary": stats.get_summary(),
        "timeline_7d": stats.get_timeline(days=7),
        "priority_trends": stats.get_priority_trends(),
        "response_times": stats.get_response_times(),
        "communication_matrix": stats.get_communication_matrix()
    }
    
    full_text = json.dumps(full_report, indent=2)
    
    # Compress
    compressed = compressor.compress_text(
        full_text,
        query="key communication metrics and insights",
        method="summary"
    )
    
    print(f"Original size: {len(full_text)} characters")
    print(f"Compressed size: {compressed.compressed_size} characters")
    print(f"Reduction: {(1 - compressed.compressed_size/len(full_text))*100:.1f}%")
    
    return {
        "compressed_report": compressed.compressed_text,
        "original_size": len(full_text),
        "compressed_size": compressed.compressed_size,
        "token_savings": compressed.estimated_token_savings
    }

# Example usage
result = generate_compressed_report()
print(f"\nCompressed Report:\n{result['compressed_report']}")
```

**Result:** Token-efficient report sharing

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools with SynapseStats

**Why:** Demonstrate real production integration

**Code:**

```python
from synapsestats import SynapseStats
from taskqueuepro import TaskQueuePro
from synapselink import quick_send
from agenthealth import AgentHealth
from datetime import datetime

def comprehensive_team_review(agent_name="FORGE"):
    """Complete team communication review workflow."""
    
    print(f"=== Team Communication Review - {datetime.now().strftime('%Y-%m-%d')} ===\n")
    
    # Initialize tools
    stats = SynapseStats()
    queue = TaskQueuePro()
    health = AgentHealth()
    
    # 1. Get overall communication health
    summary = stats.get_summary()
    print(f"[1] Communication Summary")
    print(f"    Total messages: {summary['total_messages']}")
    print(f"    Reply rate: {summary['reply_rate']}")
    print(f"    Most active: {summary['most_active_agent']}")
    
    # 2. Check each agent
    agents = ['FORGE', 'ATLAS', 'CLIO', 'NEXUS', 'BOLT']
    print(f"\n[2] Agent Status")
    
    concerns = []
    for agent in agents:
        agent_stats = stats.get_agent_stats(agent)
        agent_health = health.get_health(agent)
        
        status = agent_health.get('status', 'unknown')
        response = agent_stats['response_rate']
        
        print(f"    {agent}: {status}, response rate {response}")
        
        if response != "N/A" and float(response.rstrip('%')) < 30:
            concerns.append(f"{agent} has low response rate ({response})")
    
    # 3. Check task queue alignment
    active_tasks = queue.list_tasks(status="in_progress")
    print(f"\n[3] Task Queue")
    print(f"    Active tasks: {len(active_tasks)}")
    
    # 4. Generate insights
    print(f"\n[4] Insights")
    
    reply_rate = float(summary['reply_rate'].rstrip('%'))
    if reply_rate < 40:
        print(f"    [!] Team reply rate below 40% - coordination may be suffering")
    else:
        print(f"    [OK] Team reply rate healthy at {reply_rate}%")
    
    for concern in concerns:
        print(f"    [!] {concern}")
    
    # 5. Create summary message
    report_body = f"""Team Communication Review - {datetime.now().strftime('%Y-%m-%d')}

Summary:
- Total messages: {summary['total_messages']}
- Reply rate: {summary['reply_rate']}
- Most active: {summary['most_active_agent']}
- Active tasks: {len(active_tasks)}

Concerns:
{chr(10).join('- ' + c for c in concerns) if concerns else '- None'}

Generated by automated team review workflow.
"""
    
    print(f"\n[5] Review complete. Ready to send report.")
    
    return {
        "summary": summary,
        "concerns": concerns,
        "active_tasks": len(active_tasks),
        "report": report_body
    }

# Example usage
result = comprehensive_team_review()
# Optionally send the report:
# quick_send("ALL_AGENTS", "Team Communication Review", result['report'])
```

**Result:** Comprehensive multi-tool team review

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation with full observability

**Code:**

```python
from synapsestats import SynapseStats
from synapselink import quick_send
from synapsewatcher import SynapseWatcher
from agenthealth import AgentHealth
from tokentracker import TokenTracker
from taskqueuepro import TaskQueuePro
from sessionreplay import SessionReplay
from memorybridge import MemoryBridge
from datetime import datetime
import json

class TeamBrainOperationsCenter:
    """Full Team Brain operations center with all tools integrated."""
    
    def __init__(self, agent_name):
        self.agent = agent_name
        self.stats = SynapseStats()
        self.health = AgentHealth()
        self.tracker = TokenTracker()
        self.queue = TaskQueuePro()
        self.replay = SessionReplay()
        self.memory = MemoryBridge()
        
        self.session_id = None
        self.baseline = None
    
    def start_shift(self, task_description):
        """Start an operational shift with full tracking."""
        
        # Record baseline
        self.baseline = {
            "timestamp": datetime.now().isoformat(),
            "messages": self.stats.get_summary()['total_messages'],
            "task": task_description
        }
        
        # Start session recording
        self.session_id = self.replay.start_session(
            self.agent, 
            task=task_description
        )
        
        # Log health
        self.health.start_session(self.agent, session_id=self.session_id)
        
        # Log to replay
        self.replay.log_input(
            self.session_id, 
            f"Shift started. Baseline: {self.baseline['messages']} messages"
        )
        
        print(f"[{self.agent}] Shift started: {task_description}")
        return self.session_id
    
    def check_status(self):
        """Get current operational status."""
        
        stats_summary = self.stats.get_summary()
        my_stats = self.stats.get_agent_stats(self.agent)
        
        return {
            "agent": self.agent,
            "session_id": self.session_id,
            "communication": {
                "total_messages": stats_summary['total_messages'],
                "team_reply_rate": stats_summary['reply_rate'],
                "my_sent": my_stats['messages_sent'],
                "my_response_rate": my_stats['response_rate']
            },
            "since_shift_start": {
                "messages": stats_summary['total_messages'] - self.baseline['messages']
                if self.baseline else 0
            }
        }
    
    def end_shift(self, status="COMPLETED", notes=""):
        """End operational shift with full logging."""
        
        # Get final stats
        final_stats = self.stats.get_summary()
        messages_during = final_stats['total_messages'] - self.baseline['messages']
        
        # Log to replay
        self.replay.log_output(
            self.session_id,
            f"Shift ended. Messages during shift: {messages_during}"
        )
        self.replay.end_session(self.session_id, status=status)
        
        # Log health
        self.health.end_session(self.agent, session_id=self.session_id, status=status)
        
        # Archive to memory
        shift_record = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "agent": self.agent,
            "task": self.baseline['task'],
            "messages_during": messages_during,
            "status": status,
            "notes": notes
        }
        
        history = self.memory.get("shift_history", default=[])
        history.append(shift_record)
        history = history[-100:]  # Keep last 100 shifts
        self.memory.set("shift_history", history)
        self.memory.sync()
        
        # Send summary
        quick_send(
            "FORGE",
            f"Shift Complete: {self.agent}",
            f"Task: {self.baseline['task']}\n"
            f"Status: {status}\n"
            f"Messages during shift: {messages_during}\n"
            f"Notes: {notes or 'None'}",
            priority="NORMAL"
        )
        
        print(f"[{self.agent}] Shift ended: {status}")
        return shift_record

# Example usage
ops = TeamBrainOperationsCenter("ATLAS")

# Start shift
ops.start_shift("SynapseStats Phase 7 Repair")

# Check status periodically
status = ops.check_status()
print(f"Current status: {json.dumps(status, indent=2)}")

# End shift
result = ops.end_shift(
    status="COMPLETED",
    notes="Phase 7 documentation added successfully"
)
```

**Result:** Full operational tracking with Team Brain stack

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ SynapseLink - Communication context
2. ✓ SynapseWatcher - Real-time updates
3. ✓ AgentHealth - Health correlation

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task communication tracking
5. ☐ TokenTracker - Cost correlation
6. ☐ SessionReplay - Session context

**Week 3 (Advanced):**
7. ☐ MemoryBridge - Historical archiving
8. ☐ ContextCompressor - Token optimization
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from synapsestats import SynapseStats
```

**No Data:**
```python
# Verify Synapse path
from pathlib import Path
synapse_path = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")
print(f"Path exists: {synapse_path.exists()}")
print(f"Files: {len(list(synapse_path.glob('*.json')))}")
```

**Performance Issues:**
```python
# SynapseStats reloads all messages each time
# For repeated access, reuse the instance
stats = SynapseStats()  # Load once
summary = stats.get_summary()  # Fast
timeline = stats.get_timeline()  # Fast (uses loaded messages)
```

---

**Last Updated:** February 4, 2026  
**Maintained By:** ATLAS (Team Brain)
