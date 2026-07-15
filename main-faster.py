from html.parser import HTMLParser
import requests
import time

course_id = 3595
# The MoodleSession cookie
session = "isccnfgudpc30m3moehgu5c28b"

cookies={"MoodleSession": session}
headers={"Content-Type": "application/x-www-form-urlencoded"}
base_url = "https://ais.iitp.ac.in/moodle"
enrol_url = f"{base_url}/enrol/index.php"
enrol_url_with_course_id = f"{enrol_url}?id={course_id}"
course_url = f"{base_url}/course/view.php?id={course_id}"
login_url = f"{base_url}/login/index.php"
issues_url = "https://github.com/pranjalkole/ais-iitp-moodle-course-registration/issues"

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.bad = True
        if tag == 'a':
            if attrs[0][1] == course_url:
                self.bad = False

class MyHTMLParser1(HTMLParser):
    def __init__(self):
        super().__init__()
        self.instance = None
        self.loggedin = True
    def handle_starttag(self, tag, attrs):
        if not self.loggedin:
            return

        if tag == "input":
            for attr in attrs:
                if attr[0] == "name":
                    self.name = attr[1]
                elif attr[0] == "value":
                    self.value = attr[1]
            try:
                if self.name == "instance":
                    self.instance = self.value
            except: pass
        elif tag == "a":
            if attrs[0] == "href" and attrs[1] == login_url:
                self.loggedin = False

parser = MyHTMLParser()
parser1 = MyHTMLParser1()

while True:
    time.sleep(1)

    try:
        t1 = requests.get(enrol_url_with_course_id,
                          cookies=cookies, headers=headers, verify=False, allow_redirects=False)
    except requests.exceptions.ConnectionError:
        print("Failed to connect to website")
        continue

    body = t1.content.decode("utf-8")
    parser1.feed(body)
    if not parser1.loggedin:
        print("MoodleSession cookie expired")
    elif parser1.instance is None:
        print("No enroll button found")
        continue

    # TODO: untested
    idx = body.find("\"sesskey\":\"")
    idxend = body[idx+11:].find("\"")
    if idx == -1:
        print(f"Unexpected error occurred. Please create an issue at {issues_url} with details")
        exit()
    else:
        sesskey = body[idx+11:idxend]

    t = requests.post(enrol_url,
                      data=f"id={course_id}&instance={parser1.instance}&sesskey={sesskey}&_qf__{parser1.instance}_enrol_autoenrol%5Cenrol_form=1&mform_isexpanded_id_autoenrolheader=1&submitbutton=Enrol+me",
                      cookies=cookies, headers=headers, verify=False, allow_redirects=False)
    parser.feed(t.content.decode('utf-8'))

    if parser.bad:
        print(f"Failed to enroll in course at time {time.time()}. Please enroll manually at {enrol_url_with_course_id} and create an issue at {issues_url} with details")
        continue

    print("Enrolled in course")
    exit()
