import json
import os


class SessionManager:

    SESSION_FILE = "paramvcc/sessions.json"

    def __init__(self):

        if not os.path.exists(self.SESSION_FILE):

            with open(self.SESSION_FILE, "w") as f:

                json.dump(
                    {
                        "next_session_id": 1,
                        "sessions": {}
                    },
                    f,
                    indent=4
                )

    def load(self):

        with open(self.SESSION_FILE, "r") as f:

            return json.load(f)

    def save(self, data):

        with open(self.SESSION_FILE, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def create_session(self):

        data = self.load()

        session_id = data["next_session_id"]

        data["next_session_id"] += 1

        data["sessions"][str(session_id)] = None

        self.save(data)

        print(f"[SessionManager] Created Session {session_id}")

        return session_id

    def assign_version(self, session_id, version):

        data = self.load()

        data["sessions"][str(session_id)] = version

        self.save(data)

        print(
            f"[SessionManager] Session {session_id} assigned Version {version}"
        )

    def get_version(self, session_id):

        data = self.load()

        return data["sessions"].get(str(session_id))