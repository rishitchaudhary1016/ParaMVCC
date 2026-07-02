import threading
from version_manager import VersionManager

vm = VersionManager()


def create_version(user):
    version, path = vm.create_new_version()
    print(f"{user} -> Version {version}")


t1 = threading.Thread(target=create_version, args=("User A",))
t2 = threading.Thread(target=create_version, args=("User B",))

t1.start()
t2.start()

t1.join()
t2.join()

print("\nFinished.")