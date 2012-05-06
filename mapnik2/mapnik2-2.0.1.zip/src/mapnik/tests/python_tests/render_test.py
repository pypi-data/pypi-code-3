#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

import os, mapnik
from nose.tools import *

from mapnik.tests.python_tests.utilities import execution_path
from mapnik.tests.python_tests.utilities import Todo

def setup():
    # All of the paths used are relative, if we run the tests
    # from another directory we need to chdir()
    os.chdir(execution_path('.'))


def test_simplest_render():
    m = mapnik.Map(256, 256)
    i = mapnik.Image(m.width, m.height)

    mapnik.render(m, i)

    s = i.tostring()

    eq_(s, 256 * 256 * '\x00\x00\x00\x00')

def test_render_image_to_string():
    i = mapnik.Image(256, 256)
    
    i.background = mapnik.Color('black')
    
    s = i.tostring()

    eq_(s, 256 * 256 * '\x00\x00\x00\xff')

    s = i.tostring('png')

def test_setting_alpha():
    w,h = 256,256
    im1 = mapnik.Image(w,h)
    # white, half transparent
    im1.background = mapnik.Color('rgba(255,255,255,.5)')
    
    # pure white
    im2 = mapnik.Image(w,h)
    im2.background = mapnik.Color('rgba(255,255,255,1)')
    im2.set_alpha(.5)
        
    eq_(len(im1.tostring()), len(im2.tostring()))


def test_render_image_to_file():
    i = mapnik.Image(256, 256)
    
    i.background = mapnik.Color('black')

    if mapnik.has_jpeg():
        i.save('test.jpg')
    i.save('test.png', 'png')

    if os.path.exists('test.jpg'):
        os.remove('test.jpg')
    else:
        return False
    
    if os.path.exists('test.png'):
        os.remove('test.png')
    else:
        return False

def get_paired_images(w,h,mapfile):
    tmp_map = 'tmp_map.xml'
    m = mapnik.Map(w,h)
    mapnik.load_map(m,mapfile)
    i = mapnik.Image(w,h)
    m.zoom_all()
    mapnik.render(m,i)
    mapnik.save_map(m,tmp_map)
    m2 = mapnik.Map(w,h)
    mapnik.load_map(m2,tmp_map)
    i2 = mapnik.Image(w,h)
    m2.zoom_all()
    mapnik.render(m2,i2)
    os.remove(tmp_map)
    return i,i2    

def test_render_from_serialization():
    i,i2 = get_paired_images(100,100,'../data/good_maps/building_symbolizer.xml')
    eq_(i.tostring(),i2.tostring())

    i,i2 = get_paired_images(100,100,'../data/good_maps/polygon_symbolizer.xml')
    eq_(i.tostring(),i2.tostring())


