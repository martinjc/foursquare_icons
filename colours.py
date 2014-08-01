import os

#
# colour name, and imagemagick colour name
colours = {
    'red' : 'red',
    'crimson' : 'crimson',
    'pink' : 'DeepPink',
    'purple' : 'purple',
    'indigo' : 'indigo',
    'blue' : 'blue',
    'navy' : 'navy',
    'turquoise' : 'turquoise1',
    'teal' : 'teal',
    'lime' : 'lime',
    'yellow' : 'yellow',
    'orange' : 'orange',
}

#
# list all the files in the current directory
current_dir = os.getcwd( )
files = os.listdir( current_dir )

#
# run through the file list
for fname in files:
    # for all the png's
    if '.png' in fname:
        # get the file name
        stripped_name = fname[ :fname.rfind( '.' ) ]
        # convert to a new colour and save
        for colour, magickcolour in colours.iteritems( ):
            colour_name = '%s_%s.png' % ( stripped_name, colour)
            os.system( 'convert %s +level-colors %s, %s'
                        % ( fname, magickcolour, colour_name ) )