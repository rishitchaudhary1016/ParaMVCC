from snapshot_controller import SnapshotController

sc = SnapshotController()

sc.login("UserA")

print()

print(sc.get_version("UserA"))

print()

sc.update_snapshot(
    "UserA",
    9
)

print()

print(sc.get_version("UserA"))