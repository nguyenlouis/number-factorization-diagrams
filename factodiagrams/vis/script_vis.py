# %%
import math
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.widgets import Button

### Class

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x  # Point x position
        self.y = y  # Point y position


class Draw:

    fps = 60  # Animation framerate
    animation_duration = 0.3
    pause_duration = 0.6  # Pause duration at animation end
    fig = None
    ax = None
    buttons = {}
    txt = None  # Text Artist
    speed_txt = None  # Text Artist => Display speed speed

    points = []
    target_positions = []

    status = 'pause'
    speed = 1  # Animation speed speed
    n = 1

    def __init__(self, fps=60, animation_duration=0.3, pause_duration=0.6):
        self.fps = fps
        self.animation_duration = animation_duration
        self.pause_duration = pause_duration
        self.fig, self.ax = plt.subplots()
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        # Hide axis
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_aspect(1)
        # Event on close window
        self.fig.canvas.mpl_connect('close_event', self.on_close)

        # Create buttons
        self.buttons['prev'] = Button(
            plt.axes([0.59, 0.05, 0.1, 0.075]), 'Sp. -')
        self.buttons['next'] = Button(
            plt.axes([0.81, 0.05, 0.1, 0.075]), 'Sp. +')
        self.buttons['play'] = Button(
            plt.axes([0.7, 0.05, 0.1, 0.075]), 'Play')

        # Buttons on click events
        self.buttons['prev'].on_clicked(self.decrease_speed)
        self.buttons['next'].on_clicked(self.increase_speed)
        self.buttons['play'].on_clicked(self.play_pause)

        self.frame(self.n)
        self.play_pause(None)
        plt.show()

    def on_close(self, e):
        exit(0)

    def play_pause(self, e):
        if self.status == 'pause':
            self.status = 'play'
        else:
            self.status = 'pause'
        self.buttons['play'].label.set_text(
            "Play" if self.status == 'play' else "Pause")
        while 1:
            if self.status == 'pause':
                return
            self.display_next_iter()

    def display_next_iter(self):
        if self.speed > 0:
            self.n = self.n + 1
        else:
            if self.n > 1:
                self.n = self.n - 1
            else:
                self.play_pause(None)
        self.frame(self.n, True if self.speed < 1 else False)

    # Vit+ button event on_clicked => increase speed and display speed text
    def increase_speed(self, e):
        if self.speed == -1:
            self.speed = 1
        else:
            self.speed = self.speed + 1
        self.display_speed()

    # Vit- button event on_clicked => decrease speed and display speed text
    def decrease_speed(self, e):
        if self.speed == 1:
            self.speed = -1
        else:
            self.speed = self.speed - 1
        self.display_speed()

    # Display text with n and factors
    def display_text(self, n, factors):
        # Remove text if exists
        if self.txt:
            Artist.remove(self.txt)
        # Text displays:
        #  - n
        #  - factors, joined with ' x '
        #  - factor divided by '2 x 2' if equals 4
        #  - 'prime' if n is prime number
        if n == 1:
            f = ' '
        elif n == 4:
            f = '(2 x 2)'
        else:
            f = '({0})'.format(' x '.join(('2 x 2' if x == 4 else str(x))
                                          for x in factors) if len(factors) > 1 else "prime")
        self.txt = plt.text(-1.1, 1.5, '{0} {1}'.format(self.n, f))

    # Display speed text
    def display_speed(self):
        # Remove text if exists
        if self.speed_txt:
            Artist.remove(self.speed_txt)
        self.speed_txt = plt.text(-1.1, 1.1,
                                  'Speed : {0}'.format(str(self.speed)))

    def generate_color(self, i, n):  # creates RGB code that covers the entire color spectrum
        if i < n / 6:
            red = 1
            green = 6 * i / n
            blue = 0
        elif i < 2 * n / 6:
            red = 1 - 6 * (i - n / 6) / n
            green = 1
            blue = 0
        elif i < 3 * n / 6:
            red = 0
            green = 1
            blue = 6 * (i - n / 3) / n
        elif i < 4 * n / 6:
            red = 0
            green = 1 - 6 * (i - n / 2) / n
            blue = 1
        elif i < 5 * n / 6:
            red = 6 * (i - 2 * n / 3) / n
            green = 0
            blue = 1
        else:
            red = 1
            green = 0
            blue = 1 - 6 * (i - 5 * n / 6) / n
        return red * 0.5, green * 0.5, blue * 0.5  # 50% to decrease brightness

    # Compute positions and display each points at each frame
    def frame(self, n, reverse=False):
        # Generate factors
        factors = fours(n)

        # Display text with N and factors
        self.display_text(n, factors)
        # Display animation speed
        self.display_speed()

        pts = generatePoints(factors)

        # Only display points at start
        if not self.points:
            self.points = pts
            self.display_points(self.points)
            plt.pause((self.pause_duration * 1 / abs(self.speed)))
        else:
            self.target_positions = pts
            total_frames = int(
                (self.animation_duration * 1 / abs(self.speed)) * self.fps)
            # Compute each point new position for each frame
            for f in range(total_frames):
                curr_pos = []
                points_count = len(self.points)
                if reverse:
                    points_count = points_count - 1
                for i in range(points_count):
                    curr_pos.append(self.compute_current_position(
                        self.points[i], self.target_positions[i], total_frames, f))
                # Position for last point
                curr_pos.append(self.compute_current_position(self.points[len(
                    self.points) - 1], self.target_positions[len(self.target_positions) - 1], total_frames, f))
                # Display all points for this frame
                self.display_points(curr_pos)
                plt.pause(1 / self.fps)
            plt.pause((self.pause_duration * 1 / abs(self.speed)))
            self.points = self.target_positions

    # Compute point position at the frame current_frame
    def compute_current_position(self, o, t, total_frames, current_frame):
        x = o.x + ((t.x - o.x) / total_frames) * (current_frame + 1)
        y = o.y + ((t.y - o.y) / total_frames) * (current_frame + 1)
        return Point(x, y)

    # Clear previous points and display new points
    def display_points(self, points):
        while self.ax.artists != []:
            self.ax.artists[0].remove()
        n = len(points)
        for i, p in enumerate(points):
            red, green, blue = self.generate_color(i, n)
            circle = plt.Circle((p.x, p.y), radius=r(n),
                                color=(blue, green, red))
            self.ax.add_artist(circle)


