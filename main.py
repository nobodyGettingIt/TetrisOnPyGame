import pygame as pg
import sys

from Field import Field, Shape

from random import randint


black = (0,0,0)

numOfShapes = ['I', 'O', 'J', 'L', 'S', 'T', 'Z']

class Game:
    def __init__(self, h, w):
        size = self.h, self.w = h, w
        self.screen = pg.display.set_mode(size) 
        
        self.fps = 60
        self.done = False
        self.clock = pg.time.Clock()

        self.dtCounterForUpdate = 0
        self.updatePeriod = 0.15

        self.field = Field(h//10, w//10, self.screen)
        self.shape = Shape(self.field, numOfShapes[randint(0, 6)])
        
    
    def update(self, dt):
        self.field.update()
        
        
        if not self.shape.fall():
            self.shape = Shape(self.field, numOfShapes[randint(0, 6)])
            

    
    def render(self):
        self.screen.fill(black)

        self.field.draw()
        self.shape.draw(self.screen)

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: self.done = True
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.shape.moveLeft()
                elif event.key == pg.K_d:
                    self.shape.moveRight()
                elif event.key == pg.K_r:
                    self.shape.rotate()

    def mainLoop(self):
        dt = 0
        self.clock.tick(self.fps)
        while not self.done:
            if self.dtCounterForUpdate >= self.updatePeriod:
                self.update(dt)
                self.dtCounterForUpdate = 0

            self.events()
            self.render()
            
            dt = self.clock.tick(self.fps)/1000.0
            self.dtCounterForUpdate += dt
        


def main():
    pg.init()
    
    g = Game(200, 400)
    g.mainLoop()
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()

            
