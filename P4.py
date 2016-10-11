# CS 558 Assignment 4
# Author: Jieru Hu
# ID: 9070194544

import turtle
import math

#define a Vertex
class Vertex: 
	def __init__(self, point):
		self.x = point.x
		self.y = point.y
		self.pt = point
		self.edge = None
		
	def setEdge(self, edge):
		self.edge = edge
		

#define an edge
class Edge:
	def __init__(self, sv, ev):
		self.sv = sv
		self.ev = ev
		self.twin = None
		self.next = None
		self.prev = None
		self.face = None
		self.marked = False
		self.center = None
		self.tcenter = None
		self.drawn = False
		
	def settwin(self, twin):
		self.twin = twin
		
	def setnext(self, next): 
		self.next = next
	
	def setPre(self, prev):
		self.prev = prev
		
	def setTriangle(self, face):
		self.face = face

	def mark(self):
		self.marked = True
	
	def unmark(self):
		self.marked = False

	def setcenter(self,p1):
		self.center = p1

	def settcenter(self,p2):
		self.tcenter = p2

	def setdrawn(self):
		self.drawn = True

	def tostring(self):
		return "(" + str(self.sv.x) + "," + str(self.sv.y)+"), ("+str(self.ev.x) + ","+str(self.ev.y)+")"

#define a face (Triangle)
class Triangle:
	def __init__(self,edge):
		self.edge = edge

#define a point
class point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#define a vector
class vector:
	def __init__(self, u, v):
		self.u=u
		self.v=v

	def length(self):
		return pow(pow(abs(self.u),2) + pow(abs(self.v),2), 0.5)

#return the crossproduct of two vectors
def crossProduct(v1x, v1y, v2x, v2y):
	return (v1x*v2y - v2x*v1y)

#return the sine value of two vectors
def sinAngle(sv,ev):
	return crossProduct(sv.u,sv.v,ev.u,ev.v)/sv.length()/ev.length()

#returns the cosine value of two vectors
def cosAngle(sv, ev):
	return (sv.u*ev.u+sv.v*ev.v) / sv.length() / ev.length()

#returns a convex hull
def CreateCH(points):

	#find bottom left point
	extremeIndex = 0
	minx = points[0].x
	miny = points[0].y
	for i in range(1,len(points)): 
		if minx > points[i].x:
			extremeIndex = i
			minx = points[i].x
			miny = points[i].y
		if minx == points[i].x:
			if miny > points[i].y:
				etremeIndex = i
				minx = points[i].x
				miny = points[i].y
	
	#create convexHull
	convexHull = []
	#add first point
	convexHull.append(points[extremeIndex])

	
	#start with the extreme point and horizontal vector
	currV = vector(0,-1)
	currIndex = 0
	currCosAngle = 0
	currLength = 0
	currVertex = points[extremeIndex]
	
	incomplete = True
	while incomplete == True: 
	
		currCosAngle = -2
		#find point the forms smallest angle
		for point in points: 
			if point.x == currVertex.x and point.y == currVertex.y:
				continue
			tempCosAngle = cosAngle(currV, vector(point.x-currVertex.x, point.y-currVertex.y))
			tempLength = vector(point.x-currVertex.x, point.y-currVertex.y).length()
			
			if tempCosAngle - currCosAngle > 0.00000001:
				currCosAngle = tempCosAngle
				currLength = tempLength
				currPoint = point
			else:
				if  abs(tempCosAngle - currCosAngle) < 0.00000001:
					if tempLength > currLength:
						currCosAngle = tempCosAngle
						currLength = tempLength
						currPoint = point
						
		#check if the algorithm is finished
		if currPoint.x == minx and currPoint.y == miny:
			incomplete = False
			break
		#if a point is found and it is not the start point:
		#add point to convexHull		
		convexHull.append(currPoint)
		#update reference vector
		currV = vector(currPoint.x - currVertex.x, currPoint.y-currVertex.y)
		#update angle Vertex
		currVertex = currPoint	

	return convexHull	
	