### Def

# Compute prime factors
def prime_factors(n):
    i = 2
    factors = []
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
    if n == 1:
        return [1]
    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4

    return factors + prime_factors(n)

# Compute radius of a point


def r(n):
    # n = number of small circles
    if n == 1:
        return 1
    s = math.sin(math.pi / n)
    return s / (s + 1)

# Generate and distribute points`


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

    if factors == [1]:
        return [Point(0, 0)]
    # Instantiate points for each prime factors
    while (len(factors)):
        d = d * n * 0.85  # scale depth
        n = factors.pop()  # build points from outwards

        # Compute offset
        if(n == 4):
            da = - math.pi / 4

        elif(n == 2):
            da = - math.pi / 2
        else:
            da = math.pi / 2

        if (len(points) == 0):  # check for first set of points
            for i in range(n):
                a = i * 2 * math.pi / n + da
                x = math.cos(a)
                y = math.sin(a)
                point = Point(x, y)
                points.append(point)
        else:  # iteratively build points by keeping track of parentPoints
            if(n == 2):  # rotation of groups of 2 to align with their parent points
                # for prime numbers times 2 (double circle) - aligned with absolute center (0,0)
                if (len(parentPoints) == 0):
                    # create shallow copy of points
                    parentPoints = list(points)
                    points = []  # reset points
                    for parentPoint in parentPoints:
                        for i in range(n):
                            x = parentPoint.x + (1-2*i)*parentPoint.x / d
                            y = parentPoint.y + (1-2*i)*parentPoint.y / d
                            point = Point(x, y)
                            points.append(point)
                else:  # for every other group of 2 - aligned with their 'grandparent points'
                    # create shallow copy of points without deleting previous parent points ('grandparent points')
                    parentPoints2 = list(points)
                    points = []  # reset points
                    j = 0
                    for parentPoint2 in parentPoints2:
                        coef = len(parentPoints2)/len(parentPoints)
                        for i in range(n):
                            x = parentPoints[int(
                                j//coef)].x + (parentPoint2.x - parentPoints[int(j//coef)].x) * (1.5-i*0.8)
                            y = parentPoints[int(
                                j//coef)].y + (parentPoint2.y - parentPoints[int(j//coef)].y) * (1.5-i*0.8)
                            point = Point(x, y)
                            points.append(point)
                        j += 1
            else:
                parentPoints = list(points)  # create shallow copy of points
                points = []  # reset points
                for parentPoint in parentPoints:  # build new points using parentPoints
                    for i in range(n):
                        a = i * 2 * math.pi / n + da
                        x = parentPoint.x + math.cos(a) / d
                        y = parentPoint.y + math.sin(a) / d
                        point = Point(x, y)
                        points.append(point)
    return points


# %%
d = Draw(60, 0.3, 0.6)
