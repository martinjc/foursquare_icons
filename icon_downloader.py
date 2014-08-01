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
def process_category( category_json ):
    if not category_json['icon'] in icons:
        icons.append( category_json['icon'] )

    if 'categories' in category_json:
        [ process_category( c ) for c in category_json['categories'] ]

if __name__ == "__main__":

    url = api_base_url + '/venues/categories?' + urllib.urlencode( params )

    print url

    try:
        response = urllib2.urlopen( url )
    except urllib2.HTTPError, e:
        raise e
    except urllib2.URLError, e:
        raise e

    raw_data = response.read( )
    py_data = json.loads( raw_data )

    categories_json = py_data['response']

    # extract all the categories
    for category in categories_json['categories']:
        process_category( category )
    
    print len(icons)

    current_dir = os.getcwd()

    # download all the icons
    for count, icon in enumerate(icons):
        print icon
        sizes = icon['sizes']
        for size in sizes:
            size_dir = '%s/%s' % ( current_dir, size )
            
            if not os.path.exists( size_dir ):
                os.makedirs( size_dir )
            try:
                url = '%s%s.png' % ( icon['prefix'], size )
                print url
                u = urllib2.urlopen( url )
                file_name = '%s/%s.png' % ( size_dir, icon['prefix'].rstrip('_').replace( 'https://foursquare.com/img/categories/', '' ).replace('/', '_') )
                localFile = open( file_name, 'w' )
                localFile.write( u.read( ) )
                localFile.close( )
            except Exception, e:
                pass