#checks the position of the point with respect to the triangle
#return -1 if the point lies outside of the Triangle
#return 0 if the point lies inside the Triangle
#return 1 if the point lies on the fist edge of Triangle
#return 2 if the point lies on the second edge of Triangle
#return 3 if the point lies on the third edge of Triangle
def inTriangle(Triangle,point):
	e1 = Triangle.edge
	e2 = e1.next
	e3 = e2.next
	
	cp1 = crossProduct(e1.ev.x-e1.sv.x,e1.ev.y-e1.sv.y, point.x-e1.sv.x,point.y-e1.sv.y)

	if cp1 == 0:
		check1 = abs(point.x-e1.ev.x) + abs(point.x-e1.sv.x) - abs(e1.ev.x-e1.sv.x)
		check2 = abs(point.y-e1.ev.y) + abs(point.y-e1.sv.y) - abs(e1.ev.y-e1.sv.y)
		if check1 == 0 and check2 == 0: 
			return 1
				

	cp2 = crossProduct(e2.ev.x-e2.sv.x,e2.ev.y-e2.sv.y, point.x-e2.sv.x,point.y-e2.sv.y)

	if cp2 == 0: 
		check1 = abs(point.x-e2.ev.x) + abs(point.x-e2.sv.x) - abs(e2.ev.x-e2.sv.x)
		check2 = abs(point.y-e2.ev.y) + abs(point.y-e2.sv.y) - abs(e2.ev.y-e2.sv.y)
		if check1 == 0 and check2 == 0: 
			return 2
				

	cp3 = crossProduct(e3.ev.x-e3.sv.x,e3.ev.y-e3.sv.y, point.x-e3.sv.x,point.y-e3.sv.y)

	if cp3 == 0: 
		check1 = abs(point.x-e3.ev.x) + abs(point.x-e3.sv.x) - abs(e3.ev.x-e3.sv.x)
		check2 = abs(point.y-e3.ev.y) + abs(point.y-e3.sv.y) - abs(e3.ev.y-e3.sv.y)
		if check1 == 0 and check2 == 0: 
			return 3
	

	if cp1>0 and cp2>0 and cp3>0:
		return 0 

	return -1
	
