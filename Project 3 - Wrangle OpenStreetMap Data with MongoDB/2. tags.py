#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
check the "k" value for each "<tag>"
count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
problemchars_dict = {}
other_tags_dict = {}

def key_type(element, keys):
    # to get some insight and statistics about the "problematic" and "other" tags, we save these tags
    # and count their frequencies in these two dictionaries
    global problemchars_dict
    global other_tags_dict

    if element.tag == "tag":
        k_val = element.get('k')

        if lower.search(k_val):
            keys['lower'] += 1
        elif lower_colon.search(k_val):
            keys['lower_colon'] += 1
        elif problemchars.search(k_val):
            if k_val in problemchars_dict.keys():
                problemchars_dict[k_val] += 1
            else:
                problemchars_dict[k_val] = 1
            keys['problemchars'] += 1
        else:
            if k_val in other_tags_dict.keys():
                other_tags_dict[k_val] += 1
            else:
                other_tags_dict[k_val] = 1
            keys['other'] += 1
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


keys = process_map('albuquerque_new-mexico.osm')
pprint.pprint(keys)
pprint.pprint(problemchars_dict)
pprint.pprint(other_tags_dict)

""" OUTPUT

{'lower': 104660, 'lower_colon': 115719, 'other': 2269, 'problemchars': 8}
{'Prickly Pear': 3, 'Salt Bush': 4, 'source;cycleway': 1}
{'Dandelion': 2,
 'FIXME': 149,
 'Juniper': 2,
 'gnis:Class': 34,
 'gnis:County': 34,
 'gnis:County_num': 34,
 'gnis:ST_alpha': 34,
 'gnis:ST_num': 34,
 'gnis:feature_id_1': 1,
 'is_in:iso_3166_2': 7,
 'name1': 4,
 'name2': 1,
 'name_1': 309,
 'name_2': 11,
 'service:bicycle:chain_tool': 1,
 'socket:nema_5_20': 2,
 'socket:type1': 2,
 'socket:type1_combo': 1,
 'tiger:CLASSFP': 7,
 'tiger:CPI': 7,
 'tiger:FUNCSTAT': 7,
 'tiger:LSAD': 7,
 'tiger:MTFCC': 7,
 'tiger:NAME': 7,
 'tiger:NAMELSAD': 7,
 'tiger:PCICBSA': 7,
 'tiger:PCINECTA': 7,
 'tiger:PLACEFP': 7,
 'tiger:PLACENS': 7,
 'tiger:PLCIDFP': 7,
 'tiger:STATEFP': 7,
 'tiger:name_base_1': 553,
 'tiger:name_base_2': 170,
 'tiger:name_base_3': 34,
 'tiger:name_direction_suffix_1': 74,
 'tiger:name_direction_suffix_2': 46,
 'tiger:name_type_1': 181,
 'tiger:name_type_2': 46,
 'tiger:zip_left_1': 200,
 'tiger:zip_left_2': 57,
 'tiger:zip_left_3': 13,
 'tiger:zip_left_4': 1,
 'tiger:zip_right_1': 111,
 'tiger:zip_right_2': 25,
 'tiger:zip_right_3': 4,
 'tiger:zip_right_4': 1}
"""