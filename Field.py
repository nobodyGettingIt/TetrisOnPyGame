import pygame as pg

shapes = {
    'I': ((0,-2), (0,-1), (0,-3), (0,-4)),
    'O': ((0,-2), (0,-1), (1,-2), (1,-1)),
    'J': ((1,-2), (1,-3), (1,-1), (0,-1)),
    'L': ((1,-2), (1,-1), (1,-3), (2,-1)),
    'S': ((1,-2), (1,-1), (0,-1), (2,-2)),
    'T': ((1,-1), (1,-1), (1,-2), (2,-1)),
    'Z': ((1,-1), (0,-2), (1,-2), (2,-1))
}


red = (255, 0, 0)

class Field:
    def __init__(self, sx, sy, screen):
        self.sx = sx
        self.sy = sy
        self.matrix = [[0 for i in range(sy)] for i in range(sx)]

        self.screen = screen

    def putBlock(self, x, y):
        if not self.blockIsEmpty(x,y):
            raise Exception('This coordinats is alredy used')
        self.matrix[x][y] = 1

    def blockIsEmpty(self, x, y):
        if x<0 or x>=self.sx:
            return False

        if y>=self.sy:
            return False
        elif y<0:
            return True

        if self.matrix[x][y]==0:
            return True
        else:
            return False


    def update(self):
        self.checkLines()

    def checkLines(self):
        for y in range(self.sy):
            if self.checkLine(y):
                self.deleteLine(y)
                self.lowerRows(y)
            

    def checkLine(self, y):
        for i in self.matrix:
            if i[y] == 0:
                return False

        return True

    def deleteLine(self, y):
        for i in self.matrix:
            i[y] = 0
        
    def lowerRows(self, fromWhere):
        for i in self.matrix:
            for j in range(fromWhere - 1, -1, -1):
                i[j + 1] = i[j]
                i[j] = 0 

    def draw(self):
        for x in range(self.sx):
            for y in range(self.sy):
                if self.matrix[x][y] != 0:
                    pg.draw.rect(self.screen, red, ((x*10, y*10), (10, 10)))
        
blue = (0,0,255)

class Block:
    def __init__(self, px, py, field):
        self.px = px
        self.py = py
        self.field = field


    def draw(self, screen):
        pg.draw.rect(screen, blue, ((self.px*10, self.py*10),(10, 10)))


    def checkfall(self):
        if self.lowerBlockIsEmpty():
            return True
        else:
            return False
        

    def fall(self):
        self.py += 1
        
    def lowerBlockIsEmpty(self):
        return self.field.blockIsEmpty(self.px, self.py+1)

    def stopFalling(self):
        self.field.putBlock(self.px, self.py)

    def checkMoveLeft(self):
        return self.field.blockIsEmpty(self.px-1, self.py)

    def checkMoveRight(self):
        return self.field.blockIsEmpty(self.px+1, self.py)
        

    def moveLeft(self):
        self.px -= 1
        

    def moveRight(self):
        self.px += 1


    def checkrotate(self, axispx, axispy, lastBlockForLine):
        if self.py <= 0:
            return False


        dy = axispy-self.py
        dx = axispx-self.px
        
        px = axispx + dy
        py = axispy - dx

        if lastBlockForLine is not None:
            x = axispx - lastBlockForLine[0]
            y = axispy - lastBlockForLine[1]

            if x > 0 and y > 0:
                px -= 1
            elif x > 0 and y < 0:
                py -= 1
            elif x < 0 and y < 0:
                px += 1
            elif x < 0 and y > 0:
                py += 1

        if self.checkChangePos(px, py):
            self.rpx = px
            self.rpy = py
            return True
        else:
            return False
        

    def rotate(self):
        if self.rpx is not None and self.rpy is not None:
            self.px = self.rpx
            self.py = self.rpy

            self.rpx = self.rpy = None
            

        
    def checkChangePos(self, newpx, newpy):
        return self.field.blockIsEmpty(newpx, newpy)
            
        
            

class Shape:
    def __init__(self, field, typeOfShape, windowSize):
        coords = shapes[typeOfShape]
        h, w = windowSize[0], windowSize[1]
        
        self.blocks = [
                    Block(w//20 + coords[0][0], coords[0][1], field),
                    Block(w//20 + coords[1][0], coords[1][1], field),
                    Block(w//20 + coords[2][0], coords[2][1], field),
                    Block(w//20 + coords[3][0], coords[3][1], field)
                ]
        self.type = typeOfShape
        
            
        

    def fall(self):
        needToStop = False
        for i in self.blocks:
            if not i.checkfall():
                needToStop = True

        if needToStop:
            for i in self.blocks:
                i.stopFalling()
            
            return False
        else:
            for i in self.blocks:
                i.fall()
                
            return True
        
                
                

    def draw(self, screen):
        for i in self.blocks:
            i.draw(screen)
    
    
    def moveLeft(self):
        canWeMove = True
        for i in self.blocks:
            if not i.checkMoveLeft():
                canWeMove = False
                break

        if canWeMove:
            for i in self.blocks:
                i.moveLeft()

    def moveRight(self):
        canWeMove = True
        for i in self.blocks:
            if not i.checkMoveRight():
                canWeMove = False
                break

        if canWeMove:
            for i in self.blocks:
                i.moveRight()

    def rotate(self):
        if self.type == 'O':
            return
        elif self.type == 'I':
            canWeRotate = True
            for i in self.blocks:
                if not i.checkrotate(self.blocks[0].px, self.blocks[0].py, (self.blocks[3].px, self.blocks[3].py)):
                    canWeRotate = False
                    return
                
            if canWeRotate:
                for i in self.blocks:
                    i.rotate()
            
        else:
            canWeRotate = True
            for i in self.blocks:
                if not i.checkrotate(self.blocks[0].px, self.blocks[0].py, None):
                    canWeRotate = False
                    return
                
            if canWeRotate:
                for i in self.blocks:
                    i.rotate()
            
             
        