grid_correct = {"keys": ["", "North West", "North East", "South West", "South East"], "data": {"South East": {"Name": "South East"}, "North East": {"Name": "North East"}, "North West": {"Name": "North West"}, "South West": {"Name": "South West"}}, "grid": ["                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "         !!!                                 ###                ", "        !!!!!                               #####               ", "        !!!!!                               #####               ", "         !!!                                 ###                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "        $$$$                                %%%%                ", "        $$$$$                               %%%%%               ", "        $$$$$                               %%%%%               ", "         $$$                                 %%%                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                ", "                                                                "]}


def resolve(grid,x,y):
    """ Resolve the attributes for a given pixel in a grid.
    
    js version: 
      https://github.com/mapbox/mbtiles-spec/blob/master/1.1/utfgrid.md
    spec:
      https://github.com/mapbox/wax/blob/master/control/lib/gridutil.js
    
    """
    utf_val = grid['grid'][x][y]
    #http://docs.python.org/library/functions.html#ord
    codepoint = ord(utf_val)
    if (codepoint >= 93):
        codepoint-=1
    if (codepoint >= 35):
        codepoint-=1
    codepoint -= 32
    key = grid['keys'][codepoint]
    return grid['data'].get(key)


def test_render_grid():
    places_ds = mapnik.PointDatasource()
    places_ds.add_point(143.10,-38.60,'Name','South East')
    places_ds.add_point(142.48,-38.60,'Name','South West')
    places_ds.add_point(142.48,-38.38,'Name','North West')
    places_ds.add_point(143.10,-38.38,'Name','North East')
    s = mapnik.Style()
    r = mapnik.Rule()
    #symb = mapnik.PointSymbolizer()
    symb = mapnik.MarkersSymbolizer()
    symb.width = 10
    symb.height = 10
    symb.allow_overlap = True
    r.symbols.append(symb)
    label = mapnik.TextSymbolizer(mapnik.Expression('[Name]'),
                'DejaVu Sans Book',
                10,
                mapnik.Color('black')
                )
    label.allow_overlap = True
    label.displacement = (0,-10)
    #r.symbols.append(label)

    s.rules.append(r)
    lyr = mapnik.Layer('Places')
    lyr.datasource = places_ds
    lyr.styles.append('places_labels')
    m = mapnik.Map(256,256)
    m.append_style('places_labels',s)
    m.layers.append(lyr)
    ul_lonlat = mapnik.Coord(142.30,-38.20)
    lr_lonlat = mapnik.Coord(143.40,-38.80)
    m.zoom_to_box(mapnik.Box2d(ul_lonlat,lr_lonlat))
    grid = mapnik.render_grid(m,0,key='Name',resolution=4,fields=['Name'])
    eq_(grid,grid_correct)
    eq_(resolve(grid,0,0),None)
    
    # check every pixel of the nw symbol
    expected = {"Name": "North West"}
    
    # top row
    eq_(resolve(grid,23,9),expected)
    eq_(resolve(grid,23,10),expected)
    eq_(resolve(grid,23,11),expected)

    # core
    eq_(resolve(grid,24,8),expected)
    eq_(resolve(grid,24,9),expected)
    eq_(resolve(grid,24,10),expected)
    eq_(resolve(grid,24,11),expected)
    eq_(resolve(grid,24,12),expected)
    eq_(resolve(grid,25,8),expected)
    eq_(resolve(grid,25,9),expected)
    eq_(resolve(grid,25,10),expected)
    eq_(resolve(grid,25,11),expected)
    eq_(resolve(grid,25,12),expected)
    
    # bottom row
    eq_(resolve(grid,26,9),expected)
    eq_(resolve(grid,26,10),expected)
    eq_(resolve(grid,26,11),expected)
    
def test_render_points():

    if not mapnik.has_cairo(): return

    # create and populate point datasource (WGS84 lat-lon coordinates)
    places_ds = mapnik.PointDatasource()
    places_ds.add_point(142.48,-38.38,'Name','Westernmost Point') # westernmost
    places_ds.add_point(143.10,-38.60,'Name','Southernmost Point') # southernmost
    # create layer/rule/style
    s = mapnik.Style()
    r = mapnik.Rule()
    symb = mapnik.PointSymbolizer()
    symb.allow_overlap = True
    r.symbols.append(symb)
    s.rules.append(r)
    lyr = mapnik.Layer('Places','+proj=latlon +datum=WGS84')
    lyr.datasource = places_ds
    lyr.styles.append('places_labels')
    # latlon bounding box corners
    ul_lonlat = mapnik.Coord(142.30,-38.20)
    lr_lonlat = mapnik.Coord(143.40,-38.80)
    # render for different projections 
    projs = { 
        'latlon': '+proj=latlon +datum=WGS84',
        'merc': '+proj=merc +datum=WGS84 +k=1.0 +units=m +over +no_defs',
        'google': '+proj=merc +ellps=sphere +R=6378137 +a=6378137 +units=m',
        'utm': '+proj=utm +zone=54 +datum=WGS84'
        }
    for projdescr in projs.iterkeys():
        m = mapnik.Map(1000, 500, projs[projdescr])
        m.append_style('places_labels',s)
        m.layers.append(lyr)
        p = mapnik.Projection(projs[projdescr])
        m.zoom_to_box(p.forward(mapnik.Box2d(ul_lonlat,lr_lonlat)))
        # Render to SVG so that it can be checked how many points are there with string comparison
        svg_file = '/tmp/%s.svg'
        mapnik.render_to_file(m, svg_file)
        num_points_present = len(places_ds.all_features())
        svg = open(svg_file,'r').read()
        num_points_rendered = svg.count('<image ')
        eq_(num_points_present, num_points_rendered, "Not all points were rendered (%d instead of %d) at projection %s" % (num_points_rendered, num_points_present, projdescr)) 

if __name__ == "__main__":
    setup()
    [eval(run)() for run in dir() if 'test_' in run]