#triangulate the points
def triangulate(points):
	#create the convex hull of the points
	ch = CreateCH(points)
	#create a list that stores the Triangularlists	
	Triangularlist = []
	

	#create vertices 
	sv = Vertex(ch[0])
	ev = Vertex(ch[1])
	v3 = Vertex(ch[2])
	#create new edges and link to vertices
	e1 = Edge(sv,ev)
	sv.setEdge(e1)
	e2 = Edge(ev,v3)
	ev.setEdge(e2)
	e3 = Edge(v3,sv)
	v3.setEdge(e3)
	#create twin edges and link them
	twe1 = Edge(ev,sv)
	twe2 = Edge(v3,ev)
	twe3 = Edge(sv,v3)
	e1.settwin(twe1)
	e2.settwin(twe2)
	e3.settwin(twe3)
	twe1.settwin(e1)
	twe2.settwin(e2)
	twe3.settwin(e3)
	#set prev and next half edges
	e1.setnext(e2)
	e2.setnext(e3)
	e3.setnext(e1)
	e1.setPre(e3)
	e2.setPre(e1)
	e3.setPre(e1)
	#create a Triangle
	tri = Triangle(e1)

	e1.setTriangle(tri)
	e2.setTriangle(tri)
	e3.setTriangle(tri)
	#add the Triangle
	Triangularlist.append(tri)
	

	if len(ch)>3:
		#for rest of points on ch, create Triangles and add to Triangularlist
		for i in range(3, len(ch)): 
			#create vertices
			v = Vertex(ch[i])
			#create edges
			e1 = Triangularlist[len(Triangularlist)-1].edge.prev.twin
			e2 = Edge(e1.ev,v)
			e3 = Edge(v,e1.sv)
			#link the edges
			e1.setnext(e2)
			e2.setnext(e3)
			e3.setnext(e1)
			e1.setPre(e3)
			e2.setPre(e1)
			e3.setPre(e1)
			#create twin edges for new to half edges
			e2twin = Edge(v,e1.ev)
			e3twin = Edge(e1.sv,v)
			#link twin edges
			e2.settwin(e2twin)
			e2twin.settwin(e2)
			e3.settwin(e3twin)
			e3twin.settwin(e3)
			#create the Triangle and add to list
			tri = Triangle(e1)
			#set each half edge to point to the face
			e1.setTriangle(tri)
			e2.setTriangle(tri)
			e3.setTriangle(tri)
			Triangularlist.append(tri)
			
	#get the points that lie inside the convex hull and store into a list inner
	inner = []
	for i in range(0,len(points)): 
		if points[i] not in ch: 
			inner.append(points[i])

				
	#Add each point in the Inner into the triangulation
	for i in range(0,len(inner)): 

		for j in range(0,len(Triangularlist)):
			check = inTriangle(Triangularlist[j],inner[i])
			
			#if point is outside of the Triangle, check next Triangle
			if check == -1: 
				continue
				
			#Point int completely inside the triangle
			if check == 0: 
				e1 = Triangularlist[j].edge
				e2 = e1.next
				e3 = e2.next
				v = Vertex(inner[i])
				

				#first the edges set bound the Triangle
				t1e1 = e1
				t1e2 = Edge(e1.ev,v)
				t1e3 = Edge(v,e1.sv)

				v.setEdge(t1e2)

				t1e1.setnext(t1e2)
				t1e2.setnext(t1e3)
				t1e3.setnext(t1e1)
				t1e1.setPre(t1e3)
				t1e3.setPre(t1e2)
				t1e2.setPre(t1e1)
				

				t1 = Triangle(t1e1)
				Triangularlist.append(t1)
				#set edges to point to the face they bound
				t1e1.setTriangle(t1)
				t1e2.setTriangle(t1)
				t1e3.setTriangle(t1)
				
				
				#connect Vertex to e2 and form second Triangle and add to Triangularlist
				#first create the edges that bound t2
				t2e1 = e2
				t2e2 = Edge(e2.ev,v)
				t2e3 = Edge(v,e2.sv)
				#connect the edges
				t2e1.setnext(t2e2)
				t2e2.setnext(t2e3)
				t2e3.setnext(t2e1)
				t2e1.setPre(t2e3)
				t2e3.setPre(t2e2)
				t2e2.setPre(t2e1)
				
				#create the Triangle and add to list
				t2 = Triangle(t2e1)
				Triangularlist.append(t2)
				#set edges to point to the face they bound
				t2e1.setTriangle(t2)
				t2e2.setTriangle(t2)
				t2e3.setTriangle(t2)
				
				#connect Vertex to e3 and form third Triangle and add to Triangularlist
				#first create the edges that bound t3
				t3e1 = e3
				t3e2 = Edge(e3.ev,v)
				t3e3 = Edge(v,e3.sv)
				#connect the edges
				t3e1.setnext(t3e2)
				t3e2.setnext(t3e3)
				t3e3.setnext(t3e1)
				t3e1.setPre(t3e3)
				t3e3.setPre(t3e2)
				t3e2.setPre(t3e1)
				
				#create the Triangle and add to list
				t3 = Triangle(t3e1)
				Triangularlist.append(t3)
				#set half edges to point to the face they bound
				t3e1.setTriangle(t3)
				t3e2.setTriangle(t3)
				t3e3.setTriangle(t3)
				
				#link the edges that are twins
				t1e2.settwin(t2e3)
				t2e3.settwin(t1e2)
				t2e2.settwin(t3e3)
				t3e3.settwin(t2e2)
				t3e2.settwin(t1e3)
				t1e3.settwin(t3e2)
				
				Triangularlist.pop(j)
				break

			#Point are exactly on the edge of the triangle
			else: 
				if check == 1: 
					e1 = Triangularlist[j].edge
					e2 = e1.next
					e3 = e2.next
					v = Vertex(inner[i])
				
				if check == 2: 
					e1 = Triangularlist[j].edge.next
					e2 = e1.next
					e3 = e2.next
					v = Vertex(inner[i])
				
				if check == 3: 
					e1 = Triangularlist[j].edge.prev
					e2 = e1.next
					e3 = e2.next
					v = Vertex(inner[i])
					 

				#first the edges set bound the Triangle
				t1e1 = e2
				t1e2 = Edge(e2.ev,v)
				t1e3 = Edge(v,e1.ev)

				t1e1.setnext(t1e2)
				t1e2.setnext(t1e3)
				t1e3.setnext(t1e1)
				t1e1.setPre(t1e3)
				t1e3.setPre(t1e2)
				t1e2.setPre(t1e1)
				#create the Triangle
				t1 = Triangle(t1e1)
				Triangularlist.append(t1)

				t1e1.setTriangle(t1)
				t1e2.setTriangle(t1)
				t1e3.setTriangle(t1)
				

				#first create the edges that bound t2
				t2e1 = e3
				t2e2 = Edge(e3.ev,v)
				t2e3 = Edge(v,e3.sv)

				t2e1.setnext(t2e2)
				t2e2.setnext(t2e3)
				t2e3.setnext(t2e1)
				t2e1.setPre(t2e3)
				t2e3.setPre(t2e2)
				t2e2.setPre(t2e1)

				t2 = Triangle(t2e1)
				Triangularlist.append(t2)

				t2e1.setTriangle(t2)
				t2e2.setTriangle(t2)
				t2e3.setTriangle(t2)
				
				#check if the twin edge is bounded to a triangle
				if not e1.twin.next is None: 
					e4 = e1.twin
					e5 = e4.next
					e6 = e5.next
					
					for k in range(0,len(Triangularlist)):
						#if the Triangle has the same edge remove the Triangle and end the loop
						temp1 = Triangularlist[k].edge
						temp2 = temp1.next
						temp3 = temp2.next
						if temp1.sv.x == e4.sv.x and temp1.sv.y == e4.sv.y and temp1.ev.x == e4.ev.x and temp1.ev.y == e4.ev.y: 
							Triangularlist.pop(k)
							break
						if temp2.sv.x == e4.sv.x and temp2.sv.y == e4.sv.y and temp2.ev.x == e4.ev.x and temp2.ev.y == e4.ev.y: 
							Triangularlist.pop(k)
							break
						if temp3.sv.x == e4.sv.x and temp3.sv.y == e4.sv.y and temp3.ev.x == e4.ev.x and temp3.ev.y == e4.ev.y: 
							Triangularlist.pop(k)
							break
					

					t3e1 = e5
					t3e2 = Edge(e5.ev,v)
					t3e3 = Edge(v,e5.sv)

					t3e1.setnext(t3e2)
					t3e2.setnext(t3e3)
					t3e3.setnext(t3e1)
					t3e1.setPre(t3e3)
					t3e3.setPre(t3e2)
					t3e2.setPre(t3e1)

					t3 = Triangle(t3e1)
					Triangularlist.append(t3)

					t3e1.setTriangle(t3)
					t3e2.setTriangle(t3)
					t3e3.setTriangle(t3)
					

					t4e1 = e6
					t4e2 = Edge(e6.ev,v)
					t4e3 = Edge(v,e6.sv)

					t4e1.setnext(t4e2)
					t4e2.setnext(t4e3)
					t4e3.setnext(t4e1)
					t4e1.setPre(t4e3)
					t4e3.setPre(t4e2)
					t4e2.setPre(t4e1)
					t4 = Triangle(t4e1)
					Triangularlist.append(t4)
					t4e1.setTriangle(t4)
					t4e2.setTriangle(t4)
					t4e3.setTriangle(t4)

					t1e3.settwin(t4e2)
					t4e2.settwin(t1e3)
					t4e3.settwin(t3e2)
					t3e2.settwin(t4e3)
					t3e3.settwin(t2e2)
					t2e2.settwin(t3e3)
					t2e3.settwin(t1e2)
					t1e2.settwin(t2e3)
					
					#remove
					
				
				#link the twin edges as follow
				else: 
					t1e2.settwin(t2e3)
					t2e3.settwin(t1e2)
					t2e2twin = Edge(v,e1.sv)
					t2e2.settwin(t2e2twin)
					t2e2twin.settwin(t2e2)
					t1e3twin = Edge(e1.ev,v)
					t1e3.settwin(t1e3twin)
					t1e3twin.settwin(t1e3)
					
				#remove the Triangle
				Triangularlist.pop(j)
				break
			break	
		
	return Triangularlist

