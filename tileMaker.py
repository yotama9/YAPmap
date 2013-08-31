#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
This is a helper program to TAPmap.py. It is used to create tiles and add them to a menu.
"""



import sys,os
import re
from PyQt4 import QtGui, QtCore
from tile import *

class MainGui(QtGui.QWidget):
    
    def __init__(self):
        #Setting some important constant. 
        super(MainGui,self).__init__()

        # The starting and ending of the tile drawing area
        self.startX = 25
        self.startY = 15
        self.endX = 425
        self.endY = 415
        self.curFam = ''
        self.mousePos = [-1,-1]
        self.eraseMode = False
        self.overWriteMode = False


        # Here we store the data about each square
        self.squares = dict()
        #The initial parameters 
        self.color = QtGui.QColor(0,0,0,255)
        self.tileFamilies = dict()
        self.fams = []
        self.initUI()

    def initUI(self):
        # Setting the window
        self.setGeometry(10,10,self.endX + 100,self.endY)
        self.setWindowTitle('YAPMaker.py')
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(self.endX+125,self.endY+15)
        self.layout = QtGui.QVBoxLayout(self)
        self.makeButtons()
        self.show()
    
    def makeButtons(self):
        self.closeButton = QtGui.QPushButton('Close',self)
        self.closeButton.clicked.connect(self.closePressed)
        self.layout.addWidget(self.closeButton)
        self.colButton = QtGui.QPushButton('Color',self)
        self.colButton.clicked.connect(self.deterColor)
        self.layout.addWidget(self.colButton)
        self.loadTilesNames()
        self.famCombo = QtGui.QComboBox(self)
        self.famCombo.addItems(self.fams)
        self.layout.addWidget(self.famCombo)
        self.nameCombo = QtGui.QComboBox(self)
        self.nameCombo.addItems(self.names)
        self.layout.addWidget(self.nameCombo)
        self.paintStatus = QtGui.QButtonGroup(self)
        self.paintButton = QtGui.QRadioButton('Paint',self)
        self.eraseButton = QtGui.QRadioButton('Erase',self)
        self.overWriteButton = QtGui.QRadioButton('Keep',self)
        self.paintStatus.addButton(self.paintButton)
        self.paintStatus.addButton(self.eraseButton)
        self.paintStatus.addButton(self.overWriteButton)
        self.layout.addWidget(self.paintButton)
        self.layout.addWidget(self.eraseButton)
        self.layout.addWidget(self.overWriteButton)
        self.paintButton.setChecked(True)

        
    def loadTilesNames(self):
        tilesPath = './Tiles'
        tiles = os.walk(tilesPath).__next__()
        self.fams = tiles[1]
        self.names = []
        if (len(self.fams) > 0):
            fam = self.fams[0]
            path = tilesPath + '/' + fam
            names = os.walk(path).__next__()[2]
            for n in names:
                parts = n.split('.')
                if not len(parts) == 2: continue
                if not parts[1] == 'tile': continue
                self.names.append(parts[0])
        self.fams.append('new family')
        self.names.append('new tile')


    def deterColor(self):
        self.color = QtGui.QColorDialog.getColor()
        if not self.color.isValid():
            self.color = QtGui.QColor(0,0,0,255)
    

    def updateButtons(self):
        self.famCombo.move(self.endX + 30,15)
        self.famCombo.resize(80,30)
        self.updateNameCombo()
        self.nameCombo.move(self.endX + 30,50)
        self.nameCombo.resize(80,30)
        self.closeButton.move(self.endX +30,85)
        self.closeButton.resize(80,30)
        self.colButton.move(self.endX +30,120)
        self.colButton.resize(80,30)
        self.paintButton.move(self.endX +30, 155)
        self.paintButton.resize(80,30)
        self.eraseButton.move(self.endX +30,190)
        self.eraseButton.resize(80,30)
        self.overWriteButton.move(self.endX+30,225)
        self.overWriteButton.resize(80,30)

    def updateNameCombo(self):
        #The tiles family
        fam = self.famCombo.currentText()
        # Erasing the old names
        if self.curFam == fam:
            return
        while self.nameCombo.count() > 0:
            self.nameCombo.removeItem(0)
        self.curFam = fam[:]
        self.names = []
        if fam == 'new family': 
            self.names = ['new tile']
        #The new names
        else:
            path = './Tiles/{fam}'.format(fam=fam)
            names = os.walk(path).__next__()[2]
            for name in names:
                parts = name.split('.')
                if not len (parts) == 2: continue
                if not parts[1] == 'tile': continue
                self.names.append(parts[0])
            self.names.append('new tile')
        self.nameCombo.addItems(self.names)
        


    def paintEvent(self,event):
        self.updateButtons()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.paintFrames(qp)
        self.markMouse(qp)
        self.colorTiles(qp)
        qp.end()

    def colorTiles(self,qp):
        trmSquares = []
        for square in self.squares:
            color = self.squares[square]
            qp.setBrush(color)
            pen = qp.pen()
            pen.setColor(QtGui.QColor(0,0,0,0))
            qp.setPen(pen)
            i,j = square[0], square[1]
            if i >= 50 or j >= 50:
                trmSquares.append(square)
                continue
            x,y = self.indexToXy(i,j)
            qp.drawRect(x,y,8,8)
            tileX,tileY = self.indexToTile(i,j)
            qp.drawRect(tileX,tileY,1,1)

        for square in trmSquares:
            del self.squares[square]
            
    def indexToTile(self,i,j):
        x = self.endX + i
        y = self.endY - 50 + j
        return (x,y)
    def markMouse(self,qp):
        """ draw a square arround the mouse """
        if (self.mousePos[0] < 0 or self.mousePos[1] < 0): return
        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        x,y = self.mousePos
        x,y = self.indexToXy(x,y)
        qp.drawLine(x,y,x+8, y)
        qp.drawLine(x,y+8,x+8, y+8)
        qp.drawLine(x,y,x,y+8)
        qp.drawLine(x+8,y,x+8,y+8)


    def xyToIndex(self,x,y):
        """ handle the translation of xy coordinates to index """
        if x < self.startX or x > self.endX or y < self.startY or y > self.endY:
            return (-1,-1)
        else:
            out = [int((x - self.startX)/8) ,int((y - self.startY)/8)]
        return out

    def indexToXy(self,i,j):
        """ Convert ij coordinates to actual position on the screen """
        out = [i*8 + self.startX,j*8+ self.startY]
        return out
        
    def mousePressEvent(self,e):
        """ Color the square under the mouse"""
        x,y = e.x(), e.y()
        i,j = self.xyToIndex(x,y)
        if x < self.startX or y < self.startY: return
        if x > self.endX or y > self.endY: return
        ij = (i,j)
        if self.eraseMode: #Erase this square
            if ij in self.squares: #Check it is collored
                del self.squares[ij]
        elif self.overWriteMode == True :
            if not ij in self.squares:
                self.squares[ij] = self.color
        else:
            self.squares[ij] = self.color
        self.update()

    def mouseMoveEvent(self,e):
        """ Color all the tiles that I select with the mouse """
        x,y = e.x(), e.y()
        if x < self.startX or y < self.startY: return
        if x > self.endX or y > self.endY: return
        i,j = self.xyToIndex(x,y)
        ij = (i,j)
        if self.eraseMode: #Erase this square
            if ij in self.squares: #Check it is colorred
                del self.squares[ij]
        elif self.overWriteMode == True : # The colorred tile are protected
            if not ij in self.squares: #This tile is not colorred
                self.squares[ij] = self.color
        else:
            self.squares[ij] = self.color
        return
        

    def paintFrames(self,qp):
        """ draw frames around the drawing area and the sample tile area"""
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        """ The drawing area"""
        qp.drawLine(self.startX, self.startY, self.endX, self.startY)
        qp.drawLine(self.startX, self.endY, self.endX, self.endY)
        qp.drawLine(self.startX, self.startY, self.startX, self.endY)
        qp.drawLine(self.endX, self.startY, self.endX, self.endY)
        """ The sample tile""" 
        qp.drawLine(self.endX,self.endY-50,self.endX+50,self.endY-50)
        qp.drawLine(self.endX,self.endY-50,self.endX+50,self.endY-50)
        qp.drawLine(self.endX+50,self.endY-50,self.endX+50,self.endY)
        qp.drawLine(self.endX,self.endY,self.endX+50,self.endY)
        
        """ Updating the paint status """
        self.eraseMode = False
        self.overWriteMode = False

        if self.eraseButton.isChecked():
            self.eraseMode = True
        elif self.overWriteButton.isChecked():
            self.overWriteMode = True
            

    def eventFilter(self,source,event):
        if event.type() == QtCore.QEvent.MouseMove:
            x,y = int(event.x()), int(event.y())
            if x < self.startX or x >= self.endX:
                self.mousePos = [-1,-1] 
                return False
            elif y < self.startY or y >= self.endY:
                self.mousePos = [-1,-1] 
                return False
            i,j = self.xyToIndex(x,y)
            self.mousePos = [i,j]
            self.update()
        return False

    def closePressed(self):
        self.closeProcedure()
        
    def closeEvent(self,e):
        self.closeProcedure()
        e.ignore()
        
    def closeProcedure(self):
        msg = "This will close the tile editor. Are you sure?"
        replay = QtGui.QMessageBox.question(self, 'Message',
                                            msg, QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if replay == QtGui.QMessageBox.No:
            return
        msg = "Save tile?"
        replay = QtGui.QMessageBox.question(self, 'Message',
                                            msg, QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if replay == QtGui.QMessageBox.No:
            exit()
        if self.saveTile():
            exit()
        
    def saveTile(self):
        #Getting the family and name of the tile
        if self.curFam == 'new family': 
            goodFam = self.makeFamily()
            if not goodFam: return False

        path = './Tiles/' + self.curFam + '/'
        # Add here a function for the case of new family
        name = self.nameCombo.currentText() 
        msg = 'Enter tile name'
        if not name == 'new tile':
            name += '.tile'
        while name == 'new tile':
            name,ok = QtGui.QInputDialog.getText(self, 'Input Dialog',msg)
            if not ok:
                return False
            if not re.match("^[A-Za-z0-9_-]*$",name) or name == '':
                name = 'new tile'
                msg = 'Invalid tile names.\nonly letters and numbers are valid.\nEnter tile name'
            if not name == 'new tile':
                name += '.tile'
            # Check if this tile files exist
            tiles = os.walk(path).__next__()[2]
            if name in tiles:
                msg = "Tile file exist. Append?"
                replay = QtGui.QMessageBox.question(self, 'Message',
                                            msg, QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
                print (replay)
                if replay == QtGui.QMessageBox.No:
                    msg = 'Enter tile name'
                    name = 'new tile'
                else:
                    name = replay
        path += name
        outFile = open(path,'a')
        outFile.write ('tile:\n')
        for ij in self.squares:
            line = '{i},{j}\t'.format(i=ij[0],j=ij[1])
            color = self.squares[ij]
            line += str(color.red())
            line += '\t'
            line += str(color.green())
            line += '\t'
            line += str(color.blue())
            line += '\t'
            line += str(color.alpha())
            line += '\n'
            outFile.write(line)
        outFile.close()
        return True
                
        
    def makeFamily(self):
        # This will be used to create tile family
        msg = 'What tile family would you like to create?'
        name,ok = QtGui.QInputDialog.getText(self, 'Input Dialog',msg)
        if not ok:
            return False
        
        while name in self.fams: # The tile family exist, allow the user to change tile family or append to the existing one
            msg2 = 'tile family exist, append?'
            replay = QtGui.QMessageBox.question(self, 'Message', msg2, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if replay == QtGui.QMessageBox.Yes:
                self.curFam = name
                return True #Change to True
            name,ok = QtGui.QInputDialog.getText(self, 'Input Dialog',msg)
            if not ok:
                return False
        self.curFam = name
        return True #change to True


def main():
    app = QtGui.QApplication(sys.argv)
    window=MainGui()
    app.installEventFilter(window)
    
    sys.exit(app.exec_())
    
    sys.exit(app.exec())

if __name__== '__main__':
    main()
