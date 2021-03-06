'''
pastebin.py
Author: Ryan Clough
Scrapes Pastebin in real time over the TOR network
If there is a match on a keyword (located in keywords.txt)
save the file locally.

Developed for Windows 7
'''

import re
import os
import sys
import time
import socks
import urllib2
from os import path as op
from datetime import datetime

# TOR Proxy
from sockshandler import SocksiPyHandler
opener = urllib2.build_opener(SocksiPyHandler(
    socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050))

# A few variables
_verbose = True
dir = op.dirname(op.realpath(__file__))
pastebin_overload = 'Hey, it seems you are requesting a little bit too \
                     much from Pastebin. Please slow down!'
timeout = 10


def get_url(url):
    try:
        html = opener.open(url, timeout=timeout).read()
    except KeyboardInterrupt:
        # Kill program if Control-C is pressed
        sys.exit(0)
    except:
        # Restart TOR if theres a problem
        e = sys.exc_info()[0]
        if _verbose:
            print "ERROR: " + str(e)
        os.system('for process in $(ps aux |grep -i /usr/local/opt/tor/bin/tor | cut -d " " -f12); do sudo kill $process; done')
        if _verbose:
            print "INFO: Restarting TOR"
        time.sleep(1)
        os.system('tor')
        return ''

    # See if pastebin is complaining
    if html == pastebin_overload:
        if _verbose:
            print 'ERROR: Too many requests'
        time.sleep(5)
        return ''
    # If not, we are good
    elif html:
        return html
    # Tor download error, skip it and move on
    else:
        if _verbose:
            print 'ERROR: Download is empty - ' + url
        return ''


# Get the most recent 200 pastes from pastebin.com/archive
def get_recent_pastes():
    html = get_url('http://pastebin.com/archive')
    pastes = re.findall(r' \/><a href=\"\/(.+?)\">(.+?)<\/a><\/td>', html)
    return pastes


# Get raw, individual paste given a paste id
def get_paste(paste_id):
    url = 'http://pastebin.com/raw.php?i=' + paste_id
    return get_url(url)


def main():
    # Insert the 200 latest pastes into recent pastes
    # so we don't start out way behind real time
    recent_pastes = []
    for paste_id, paste_title in get_recent_pastes():
        recent_pastes.append(paste_id)

    while True:
        # Once we have processed 65 pastes, reset recent pastes to
        # make sure we dont fall behind real time
        if len(recent_pastes) > 275:
            if _verbose:
                print 'INFO: Resetting recent_pastes'
            recent_pastes = []
            for paste_id, paste_title in get_recent_pastes():
                recent_pastes.append(paste_id)

        #Get the new pastes and continue if successful
        new_pastes = get_recent_pastes()
        if new_pastes:
            for paste_id, paste_title in new_pastes:
                if paste_id not in recent_pastes:

                    # Get paste and check for errors
                    paste_text = get_paste(paste_id)
                    if paste_text == '':
                        continue
                    if _verbose:
                        print 'INFO: Success ' + paste_id

                    # Run paste text against keywords and record hits
                    keywords = [line.strip() for line in open(
                        op.join(dir, 'keywords.txt'), 'r')
                    ]
                    hits = []
                    for keyword in keywords:
                        if keyword.lower() in paste_text.lower():
                            hits.append(keyword)

                    # If there are hits, save to file system
                    if hits:
                        if _verbose:
                            print 'INFO: Keyword Hit ' + paste_id + ' ' + ','.join(hits)
                        year = datetime.now().strftime('%Y')
                        month = datetime.now().strftime('%m')
                        date = datetime.now().strftime('%d')
                        yyyymmdd = datetime.now().strftime('%Y%m%d')

                        if not op.exists(op.join(dir, 'Pastebin')):
                            os.makedirs(op.join(dir, 'Pastebin'))
                        os.chdir(op.join(dir, 'Pastebin'))
                        if not op.exists(op.join(year, month, date)):
                            os.makedirs(op.join(year, month, date))

                        os.chdir(op.join(year, month, date))
                        fname = yyyymmdd + '_' + paste_id
                        for hit in hits:
                            fname += '_' + ''.join(ch for ch in hit if ch.isalnum())
                        fname += '.txt'
                        with open(fname, 'w') as f:
                            f.write('Title: ' + paste_title + '\n')
                            f.write(paste_text)

                    # Add current paste to recent paste list
                    recent_pastes.append(paste_id)


if __name__ == '__main__':
    main()
