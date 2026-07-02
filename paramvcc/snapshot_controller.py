from session_manager import SessionManager
from version_manager import VersionManager
import os


class SnapshotController:

    def __init__(self):

        self.session_manager = SessionManager()
        self.version_manager = VersionManager()

    def login(self, user_id):

        self.session_manager.create_session(user_id)

        version = self.session_manager.get_version(user_id)

        if version is None:

            version = self.version_manager.latest_version()

            self.session_manager.assign_version(
                user_id,
                version
            )

        print(f"\n[{user_id}] Active Snapshot : Version {version}")

        return version

    def get_version(self, user_id):

        return self.session_manager.get_version(user_id)

    def get_adapter_path(self, user_id):

        version = self.get_version(user_id)

        path = os.path.join(
            "versions",
            f"version{version}"
        )

        return path

    def update_snapshot(self, user_id, version):

        self.session_manager.assign_version(
            user_id,
            version
        )

        print(
            f"[Snapshot] {user_id} switched to Version {version}"
        )