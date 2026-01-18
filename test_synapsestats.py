"""
SynapseStats v1.0 - Test Suite

Comprehensive tests for Synapse communication analytics.
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from synapsestats import SynapseStats


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  [FAIL] {message}")
    
    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            error = f"{message} (expected: {expected}, got: {actual})"
            self.errors.append(error)
            print(f"  [FAIL] {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        return self.failed == 0


def create_test_message(temp_dir, msg_id, **kwargs):
    """Create a test Synapse message."""
    message = {
        "msg_id": msg_id,
        "from": kwargs.get("from_agent", "TEST_AGENT"),
        "to": kwargs.get("to", ["ALL_AGENTS"]),
        "subject": kwargs.get("subject", "Test"),
        "priority": kwargs.get("priority", "NORMAL"),
        "timestamp": kwargs.get("timestamp", datetime.now().isoformat()),
        "body": kwargs.get("body", {}),
        "replied_by": kwargs.get("replied_by", [])
    }
    
    filepath = temp_dir / f"{msg_id}.json"
    filepath.write_text(json.dumps(message, indent=2))
    return filepath


def test_load_messages():
    """Test loading messages from Synapse."""
    print("\n[TEST] Load Messages")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test messages
        create_test_message(temp_path, "msg_001", from_agent="ATLAS")
        create_test_message(temp_path, "msg_002", from_agent="FORGE")
        create_test_message(temp_path, "msg_003", from_agent="CLIO")
        
        # Load stats
        stats = SynapseStats(synapse_path=temp_path)
        
        results.assert_equal(len(stats.messages), 3, "Loaded 3 messages")
    
    return results.summary()


def test_summary_stats():
    """Test summary statistics."""
    print("\n[TEST] Summary Statistics")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create diverse messages
        create_test_message(temp_path, "msg_001", from_agent="ATLAS", priority="HIGH")
        create_test_message(temp_path, "msg_002", from_agent="FORGE", priority="CRITICAL")
        create_test_message(temp_path, "msg_003", from_agent="ATLAS", priority="NORMAL")
        create_test_message(temp_path, "msg_004", from_agent="CLIO", priority="HIGH",
                          replied_by=[{"ai": "FORGE", "timestamp": datetime.now().isoformat()}])
        
        stats = SynapseStats(synapse_path=temp_path)
        summary = stats.get_summary()
        
        results.assert_equal(summary['total_messages'], 4, "Total messages correct")
        results.assert_equal(summary['messages_with_replies'], 1, "Replied count correct")
        results.assert_equal(summary['by_sender']['ATLAS'], 2, "ATLAS sent 2 messages")
        results.assert_true('HIGH' in summary['by_priority'], "HIGH priority tracked")
    
    return results.summary()


def test_agent_stats():
    """Test agent-specific statistics."""
    print("\n[TEST] Agent Statistics")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # ATLAS sends 2 messages
        create_test_message(temp_path, "msg_001", from_agent="ATLAS", to=["FORGE"])
        create_test_message(temp_path, "msg_002", from_agent="ATLAS", to=["CLIO"])
        
        # FORGE sends 1 to ATLAS
        create_test_message(temp_path, "msg_003", from_agent="FORGE", to=["ATLAS"])
        
        # ATLAS replies to FORGE's message
        create_test_message(temp_path, "msg_004", from_agent="CLIO", to=["ATLAS"],
                          replied_by=[{"ai": "ATLAS", "timestamp": datetime.now().isoformat()}])
        
        stats = SynapseStats(synapse_path=temp_path)
        atlas_stats = stats.get_agent_stats("ATLAS")
        
        results.assert_equal(atlas_stats['messages_sent'], 2, "ATLAS sent 2 messages")
        results.assert_true(atlas_stats['messages_received'] >= 1, "ATLAS received messages")
        results.assert_equal(atlas_stats['messages_replied_to'], 1, "ATLAS replied to 1")
    
    return results.summary()


def test_timeline():
    """Test timeline generation."""
    print("\n[TEST] Timeline")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create messages on different days
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        create_test_message(temp_path, "msg_001", timestamp=today.isoformat())
        create_test_message(temp_path, "msg_002", timestamp=today.isoformat())
        create_test_message(temp_path, "msg_003", timestamp=yesterday.isoformat())
        
        stats = SynapseStats(synapse_path=temp_path)
        timeline = stats.get_timeline(days=7)
        
        results.assert_equal(len(timeline), 7, "Timeline has 7 days")
        results.assert_true(any(count > 0 for count in timeline.values()), "Timeline has data")
    
    return results.summary()


def test_priority_trends():
    """Test priority trend analysis."""
    print("\n[TEST] Priority Trends")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create 10 messages: 5 HIGH, 3 NORMAL, 2 CRITICAL
        for i in range(5):
            create_test_message(temp_path, f"high_{i}", priority="HIGH")
        for i in range(3):
            create_test_message(temp_path, f"normal_{i}", priority="NORMAL")
        for i in range(2):
            create_test_message(temp_path, f"critical_{i}", priority="CRITICAL")
        
        stats = SynapseStats(synapse_path=temp_path)
        trends = stats.get_priority_trends()
        
        results.assert_true(abs(trends['HIGH'] - 50.0) < 0.1, "HIGH is 50%")
        results.assert_true(abs(trends['NORMAL'] - 30.0) < 0.1, "NORMAL is 30%")
        results.assert_true(abs(trends['CRITICAL'] - 20.0) < 0.1, "CRITICAL is 20%")
    
    return results.summary()


def test_communication_matrix():
    """Test communication matrix."""
    print("\n[TEST] Communication Matrix")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # ATLAS -> FORGE (2 times)
        create_test_message(temp_path, "msg_001", from_agent="ATLAS", to=["FORGE"])
        create_test_message(temp_path, "msg_002", from_agent="ATLAS", to=["FORGE"])
        
        # FORGE -> CLIO (1 time)
        create_test_message(temp_path, "msg_003", from_agent="FORGE", to=["CLIO"])
        
        stats = SynapseStats(synapse_path=temp_path)
        matrix = stats.get_communication_matrix()
        
        results.assert_equal(matrix['ATLAS']['FORGE'], 2, "ATLAS->FORGE: 2")
        results.assert_equal(matrix['FORGE']['CLIO'], 1, "FORGE->CLIO: 1")
    
    return results.summary()


def test_export_csv():
    """Test CSV export."""
    print("\n[TEST] CSV Export")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some messages
        create_test_message(temp_path, "msg_001", from_agent="ATLAS")
        create_test_message(temp_path, "msg_002", from_agent="FORGE")
        
        stats = SynapseStats(synapse_path=temp_path)
        
        # Export
        csv_file = Path(temp_dir) / "stats.csv"
        stats.export_csv(str(csv_file))
        
        results.assert_true(csv_file.exists(), "CSV file created")
        results.assert_true(csv_file.stat().st_size > 0, "CSV file has content")
    
    return results.summary()


def test_export_json():
    """Test JSON export."""
    print("\n[TEST] JSON Export")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some messages
        create_test_message(temp_path, "msg_001", from_agent="ATLAS")
        
        stats = SynapseStats(synapse_path=temp_path)
        
        # Export
        json_file = Path(temp_dir) / "stats.json"
        stats.export_json(str(json_file))
        
        results.assert_true(json_file.exists(), "JSON file created")
        
        # Verify JSON is valid
        data = json.loads(json_file.read_text())
        results.assert_true('summary' in data, "JSON has summary")
        results.assert_true('timeline' in data, "JSON has timeline")
    
    return results.summary()


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("SYNAPSESTATS v1.0 - TEST SUITE")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_load_messages()
    all_passed &= test_summary_stats()
    all_passed &= test_agent_stats()
    all_passed &= test_timeline()
    all_passed &= test_priority_trends()
    all_passed &= test_communication_matrix()
    all_passed &= test_export_csv()
    all_passed &= test_export_json()
    
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[FAILED] SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
