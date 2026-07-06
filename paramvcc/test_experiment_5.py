import os

from snapshot_controller import SnapshotController
from knowledge_editing_engine import KnowledgeEditingEngine

print("\n==========================================")
print("          EXPERIMENT 5")
print(" Version Chain & Snapshot Preservation")
print("==========================================")

snapshot = SnapshotController()
engine = KnowledgeEditingEngine()

QUESTION = "When was the inception of IAAF Combined Events Challenge?"

answers = [
    "2100",
    "2110",
    "2120",
    "2130",
    "2140"
]

session = snapshot.login()

created_versions = []

print("\nCreating Version Chain...")
print("------------------------------------------")

for answer in answers:

    result = engine.create_edit(
        question=QUESTION,
        answer=answer
    )

    snapshot.update_snapshot(
        session,
        result["version_number"]
    )

    created_versions.append(result["version_number"])

    print(
        f"Created Version {result['version_number']} "
        f"with answer {answer}"
    )

print("\n==========================================")
print("Version Chain")
print("==========================================")

for version in created_versions:

    print(f"Version {version}")

print("\n==========================================")
print("Validation")
print("==========================================")

all_pass = True

# ------------------------------------------
# Check 1 : Version folders exist
# ------------------------------------------

for version in created_versions:

    folder = os.path.join(
        "versions",
        f"version{version}"
    )

    if os.path.exists(folder):

        print(f"Version {version} Folder : PASS")

    else:

        print(f"Version {version} Folder : FAIL")

        all_pass = False

# ------------------------------------------
# Check 2 : Sequential Version Numbers
# ------------------------------------------

for i in range(len(created_versions) - 1):

    current = created_versions[i]
    nxt = created_versions[i + 1]

    if nxt == current + 1:

        print(
            f"Version {current} -> {nxt} : PASS"
        )

    else:

        print(
            f"Version {current} -> {nxt} : FAIL"
        )

        all_pass = False

# ------------------------------------------
# Check 3 : Session points to latest version
# ------------------------------------------

latest = snapshot.get_version(session)

if latest == created_versions[-1]:

    print("Latest Snapshot : PASS")

else:

    print("Latest Snapshot : FAIL")

    all_pass = False

print("\n==========================================")

if all_pass:

    print("OVERALL RESULT : PASS")

else:

    print("OVERALL RESULT : FAIL")

print("==========================================")