from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
zbuffer = new_zbuffer()
color = [ 0, 255, 0 ]
edges = []
polygons = []
t = new_matrix()
ident(t)
csystems = [ t ]

triX=[0, 5, 2]
triY=[0, 5, 3]
parse_file( 'script', edges, polygons, csystems, screen, zbuffer, color )
#polygons=[]
#add_polygon( polygons, 0,0,1,5,5,1,2,3,0)
#scanline_convert(polygons, 0, screen, zbuffer )