#use turtle to draw the triangulation
def draw(Triangles, points):
	#input check
	if Triangles is None or points is None: 
		print("Input to visual is not valid")
		return 0
		
	#compute the suitable dimensions
	xdim = 0
	ydim = 0
	xmax = points[0].x
	xmin = points[0].x
	ymax = points[0].y
	ymin = points[0].y
	for point in points: 
		if point.x > xmax: 
			xmax = point.x
		if point.x < xmin: 
			xmin = point.x
		if point.y > ymax: 
			ymax = point.y
		if point.y < ymin: 
			ymin = point.y
	xdim = xmax - xmin
	ydim = ymax - ymin

	#use xdim and ydim to find the scaling factor (sf) for turtle
	if xdim > ydim: 
		sf = (600/xdim)
	else: 
		sf = (600/ydim)
	
	
	#setup turtle
	turtle.setup(xdim*sf*1.2+30, ydim*sf*1.2+30)
	wn = turtle.Screen()
	wn.bgcolor("black")
	
	#offset of screen 
	offsetx = xdim*sf/2+xmin*sf
	offsety = ydim*sf/2+ymin*sf
	
	#create invisible turtle 
	t = turtle.Turtle()
	t.color("white")
	t.penup()
	t.speed(9)
	
	#draw the Triangles
	for tri in Triangles: 
		t.setposition(tri.edge.sv.x*sf-offsetx,tri.edge.sv.y*sf-offsety)
		t.pendown()
		t.setposition(tri.edge.next.sv.x*sf-offsetx,tri.edge.next.sv.y*sf-offsety)
		t.setposition(tri.edge.next.next.sv.x*sf-offsetx,tri.edge.next.next.sv.y*sf-offsety)
		t.setposition(tri.edge.sv.x*sf-offsetx,tri.edge.sv.y*sf-offsety)
		t.penup()
		
	wn.exitonclick()

