import pygame as pygm
from random import randint
from particule import Particule
from constant import *

#https://www.youtube.com/watch?v=makaJpLvbow&list=WL&index=1

config = {"r": 100,"alpha": 180, "beta": 17, "velocity": 3, "radius": 20}
#config = {"r": 5,"alpha": 0, "beta": 0, "velocity": 0, "radius": 5}

        
class App():

    def __init__(self) -> None:

        pygm.init()

        self.screen = pygm.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        
        self.clock = pygm.time.Clock()

        self.particules: list['Particule'] = []

        #self.test_part()
        self.create_particules()

        self.run = True

        self.boucle()

    def create_particules(self):

        for y in range(500):

            for x in range(500):

                if randint(1,1000) == 50:

                    self.particules.append(Particule(self.screen,x*2,y*2,config["radius"],GREEN,config["beta"],config["velocity"],config["alpha"],config["r"]))

    def test_part(self):

        self.particules = [Particule(self.screen,500,500,75,PINK,17,0,0,50),Particule(self.screen,500,500,20,PINK,0,0,0,50)]

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

        #self.particules[1].pos_x = pygm.mouse.get_pos()[0]
        #self.particules[1].pos_y = pygm.mouse.get_pos()[1]
        #self.particules[1].draw_range_b = True
        #print(self.particules[1].neighbor)

    def update_particules(self):

        for particule in self.particules:
                
            particule.update()

        self.test()

            
    def check_neighbor_particule(self):

        def distance_with_origin(particule: 'Particule'):

            return particule.get_distance_with_pos((0,0))
        
        liste_trie = sorted(self.particules,key=distance_with_origin)

        p = 0

        for particule in liste_trie:

            result = []

            p_range = particule.distance_check

            for particule_to_check in liste_trie[p+1:]:

                distance = particule.get_distance_with_particule(particule_to_check)

                if distance > p_range:

                    break

                else:
                    
                    result.append([particule.right(particule_to_check), distance])

            for particule_to_check in reversed(liste_trie[:p]):

                distance = particule.get_distance_with_particule(particule_to_check)

                if distance > p_range:

                    break

                else:
                    
                    result.append([particule.right(particule_to_check), distance])

            p += 1

            particule.neighbor = result

    def test(self):

         for particule in self.particules:

            result = []

            for particule_to_check in self.particules:

                if particule.is_neighbor(particule_to_check):

                    result.append([particule.right(particule_to_check), particule.get_distance_with_particule(particule_to_check)])

            particule.neighbor = result

    def draw(self):

        self.screen.fill((255,255,255))

        self.draw_particules()

        pygm.display.flip()

    def draw_particules(self):

        for particule in self.particules:

            particule.draw()

App()