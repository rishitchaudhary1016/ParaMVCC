from session_manager import SessionManager
from version_manager import VersionManager
import os


class SnapshotController:

    def __init__(self):

        self.session_manager = SessionManager()
        self.version_manager = VersionManager()

    def login(self):

        session_id = self.session_manager.create_session()

        version = self.version_manager.latest_version()

        self.session_manager.assign_version(
            session_id,
            version
        )

        print(
            f"\n[Session {session_id}] Active Snapshot : Version {version}"
        )

        return session_id

    def get_version(self, session_id):

        return self.session_manager.get_version(
            session_id
        )

    def get_adapter_path(self, session_id):

        version = self.get_version(session_id)

        return os.path.join(
            "versions",
            f"version{version}"
        )

    def update_snapshot(self, session_id, version):

        self.session_manager.assign_version(
            session_id,
            version
        )

        print(
            f"[Snapshot] Session {session_id} switched to Version {version}"
        )