#Calculate the determinant to determine if the given edge is Delaunay
def isLocallyDelaunay(e1): 

	if e1.next is None or e1.twin.next is None: 
		return True

	sv = e1.sv
	ev = e1.ev
	v3 = e1.next.ev
	v4 = e1.twin.next.ev
	#determinant test
	a = sv.x-v4.x
	b = sv.y-v4.y
	c = pow(sv.x,2) - pow(v4.x,2) + pow(sv.y,2) - pow(v4.y,2)
	d = ev.x-v4.x
	e = ev.y-v4.y
	f = pow(ev.x,2) - pow(v4.x,2) + pow(ev.y,2) - pow(v4.y,2)
	g = v3.x-v4.x
	h = v3.y-v4.y
	i = pow(v3.x,2) - pow(v4.x,2) + pow(v3.y,2) - pow(v4.y,2)
	
	if a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h > 0: 
		return False
	else:
		return True


# Returns a Delaunay triangulation
def makeDelaunay(Triangles): 
	
	#create a stack to keep track of non-locally delaunay edges that needs checking
	stack = []
	
	#for every edge in the Triangularlist
	for tri in Triangles: 
		e1 = tri.edge
		e2 = e1.next
		e3 = e2.next
		
		#skinner e1 if e1 is already marked
		if not e1.marked == True: 
			#check if e1 is not locally delauney
			if not isLocallyDelaunay(e1): 
				e1.mark()
				e1.twin.mark()
				stack.append(e1)
		
		#skinner e2 if e2 is already marked
		if not e2.marked == True: 
			#check if e2 is not locally delauney
			if not isLocallyDelaunay(e2): 
				e2.mark()
				e2.twin.mark()
				stack.append(e2)
		
		#skinner e3 if e3 is already marked
		if not e3.marked == True: 
			#check if e3 is not locally delauney
			if not isLocallyDelaunay(e3): 
				e3.mark()
				e3.twin.mark()
				stack.append(e3)
				

	while not len(stack)==0:
		#pop an half edge
		e = stack.pop()
		#unmark the half edge
		e.unmark()
		#check delaunay
		if isLocallyDelaunay(e): 
			continue 
		else: 
			#edge is not locally delaunay

			etwin = e.twin
			

			Triangles.remove(e.face)
			Triangles.remove(etwin.face)

			#original boundaries of the quad in ccw
			e1 = e.next
			e2 = e1.next
			e3 = etwin.next
			e4 = e3.next
			#create two edges
			enew = Edge(e3.ev, e1.ev)
			enewtwin = Edge(e1.ev, e3.ev)
			
			#link twin edges
			enew.settwin(enewtwin)
			enewtwin.settwin(enew)
			

			#first Triangle next and prev edges
			e2.setnext(e3)
			e3.setnext(enew)
			enew.setnext(e2)
			e2.setPre(enew)
			enew.setPre(e3)
			e3.setPre(e2)
			#second Triangle next and prev edges
			e1.setnext(enewtwin)
			enewtwin.setnext(e4)
			e4.setnext(e1)
			e1.setPre(e4)
			e4.setPre(enewtwin)
			enewtwin.setPre(e1)
			
			#create first Triangle
			t1 = Triangle(e2)
			#set half edges face pointers
			e2.setTriangle(t1)
			e3.setTriangle(t1)
			enew.setTriangle(t1)
			
			#create second Triangle
			t2 = Triangle(e1)
			#set half edges face pointers
			e1.setTriangle(t2)
			enewtwin.setTriangle(t2)
			e4.setTriangle(t2)
			
			#add both Triangles 
			Triangles.append(t1)
			Triangles.append(t2)
			
			#push four edges into stack if they are unmarked
			if e1.marked == False:
				e1.mark()
				stack.append(e1)
			if e2.marked == False:
				e2.mark()
				stack.append(e2)
			if e3.marked == False:
				e3.mark()
				stack.append(e3)
			if e4.marked == False:
				e4.mark()
				stack.append(e4)

#computer the circumcircle formed by p1, p2, p3
def computeCenter(p1x,p1y,p2x,p2y,p3x,p3y):
	# compute the x-coordinate of the center
	x1 = computeDeterminant(pow(p1x,2)+pow(p1y,2),p1y,1,pow(p2x,2)+pow(p2y,2),p2y,1,pow(p3x,2)+pow(p3y,2),p3y,1)
	x2 = 2*computeDeterminant(p1x, p1y, 1, p2x, p2y, 1, p3x, p3y, 1)
	x = x1/x2
	# compute the x-coordinate of the center
	y1 = computeDeterminant(p1x,pow(p1x,2)+pow(p1y,2),1,p2x,pow(p2x,2)+pow(p2y,2),1,p3x,pow(p3x,2)+pow(p3y,2),1)
	y = y1/x2
	return point(x,y)

#returns true if the point to the right of the vector
def toRight(v1,v2,point):
	vector1 = [point[0]-v1[0], point[1]-v1[1]]
	vector2 = [v2[0] - v1[0], v2[1] - v1[1]]
	cp = crossProduct(vector1[0],vector1[1],vector2[0],vector2[1])
	if cp > 0:
		return True
	else:
		return False

