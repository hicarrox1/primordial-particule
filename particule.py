import math
import pygame as pygm
from constant import *

BLUE = (0,0,255)
PINK = (181, 51, 175)
YELLOW = (243, 255, 51)
GREEN = (82, 181, 22)
BROWN = (148, 107, 64)

class Particule():
     

    def __init__(self, surface: 'pygm.Surface', pos_x: int, pos_y: int, radius: int, color: tuple, orientation: int, velocity: int, alpha: int, distance_check: int) -> None:
          
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.radius = radius
        self.color = color

        self.surface = surface

        self.orientation = math.radians(orientation)
        
        self.end_point_orientation = [(math.cos(self.orientation)*radius)+self.pos_x,(math.sin(self.orientation)*radius)+self.pos_y]
        self.velocity = velocity
        self.alpha = math.radians(alpha)

        self.direction = [0,0]

        self.distance_check = distance_check

        self.neighbor = []

        self.draw_range_b = False

    def draw(self):

        self.pos_x = self.pos_x%SCREEN_WIDTH
        self.pos_y = self.pos_y%SCREEN_HEIGHT
        #self.end_point_orientation[0] = self.end_point_orientation[0]%SCREEN_WIDTH
        #self.end_point_orientation[1] = self.end_point_orientation[1]%SCREEN_HEIGHT

        if self.draw_range_b:

            self.draw_range()
    
        pygm.draw.circle(self.surface, self.color, (self.pos_x,self.pos_y), self.radius)
        #pygm.draw.line(self.surface, (0,0,0), (self.pos_x,self.pos_y), (self.end_point_orientation[0],self.end_point_orientation[1]))
    
    def draw_range(self):

        pygm.draw.circle(self.surface, PINK, (self.pos_x,self.pos_y), self.distance_check)

    def update(self):

        self.avance()
        self.set_color()

    def set_color(self):

        Nt = len(self.neighbor)

        Nt1 = 0

        for b in self.neighbor:

            if b[1] <= (self.distance_check*100)/5:

                Nt1 += 1

        if 15 < Nt and Nt <= 30:
            
            self.color = BLUE 
            
        elif Nt > 30:
            self.color = YELLOW
        
        elif 13 <= Nt and Nt <= 15:
            self.color = BROWN

        elif Nt1 > 15:
            self.color = PINK 
        
        else:
            self.color = GREEN

    def get_direction(self):

        self.direction[0] = self.velocity*math.cos(self.orientation)
        self.direction[1] = self.velocity*math.sin(self.orientation)

    def avance(self):

        Nt = len(self.neighbor)

        Rt = 0

        for b in self.neighbor:

            if b[0] == True:

                Rt += 1

        Lt = Nt - Rt

        sign = lambda x: (x > 0) - (x < 0)

        self.delta_phi = self.alpha+ 17*Nt*sign(Rt-Lt)

        self.orientation = (self.orientation + self.delta_phi)%math.radians(360)

        self.get_direction()

        self.pos_x += self.direction[0]
        self.pos_y += self.direction[1]

        self.end_point_orientation = [(math.cos(self.orientation)*self.radius)+self.pos_x,(math.sin(self.orientation)*self.radius)+self.pos_y]

    def get_distance_with_particule(self, particule: 'Particule') -> float:

        return self.get_distance_with_pos((particule.pos_x,particule.pos_y))

    def get_distance_with_pos(self, pos: tuple) -> float:

        return math.sqrt( (self.pos_x - pos[0])**2 + (self.pos_y - pos[1])**2 )
    
    def right(self, particule: 'Particule') -> bool:

        a = math.sqrt(((self.pos_x+self.radius)-particule.pos_x)**2 + (self.pos_y-particule.pos_y)**2)
        b = self.radius
        c = math.sqrt((self.pos_x-particule.pos_x)**2 + (self.pos_y-particule.pos_y)**2)

        o = self.orientation

        try:
            result = math.acos((b**2 + c**2 - a**2) / (2*b*c))
        except:
            result = 0

        if (self.pos_y - particule.pos_y) >= 0:

            result = math.radians(360) - result

        particule_angle = math.degrees(result-o)

        if particule_angle < 180 and particule_angle > 0:
            return True
        
        else:
            return False
        
    
    def is_neighbor(self, particule: 'Particule') -> bool:

        if self.get_distance_with_particule(particule) <= self.distance_check:

            return True
        
        else:
            return False
        
    def __str__(self) -> str:
        return str(self.color)