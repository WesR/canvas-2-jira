from jira import JIRA
from ics import Calendar
import requests
import re
import json

jira = JIRA(server='jiraaddress', basic_auth=('un', 'pw'))
cal = Calendar(requests.get("https://uncc.instructure.com/feeds/calendars/user_<ect>.ics").text)
with open("done.json") as fi:
    done = json.load(fi)
defaultAssign = "YOUR JIRA USERNAME"

events = list(cal.timeline)
for x in range(len(events)):
    if (events[x].uid not in done):
        issue_dict = {
            'project': 'CAN',
            'summary': '[' + '-'.join(map(str, re.search('\[(.+?)\]', events[x].name).group(1).split('-', 1 )[1].split('-')[0:2])) + '] ' + re.search('.+?(?=\[.+?\])', events[x].name).group(0),
            'description': events[x].description,
            'duedate' : str(events[x].end.date()),
            'assignee': {'name': defaultAssign},
            'issuetype': {'name': 'Task'},
        }
        jira.create_issue(fields=issue_dict)
        print("New task added")
        done.append(events[x].uid)

with open('done.json', 'w') as fi:
    json.dump(done, fi)

print("done")