#draw the shape for part b
def drawShape(Triangles,bound,points):
	if Triangles is None or points is None:
		print("Input to visual is not valid")
		return 0
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	xdimension = xmax - xmin
	ydimension = ymax - ymin
	if xdimension > ydimension:
		sf = (1000/xdimension)
	else:
		sf = (1000/ydimension)

	#setup turtle
	turtle.setup(xdimension*sf, ydimension*sf)
	wn = turtle.Screen()
	wn.bgcolor("black")
	wn.title("Shape")

	#set up the offset
	offsetx = (xmin+xmax)*sf/2
	offsety = (ymin+ymax)*sf/2

	#create invisible turtle
	t = turtle.Turtle()
	t.color("white")
	t.penup()
	t.speed(15)

	t.tracer(10,0)
	#draw the points
	for p in points:
		t.setposition(p.x*sf-offsetx,p.y*sf-offsety)
		t.pendown()
		t.dot(2,"red")
		t.penup()

	#draw the boundary
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.pendown()
	t.setposition(xmin*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymin*sf-offsety)
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.penup()

	for tri in Triangles:
		tri.edge.unmark()
		tri.edge.next.unmark()
		tri.edge.prev.unmark()

	#draw the voronoi diagram
	for tri in Triangles:
		e = tri.edge

		for i in range(3):

			if e.marked == False:
				e.mark()
				e.twin.mark()
				a = e.sv.pt
				b = e.ev.pt
				c = e.center
				d = e.tcenter
				ptodraw = decideEdge(a,b,c,d)
				p1 = ptodraw[0]
				p2 = ptodraw[1]
				if e.twin.face == None:
					p1 = a
					p2 = b
				t.setposition(p1.x*sf-offsetx,p1.y*sf-offsety)
				t.pendown()
				t.setposition(p2.x*sf-offsetx,p2.y*sf-offsety)
				t.penup()
			e = e.next
	t._update()
	#wn.bye()
	wn.exitonclick()



#given the endpoints of the delaunay edge a and b, and dual endpoints c and d
#return the correct edge to draw
def decideEdge(pa,pb,pc,pd):
	#vector from b to a
	btoa = vector(pa.x-pb.x,pa.y-pb.y)
	btoc = vector(pc.x-pb.x,pc.y-pb.y)
	btod = vector(pd.x-pb.x,pd.y-pb.y)
	cpc = crossProduct(btoc.u,btoc.v,btoa.u,btoa.v)
	cpd = crossProduct(btod.u,btod.v,btoa.u,btoa.v)


	sv = pa
	ev = pb
	v3 = pc
	v4 = pd

	#determinant test
	a = sv.x-v4.x
	b = sv.y-v4.y
	c = pow(sv.x,2) - pow(v4.x,2) + pow(sv.y,2) - pow(v4.y,2)
	d = ev.x-v4.x
	e = ev.y-v4.y
	f = pow(ev.x,2) - pow(v4.x,2) + pow(ev.y,2) - pow(v4.y,2)
	g = v3.x-v4.x
	h = v3.y-v4.y
	i = pow(v3.x,2) - pow(v4.x,2) + pow(v3.y,2) - pow(v4.y,2)

	if a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h > 0:
		#return delaunay edge
		return [pc,pd]
	else:
		#return dual edge
		return [pa,pb]



# draw the Voronoi diagram based on the Triangles data structure
def drawVoronoi(Triangles,bound,points):


	if Triangles is None or points is None:
		print("Input to visual is not valid")
		return 0
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	xdimension = xmax - xmin
	ydimension = ymax - ymin
	if xdimension > ydimension:
		sf = (1000/xdimension)
	else:
		sf = (1000/ydimension)

	#setup turtle
	turtle.setup(xdimension*sf, ydimension*sf)
	wn = turtle.Screen()
	wn.bgcolor("black")
	wn.title("Voronoi diagram")

	#set up the offset
	offsetx = (xmin+xmax)*sf/2
	offsety = (ymin+ymax)*sf/2

	#create invisible turtle
	t = turtle.Turtle()
	t.color("white")
	t.penup()
	t.speed(15)

	t.tracer(10,0)
	#draw the points
	for p in points:
		t.setposition(p.x*sf-offsetx,p.y*sf-offsety)
		t.pendown()
		t.dot(2,"red")
		t.penup()

	#draw the boundary
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.pendown()
	t.setposition(xmin*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymin*sf-offsety)
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.penup()


	#draw the voronoi diagram
	for tri in Triangles:
		e = tri.edge
		for i in range(3):
			if e.drawn == False:
				#draw each dual edge
				center = e.center
				tcenter = e.tcenter
				#print e.tostring()
				t.setposition(center.x*sf-offsetx,center.y*sf-offsety)
				t.pendown()
				t.setposition(tcenter.x*sf-offsetx,tcenter.y*sf-offsety)
				e.twin.setdrawn()
				t.penup()

			e = e.next
	t._update()
	#wn.bye()
	wn.exitonclick()


