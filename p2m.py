from BeautifulSoup import BeautifulSoup
from mailbox import Maildir, MaildirMessage
from datetime import datetime
import time

doc = open('ex.html').read()

soup = BeautifulSoup(doc)

def findDate(s):
    dateStr = s.find('a').text

    if dateStr.startswith('Today'):
        today = datetime.today().strftime('%Y-%m-%d')
        dateStr = today + dateStr[5:]

    date = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
    return date

def findAuthor(s):
    return s.find('strong').text

md=Maildir('out')

for s in soup.findAll('div', 'blockpost'):
    m = MaildirMessage()

    m['Date'] = findDate(s).strftime("%a, %d %b %Y %H:%M:%S %z")
    m['From'] = '%s <nobody@localhost>' % findAuthor(s)

    m.set_payload(s.find('div', 'postmsg').text, 'UTF-8')

    md.add(m)

    
