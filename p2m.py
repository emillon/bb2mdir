from BeautifulSoup import BeautifulSoup
from mailbox import MaildirMessage
from datetime import datetime

doc = open('ex.html').read()

soup = BeautifulSoup(doc)

for s in soup.findAll('div', 'blockpost'):
    #m = MaildirMessage()

    # Date
    dateStr = s.find('a').text

    if dateStr.startswith('Today'):
        today = datetime.today().strftime('%Y-%m-%d')
        dateStr = today + dateStr[5:]
    
    date = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
    print date
