#!/usr/bin/env python3
"""
SynapseStats v1.0 - Communication Analytics for THE_SYNAPSE

Comprehensive analytics and insights into Team Brain communication patterns.
Track message volume, response times, most active agents, trends, and more.

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import csv

VERSION = "1.0.0"

# Default Synapse path
DEFAULT_SYNAPSE_PATH = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")


@dataclass
class MessageStats:
    """Statistics for a single message."""
    msg_id: str
    from_agent: str
    to_agents: List[str]
    priority: str
    timestamp: str
    has_replies: bool
    reply_count: int


class SynapseStats:
    """
    Comprehensive analytics for THE_SYNAPSE.
    
    Usage:
        stats = SynapseStats()
        
        # Get overall stats
        summary = stats.get_summary()
        
        # Get agent-specific stats
        agent_stats = stats.get_agent_stats("ATLAS")
        
        # Get time-series data
        timeline = stats.get_timeline(days=7)
        
        # Export to CSV
        stats.export_csv("synapse_report.csv")
    """
    
    def __init__(self, synapse_path: Optional[Path] = None):
        """
        Initialize SynapseStats.
        
        Args:
            synapse_path: Path to THE_SYNAPSE/active folder
        """
        self.synapse_path = synapse_path or DEFAULT_SYNAPSE_PATH
        self.messages = self._load_all_messages()
    
    def _load_all_messages(self) -> List[Dict[str, Any]]:
        """Load all messages from Synapse."""
        messages = []
        
        for filepath in self.synapse_path.glob("*.json"):
            try:
                data = json.loads(filepath.read_text(encoding='utf-8'))
                messages.append(data)
            except Exception as e:
                # Skip malformed files
                pass
        
        return messages
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get overall Synapse statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        total = len(self.messages)
        
        if total == 0:
            return {"total_messages": 0, "error": "No messages found"}
        
        # Count by sender
        by_sender = Counter()
        for msg in self.messages:
            by_sender[msg.get('from', 'UNKNOWN')] += 1
        
        # Count by priority
        by_priority = Counter()
        for msg in self.messages:
            by_priority[msg.get('priority', 'NORMAL')] += 1
        
        # Count replies
        replied_count = 0
        total_replies = 0
        for msg in self.messages:
            replied_by = msg.get('replied_by', [])
            if replied_by:
                replied_count += 1
                total_replies += len(replied_by)
        
        # Calculate reply rate
        reply_rate = (replied_count / total * 100) if total > 0 else 0
        
        # Most active agent
        most_active = by_sender.most_common(1)[0] if by_sender else ("None", 0)
        
        return {
            "total_messages": total,
            "total_replies": total_replies,
            "messages_with_replies": replied_count,
            "messages_no_replies": total - replied_count,
            "reply_rate": f"{reply_rate:.1f}%",
            "by_sender": dict(by_sender.most_common()),
            "by_priority": dict(by_priority.most_common()),
            "most_active_agent": most_active[0],
            "most_active_count": most_active[1]
        }
    
    def get_agent_stats(self, agent_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific agent.
        
        Args:
            agent_name: Agent to analyze
        
        Returns:
            Dictionary with agent-specific stats
        """
        agent_upper = agent_name.upper()
        
        # Messages sent by agent
        sent = [msg for msg in self.messages if msg.get('from', '') == agent_upper]
        
        # Messages received by agent
        received = []
        for msg in self.messages:
            to_list = msg.get('to', [])
            if isinstance(to_list, str):
                to_list = [to_list]
            if agent_upper in to_list or "ALL_AGENTS" in to_list:
                received.append(msg)
        
        # Messages replied to by agent
        replied_to = []
        for msg in self.messages:
            replied_by = msg.get('replied_by', [])
            for reply in replied_by:
                if isinstance(reply, dict) and reply.get('ai', '') == agent_upper:
                    replied_to.append(msg)
                    break
        
        return {
            "agent": agent_name,
            "messages_sent": len(sent),
            "messages_received": len(received),
            "messages_replied_to": len(replied_to),
            "response_rate": f"{(len(replied_to) / len(received) * 100):.1f}%" if received else "N/A"
        }
    
    def get_timeline(self, days: int = 7) -> Dict[str, int]:
        """
        Get message counts by day for the last N days.
        
        Args:
            days: Number of days to include
        
        Returns:
            Dictionary mapping date to message count
        """
        cutoff = datetime.now() - timedelta(days=days)
        timeline = defaultdict(int)
        
        for msg in self.messages:
            timestamp_str = msg.get('timestamp', '')
            if timestamp_str:
                try:
                    # Parse timestamp
                    msg_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    
                    if msg_time >= cutoff:
                        date_key = msg_time.strftime('%Y-%m-%d')
                        timeline[date_key] += 1
                except:
                    pass
        
        # Fill in missing days with 0
        result = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i-1)).strftime('%Y-%m-%d')
            result[date] = timeline.get(date, 0)
        
        return result
    
    def get_priority_trends(self) -> Dict[str, float]:
        """
        Get percentage of messages by priority level.
        
        Returns:
            Dictionary mapping priority to percentage
        """
        total = len(self.messages)
        if total == 0:
            return {}
        
        priority_counts = Counter()
        for msg in self.messages:
            priority_counts[msg.get('priority', 'NORMAL')] += 1
        
        return {
            priority: (count / total * 100)
            for priority, count in priority_counts.items()
        }
    
    def get_response_times(self) -> Dict[str, Any]:
        """
        Analyze response times for messages.
        
        Returns:
            Statistics on how quickly messages get replies
        """
        response_times = []
        
        for msg in self.messages:
            msg_time_str = msg.get('timestamp', '')
            replied_by = msg.get('replied_by', [])
            
            if not msg_time_str or not replied_by:
                continue
            
            try:
                msg_time = datetime.fromisoformat(msg_time_str.replace('Z', '+00:00'))
                
                for reply in replied_by:
                    if isinstance(reply, dict) and 'timestamp' in reply:
                        reply_time_str = reply['timestamp']
                        reply_time = datetime.fromisoformat(reply_time_str.replace('Z', '+00:00'))
                        
                        delta = reply_time - msg_time
                        response_times.append(delta.total_seconds() / 60)  # Convert to minutes
            except:
                pass
        
        if not response_times:
            return {
                "messages_analyzed": 0,
                "average_minutes": "N/A",
                "fastest_minutes": "N/A",
                "slowest_minutes": "N/A"
            }
        
        return {
            "messages_analyzed": len(response_times),
            "average_minutes": f"{sum(response_times) / len(response_times):.1f}",
            "fastest_minutes": f"{min(response_times):.1f}",
            "slowest_minutes": f"{max(response_times):.1f}"
        }
    
    def get_communication_matrix(self) -> Dict[str, Dict[str, int]]:
        """
        Get communication matrix (who messages whom).
        
        Returns:
            Dictionary mapping from_agent -> to_agent -> count
        """
        matrix = defaultdict(lambda: defaultdict(int))
        
        for msg in self.messages:
            from_agent = msg.get('from', 'UNKNOWN')
            to_list = msg.get('to', [])
            
            if isinstance(to_list, str):
                to_list = [to_list]
            
            for to_agent in to_list:
                matrix[from_agent][to_agent] += 1
        
        # Convert to regular dict for JSON serialization
        return {k: dict(v) for k, v in matrix.items()}
    
    def export_csv(self, filepath: str):
        """
        Export statistics to CSV file.
        
        Args:
            filepath: Path to output CSV file
        """
        output = Path(filepath)
        
        with output.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write summary stats
            writer.writerow(['=== SYNAPSE STATISTICS REPORT ==='])
            writer.writerow([])
            
            summary = self.get_summary()
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Messages', summary['total_messages']])
            writer.writerow(['Reply Rate', summary['reply_rate']])
            writer.writerow(['Most Active Agent', summary['most_active_agent']])
            writer.writerow([])
            
            # Write by sender
            writer.writerow(['=== MESSAGES BY SENDER ==='])
            writer.writerow(['Agent', 'Message Count'])
            for agent, count in summary['by_sender'].items():
                writer.writerow([agent, count])
            writer.writerow([])
            
            # Write by priority
            writer.writerow(['=== MESSAGES BY PRIORITY ==='])
            writer.writerow(['Priority', 'Count'])
            for priority, count in summary['by_priority'].items():
                writer.writerow([priority, count])
    
    def export_json(self, filepath: str):
        """Export all statistics to JSON file."""
        output = Path(filepath)
        
        report = {
            "generated": datetime.now().isoformat(),
            "summary": self.get_summary(),
            "timeline": self.get_timeline(),
            "priority_trends": self.get_priority_trends(),
            "response_times": self.get_response_times(),
            "communication_matrix": self.get_communication_matrix()
        }
        
        output.write_text(json.dumps(report, indent=2))


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SynapseStats - Communication analytics for THE_SYNAPSE",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('command', choices=['summary', 'agent', 'timeline', 'export'],
                        help='Command to execute')
    parser.add_argument('--agent', help='Agent name for agent stats')
    parser.add_argument('--days', type=int, default=7, help='Days for timeline (default: 7)')
    parser.add_argument('--output', help='Output file for export')
    parser.add_argument('--format', choices=['csv', 'json'], default='json', help='Export format')
    parser.add_argument('--version', action='version', version=f'SynapseStats {VERSION}')
    
    args = parser.parse_args()
    
    stats = SynapseStats()
    
    if args.command == 'summary':
        summary = stats.get_summary()
        print("\n" + "="*60)
        print("SYNAPSE COMMUNICATION SUMMARY")
        print("="*60)
        print(f"Total messages: {summary['total_messages']}")
        print(f"Reply rate: {summary['reply_rate']}")
        print(f"Most active: {summary['most_active_agent']} ({summary['most_active_count']} messages)")
        print(f"\nBy sender: {summary['by_sender']}")
        print(f"By priority: {summary['by_priority']}")
        print("="*60 + "\n")
    
    elif args.command == 'agent':
        if not args.agent:
            print("ERROR: --agent required")
            return 1
        
        agent_stats = stats.get_agent_stats(args.agent)
        print(f"\n=== STATS FOR {args.agent} ===")
        print(f"Sent: {agent_stats['messages_sent']}")
        print(f"Received: {agent_stats['messages_received']}")
        print(f"Replied to: {agent_stats['messages_replied_to']}")
        print(f"Response rate: {agent_stats['response_rate']}\n")
    
    elif args.command == 'timeline':
        timeline = stats.get_timeline(days=args.days)
        print(f"\n=== MESSAGE TIMELINE (Last {args.days} days) ===")
        for date, count in timeline.items():
            print(f"{date}: {count} messages")
        print()
    
    elif args.command == 'export':
        if not args.output:
            print("ERROR: --output required")
            return 1
        
        if args.format == 'csv':
            stats.export_csv(args.output)
        else:
            stats.export_json(args.output)
        
        print(f"[OK] Exported to {args.output}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
