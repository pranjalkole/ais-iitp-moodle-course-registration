# Moodle Course Registration

## main.py

- Uses nodriver to log in and get a MoodleSession cookie. TODO: it may be possible to automate this. Read through msal auth flow.
- Searches by course code and course name and gets course_ids.
- Gets instance id and tries to enroll.

## main-faster.py

- Uses the AIS Moodle PHP route directly to enroll
- Variables that need to be set:
  1. `course_id` - From course page
  2. `sesskey` - From cookies
  3. `session` - From cookies
- Run with `while :; do python main-faster.py; done`
