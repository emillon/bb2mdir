"""
Code specific to punBB.
"""

from mailbox import MaildirMessage
from datetime import datetime
from html2text import html2text

def find_date(soup):
    "Return the date of a message as a datetime object"
    date = soup.find('a').text

    if date .startswith('Today'):
        today = datetime.today().strftime('%Y-%m-%d')
        date = today + date[5:]

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date

def parse_div(soup):
    "Parses a message div (class blockpost) and return a MaildirMessage"
    print soup['id']
    msg = MaildirMessage()

    msg['Date'] = find_date(soup).strftime("%a, %d %b %Y %H:%M:%S %z")
    msg['From'] = '%s <nobody@localhost>' % soup.find('strong').text
    msg['Subject'] = soup.find('h3').text

    body = soup.find('div', 'postmsg')
    body = html2text(str(body).decode('utf-8'))

    msg.set_payload(body, 'UTF-8')

    return msg

