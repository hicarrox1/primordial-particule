import pygame as pygm
import math

BLUE = (0,0,255)
PINK = (255, 51, 233)
JAUNE = (243, 255, 51)
GREEN = (82, 181, 22)

#https://www.youtube.com/watch?v=makaJpLvbow&list=WL&index=1

class Particule():
     

    def __init__(self, surface: 'pygm.Surface', pos_x: int, pos_y: int, radius: int, color: tuple, orientation: int, velocity: int, alpha: int, distance_check: int) -> None:
          
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.radius = radius
        self.color = color

        self.surface = surface

        self.orientation = math.radians(orientation)
        self.end_point_orientation = (math.cos(self.orientation)*radius)+self.pos_x,(math.sin(self.orientation)*radius)+self.pos_y
        self.velocity = velocity
        self.alpha = math.radians(alpha)

        self.direction = [0,0]

        self.distance_check = distance_check

        self.neighbor = []

    def draw(self):
    
        pygm.draw.circle(self.surface, self.color, (self.pos_x,self.pos_y), self.radius)
        pygm.draw.line(self.surface, (0,0,0), (self.pos_x,self.pos_y), (self.end_point_orientation[0],self.end_point_orientation[1]))

    def update(self):

        self.avance()

    def get_direction(self):

        self.direction[0] = self.velocity*math.cos(self.orientation)
        self.direction[1] = self.velocity*math.sin(self.orientation)

    def avance(self):

        self.get_direction()

        self.pos_x += self.direction[0]
        self.pos_y += self.direction[1]

        self.orientation += self.alpha

        self.end_point_orientation = (math.cos(self.orientation)*self.radius)+self.pos_x,(math.sin(self.orientation)*self.radius)+self.pos_y

        Nt = len(self.neighbor)

        Rt = 0

        for b in self.neighbor:

            if b == True:

                Rt += 1

        Lt = Nt - Rt

        sign = lambda x: (x > 0) - (x < 0)

        #self.orientation = self.orientation+ 17*Nt*sign(Rt-Lt)

    def get_distance_with_particule(self, particule: 'Particule') -> float:

        return self.get_distance_with_pos((particule.pos_x,particule.pos_y))

    def get_distance_with_pos(self, pos: tuple) -> float:

        return math.sqrt( (self.pos_x - pos[0])**2 + (self.pos_y - pos[1])**2 )
    
    def right(self, particule: 'Particule') -> bool:

        a = math.sqrt(((self.pos_x+self.radius)-particule.pos_x)**2 + (self.pos_y-particule.pos_y)**2)
        b = self.radius
        c = math.sqrt((self.pos_x-particule.pos_x)**2 + (self.pos_y-particule.pos_y)**2)

        if (2*b*c) != 0:
            try:
                result = math.acos((b**2 + c**2 - a**2) / (2*b*c))
            except:
                result = 0

        if (self.pos_y - particule.pos_y) >= 0:

            result = math.radians(360) - result

        particule_angle = math.degrees(result-self.orientation)

        if particule_angle < 180 and particule_angle > 0:
            return True
        
        else:
            return False
    
    def is_neighbor(self, particule: 'Particule') -> bool:

        if self.distance_check <= self.get_distance_with_particule(particule):

            return True, self.right(particule)
        
        else:
            return False, None
        
    def __str__(self) -> str:
        return str(self.color)
        
class App():

    def __init__(self) -> None:

        pygm.init()

        SCREEN_WIDTH = 600
        SCREEN_HEIGHT= 400

        self.screen = pygm.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.clock = pygm.time.Clock()

        self.particules = [Particule(self.screen,300,200,75,GREEN,17,0.67,180,100),Particule(self.screen,500,220,20,PINK,17,0.67,180,100),Particule(self.screen,100,150,20,PINK,17,0.67,180,100)
                           ,Particule(self.screen,500,100,20,PINK,17,0.67,180,100),Particule(self.screen,500,300,20,BLUE,17,0.67,180,100),Particule(self.screen,500,200,20,JAUNE,17,0.67,180,100)]

        self.run = True

        self.boucle()

    def boucle(self):

        while self.run:

            self.update()

            self.draw()

        pygm.quit()

    def update(self):

        for event in pygm.event.get():

                if event.type == pygm.QUIT:

                    self.run = False

        self.update_particules()

        self.particules[1].pos_x = pygm.mouse.get_pos()[0]
        self.particules[1].pos_y = pygm.mouse.get_pos()[1]

    def update_particules(self):

        self.check_neighbor_particule()

        for particule in self.particules:
                
            particule.update()

    def check_neighbor_particule(self):

        def distance_with_origin(particule: 'Particule'):

            return particule.get_distance_with_pos((0,0))
        
        liste_trie = sorted(self.particules,key=distance_with_origin)

        p = 0

        for particule in liste_trie:

            result = []

            p_range = particule.distance_check

            for particule_to_check in liste_trie[p+1:]:

                if particule.get_distance_with_particule(particule_to_check) > p_range:

                    break

                else:
                    
                    result.append(particule.right(particule_to_check))

            for particule_to_check in reversed(liste_trie[:p]):

                if particule.get_distance_with_particule(particule_to_check) > p_range:

                    break

                else:
                    
                    result.append(particule.right(particule_to_check))
            
            p += 1

            particule.neighbor = result

    def draw(self):

        self.screen.fill((255,255,255))

        self.draw_particules()

        pygm.display.flip()

    def draw_particules(self):

        for particule in self.particules:

            particule.draw()

App()