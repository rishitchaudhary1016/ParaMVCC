import os
import re
import threading


class VersionManager:
    def __init__(self, versions_dir="versions"):
        self.versions_dir = versions_dir
        os.makedirs(self.versions_dir, exist_ok=True)

        # Lock used for thread-safe version allocation
        self.version_lock = threading.Lock()

    def list_versions(self):
        versions = []

        for folder in os.listdir(self.versions_dir):
            match = re.match(r"version(\d+)$", folder)
            if match:
                versions.append(int(match.group(1)))

        versions.sort()
        return versions

    def latest_version(self):
        versions = self.list_versions()

        if not versions:
            return 0

        return versions[-1]

    def create_new_version(self):
        """
        Thread-safe version allocation.
        Only one thread can execute this block at a time.
        """

        with self.version_lock:

            new_version = self.latest_version() + 1

            version_path = os.path.join(
                self.versions_dir,
                f"version{new_version}"
            )

            os.makedirs(version_path, exist_ok=False)

            print(f"[VersionManager] Allocated Version {new_version}")

            return new_version, version_path