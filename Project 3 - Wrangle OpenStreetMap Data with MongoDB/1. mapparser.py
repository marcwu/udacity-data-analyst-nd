#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script determines the tags and their count in the osm file.
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event,elem in ET.iterparse(filename):
        if elem.tag in tags.keys():
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags


tags = count_tags('albuquerque_new-mexico.osm')
pprint.pprint(tags)
""" OUTPUT

{'bounds': 1,
 'member': 1795,
 'nd': 340021,
 'node': 272498,
 'osm': 1,
 'relation': 229,
 'tag': 222656,
 'way': 41973}
"""