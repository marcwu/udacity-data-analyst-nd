#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "albuquerque_new-mexico.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# I found six special cases during my auditing. Since I am not sure how to correct them, I
# leave them untouched. Interestingly, they give an idea of how to improve the street
# names further. These cases are:
# - 11115
# - 4th Street NW Suite 250
# - Gold Between 1st and 2nd
# - 5th
# - 1833 8th Street NorthwestAlbuquerque, NM 87102
# - 3301 Menaul Blvd. NE Suite A', 'Juan Tabo NE, Suite A
expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place', 'Square', 'Lane', 'Road', 
            'Trail', 'Parkway', 'Commons',
            'Oeste', 'Southeast', 'Southwest', 'Northwest', 'Northeast', 'Vista',
            'Yale', 'School', 'Morningside', 'Freeway', 'Felipe', 'East', 'Circle',
            'Central', 'Broadway', 'Basehart', 
            '11115',
            '250',
            '2nd',
            '5th',
            '87102',
            'A',]

# Corrections
mapping = { 
            'Ave': 'Avenue',
            'avenue': 'Avenue',
            'AvenueSW': 'Avenue Southwest',
            'NE': 'Northeast',
            'NE.': 'Northeast',
            'Norhteast': 'Northeast',
            'NW': 'Northwest',
            'Pl': 'Place',
            'SE': 'Southeast',
            'SouthWest': 'Southwest',
            'SW': 'Southwest',
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_postal_code(postalcode_types, postal_code, postalcode_count):
    """
    Input:
        - postalcode_types, a dictionary containing unexpected postal codes
        - postal_code, a string to be audited
        - postalcode_count, a dictionary to count different postal codes
    This function audits a single postal code from Albuquerque, keeping
    track of unexpected formats and updating a frequency count
    """
    # try to match for ZIP format, our expected standard
    # Albuquerque postal codes are in form of (871XX)
    if re.match(r'^871\d{2}$', postal_code):
        postalcode_count["ZIP"] += 1
    
    # try to match for ZIP+4 format (871XX-XXXX)
    elif re.match(r'^871\d{2}-\d{4}$', postal_code):
        postalcode_types[postal_code].add(postal_code)
        postalcode_count["ZIP+4"] += 1
    
    # non-standard format
    else:
        postalcode_types[postal_code].add(postal_code)
        postalcode_count["OTHER"] += 1


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postalcode_types = defaultdict(set)
    postalcode_count = {"ZIP": 0, "ZIP+4": 0, "OTHER": 0}
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_postal_code(tag):
                    audit_postal_code(postalcode_types, tag.attrib['v'], postalcode_count)

    osm_file.close()
    return street_types, postalcode_types, postalcode_count


def update_name(name, mapping):
    # break down street name into its components, correct the last part,
    # and rebuild the street name again
    fixed_name = name.split(' ')
    fixed_name[-1] = mapping[fixed_name[-1]]
    return ' '.join(fixed_name)

def update_postal_code(postal_code):
    if re.match(r'^871\d{2}-\d{4}$', postal_code):
        return postal_code[:5]
    elif re.match(r'^NM', postal_code):
        return postal_code[3:]
    else:
        return ""

st_types, postalcode_types, postalcode_count = audit(OSMFILE)
pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name



pprint.pprint(dict(postalcode_types))
print postalcode_count
# standardizing postal codes
for postalcode_type, postalcodes in postalcode_types.iteritems():
    for pcode in postalcodes:
        better_code = update_postal_code(pcode)
        print pcode, "=>", better_code

""" OUTPUT

{'Ave': set(['8700 Central Ave']),
 'AvenueSW': set(['Cental AvenueSW']),
 'NE': set(['1915 Roma Ave. NE',
            'Anderson School of Management 1924 Las Lomas NE',
            'Balloon Museum Drive NE',
            'Central Ave NE',
            'Central Avenue NE',
            'Cutler Ave. NE',
            'Eubank Blvd NE',
            'Eubank NE',
            'Girard Boulevard NE',
            'Glendale Ave NE',
            'LOMAS BLVD NE',
            'Paseo Alameda NE',
            'Renaissance Boulevard NE',
            'Richmond Dr. NE',
            'Uptown Loop Rd NE']),
 'NE.': set(['Menaul Blvd. NE.']),
 'NW': set(['Valley View Dr NW']),
 'Norhteast': set(['Comanche Road Norhteast']),
 'Pl': set(['Mullhacen Pl']),
 'SE': set(['3400 Crest Ave. SE',
            'Bobby Foster SE',
            'Clark Ave SE',
            'Girard Blvd SE',
            'Girard SE',
            'Randolph Ave SE',
            'Silver Ave SE']),
 'SW': set(['Bridge Boulevard SW']),
 'SouthWest': set(['16th Street SouthWest']),
 'avenue': set(['Central avenue'])}
Menaul Blvd. NE. => Menaul Blvd. Northeast
16th Street SouthWest => 16th Street Southwest
Cental AvenueSW => Cental Avenue Southwest
Bridge Boulevard SW => Bridge Boulevard Southwest
1915 Roma Ave. NE => 1915 Roma Ave. Northeast
Paseo Alameda NE => Paseo Alameda Northeast
Uptown Loop Rd NE => Uptown Loop Rd Northeast
Cutler Ave. NE => Cutler Ave. Northeast
Anderson School of Management 1924 Las Lomas NE => Anderson School of Management 1924 Las Lomas Northeast
Balloon Museum Drive NE => Balloon Museum Drive Northeast
LOMAS BLVD NE => LOMAS BLVD Northeast
Central Avenue NE => Central Avenue Northeast
Eubank Blvd NE => Eubank Blvd Northeast
Glendale Ave NE => Glendale Ave Northeast
Central Ave NE => Central Ave Northeast
Renaissance Boulevard NE => Renaissance Boulevard Northeast
Richmond Dr. NE => Richmond Dr. Northeast
Girard Boulevard NE => Girard Boulevard Northeast
Eubank NE => Eubank Northeast
Mullhacen Pl => Mullhacen Place
8700 Central Ave => 8700 Central Avenue
Comanche Road Norhteast => Comanche Road Northeast
Central avenue => Central Avenue
Girard SE => Girard Southeast
Girard Blvd SE => Girard Blvd Southeast
Bobby Foster SE => Bobby Foster Southeast
Silver Ave SE => Silver Ave Southeast
3400 Crest Ave. SE => 3400 Crest Ave. Southeast
Clark Ave SE => Clark Ave Southeast
Randolph Ave SE => Randolph Ave Southeast
Valley View Dr NW => Valley View Dr Northwest
{'1019': set(['1019']),
 '87102-3116': set(['87102-3116']),
 '87106-1432': set(['87106-1432']),
 '87106-5117': set(['87106-5117']),
 '87108-2928': set(['87108-2928']),
 '87108-3217': set(['87108-3217']),
 '87108-3298': set(['87108-3298']),
 '87108-9998': set(['87108-9998']),
 '87109-2426': set(['87109-2426']),
 '87109-2465': set(['87109-2465']),
 '87110-4099': set(['87110-4099']),
 '87110-9998': set(['87110-9998']),
 '87111-6012': set(['87111-6012']),
 '87112-5582': set(['87112-5582']),
 '87112-5614': set(['87112-5614']),
 '87112-9998': set(['87112-9998']),
 '87113-2321': set(['87113-2321']),
 '87117-0001': set(['87117-0001']),
 '87120-1367': set(['87120-1367']),
 '87120-3033': set(['87120-3033']),
 '87120-8783': set(['87120-8783']),
 '87123-1202': set(['87123-1202']),
 '87123-2723': set(['87123-2723']),
 '87123-2755': set(['87123-2755']),
 '87123-2887': set(['87123-2887']),
 '87123-3035': set(['87123-3035']),
 '89197': set(['89197']),
 'NM 87110': set(['NM 87110']),
 'NM 87122': set(['NM 87122'])}
{'OTHER': 5, 'ZIP+4': 31, 'ZIP': 2174}
87123-1202 => 87123
87108-9998 => 87108
87117-0001 => 87117
89197 =>
87108-2928 => 87108
NM 87122 => 87122
87112-5614 => 87112
87123-2723 => 87123
87112-5582 => 87112
1019 =>
87111-6012 => 87111
87110-9998 => 87110
87112-9998 => 87112
87123-3035 => 87123
87120-1367 => 87120
87123-2887 => 87123
87106-5117 => 87106
87110-4099 => 87110
87106-1432 => 87106
87109-2426 => 87109
NM 87110 => 87110
87113-2321 => 87113
87120-3033 => 87120
87120-8783 => 87120
87108-3298 => 87108
87102-3116 => 87102
87123-2755 => 87123
87108-3217 => 87108
87109-2465 => 87109
"""