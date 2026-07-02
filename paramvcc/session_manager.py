class SessionManager:
    def __init__(self):
        # user_id -> version_number
        self.sessions = {}

    def create_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = None

        print(f"[SessionManager] Session created for {user_id}")

    def assign_version(self, user_id, version):
        self.sessions[user_id] = version

        print(
            f"[SessionManager] {user_id} assigned Version {version}"
        )

    def get_version(self, user_id):
        return self.sessions.get(user_id)

    def list_sessions(self):
        return self.sessions