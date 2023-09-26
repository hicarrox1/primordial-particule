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
        self.velocity = velocity
        self.alpha = math.radians(alpha)

        self.direction = [0,0]

        self.distance_check = distance_check

    def draw(self):
    
        pygm.draw.circle(self.surface, self.color, (self.pos_x,self.pos_y), self.radius)

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

    def get_distance(self, particule: 'Particule') -> float:

        return math.sqrt( (self.pos_x - particule.pos_x)**2 + (self.pos_y - particule.pos_y)**2 )
    
    def right(self, particule: 'Particule') -> bool:

        if self.pos_y < particule.pos_y:
            return True
        else:
            return False
    
    def is_neighbor(self, particule: 'Particule') -> bool:

        if self.distance_check <= self.get_distance(particule):

            return True, self.right(particule)
        
        else:

            return False, None
        
class App():

    def __init__(self) -> None:

        pygm.init()

        SCREEN_WIDTH = 600
        SCREEN_HEIGHT= 400

        self.screen = pygm.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.clock = pygm.time.Clock()

        self.particules = [Particule(self.screen,300,200,75,GREEN,17,75,180,5),Particule(self.screen,100,300,20,PINK,0,0,0,0)]

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

    def update_particules(self):

        for particule in self.particules:
                
            particule.update()

        print(self.particules[0].get_distance(self.particules[1]))

    def draw(self):

        self.screen.fill((255,255,255))

        self.draw_particules()

        pygm.display.flip()

    def draw_particules(self):

        for particule in self.particules:

            particule.draw()

App()