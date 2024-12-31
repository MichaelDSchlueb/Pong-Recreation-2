import pygame
from Ball import Ball
from Paddle import Paddle
from Constants import *
from Emitter import Emitter
from Particle import Particle
from random import *

class Pong:

    def __init__(self):
        self.__ball = Ball(BALL_COLOR, HEIGHT/DIVIDE_TWO, WIDTH/DIVIDE_TWO, RADIUS)
        self.__paddleLeft = Paddle(PADDLE_COLOR, PADDLE_LEFT_X, PADDLE_LEFT_Y, PADDLE_WIDTH, PADDLE_HEIGHT) 
        self.__paddleRight = Paddle(PADDLE_COLOR, PADDLE_RIGHT_X, PADDLE_LEFT_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.__score = pygame.math.Vector2(START_X,START_Y)
        self.__defaultMode = True
        self.__specialMode = False
        self.__complexMode = False
        self.__emitter = Emitter((self.__ball.getCenterX(), self.__ball.getCenterY()), EMITTER_VISIBILITY, EMITTER_RATE)
        self.__win = False
    

    def reset(self):
        self.__paddleLeft.setCenterX(PADDLE_LEFT_X)
        self.__paddleLeft.setCenterY(PADDLE_LEFT_Y)
        self.__paddleRight.setCenterX(PADDLE_RIGHT_X)
        self.__paddleRight.setCenterY(PADDLE_LEFT_Y)
        self.__ball.setCenterX(HEIGHT/DIVIDE_TWO)
        self.__ball.setCenterY(WIDTH/DIVIDE_TWO)
        self.__ball.setYDir(START_Y)
        self.__ball.setXDir(START_X)
        self.__score = pygame.Vector2(START_X,START_Y)

    def setP1Score(self):
        self.__score[P_ONE_SCORE] += INCREMENT_SCORE

    def setP2Score(self):
        self.__score[P_TWO_SCORE] += INCREMENT_SCORE

    def getP1Score(self):
        return self.__score[P_ONE_SCORE]

    def getP2Score(self):
        return self.__score[P_TWO_SCORE]

    def toggleDefaultMode(self):
        if not self.__defaultMode:
           self.__defaultMode = not self.__defaultMode
        if self.__specialMode:
            self.__specialMode = not self.__specialMode
        elif self.__complexMode:
            self.__complexMode = not self.__complexMode

    def toggleSpecialMode(self):
        if not self.__specialMode:
            self.__specialMode = not self.__specialMode
        if self.__defaultMode:
            self.__defaultMode = not self.__defaultMode
        elif self.__complexMode:
            self.__complexMode = not self.__complexMode

    def toggleComplexMode(self):
        if not self.__complexMode:
            self.__complexMode = not self.__complexMode
        if self.__defaultMode:
            self.__defaultMode = not self.__defaultMode
        elif self.__specialMode:
            self.__specialMode = not self.__specialMode

    def run(self):
        pygame.init()

        font = pygame.font.Font('freesansbold.ttf', SCORE_SIZE)
    
        screen = pygame.display.set_mode((HEIGHT, WIDTH), pygame.RESIZABLE)

        clock = pygame.time.Clock()

        running = True

        #create the list for special mode
        particles = []
        complexParticles = []

        while running:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_r]:
                        self.reset()
                    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
                        if keys[pygame.K_w]:
                            moveKey = chr(pygame.K_w)
                        if keys[pygame.K_s]:
                            moveKey = chr(pygame.K_s)
                        if keys[pygame.K_a]:
                            moveKey = chr(pygame.K_a)
                        if keys[pygame.K_d]:
                            moveKey = chr(pygame.K_d)
                        self.__paddleLeft.move(moveKey, screenWidth, screenHeight)
                    if keys[pygame.K_i] or keys[pygame.K_k] or keys[pygame.K_j] or keys[pygame.K_l]:
                        if keys[pygame.K_i]:
                           moveKey = chr(pygame.K_i)
                        if keys[pygame.K_k]:
                            moveKey = chr(pygame.K_k)
                        if keys[pygame.K_j]:
                            moveKey = chr(pygame.K_j)
                        if keys[pygame.K_l]:
                            moveKey = chr(pygame.K_l)
                        self.__paddleRight.move(moveKey, screenWidth, screenHeight)
                    if keys[pygame.K_SPACE]:
                        self.__ball.setXDir(DIR_CHANGE_RIGHT)
                    if keys[pygame.K_0]:
                        self.toggleDefaultMode()
                    if keys[pygame.K_1]:
                        self.toggleSpecialMode()
                    if keys[pygame.K_2]:
                        self.toggleComplexMode()

            screen.fill(BACKGROUND_COLOR)

            screenWidth = pygame.display.Info().current_w

            screenHeight = pygame.display.Info().current_h

            simpleSurface = pygame.Surface((screenHeight * DIVIDE_TWO, screenWidth * DIVIDE_TWO), pygame.SRCALPHA)

            self.__paddleLeft.move(keys, screenWidth, screenHeight)

            self.__paddleRight.move(keys, screenWidth, screenHeight)
            self.__ball.move(screenWidth, screenHeight, self.__paddleLeft, self.__paddleRight, self.__score)
            pygame.draw.circle(screen, self.__ball.getColor(), (self.__ball.getCenterX(), self.__ball.getCenterY()), self.__ball.getRadius())
            self.__emitter.setPosition((self.__ball.getCenterX(), self.__ball.getCenterY()))

            if self.__specialMode and self.__ball.getXDir() != START_X:
                if self.__specialMode:
                    temp = self.__emitter.createParticles((self.__ball.getCenterX(), self.__ball.getCenterY()), SIMPLE_MAX_AGE, self.__ball.getColor(), self.__ball.getRadius())
                    particles.append(temp)
                for particle in particles:
                    trans = INITIAL_TRANSPARENCY - (INITIAL_TRANSPARENCY * (particle.getTransparency()/TRANSPARENCY_DIVIDE))
                    pygame.draw.circle(simpleSurface, (*particle.getColor(), trans), particle.getPosition(), particle.getRadius())
                    particle.setTransparency(particle.getTransparency() + TRANSPARENCY_INC)
                    particle.setAge(particle.getAge() + AGE_INC)
                    if trans <= LOWEST_TRANSPARENCY_POSSIBLE or particle.getAge() == SIMPLE_MAX_AGE:
                      particles.remove(particle)

            elif self.__complexMode and self.__ball.getXDir() != START_X:
                complexParticles.append(self.__emitter.createComplexParticles([self.__ball.getCenterX(), self.__ball.getCenterY()], COMPLEX_MAX_AGE, (RED,randint(COLOR_MIN,COLOR_MAX),BLUE), self.__ball.getRadius() * DOUBLE_RADIUS))
                for complexParticle in complexParticles:
                    for particle in complexParticle:
                          trans = INITIAL_TRANSPARENCY - (INITIAL_TRANSPARENCY * (particle.getTransparency()/TRANSPARENCY_DIVIDE))
                          pygame.draw.circle(simpleSurface, (*particle.getColor(), trans), particle.getPosition(), particle.getRadius())
                          particle.setRadius(particle.getRadius() - RADIUS_DECREMENT)
                          particle.setTransparency(particle.getTransparency() + TRANSPARENCY_INC)
                          particle.setAge(particle.getAge() + AGE_INC)
                          pygame.draw.circle(simpleSurface, self.__ball.getColor(), self.__ball.getPosition(), self.__ball.getRadius() * DIVIDE_TWO)
                          if particle.getAge() >= COMPLEX_MAX_AGE:
                             complexParticle.remove(particle)
        
            screen.blit(simpleSurface,SIMPLE_SURFACE_PTS)                        

            pygame.draw.rect(screen, self.__paddleLeft.getColor(), pygame.Rect(self.__paddleLeft.getCenterX(), self.__paddleLeft.getCenterY(), PADDLE_WIDTH, PADDLE_HEIGHT))

            pygame.draw.rect(screen, self.__paddleRight.getColor(), pygame.Rect(self.__paddleRight.getCenterX(), self.__paddleRight.getCenterY(), PADDLE_WIDTH, PADDLE_HEIGHT))


            scoreKeeper = font.render(str(self.__score), ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)

            textLocation = (SCORE_X, SCORE_Y)

            screen.blit(scoreKeeper, textLocation)

            winFont = pygame.font.Font('freesansbold.ttf', VICTORY_SIZE)
            messageLocation = (WIN_MESSAGE_LOCATION_X, WIN_MESSAGE_LOCATION_Y)

            if self.__score[P_ONE_SCORE] == WINNING_SCORE:
               winMessage = winFont.render(PLAYER_ONE_WIN, ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)
               screen.blit(winMessage, messageLocation)
               self.__win = True
               
            elif self.__score[P_TWO_SCORE] == WINNING_SCORE:
              winMessage = winFont.render(PLAYER_TWO_WIN, ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)
              screen.blit(winMessage, messageLocation)
              self.__win = True

            if self.__win:
              self.__ball.setXDir(START_X)
              self.__ball.setYDir(START_Y)
              if keys[pygame.K_SPACE]:
                   self.reset()

            self.__win = False
              

            pygame.display.flip()

            clock.tick(CLOCK_TIME)

        pygame.quit()
