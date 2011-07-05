"""
A PunBB parser that outputs a maildir.

Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
----------------------------------------------------------------------------
                       "THE BEER-WARE LICENSE"
<etienne.millon@gmail.com> wrote this file. As long as you retain this notice
you can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy me a beer in return.
----------------------------------------------------------------------------
"""

from BeautifulSoup import BeautifulSoup
from mailbox import Maildir, MaildirMessage
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

def main():
    "Program entry point"
    doc = open('ex.html').read()
    soup = BeautifulSoup(doc)
    maildir = Maildir('out')

    for msg_soup in soup.findAll('div', 'blockpost'):
        msg = parse_div(msg_soup)
        maildir.add(msg)

if __name__ == "__main__":
    main()
