#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
This is a fibble attempt to make a mapping program which is 
supposed to be fast and easy to use. One feature I try to 
implement here, is randomness. I want the mountains drawen to be
a little different from one - another. 
"""

import sys,os
from PyQt4 import QtGui, QtCore
from tile import *

class MainGui(QtGui.QWidget):
    
    def __init__(self):
        #Setting some important constant. 
        super(MainGui,self).__init__()
        # To handle keyboard keys, I use this flag
        self.keepFocus = True

        # The starting and ending of the grid
        self.endX=25
        self.endY=25
        self.startX=25
        self.startY=15
        self.count = 0
        self.fams = []
        self.names = []
        self.curFam = ''
        self.radiuses = self.makeRadiuses() # A facntion to create a dict with radiuses as key and i,j indecies as vales

        self.loadTilesNames() #Load the tile names and families from hard drive
        self.tiles = dict() #Store the tiles 
        self.selectedTiles=[] #Store the selected tiles
        self.topLeft=[0,0] #the i and j indecies of the top left
        #corner of the grid displayed

        self.mousePressed=False
        self.setColors()
        self.initUI()

    def loadTilesNames(self):
        self.tileDB = loadTiles()
        self.fams = []
        for fam in self.tileDB:
            self.fams.append(fam)
            
        self.fams = sorted (self.fams)
        
    def setColors(self):
        #Setting colors for future use
        self.blue=QtGui.QColor(0,0,255,255)
        self.black=QtGui.QColor(0,0,0,255)
        self.selBlue=QtGui.QColor(0,0,255,10)
        self.trans=QtGui.QColor(0,0,0,0)

    def initUI(self):
        # Setting the window
        self.setGeometry(10,10,1000,600)
        self.setWindowTitle('YAPmap.py')
        self.setContentsMargins(0,0,0,0)
        self.layout = QtGui.QVBoxLayout(self)
        self.makeButtons()
        self.show()

    def makeButtons(self):
        #The tile family combo box
        self.tileCombo1 = QtGui.QComboBox(self)
        for fam in self.fams:
            self.tileCombo1.addItem(fam)
        self.tileCombo1.move(self.endX-100,self.endY)
        #The tile type combo box
        self.tileCombo1.resize(10,20)
        self.tileCombo2 = QtGui.QComboBox(self) 

        self.layout.addWidget(self.tileCombo1)
        self.layout.addWidget(self.tileCombo2)
        
        self.execButton = QtGui.QPushButton('Do It',self)
        self.execButton.clicked.connect(self.buttonDoIt)
        self.layout.addWidget(self.execButton)

                
    def buttonDoIt(self):
        #For now, this will only generate non-random mountains. 
        fam = self.tileCombo1.currentText()
        tText = self.tileCombo2.currentText()
        tileData = self.tileDB[fam][tText]
        for sel in self.selectedTiles:
            tile=self.tiles[sel].write(tileData,tText)
#        self.surroundTiles()
        self.update()
        self.selectedTiles = []


    def keyPressEvent(self,event):
        super(MainGui,self).keyPressEvent(event)
        if (event.key() == QtCore.Qt.Key_Left):
            self.topLeft[0] -= 1
            self.update()
        if (event.key() == QtCore.Qt.Key_Right):
            self.topLeft[0] += 1
            self.update()
        if (event.key() == QtCore.Qt.Key_Up):
            self.topLeft[1] -= 1
            self.update()
        if (event.key() == QtCore.Qt.Key_Down):
            self.topLeft[1] += 1
            self.update()

    def moveButtons(self):
        #finding the size of the buttons so they won't
        # escape the screen
        width = self.frameSize().width()
        xsize = width - self.endX - 30
        #updating the buttons
        self.tileCombo1.move(self.endX+10,50)
        self.tileCombo1.resize(xsize,30)
        self.tileCombo2.move(self.endX+10,85)
        self.tileCombo2.resize(xsize,30)
        self.execButton.move(self.endX+10,130)
        self.execButton.resize(xsize,30)

    def updateTiles(self):
        #The tiles family
        fam = self.tileCombo1.currentText()
        # Erasing the old names
        if self.curFam == fam:
            # Nothing to do
            return
        # clear the list
        while self.tileCombo2.count() > 0:
            self.tileCombo2.removeItem(0)
        self.curFam = fam[:]
        names = self.tileDB[self.curFam]
        self.names = []
        for name in names:
            self.names.append(name)

        self.tileCombo2.addItems(self.names)


    def paintEvent(self,e):
        self.count += 1
#        print (self.count)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        self.markSelected(qp)
        qp.end()
        #Updating buttons
        self.updateTiles()
        self.moveButtons()
        if self.keepFocus:
            self.setFocus()
        else:
            self.keepFocus = True
            


    def markSelected(self,qp):
        #marking selections
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setBrush(self.selBlue)
        pen.setColor(self.trans)
        qp.setPen(pen)
        for sel in self.selectedTiles:
            x = (sel[0] - self.topLeft[0])*50 + self.startX
            y = (sel[1] - self.topLeft[1])*50 + self.startY
            qp.drawRect(x,y,50,50)
        
        

    def draw(self,qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        width= self.frameSize().width()
        height = self.frameSize().height()
        
        maxI = (width - 150)/50 - 1
        maxJ = (height - 100)/150 - 1

        #Drawing the grid
        pen.setStyle(QtCore.Qt.DotLine)
        pen.setColor(self.black)
        qp.setPen(pen)
        x = self.startX
        while x <= width -150:
            i = int((x-self.startX)/50) + self.topLeft[0]
            y = self.startY
            while y <= height - 100:
                j = int((y-self.startY)/50) + self.topLeft[1]
                qp.drawLine(x,y,x+50,y)
                qp.drawLine(x,y,x,y+50)
                if not (i,j) in self.tiles:
                    self.tiles[(i,j)] = Tile() 
                elif len(self.tiles[(i,j)].content) > 0:
                    self.tiles[(i,j)].paint(qp,x,y)
                    qp.setPen(pen) #The tile.paint function generate its own pen
                y += 50
                self.endY = y
            x += 50
            self.endX=x

        #Closing line for the grid
        qp.drawLine(self.endX,self.startY,self.endX,self.endY)
        qp.drawLine(self.startX,self.endY,self.endX,self.endY)
        
    def getNeighbors(tileIndex):
        out = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                out.append (tileIndex[0]+i,tileIndex[1]+j)
        return out

    def getSurrounding(self,sel):
        out = []
        for r in range (18,0,-1):
            if not r in self.radiuses: continue
            vals = self.radiuses[r]
            print (vals)
        
    def surroundTiles(self):
        ''' A function to try and fill tiles which sourund 
        the selected tiles ''' 

        for sel in self.selectedTiles:
            neighbors = self.getSurrounding(sel)
                
                    

            
    def mouseMoveEvent(self,e):
        super(MainGui, self).mouseMoveEvent(e)
        self.markTile(e)

    def eventFilter(self,source,event):
        """ This class is used for special events which I couldn't
        handle otherwize Most events return False to help debugin 
        """
        if event.type() == QtCore.QEvent.Paint:
            return False
        elif event.type() == QtCore.QEvent.UpdateRequest:
            return False
        elif event.type() == QtCore.QEvent.Polish:
            return False
        elif event.type() == QtCore.QEvent.PolishRequest:
            return False
        elif event.type() == QtCore.QEvent.LayoutRequest:
            return False
        elif event.type() == QtCore.QEvent.HideToParent:
            return False
        elif event.type() == QtCore.QEvent.Hide:
            return False
        elif event.type() == QtCore.QEvent.FocusOut:
            return False
        elif event.type() == QtCore.QEvent.FocusIn:
            return False
        elif event.type() == QtCore.QEvent.MouseMove:
            return False
        elif event.type() == QtCore.QEvent.WindowActivate:
            return False
        elif event.type() == QtCore.QEvent.ActivationChange:
            return False
        elif event.type() == QtCore.QEvent.SockAct:
            return False
        elif event.type() == QtCore.QEvent.Move:
            return False
        elif event.type() == QtCore.QEvent.Resize:
            return False
        elif event.type() == QtCore.QEvent.Enter:
            return False
        elif event.type() == QtCore.QEvent.HoverMove:
            if self.execButton.underMouse():
                self.execButton.setFocus()
                self.keepFocus=False
            else :
                self.keepFocus=True
            
        return False


    def markTile(self,e):

        x=e.pos().x()
        y=e.pos().y()
        if x >= self.endX: return
        if y >= self.endY: return
        if x <= self.startX: return
        if y <= self.startY: return
        i = int((x-self.startX)/50) + self.topLeft[0]
        j = int((y-self.startY)/50) + self.topLeft[0]
        if not (i,j) in self.selectedTiles:
            self.selectedTiles.append((i,j))

        self.lastI=i
        self.lastJ=j
        self.update()
    
    def makeRadiuses(self):
        radiuses = dict()
        for i in range (-3,4):
            for j in range (-3,4):
                r = i**2 + j**2
                if not r in radiuses:
                    radiuses[r] = []
                radiuses[r].append((i,j))
                
        return radiuses
                
    


def loadTiles():
    ''' A function called when the program start to load the 
    tiles directions
    the tile files directory hirrarchy is 
    <fam>/<name>.tile
    Each .tile file may holds several entries in the following format
    tile:\n 
    <x>,<y>\t<red>\t<green>\t<blue>\t<alpha>\n
    
    The "tile:" line holds only that this line tells the program to start a new tile
    <x> and <y> are the x,y coordinates inside the tile (starting from top lef) to color
    <red>,<green>,and, <blue> are the red, green, and blue values of the color. 
    Finally, <alpha> is the transperacy level (0 is compltely transparent). 
    All valus are integer and the angular brackets are not needed in the file. 
    Example line:
    26, 47, 0, 0, 127, 255
    '''
    
    tileDB = dict()
    tilesPath = './Tiles'
    fams = os.walk(tilesPath).__next__()[1]
    for fam in fams:
        tileDB[fam] = dict()    
        path = tilesPath + '/' + fam
        names = os.walk(path).__next__()[2]
        for n in names:
            parts = n.split('.')
            if not len(parts) == 2: continue
            if not parts[1] == 'tile': continue
            tileDB[fam][parts[0]] = []
            file = open(path + '/'+n).readlines()[:]
            tile = []
            for line in file:
                if 'tile:' in line:
                    if len(tile) == 0: continue
                    tileDB[fam][parts[0]].append(tile)
                    tile = []
                    continue
                line = line.split()
                xyindex = line[0].split(',')
                xyindex = (int(xyindex[0]),int(xyindex[1]))
                tileLine = [xyindex,int(line[1]),int(line[2]),int(line[3]),int(line[4])]
                tile.append(tileLine)
            if not len(tile) == 0:
                tileDB[fam][parts[0]].append(tile)
            
              
    '''removing empty entries'''
    out = dict()
    for fam in tileDB:
        if len(tileDB[fam]) == 0:
            continue
        out[fam] = dict()
        for tile in tileDB[fam]:
            if len(tileDB[fam][tile]) == 0: 
                continue
            out[fam][tile] = tileDB[fam][tile][:]
    
    return out




    

def main():
    app = QtGui.QApplication(sys.argv)
    window=MainGui()
    app.installEventFilter(window)
    
    sys.exit(app.exec_())
    
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()
