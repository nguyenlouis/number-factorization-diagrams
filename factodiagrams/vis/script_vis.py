#%%
import math 
import matplotlib.pyplot as plt
from matplotlib import animation, rc


#%%
### Class

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x # Point x position
        self.y = y # Point y position

# Visualization class
class Vis:
	def __init__(self, number, speed):
		self.number = number # Actual number used to compute prime factors
		self.speed = speed # Animation speed

	# Compute prime factors using self.number
	def factors(self):
		return fours(self.number)

	# Compute points coordinates and return generated list of points
	def points(self):
		return generatePoints(self.factors())


### Def

# Compute prime factors
def prime_factors(n):
    i = 2
    factors = []
    # if n==1:
    #     factors.append(1)
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def fours(n):
    # Re groupement de 2x2 en 4
    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4

    return factors + prime_factors(n) 

# Compute radius of a point
def r(n):
    # n = number of small circles 
    s = math.sin(math.pi / n)
    return s / (s + 1)

# Generate and distribute points
def generatePoints(factors):
	# initialize variables
	parentPoints = []
	points = []
	a = 0
	x = 0
	y = 0
	da = 0

	point = 0
	n = 1
	d = 1

	if factors == [1] :
		return [Point(0,0)]
    
	# Instantiate points for each prime factors
	while (len(factors)):
		d = d * n * 0.85 # scale depth
		n = factors.pop() # build points from outwards

		# Compute offset
		if(n == 4):
		    da = - math.pi / 4 

		elif(n == 2):
		    da = - math.pi 
		else :
		    da = math.pi / 2

		if (len(points) == 0): # check for first set of points
		    for i in range(n):
		    	a = i * 2 * math.pi / n + da
		    	x = math.cos(a)
		    	y = math.sin(a)
		    	point = Point(x, y)
		    	points.append(point)
		else : # iteratively build points by keeping track of parentPoints
			if(n == 2): # rotation of groups of 2 to align with their parent points
				if (len(parentPoints) == 0): # for prime numbers times 2 (double circle) - aligned with absolute center (0,0)
					parentPoints = list(points) # create shallow copy of points
					points = [] # reset points
					for parentPoint in parentPoints :
						for i in range(n):
							x = parentPoint.x + (1-2*i)*parentPoint.x / d
							y = parentPoint.y + (1-2*i)*parentPoint.y / d
							point = Point(x, y)
							points.append(point)
				else: # for every other group of 2 - aligned with their 'grandparent points'
					parentPoints2 = list(points) # create shallow copy of points without deleting previous parent points ('grandparent points')
					points = [] # reset points
					j = 0
					for parentPoint2 in parentPoints2 :
						coef = len(parentPoints2)/len(parentPoints)
						for i in range(n):
							x = parentPoints[int(j//coef)].x + (parentPoint2.x - parentPoints[int(j//coef)].x) * (1.5-i*0.8)
							y = parentPoints[int(j//coef)].y + (parentPoint2.y - parentPoints[int(j//coef)].y) * (1.5-i*0.8)
							point = Point(x, y)
							points.append(point)
						j += 1
			else:
				parentPoints = list(points) # create shallow copy of points
				points = [] # reset points
				for parentPoint in parentPoints: # build new points using parentPoints
					for i in range(n):
						a = i * 2 * math.pi / n + da
						x = parentPoint.x + math.cos(a) / d
						y = parentPoint.y + math.sin(a) / d
						point = Point(x, y)
						points.append(point)
	return points





    
#%%
def animate(c):
    for n in range(2,c):
        circle(n)


#%% 
def circle(n):
    sub = []
    for i in range(n):
        # rainbow points
        if i < n/6 :
            red = 1
            green = 6*i/n
            blue = 0
        elif i < 2*n/6 :
            red = 1-6*(i-n/6)/n
            green = 1
            blue = 0
        elif i < 3*n/6 :
            red = 0
            green = 1
            blue = 6*(i-n/3)/n
        elif i < 4*n/6 :
            red = 0
            green = 1-6*(i-n/2)/n
            blue = 1
        elif i < 5*n/6 :
            red = 6*(i-2*n/3)/n
            green = 0
            blue = 1
        else :
            red = 1
            green = 0
            blue = 1-6*(i-5*n/6)/n
        
        pts = generatePoints(fours(n))
        circle = plt.Circle((pts[i].x, pts[i].y), radius=r(n), color=(red, green, blue))
        sub.append(ax.add_artist(circle))
    plt.pause(0.5)
    for s in sub:
        s.remove()


# suppr axes
fig, ax = plt.subplots()
plt.xlim(-2, 2)
plt.ylim(-2, 2)
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_aspect(1)
animate(30)
plt.show()


