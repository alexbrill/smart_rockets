import pygame
from pygame import *
from sys import exit
from math import sqrt, sin, cos, pi
from random import random, randint

SIZE  = W, H = (800, 600)
NAME  = "ROCKETS"
FPS   = 30
WHITE = (255, 255, 255)
BLACK = (0  , 0  , 0  )
GREY  = (51 , 51 , 51 )
BLUE  = (0  , 0  , 255)

#__population__
POPSIZE = 25
LIFESPAN = 200

#__rocket__
LENG = 30
THICK = 10
SPEED = 3
SCL = LENG / SPEED

#__________________________________
def dist(x0, y0, x1 = 0, y1 = 0):
    return sqrt((x1 - x0)**2 + (y1 - y0)**2)

DIAG = dist(W, H)

def rotate(x, y, a, off_x = 0, off_y = 0):
    rx = x * cos(a) - y * sin(a) + off_x
    ry = x * sin(a) + y * cos(a) + off_y
    return [rx, ry]
#__________________________________
class vect:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)

    def get_r(self):
        return (round(self.x), round(self.y))

    def rand(self):
        angle = random() * 2*pi
        self.x, self.y = rotate(0, -SPEED, angle)

    def add(self, sec):
        self.x = self.x + sec.x
        self.y = self.y + sec.y
        
    def mult(self, scl):
        self.x = self.x * scl
        self.y = self.y * scl

    def sum(self, sec, scl = 1):
        return vect(self.x + sec.x * scl, self.y + sec.y * scl)

    def leng(self):
        return sqrt(self.x**2 + self.y**2)

    def copy(self):
        return self

#__________________________________
class Rocket:
    def __init__(self, x = W/2, y = H, dna = None):
        if dna is not None:
            self.dna = dna
        else:
            self.dna = DNA()
        self.pos = vect(x, y)
        self.vel = vect()
        self.acc = vect()
        self.leng = LENG
        self.thick = THICK
        self.fitness = 0

    def calcFitness(self, target):
        d = dist(self.pos.x, self.pos.y, target.x, target.y)
        self.fitness = DIAG - d

    def applyForce(self, force):
        self.acc.add(force)

    def update(self, count):
        print(count)
        self.applyForce(self.dna.genes[count])
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        
    def show(self, screen):
        leng = self.vel.leng()
        scl = self.leng / leng
        heading = self.pos.sum(self.vel, scl)
        draw.line(screen, WHITE, self.pos.get(), heading.get(), self.thick)
                  
#__________________________________
class Population:
    def __init__(self, popsize):
        self.count = 0
        self.rockets = []
        self.popsize = popsize
        self.matingpool = []
        for n in range(self.popsize):
            self.rockets.append(Rocket())

    def evaluate(self, target):
        maxfit = 0
        for el in self.rockets:
            el.calcFitness(target)
            if el.fitness > maxfit:
                maxfit = el.fitness
        for n in range(len(self.rockets)):
            self.rockets[n].fitness = self.rockets[n].fitness / maxfit
        self.matingpool.clear()
        for el in self.rockets:
            n = round(el.fitness * 100)
            for i in range(n):
                self.matingpool.append(el)
        
    def selection(self):
        newpop = []
        for n in range(len(self.rockets)):
            parA = self.matingpool[randint(0, len(self.matingpool))].dna
            parB = self.matingpool[randint(0, len(self.matingpool))].dna
            child = parA.crossover(parB)
            self.rockets[n] = Rocket(W/2, H, child)
        self.rockets = newpop.copy()

    def run(self, screen, target):
        self.count = self.count + 1
        if self.count >= LIFESPAN:
            self.evaluate(target)
            self.selection()
            self.count = 0
        for el in self.rockets:
            el.update(self.count)
            el.show(screen)
#__________________________________
class DNA:
    def __init__(self, genes = None):
        self.leng = LIFESPAN
        if genes is not None:
            self.genes = genes.copy()
        else:
            self.genes = []
            for n in range(self.leng):
                gene = vect()
                gene.rand()
                gene.mult(0.5)
                self.genes.append(gene.copy())

    def crossover(self, par):
        newdna = [0] * len(self.genes)
        mid = round(randint(0, len(self.genes)))                               
        for n in range(len(self.genes)):
            if n > mid:
                newdna[n] = self.genes[n]
            else:
                newdna[n] = par.genes[n]
        return DNA(newdna)
            
                               
    
#__________________________________
def run():
    pygame.init()
    display.set_caption(NAME)
    screen = display.set_mode(SIZE)
    clock = time.Clock()

    pop = Population(POPSIZE)
    target = vect(W/2, 50)

    while 1:
        clock.tick(FPS)

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()

        screen.fill(GREY)
        draw.circle(screen, WHITE, target.get_r(), 16) 
        pop.run(screen, target)

        display.update()




if __name__ == "__main__":
    run()
