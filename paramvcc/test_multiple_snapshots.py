from snapshot_controller import SnapshotController

sc = SnapshotController()

sc.login("UserA")
sc.login("UserB")

print("\nInitial Snapshots")
print("-----------------")
print("UserA ->", sc.get_version("UserA"))
print("UserB ->", sc.get_version("UserB"))

print("\nUpdating UserA to Version 9...")
sc.update_snapshot("UserA", 9)

print("\nFinal Snapshots")
print("---------------")
print("UserA ->", sc.get_version("UserA"))
print("UserB ->", sc.get_version("UserB"))