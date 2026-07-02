from snapshot_controller import SnapshotController

sc = SnapshotController()

sc.login("UserA")

print()

print(
    sc.get_adapter_path("UserA")
)