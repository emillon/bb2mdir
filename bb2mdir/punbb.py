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

    def encode(data):
        "Create a header encoded as UTF-8"
        return Header(data, 'UTF-8')

    msg['Date'] = find_date(soup).strftime("%a, %d %b %Y %H:%M:%S %z")
    msg['From'] = encode('%s <nobody@localhost>' % soup.find('strong').text)
    msg['Subject'] = encode(soup.find('h3').text)

    body = soup.find('div', 'postmsg')
    body = html2text(str(body).decode('utf-8'))

    msg.set_payload(body, 'UTF-8')

    return msg

def parse_max_page(soup):
    "Compute the last page number in a thread"
    return int(soup.find('p', 'pagelink').findAll('a')[-1].text)

def msgs_on_page(soup):
    "All the message divs in a page"
    return soup.findAll('div', 'blockpost')

class PunbbThread:
    "A PunBB thread"

    def __init__(self, site, thread, maildir):
        self.site = site
        self.thread = thread
        self.maildir = maildir

    def url(self, page=1):
        "The URL for a given page (default 1) in this thread"
        print "get page %d" % page
        return "%s/viewtopic.php?id=%d&p=%d" % ( self.site['url']
                                               , self.thread
                                               , page
                                               )

    def refresh(self, ids):
        "Refresh the current maildir with respect to this thread"

        max_id = next((x['id'] for x in ids['sites']
                               if x['name'] == self.site['name']
                      ), None)

        print max_id

        page_one = urllib.urlopen(self.url()).read()
        max_page = parse_max_page(BeautifulSoup(page_one))

        page_num = max_page

        done = False

        while (done == False):
            page = urllib.urlopen(self.url(page=page_num)).read()
            soup = BeautifulSoup(page)
            msgs = msgs_on_page(soup)

            for msg in msgs:
                msg_id = int(msg['id'][1:])
                if msg_id <= max_id:
                    done = True
                else:
                    msg = parse_div(msg)
                    self.maildir.add(msg)

            page_num -= 1
            if page_num == 0:
                done = True

        return ids

