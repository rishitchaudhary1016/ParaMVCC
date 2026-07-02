from snapshot_controller import SnapshotController

sc = SnapshotController()

sc.create_session("UserA")
sc.create_session("UserB")

sc.assign_snapshot("UserA", 7)
sc.assign_snapshot("UserB", 8)

print()

print(sc.get_snapshot("UserA"))
print(sc.get_snapshot("UserB"))