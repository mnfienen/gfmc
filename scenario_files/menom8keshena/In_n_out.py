import numpy as np

def calc_area(pts):
    # use the closed-form solution derived in the notes
    A = 0.5*(pts[0,0]*pts[1,1] + pts[0,1]*pts[2,0] + pts[1,0]*pts[2,1]
            - pts[0,0]*pts[2,1] -pts[0,1]*pts[1,0] - pts[1,1]*pts[2,0])
    return A

def lineMag(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

def point_to_line_seg(testpt,pts):
	px,py = testpt
	x1,y1 = pts[0,:]
	x2,y2 = pts[1,:]
	# source of this function adapted from
	# http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/
	segment_mag = lineMag(x1,y1,x2,y2)
	u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
	u = u1/segment_mag/segment_mag
	# test for u --> if u <0 or u > 1, then closest point (normal) is outside the segment
	# in that case, find the closest endpoint and return the closest distance
	if u < 1.0e-5 or u > 1.0:
	    d1 = lineMag(px,py,x1,y1)
	    d2 = lineMag(px,py,x2,y2)
	    if d1 > d2:
		return d1
	    else:
		return d2
	else:
	    #intersection point is on the line, so the coordinates of the intersection
	    # point are ix and iy
	    ix = x1 + u * (x2 - x1)
	    iy = y1 + u * (y2 - y1)
	    return lineMag(px,py,ix,iy)
    
def eval_point_in_out(pts,test_pt,dtol):
    # returns 1 if test point is inside the triangle, 0 if outside
    # collacated points and line balls are considered INSIDE
    area_signs = 0
    for i in np.arange(3):
        eval_pts = pts.copy()
        # bail out if a point is collocated with the test point
        #print test_pt[0,0]
        #print test_pt[0,1]        
        #print eval_pts[i,0]
        #print eval_pts[i,1]
        if (eval_pts[i,0] == test_pt[0]) and (eval_pts[i,1] == test_pt[1]):
            return 1 # collcated is considered inside
        else:
            # now check for line balls, within a tolerance
            tmp = pts.copy()
            tmp = np.delete(tmp,i,0)
	    dist_pt_edge = point_to_line_seg(test_pt,tmp)
	    if dist_pt_edge <= dtol:
		return 1
#            if (test_pt[0]-tmp[0,0])*(tmp[1,1]-tmp[0,1]) == (tmp[1,0]-tmp[0,0])*(test_pt[1]-tmp[0,1]):
#                return 1
        eval_pts[i,:] = test_pt
        # we just care about the sign 
        area_signs += np.sign(calc_area(eval_pts)) 
    if np.abs(area_signs) == 1:
        # point is outside
        return 0
    else:
        return 1
    

def eval_point_in_poly(verts,points,test_pt,dtol):

    allin = 0
        

    for ct in verts:
        pts = []
        for cv in ct:
            pts.append(points[cv,:])
        pts = np.array(pts)
        allin += eval_point_in_out(pts,test_pt,dtol)
        if allin != 0:
            return 1
    return 0
