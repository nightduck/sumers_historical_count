from html.parser import HTMLParser
from urllib import request
import mysql.connector
from datetime import datetime
import re

URL = "https://connect2concepts.com/connect2/?type=bar&key=965778F9-13B8-49E7-B9AF-46D83702D026"

NONE = 0
DIV = 1

AREAS = ["Free Weight Area", "Cardio Area", "Weight Machine Area", "Rec Courts", "Pool", "South 40 Fitness Center"]

class GymParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.state = NONE
        self.occupancies = {a : [None, -1, datetime.min] for a in AREAS}
        self.area = ""

        self.open_closed_re = re.compile('Open|Closed')
        self.occup_re = re.compile('Last Count: [0-9]+')
        self.num_re = re.compile('[0-9]+')
        self.timestamp_re = re.compile('(0[1-9]|1[012])[- /.]([012][0-9]|3[01])[- /.](19|20)\d\d (0[1-9]|1[0-2]):[0-5][0-9] (PM|AM)')


    def handle_starttag(self, tag, attrs):
        if (self.state == NONE and tag == "div" and ("class", "barChart") in attrs):
            self.state = DIV

    def handle_endtag(self, tag):
        if(tag == "div"):
            self.state = NONE
            self.area = ""
            
    def handle_data(self, data):
        if (self.state == DIV):
            # See if data is string with area description
            matches = [a for a in AREAS if a in data]
            if len(matches) > 0:
                self.area = matches[0]

            # See if data is string with open/closed status
            elif self.open_closed_re.search(data) and len(self.area) > 0:
                self.occupancies[self.area][0] = "Open" in data

            # See if data is string with occupancy
            elif self.occup_re.search(data) and len(self.area) > 0:
                self.occupancies[self.area][1] = int(self.num_re.search(data)[0])

            # See if data is string with timestamp
            elif self.timestamp_re.search(data) and len(self.area) > 0:
                self.occupancies[self.area][2] = datetime.strptime(self.timestamp_re.search(data)[0], "%m/%d/%Y %I:%M %p")


passwd_fin = open("/run/secrets/db-password", 'r')
password = passwd_fin.readline().rstrip()
passwd_fin.close()

config = {
        'user': 'root',
        'password': password,
        'host': 'db',
        'port': '3306',
        'database': 'sumers_history'
    }


parser = GymParser()

req = request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

with request.urlopen(req) as page:
    parser.feed(page.read().decode("utf-8"))

connection = mysql.connector.connect(**config)
cur = connection.cursor()
for area, v in parser.occupancies.items():
    isOpen = v[0]
    count = v[1]
    timestamp = v[2].strftime('%Y-%m-%d %H:%M:%S')

    check_query = "SELECT * from sumers_history WHERE ts='%s' AND area='%s';" % (timestamp, area)
    cur.execute(check_query)
    row = cur.fetchone()
    if row == None:
        insert_query = "INSERT INTO sumers_history(Area, TS, Open_Closed, Count) VALUES ('%s', '%s', %s, %d);" % (area, timestamp, str(isOpen), count)
        cur.execute(insert_query)
        
connection.commit()
cur.close()
connection.close()