#compute a larger rectangle to enclose all the points within the boundary
def computeBound(Points):

	xmax = Points[0].x
	xmin = Points[0].x
	ymax = Points[0].y
	ymin = Points[0].y
	#compute the largest max x, min x, max y and min y
	for point in Points:
		if point.x > xmax:
			xmax = point.x
		if point.x < xmin:
			xmin = point.x
		if point.y > ymax:
			ymax = point.y
		if point.y < ymin:
			ymin = point.y

	xdimension = xmax - xmin
	ydimension = ymax - ymin

	xmin = xmin - 0.2*xdimension
	xmax = xmax + 0.2*xdimension
	ymin = ymin - 0.2*ydimension
	ymax = ymax + 0.2*ydimension

	return [xmin, xmax, ymin, ymax]


#draw the crust algorithm
def drawcrust(edgelist,totalpoints,bound):
	if edgelist is None or totalpoints is None:
		print("Input to visual is not valid")
		return 0
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	xdimension = xmax - xmin
	ydimension = ymax - ymin
	if xdimension > ydimension:
		sf = (1000/xdimension)
	else:
		sf = (1000/ydimension)

	#setup turtle
	turtle.setup(xdimension*sf, ydimension*sf)
	wn = turtle.Screen()
	wn.bgcolor("black")
	wn.title("Crust")


	#set up the offset
	offsetx = (xmin+xmax)*sf/2
	offsety = (ymin+ymax)*sf/2

	#create invisible turtle
	t = turtle.Turtle()
	t.color("white")
	t.penup()
	t.speed(15)

	t.tracer(50,0)
	#draw the points
	for p in totalpoints:
		t.setposition(p.x*sf-offsetx,p.y*sf-offsety)
		t.pendown()
		t.dot(2,"red")
		t.penup()

	#draw the boundary
	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	t.color("blue")
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.pendown()
	t.setposition(xmin*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymax*sf-offsety)
	t.setposition(xmax*sf-offsetx, ymin*sf-offsety)
	t.setposition(xmin*sf-offsetx, ymin*sf-offsety)
	t.penup()

	t.color("white")
	#draw the voronoi diagram
	for edge in edgelist:
		p1 = edge[0]
		p2 = edge[1]
		t.setposition((p1.x)*sf-offsetx,(p1.y)*sf-offsety)
		t.pendown()
		t.setposition((p2.x)*sf-offsetx,(p2.y)*sf-offsety)
		t.penup()

	t._update()

	wn.exitonclick()



# compute the determinant of a 3*3 matrix given the matrix in the scanline order
def computeDeterminant(a,b,c,d,e,f,g,h,i):
	return (a*e*i + b*f*g + c*d*h  -c*e*g - b*d*i -a*f*h)

def crust(triangles,points):
	crustpoints = []

	s = set()

	#save the points from triangulation
	for p in points:
		crustpoints.append(p)
		s.add(p)

	#save the points from the voronoi diagram
	for tri in triangles:
		crustpoints.append((tri.edge.center))

	crustTriangles = triangulate(crustpoints)

	makeDelaunay(crustTriangles)

	crustedges = []

	#unmark all the points
	for tri in triangles:
		tri.edge.unmark()
		tri.edge.next.unmark()
		tri.edge.prev.unmark()

	#add the edge to the list if the end points are all in s
	for ctri in crustTriangles:
		ce1 = ctri.edge
		ce2= ce1.next
		ce3 = ce2.next

		if ce1.marked == False:
			if ce1.sv.pt in s and ce1.ev.pt in s:
				crustedges.append([ce1.sv.pt,ce1.ev.pt])
				ce1.mark()
				ce1.twin.mark()

		if ce2.marked == False:
			if ce2.sv.pt in s and ce2.ev.pt in s:
				crustedges.append([ce2.sv.pt,ce2.ev.pt])
				ce2.mark()
				ce2.twin.mark()

		if ce3.marked == False:
			if ce3.sv.pt in s and ce3.ev.pt in s:
				crustedges.append([ce3.sv.pt,ce3.ev.pt])
				ce3.mark()
				ce3.twin.mark()
	return crustedges

