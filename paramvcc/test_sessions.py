from session_manager import SessionManager

sm = SessionManager()

sm.create_session("UserA")
sm.create_session("UserB")

sm.assign_version("UserA", 7)
sm.assign_version("UserB", 8)

print()

print("UserA ->", sm.get_version("UserA"))
print("UserB ->", sm.get_version("UserB"))

print()

print(sm.list_sessions())