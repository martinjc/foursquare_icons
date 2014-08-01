import urllib2
import urllib
import json
import os

from _credentials import access_token

# supply oauth token as parameter
params = {
    'oauth_token' : access_token,
    'v' : '20140801'
}

api_base_url = 'https://api.foursquare.com/v2'

icons = []

# function to extract category info from json and 
# process any sub-categories
def process_category(category_json):
    if not category_json['icon'] in icons:
        icons.append((category_json['id'], category_json['icon']))

    if 'categories' in category_json:
        [process_category(c) for c in category_json['categories']]

if __name__ == "__main__":

    url = api_base_url + '/venues/categories?' + urllib.urlencode(params)

    print url

    # get the latest list of categories
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        raise e
    except urllib2.URLError, e:
        raise e

    raw_data = response.read( )
    py_data = json.loads(raw_data)

    categories_json = py_data['response']

    # extract all the categories
    for category in categories_json['categories']:
        process_category(category)
    
    print len(icons)

    sizes = ["bg_32", "bg_44", "bg_64", "bg_88"]

    current_dir = os.getcwd()

    for size in sizes:
        size_dir = os.path.join(current_dir, size)
            
        if not os.path.exists(size_dir):
            os.makedirs(size_dir)

        # download all the icons
        for count, data in enumerate(icons):
            cat_id, icon = data
            print icon, cat_id
            url = '%s%s%s' % (icon['prefix'], size, icon['suffix'])
            print url
            u = urllib2.urlopen(url)
            file_name = '%s%s' % (cat_id, icon['suffix'])
            localFile = open(os.path.join(size_dir, file_name), 'w')
            localFile.write(u.read())
            localFile.close()