# compute the voronoi diagram of the triangulation, add center point to each triangle,
# find the dual edge for each edge and store them into the data structure
def computeVoronoi(Triangles, bound):

	xmin = bound[0]
	xmax = bound[1]
	ymin = bound[2]
	ymax = bound[3]
	# compute the center of each triangle and insert them
	for tri in Triangles:
		v1 = tri.edge.sv
		v2 = tri.edge.ev
		v3 = tri.edge.next.ev
		e1 = tri.edge
		e2 = e1.next
		e3 = e2.next
		center = computeCenter(v1.x,v1.y,v2.x,v2.y,v3.x,v3.y)
		e1.setcenter(center)
		e2.setcenter(center)
		e3.setcenter(center)

	for tri in Triangles:
		e = tri.edge
		for i in range(3):
			if e.twin.face is None:

				v1 = e.sv
				v2 = e.ev
				center = e.center
				mid = [(v1.x+v2.x)/2, (v1.y+v2.y)/2]
				# if the angle is 90 degree
				if center.x == mid[0] and v1.y == v2.y:
					x = center.x
					p1 = [x,ymin]
					p2 = [x,ymax]
					if toRight([v1.x,v1.y],[v2.x,v2.y],p1):
						e.settcenter(point(p1[0],p1[1]))
					if toRight([v1.x,v1.y],[v2.x,v2.y],p2):
						e.settcenter(point(p2[0],p2[1]))
				#if the angle is not 90 degree
				elif center.y == mid[1] and v1.x == v2.x:
					y =center.y
					p1 = [xmin,y]
					p2 = [xmax,y]
					if toRight([v1.x,v1.y],[v2.x,v2.y],p1):
						e.settcenter(point(p1[0],p1[1]))
					if toRight([v1.x,v1.y],[v2.x,v2.y],p2):
						e.settcenter(point(p2[0],p2[1]))
				#the midpoint and the center coincide



				else:
					if center.x == mid[0] and center.y == mid[1]:
						slope1 = (v2.y-v1.y)/(v2.x-v1.x)
						#compute the coefficient of the list
						a = -1/slope1
						b = center.y - a*center.x
					else:
						#compute the coefficient of the list
						a = (mid[1] - center.y)/(mid[0]-center.x)
						b = mid[1] - a*mid[0]
					#print a,b
					list = []
					list.append([xmin, a*xmin+b])
					list.append([xmax, a*xmax+b])
					list.append([(ymin-b)/a,ymin])
					list.append([(ymax-b)/a,ymax])

					list2 = []
					for i in list:
						if toRight([v1.x,v1.y],[v2.x,v2.y],i):
							list2.append(i)
					p1 = list2[0]
					p2 = list2[1]
					vector1 = vector(p1[0]-mid[0],p1[1]-mid[1])
					vector2 = vector(p2[0]-mid[0],p2[1]-mid[1])
					if vector1.length() > vector2.length():
						e.settcenter(point(p2[0],p2[1]))
					else:
						e.settcenter(point(p1[0],p1[1]))

			else:

				e.settcenter(e.twin.center)

			e = e.next

def main():

	file = open("testPoints.txt", "r")
	points=[]
	'''
	for i in range(0,63):
		x = 16*pow(math.sin(float(i)/10),3)
		y = 13*math.cos(float(i)/10)-5*math.cos(2*float(i)/10)-2*math.cos(3*float(i)/10)-math.cos(4*float(i)/10)
		print x,y
		points.append(point(x,y))
	'''
	#read input and create points and store into list


	'''
	#this portion of code is to read input file of format: x,y
	for line in file: 
		splitted = line.split(',')
		points.append(point(float(splitted[0]),float(splitted[1])))
		
		
	'''

	for line in file: 
		splitted = line.split()
		if len(splitted)==0:
			continue

		points.append(point(float(splitted[0]),float(splitted[1])))

	
	#create the convex hull
	ch = CreateCH(points)
	
	#do the triangulation
	Triangles = triangulate(points)
	
	#convert to Delaunay
	makeDelaunay(Triangles)

	#compute the boundary of the points
	bounds = computeBound(points)

	#compute voronoi diagram of the delaunay triangulation (fill in the new fields in the triangle)
	computeVoronoi(Triangles,bounds)

	#draw voronoi diagram
	drawVoronoi(Triangles,bounds,points)

	#draw the shape
	#drawShape(Triangles,bounds,points)

	#crust algorithm
	#get the union of points from delaunay triangulation vertex and voronoi diagram vertex

	#crustedges = crust(Triangles,points)
	#drawcrust(crustedges,points,bounds)

	#output results from Triangularlist
	#print("The number of Triangles is " + str(len(Triangles)))
	#print("The number of vertices is " + str(len(points)))
	#print("The number of edges is " + str((len(Triangles)*3+len(ch)) /2))
	
	#visualisation
	#draw(Triangles, points)
	#print "end"
	
if __name__ == "__main__":
	main()	