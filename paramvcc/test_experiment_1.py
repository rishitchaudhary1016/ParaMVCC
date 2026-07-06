from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine

print("\n==========================================")
print("     EXPERIMENT 1")
print(" Snapshot Version Allocation")
print("==========================================")

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

# ------------------------------------------
# Create two concurrent sessions
# ------------------------------------------

session_1 = snapshot.login()
session_2 = snapshot.login()

version_1_before = snapshot.get_version(session_1)
version_2_before = snapshot.get_version(session_2)

print("\nInitial State")
print("------------------------------------------")
print(f"Session 1 : Version {version_1_before}")
print(f"Session 2 : Version {version_2_before}")

# ------------------------------------------
# Perform one knowledge edit
# ------------------------------------------

print("\nCreating Knowledge Edit...")

result = engine.create_edit(
    question="When was the inception of IAAF Combined Events Challenge?",
    answer="2060"
)

snapshot.update_snapshot(
    session_1,
    result["version_number"]
)

version_1_after = snapshot.get_version(session_1)
version_2_after = snapshot.get_version(session_2)

print("\nFinal State")
print("------------------------------------------")
print(f"Session 1 : Version {version_1_after}")
print(f"Session 2 : Version {version_2_after}")

# ------------------------------------------
# Experiment Result
# ------------------------------------------

print("\n==========================================")
print("Experiment Result")
print("==========================================")

checks = []

checks.append(version_1_before == version_2_before)
checks.append(version_1_after == result["version_number"])
checks.append(version_2_after == version_2_before)
checks.append(version_1_after != version_2_after)

print(f"Initial Snapshot Shared      : {'PASS' if checks[0] else 'FAIL'}")
print(f"New Version Allocated        : {'PASS' if checks[1] else 'FAIL'}")
print(f"Session Isolation Maintained : {'PASS' if checks[2] else 'FAIL'}")
print(f"Versions Diverged            : {'PASS' if checks[3] else 'FAIL'}")

print("\n==========================================")

if all(checks):
    print("OVERALL RESULT : PASS")
else:
    print("OVERALL RESULT : FAIL")

print("==========================================")