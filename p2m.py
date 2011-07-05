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
from bb2mdir import punbb

def main():
    "Program entry point"
    doc = open('ex.html').read()
    soup = BeautifulSoup(doc)
    maildir = Maildir('out')

    for msg_soup in soup.findAll('div', 'blockpost'):
        msg = punbb.parse_div(msg_soup)
        maildir.add(msg)

if __name__ == "__main__":
    main()
