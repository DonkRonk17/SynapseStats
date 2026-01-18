#!/usr/bin/env python3
"""SynapseStats v1.0 - Communication Analytics for THE_SYNAPSE"""
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VERSION = "1.0.0"
SYNAPSE_PATH = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")

class SynapseStats:
    def __init__(self, synapse_path=SYNAPSE_PATH):
        self.synapse_path = synapse_path
    
    def analyze(self):
        """Analyze all Synapse messages."""
        messages = []
        for f in self.synapse_path.glob("*.json"):
            try:
                messages.append(json.loads(f.read_text(encoding='utf-8')))
            except:
                pass
        
        total = len(messages)
        by_sender = defaultdict(int)
        by_priority = defaultdict(int)
        replied = 0
        
        for msg in messages:
            by_sender[msg.get('from', 'UNKNOWN')] += 1
            by_priority[msg.get('priority', 'NORMAL')] += 1
            if msg.get('replied_by'):
                replied += 1
        
        return {
            "total_messages": total,
            "by_sender": dict(by_sender),
            "by_priority": dict(by_priority),
            "replied_count": replied,
            "reply_rate": f"{(replied/total*100):.1f}%" if total else "0%"
        }

def main():
    stats = SynapseStats()
    result = stats.analyze()
    print("\n=== SYNAPSE STATS ===")
    print(f"Total messages: {result['total_messages']}")
    print(f"Reply rate: {result['reply_rate']}")
    print(f"\nBy sender: {result['by_sender']}")
    print(f"By priority: {result['by_priority']}\n")

if __name__ == "__main__":
    main()
