"""
Code specific to punBB.
"""

from mailbox import MaildirMessage
from datetime import datetime
from html2text import html2text
import urllib
from BeautifulSoup import BeautifulSoup
from email.header import Header

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

    def encode(x):
        return Header(x, 'UTF-8')

    msg['Date'] = find_date(soup).strftime("%a, %d %b %Y %H:%M:%S %z")
    msg['From'] = encode('%s <nobody@localhost>' % soup.find('strong').text)
    msg['Subject'] = encode(soup.find('h3').text)

    body = soup.find('div', 'postmsg')
    body = html2text(str(body).decode('utf-8'))

    msg.set_payload(body, 'UTF-8')

    return msg

def handle(soup, maildir):
    "Handle a whole HTML document"
    for msg_soup in soup.findAll('div', 'blockpost'):
        msg = parse_div(msg_soup)
        maildir.add(msg)

def parse_max_page(soup):
    p = int(soup.find('p', 'pagelink').findAll('a')[-1].text)
    print "Max page : %d" % p
    return p

def msgs_on_page(soup):
    return soup.findAll('div', 'blockpost')

class PunbbThread:

    def __init__(self, site, thread, maildir):
        self.site = site
        self.thread = thread
        self.maildir = maildir

    def url(self, page=1):
        return "%s/viewtopic.php?id=%d&page=%d" % (self.site['url'], self.thread, page)

    def refresh(self, ids):

        max_id = next((x['id'] for x in ids['sites'] if x['name'] == self.site), None)

        page_one = urllib.urlopen(self.url()).read()
        max_page = parse_max_page(BeautifulSoup(page_one))

        page_num = max_page

        done = False

        while not done:
            page = urllib.urlopen(self.url(page=page_num)).read()
            soup = BeautifulSoup(page)
            msgs = msgs_on_page(soup)

            for msg in msgs:
                msg_id = int(msg['id'][1:])
                print "msg_id = %d" % msg_id
                if msg_id <= ids:
                    done = True

                msg = parse_div(msg)
                self.maildir.add(msg)

            page_num -= 1
            if page_num == 0:
                done = True

        return ids

