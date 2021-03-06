# Copyright (c) 2019 Remi Salmon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# imports
import re
import glob
import argparse
import webbrowser

from folium import Map
from folium.plugins import HeatMap

# constants
HEATMAP_MAXZOOM = 16

HEATMAP_GRAD = {0.0: '#000004',
                0.1: '#160b39',
                0.2: '#420a68',
                0.3: '#6a176e',
                0.4: '#932667',
                0.5: '#bc3754',
                0.6: '#dd513a',
                0.7: '#f37819',
                0.8: '#fca50a',
                0.9: '#f6d746',
                1.0: '#fcffa4'}

# functions
def main(args):
    if not args.output[-5:] == '.html':
        exit('ERROR Output file must be .html')

    gpx_files = glob.glob('{}/{}'.format(args.dir, args.filter))

    if not gpx_files:
        exit('ERROR No GPX files in {}'.format(args.dir))

    heatmap_data = []

    for gpx_file in gpx_files:
        print('Reading {}'.format(gpx_file))

        with open(gpx_file, 'r') as file:
            for line in file:
                if '<trkpt' in line:
                    r = re.findall('[-]?[0-9]*[.]?[0-9]+', line)

                    heatmap_data.append([float(r[0]), float(r[1])])

    print('Loaded {} trackpoints'.format(len(heatmap_data)))

    fmap = Map(tiles = 'CartoDB dark_matter', prefer_canvas = True, max_zoom = HEATMAP_MAXZOOM)

    HeatMap(heatmap_data, radius = args.radius, blur = args.blur, gradient = HEATMAP_GRAD, min_opacity = args.min_opacity).add_to(fmap)

    fmap.fit_bounds(fmap.get_bounds())

    fmap.save(args.output)

    print('Saved {}'.format(args.output))

    webbrowser.open(args.output, new = 2, autoraise = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate a local heatmap from Strava GPX files', epilog = 'Report issues to https://github.com/remisalmon/strava-local-heatmap-browser')

    parser.add_argument('--gpx-dir', dest = 'dir', default = 'gpx', help = 'directory containing the GPX files (default: gpx)')
    parser.add_argument('--gpx-filter', dest = 'filter', default = '*.gpx', help = 'glob filter for the GPX files (default: *.gpx)')
    parser.add_argument('--output', dest = 'output', default = 'strava_local_heatmap.html', help = 'output HTML file (default: strava_local_heatmap.html)')
    parser.add_argument('--radius', dest = 'radius', type = int, default = 2, help = 'radius of trackpoints in pixels (default: 3)')
    parser.add_argument('--blur', dest = 'blur', type = int, default = 1, help = 'amount of blur in pixels (default: 3)')
    parser.add_argument('--min-opacity', dest = 'min_opacity', type = float, default = 0.3, help = 'minimum opacity value (default: 0.3)')

    args = parser.parse_args()

    main(args)
