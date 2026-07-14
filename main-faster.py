from html.parser import HTMLParser
import requests
import time

course_id = 3595
# From M.cfg.sesskey in browser console
sesskey = "sweQNy6OLw"
# The MoodleSession cookie
session = "isccnfgudpc30m3moehgu5c28b"

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.bad = True
        if tag == 'a':
            if attrs[0][1] == f'https://ais.iitp.ac.in/moodle/course/view.php?id={course_id}':
                self.bad = False

class MyHTMLParser1(HTMLParser):
    def __init__(self):
        super().__init__()
        self.instance = None
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            for attr in attrs:
                if attr[0] == "name":
                    self.name = attr[1]
                elif attr[0] == "value":
                    self.value = attr[1]
            try:
                if self.name == "instance":
                    self.instance = self.value
            except: pass

parser = MyHTMLParser()
parser1 = MyHTMLParser1()
while True:
    # TODO: get sesskey from this request
    t1 = requests.get(f"https://ais.iitp.ac.in/moodle/enrol/index.php?id={course_id}", cookies={"MoodleSession": session}, headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False, allow_redirects=False)
    parser1.feed(t1.content.decode('utf-8'))
    if parser1.instance == None:
        print("No enroll button found")
    else:
        t = requests.post("https://ais.iitp.ac.in/moodle/enrol/index.php", data=f"id={course_id}&instance={parser1.instance}&sesskey={sesskey}&_qf__{parser1.instance}_enrol_autoenrol%5Cenrol_form=1&mform_isexpanded_id_autoenrolheader=1&submitbutton=Enrol+me", cookies={"MoodleSession": session}, headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False, allow_redirects=False)
        parser.feed(t.content.decode('utf-8'))
        if parser.bad == True:
            print(f"Failed to enroll in course at time {time.time()}. Please enroll manually at https://ais.iitp.ac.in/moodle/enrol/index.php?id={course_id}")
        else:
            print("Enrolled in course")
            exit()
    time.sleep(1)
