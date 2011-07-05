"""
A *BB parser that outputs a maildir.

Copyright (c) 2011 Etienne Millon <etienne.millon@gmail.com>
----------------------------------------------------------------------------
                       "THE BEER-WARE LICENSE"
<etienne.millon@gmail.com> wrote this file. As long as you retain this notice
you can do whatever you want with this stuff. If we meet some day, and you
think this stuff is worth it, you can buy me a beer in return.
----------------------------------------------------------------------------
"""

from BeautifulSoup import BeautifulSoup
from mailbox import Maildir
from bb2mdir import punbb

def process_bb(doc, maildir):
    soup = BeautifulSoup(doc)
    punbb.handle(soup, maildir)

def main():
    "Program entry point"

    doc = open('ex.html').read()
    maildir = Maildir('out')
    process_bb(doc, maildir)


if __name__ == "__main__":
    main()
