from display import *
from matrix import *
from gmath import *
import random
def scanline_convert(polygons, i, screen, zbuffer ):
    color = [random.randrange(255), random.randrange(255), random.randrange(255)]
    '''if len(polygons)>36:
        color[0] = 170+(i*10%50)
        color[1] = 170+(i*10%50)
        color[2]= 170+(i*10%50)
    else:
        color[0] = (180+i*5)% 255;
        color[1] = (180+i*5) % 255;
        color[2]= (177+i*5) % 255;'''
    triX=[int(polygons[i][0]), int(polygons[i+1][0]), int(polygons[i+2][0])]
    triY=[int(polygons[i][1]), int(polygons[i+1][1]), int(polygons[i+2][1])]
    triZ=[polygons[i][2], polygons[i+1][2], polygons[i+2][2]]
    xt = 0
    yt = 0
    zt = 0
    xm = 0
    ym = 0
    zm = 0
    xb = 0
    yb = 0
    zb = 0
    if(triY[0] >= triY[1] and triY[0] >= triY[2]):
        xt = triX[0]
        yt = triY[0]
        zt = triZ[0]
        if(triY[1]>=triY[2]):
            xm = triX[1]
            ym = triY[1]
            zm = triZ[1]
            xb = triX[2]
            yb = triY[2]
            zb = triZ[2]
        else:
            xb = triX[1]
            yb = triY[1]
            zb = triZ[1]
            xm = triX[2]
            ym = triY[2]
            zm = triZ[2]
    elif (triY[1] >= triY[2] and triY[1] >= triY[0]):
        xt = triX[1]
        yt = triY[1]
        zt = triZ[1]
        if(triY[0]>=triY[2]):
            xm = triX[0]
            ym = triY[0]
            zm = triZ[0]
            xb = triX[2]
            yb = triY[2]
            zb = triZ[2]
        else:
            xb = triX[0]
            yb = triY[0]
            zb = triZ[0]
            xm = triX[2]
            ym = triY[2]
            zm = triZ[2]
    else:
        xt = triX[2]
        yt = triY[2]
        zt = triZ[2]
        if(triY[0]>=triY[1]):
            xm = triX[0]
            ym = triY[0]
            zm = triZ[0]
            xb = triX[1]
            yb = triY[1]
            zb = triZ[1]
        else:
            xb = triX[0]
            yb = triY[0]
            zb = triZ[0]
            xm = triX[1]
            ym = triY[1]
            zm = triZ[1]
    dx0 = 0
    dx1 = 0
    dx1_1 = 0
    dz0 = 0
    dz1 = 0
    dz1_1 = 0
    if ym==yb or yt==ym:
        if  yt - yb != 0:
            dx0 = (xt - xb) / (yt - yb)
            dz0 = (zt - zb) / (yt - yb)
        x0 = xb
        x1 = xb
        z0 = zb
        z1 = zb
        y = yb
        if ym==yb:
            x1 = xm
            z1 = zm
            if yt - ym != 0:
                dx1 = (xt - xm) / (yt - ym)
                dz1 = (zt - zm) / (yt - ym)
        else:
            if ym - yb != 0:
                dx1 = (xm - xb) / (ym - yb)
                dz1 = (zm - zb) / (ym - yb)
        while y <= yt:
            draw_scanline(int(x0), int(x1), int(y), z0, z1, screen, zbuffer, color)
            x0 += dx0
            x1 += dx1
            z0 += dz0
            z1 += dz1
            y += 1
    else:
        if yt - yb != 0:
            dx0 = (xt - xb) / (yt - yb)
            dz0 = (zt - zb) / (yt - yb)
        if ym - yb != 0:
            dx1 = (xm - xb) / (ym - yb)
            dz1 = (zm - zb) / (ym - yb)
        if yt - ym !=0:
            dx1_1 = (xt - xm) / (yt - ym)
            dz1_1 = (zt - zm) / (yt - ym)
        x0 = xb
        x1 = xb
        z0 = zb
        z1 = zb
        y0 = yb
        y = yb
        while y <= yt:
            draw_scanline(int(x0), int(x1), int(y), z0, z1, screen, zbuffer, color)
            x0 += dx0
            x1 += dx1
            z0 += dz0
            z1 += dz1
            y += 1
            if y == ym:
                dx1 = dx1_1
                x1 = xm
                dz1 = dz1_1
                z1 = zm

def draw_scanline(x0, x1, y, z0, z1, screen, zbuffer, color):
    if x0 > x1:
        temp=x0
        x0=x1
        x1=temp
        temp=z0
        z0=z1
        z1=temp
    x = x0
    z = z0
    dz = 0
    if x1-x0 != 0:
        dz = (z1-z0) / (x1-x0)
    while x <= x1:
        if y<500 and x<500 and y>=0 and x >=0 and zbuffer[y][x] < z:
            plot(screen, zbuffer, color, x, y, z)
        x+=1
        z+=dz
def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, color ):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return

    point = 0
    while point < len(polygons) - 2:
        normal = calculate_normal(polygons, point)[:]
        if normal[2] > 0:
            '''draw_line( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       int(polygons[point+1][0]),
                       int(polygons[point+1][1]),
                       polygons[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(polygons[point][0]),
                       int(polygons[point][1]),
                       polygons[point][2],
                       int(polygons[point+2][0]),
                       int(polygons[point+2][1]),
                       polygons[point+2][2],
                       screen, zbuffer, color)'''
            scanline_convert(polygons, point, screen, zbuffer)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side

    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step
    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False
    d_z = 0
    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        if x1 - x0 != 0:
            d_z = (z1 - z0) / (x1 - x0)
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        if y1 - y0 != 0:
            d_z = (z1 - z0) / (y1 - y0)
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    while ( loop_start < loop_end ):
        if zbuffer[y][x] < z:
            plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z += d_z
        loop_start+= 1
    if zbuffer[y][x] < z:
        plot( screen, zbuffer, color, x, y, z )
