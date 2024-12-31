from Particle import Particle
from Constants import *
from random import *

class Emitter:

    def __init__(self, position, visibility, rateOfCreation):
        self.__position = position
        self.__visibility = visibility
        self.__rateOfCreation = rateOfCreation

    def setPosition(self, newPos):
        self.__position = newPos

    def createParticles(self, position, lifespan, color, radius):
        return Particle(position, color, lifespan, INITIAL_AGE, radius)

    def getPosition(self):
        return self.__position

    def createComplexParticles(self, position, lifespan, color, radius):
         magicParticle = []
         i = I_START
         while i < LOOP_COND:
             magicParticle.append(self.createParticles(position, lifespan, color, radius))
             magicParticle[i].setXCoordinate(magicParticle[i].getXCoordinate() + random())
             magicParticle[i].setYCoordinate(magicParticle[i].getYCoordinate() + randint(RAND_MIN,RAND_MAX))
             i += I_INCREMENT
         return magicParticle
             
        
