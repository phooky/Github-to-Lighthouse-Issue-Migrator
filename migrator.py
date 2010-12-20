#!/usr/bin/python

from lighthouse import Lighthouse
from github2.client import Github

# You'll need to install the proper APIs:
# pip install python-dateutil
# pip install lighthouse-python-api (probably have to do this manually)
# pip install github2

lhToken="token"
lhUrl="http://project.lighthouseapp.com"

ghToken="token"
ghUsername="username"
ghProject="org/project"

createTicket = 1
closeTicket = 1

lh = Lighthouse(token=lhToken,url=lhUrl)
                
lh.get_projects()
project = lh.projects[0]
lh.get_all_tickets(project)
print "LH project %s (%d) has %d tickets." % (project, project.id, len(project.tickets))

github=Github(username=ghUsername,api_token=ghToken,requests_per_second=0.6)
ghIssues=github.issues.list(ghProject, state="open")

print "GH project %s has %d open tickets. Importing..." % (ghProject, len(ghIssues))
for i in ghIssues:
    newTitle = i.title
    newBody = i.body
    if i.comments:
        comments = github.issues.comments(ghProject,i.number)
        for c in comments:
            newBody = newBody + "\n\nComment by %s:\n%s" % (c.user, c.body)
        newBody = newBody + "\nImported from https://github.com/%s/issues#issue/%d" % (ghProject, i.number)
    if createTicket:
        print "Creating ticket: %s" % i.title
        newTicket = lh.add_ticket(project=project,title=newTitle.encode('utf-8'),body=newBody.encode('utf-8'))
        github.issues.comment(ghProject,i.number,"Migrated to Lighthouse: %s/projects/%d/tickets/" % (lhUrl,project.id))
    if closeTicket:
        print "Closing ticket: %s" % i.title
        github.issues.close(ghProject,i.number)
            
