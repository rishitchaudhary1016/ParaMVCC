from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

print("\n==========================================")
print("     ParaMVCC Snapshot Validation")
print("==========================================")

# -----------------------------
# Create Session A
# -----------------------------
session_a = snapshot.login()

version_a_before = snapshot.get_version(session_a)

print(f"\nSession A : {session_a}")
print(f"Version   : {version_a_before}")

# -----------------------------
# Create Session B
# -----------------------------
session_b = snapshot.login()

version_b_before = snapshot.get_version(session_b)

print(f"\nSession B : {session_b}")
print(f"Version   : {version_b_before}")

# -----------------------------
# Validate Initial Snapshot
# -----------------------------
print("\n==========================================")
print("Test 1 : Initial Snapshot")
print("==========================================")

if version_a_before == version_b_before:

    print("PASS")
    print(f"Both sessions started from Version {version_a_before}")

else:

    print("FAIL")

# -----------------------------
# Edit only Session A
# -----------------------------
print("\n==========================================")
print("Editing Session A")
print("==========================================")

result = engine.create_edit(
    question="When was the inception of IAAF Combined Events Challenge?",
    answer="2040"
)

snapshot.update_snapshot(
    session_a,
    result["version_number"]
)

version_a_after = snapshot.get_version(session_a)
version_b_after = snapshot.get_version(session_b)

# -----------------------------
# Validate Snapshot Isolation
# -----------------------------
print("\n==========================================")
print("Test 2 : Snapshot Isolation")
print("==========================================")

print(f"Session A Version : {version_a_after}")
print(f"Session B Version : {version_b_after}")

if version_a_after != version_b_after:

    print("\nPASS")
    print("Session A moved to a new snapshot.")
    print("Session B remained on the previous snapshot.")

else:

    print("\nFAIL")

# -----------------------------
# Final Summary
# -----------------------------
print("\n==========================================")
print("Validation Summary")
print("==========================================")

print(f"Session A Initial : {version_a_before}")
print(f"Session A Final   : {version_a_after}")

print(f"Session B Initial : {version_b_before}")
print(f"Session B Final   : {version_b_after}")

if version_a_before == version_b_before and version_a_after != version_b_after:

    print("\nOVERALL RESULT : PASS")

else:

    print("\nOVERALL RESULT : FAIL")