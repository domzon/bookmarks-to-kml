# -*- coding: utf-8 -*-
"""
See readme.md

"""

from lxml.html import document_fromstring
import simplekml

from urllib.request import FancyURLopener
from urllib.parse import quote_plus, urlparse, parse_qsl

import os
import re
import sys
import time
import random

coords_in_content = re.compile(r'\/@(-?\d+\.\d+),(-?\d+\.\d+),')
coords_in_description = re.compile(r'^(-?\d+\.\d+),(-?\d+\.\d+)$')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'

filename = r'GoogleBookmarks.html'
if(len(sys.argv) > 1):
    filename = sys.argv[1]

print('opening ' + filename)
with open(filename) as bookmarks_file:
    data = bookmarks_file.read()

doc = document_fromstring(data)


class Browser(FancyURLopener):
    version = user_agent

for label in doc.body.iterfind('dl/dt/h3'):
    labelName = label.text_content()

    kml = simplekml.Kml()
    kml.document.name = labelName

    for element, _, url, _ in label.getparent().getnext().iterlinks():
        if 'maps.google' in url:
            description = element.text or ''
            latitude = longitude = None
            try:
                # check if the link itself contains the coordinate
                latitude, longitude = coords_in_description.search(
                    description).groups()
                print("Found point {0},{1} in description".format(
                    latitude, longitude))
            except (AttributeError, IndexError):
                safe_query = ['{0}={1}'.format(k, quote_plus(v))
                              for (k, v) in parse_qsl(urlparse(url).query)]
                url = '{0}/?{1}'.format(url.split('/?')
                                        [0], '&'.join(safe_query))

                print('GET {0} {1}'.format(url, description.encode('UTF8')))
                browser = Browser()

                # Load map and find coordinates in source of page
                sock = False
                while not sock:
                    try:
                        sock = browser.open(url)
                    except Exception as e:
                        print('Connection problem:' + repr(e))
                        print('Retrying randomly between 15 and 60 seconds.')
                        time.sleep(random.randint(15, 60))

                content = sock.read().decode("utf-8")
                sock.close()

                try:
                    latitude, longitude = coords_in_content.search(
                        content).groups()
                except (AttributeError, IndexError):
                    print('[Coordinates not found: ({0},{1}).'
                          'Try to update "user_agent"]'.format(latitude, longitude))
                    continue

            try:
                kml.newpoint(name=description,
                             coords=[(float(longitude), float(latitude))])
            except ValueError:
                print('[Invalid coordinates]')

    output = './maps/' + labelName + '.kml'
    print('saving results to ' + output)

    if not os.path.exists('./maps/'):
        os.makedirs('./maps/')

    kml.save(output)
