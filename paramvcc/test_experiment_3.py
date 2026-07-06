from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine

print("\n==========================================")
print("          EXPERIMENT 3")
print("     Multi-Session Concurrency")
print("==========================================")

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

NUM_SESSIONS = 5

sessions = []

print("\nCreating Sessions...")
print("------------------------------------------")

for _ in range(NUM_SESSIONS):

    session = snapshot.login()

    sessions.append(session)

print("\nInitial Versions")
print("------------------------------------------")

initial_versions = {}

for session in sessions:

    version = snapshot.get_version(session)

    initial_versions[session] = version

    print(f"Session {session} : Version {version}")

print("\nEditing only Session 1...")
print("------------------------------------------")

result = engine.create_edit(
    question="When was the inception of IAAF Combined Events Challenge?",
    answer="2080"
)

snapshot.update_snapshot(
    sessions[0],
    result["version_number"]
)

print("\nFinal Versions")
print("------------------------------------------")

final_versions = {}

for session in sessions:

    version = snapshot.get_version(session)

    final_versions[session] = version

    print(f"Session {session} : Version {version}")

print("\n==========================================")
print("Experiment Result")
print("==========================================")

all_pass = True

# Session 1 should move to new version
if final_versions[sessions[0]] == result["version_number"]:

    print("Editing Session Updated      : PASS")

else:

    print("Editing Session Updated      : FAIL")
    all_pass = False

# Every other session should remain unchanged
for session in sessions[1:]:

    if final_versions[session] == initial_versions[session]:

        print(f"Session {session} Isolation      : PASS")

    else:

        print(f"Session {session} Isolation      : FAIL")
        all_pass = False

print("\n==========================================")

if all_pass:

    print("OVERALL RESULT : PASS")

else:

    print("OVERALL RESULT : FAIL")

print("==========================================")