from Constants import *
class Particle:

    def __init__(self, position, color, lifeSpan, birthTime, radius):
        self.__position = position
        self.__color = color
        self.__birthTime = birthTime
        self.__age = INITIAL_AGE
        self.__lifeSpan = lifeSpan
        self.__radius = radius
        self.__transparency = INITIAL_AGE

    def setAge(self, newAge):
        self.__setAge += newAge

    def getRadius(self):
        return self.__radius

    def getColor(self):
        return self.__color

    def setAge(self, newAge):
        self.__age = newAge

    def getAge(self):
        return self.__age

    def getPosition(self):
        return self.__position

    def getTransparency(self):
        return self.__transparency

    def setTransparency(self, newValue):
        self.__transparency = newValue

    def getLifespan(self):
        return self.__lifeSpan

    def getBirthTime(self):
        return self.__birthTime
    
    def getXCoordinate(self):
        return self.__position[X_POS]

    def setXCoordinate(self, newValue):
        self.__position[X_POS] = newValue
    
    def getYCoordinate(self):
        return self.__position[Y_POS]

    def setYCoordinate(self, newValue):
        self.__position[Y_POS] = newValue

    def setRadius(self, newRadius):
        self.__radius = newRadius
