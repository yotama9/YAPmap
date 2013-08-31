from PyQt4 import QtGui,QtCore
from random import randint as rint



class Tile:
    
    def __init__(self):
        self.content = []
        self.types = []

    def write(self,tileData,tileType):
        tileNum = rint(0,len(tileData)-1)
        self.content = tileData[tileNum][:]
        self.type = [tileType]

        
    def paint(self,qp,x,y):
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        for square in self.content:
            pX = square[0][0]+x
            pY = square[0][1]+y
            red = square[1]
            green = square[2]
            blue = square[3]
            alpha = square[4]
            color = QtGui.QColor(red,green,blue,alpha)
            pen.setColor(color)
            qp.setPen(pen)
            qp.drawPoint(pX,pY)

        
                      
                
            

        


