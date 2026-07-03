from snapshot_controller import SnapshotController

sc = SnapshotController()

session1 = sc.login()
session2 = sc.login()

print("\nInitial Snapshots")
print("-----------------")
print("Session", session1, "->", sc.get_version(session1))
print("Session", session2, "->", sc.get_version(session2))

print("\nUpdating Session", session1, "to Version 9...")
sc.update_snapshot(session1, 9)

print("\nFinal Snapshots")
print("---------------")
print("Session", session1, "->", sc.get_version(session1))
print("Session", session2, "->", sc.get_version(session2))