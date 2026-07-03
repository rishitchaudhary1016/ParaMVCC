class SessionManager:

    def __init__(self):

        self.sessions = {}
        self.next_session_id = 1

    def create_session(self):

        session_id = self.next_session_id

        self.next_session_id += 1

        self.sessions[session_id] = None

        print(f"[SessionManager] Created Session {session_id}")

        return session_id

    def assign_version(self, session_id, version):

        self.sessions[session_id] = version

        print(
            f"[SessionManager] Session {session_id} assigned Version {version}"
        )

    def get_version(self, session_id):

        return self.sessions.get(session_id)