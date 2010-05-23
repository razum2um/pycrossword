#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from main import Crossword
from PyQt4 import QtCore, QtGui
HEIGHT = 12
WIDTH = 12
COL_WIDTH = 35
ROW_HIEGHT = 35

class CharLineEdit(QtGui.QLineEdit):
    def __init__(self, parent = None):
        #QtGui.QLineEdit.__init__(self, parent)
        super(CharLineEdit, self).__init__(parent)

        #self.connect(self, QtCore.SIGNAL("cursorPositionChanged()"), self, QtCore.SIGNAL("editingFinished()"))
        #self.connect(self, QtCore.SIGNAL("textChanged()"), self.finish)

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Right or ev.key() == QtCore.Qt.Key_Left:
            QtGui.QApplication.sendEvent(self, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier))
        else:
            QtGui.QLineEdit.keyPressEvent(self, ev)

    #def eventFilter( self, obj, event ):
    #    print 'event'
    #    if QtCore.Qt.Key_A <= event.key() <= QtCore.Qt.Key_Z:
    #        print event.key()
    #def finish(self):
    #    print 'we'
    #    self.emit(QtCore.SIGNAL('editingFinished()'), self.sender())

class LineEditDelegate(QtGui.QItemDelegate):
    def __init__(self, tw = None, cross = None, parent = None):
        self.cross = cross
        #print self.cross.solution()

        self.table_view = tw

        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = CharLineEdit(parent)
        editor.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
        return editor

    def paint(self, painter, option, index):
        text = index.model().data(index, QtCore.Qt.DisplayRole).toString()
        painter.save()

        
        try:
            #print index.column(), index.row()
            #print self.cross.get_cell(index.row(),index.column(),)
            if not self.cross.check_if_cell_clear(index.column(), index.row()):
                if text == self.cross.get_cell(index.column(), index.row()):
                    #print 'text == self.cross.get_cell(index.column(), index.row())'
                    # correct
                    if index == self.table_view.currentIndex():
                        #print 'index == self.table_view.currentIndex'
                        # highlight
                        painter.fillRect(option.rect, QtGui.QColor(0,232,52,200))
                    else:
                        painter.fillRect(option.rect, QtGui.QColor(0,232,52,127))
                else:
                    if not text:
                        #print 'not text'
                        if index == self.table_view.currentIndex():
                        # highlight
                            painter.fillRect(option.rect, QtGui.QColor(74,155,254,200))
                        else:
                            #print 'index == self.table_view.currentIndex'
                            #painter.eraseRect(option.rect)
                            painter.fillRect(option.rect, QtGui.QColor(74,155,254,127))
                    else:
                        # wrong
                        if index == self.table_view.currentIndex():
                        # highlight
                            painter.fillRect(option.rect, QtGui.QColor(255,55,0,200))
                        else:
                            painter.fillRect(option.rect, QtGui.QColor(255,55,0,127))

            if index == self.table_view.currentIndex() and not text:
                painter.fillRect(option.rect, QtGui.QColor(74,155,254,200))
        except TypeError:
            pass

        painter.drawText(option.rect,  QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter, text)
        painter.restore()

    def setEditorData(self, lineEdit, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole).toByteArray().data()
        lineEdit.setText(value)

    def setModelData(self, lineEdit, model, index):
        try:
            value = lineEdit.text()
            if value and not self.cross.check_if_cell_clear(index.column(), index.row()):
                model.setData(index, QtCore.QVariant(value[0]))
        except TypeError:
            pass
        

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class CrossTableView(QtGui.QTableView):
    def __init__(self, crossword = None, parent = None):
        HEIGHT = 12
        WIDTH = 12
        COL_WIDTH = 35
        ROW_HIEGHT = 35

        super(CrossTableView, self).__init__(parent)
        #self.reset()
        try:
            self.model().clear()
        except AttributeError:
            # 1st run
            print 'pass'
            pass

        model = QtGui.QStandardItemModel(WIDTH, HEIGHT)
        selection_model = QtGui.QItemSelectionModel(model)
        self.setModel(model)
        #self.model().beginResetModel()

        self.setSelectionModel(selection_model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        for i in range(WIDTH):
            self.setColumnWidth(i, COL_WIDTH)
        for i in range(HEIGHT):
            self.setRowHeight(i, ROW_HIEGHT)
        
        #if crossword:
        #delegate = LineEditDelegate(self, crossword)
        #self.setItemDelegate(delegate)
        
        #for row in range(4):
        #    for column in range(2):
        #        index = model.index(row, column, QtCore.QModelIndex())
        #        model.setData(index, QtCore.QVariant((row+1) * (column+1)))
        
        #self.setWindowTitle("Delegate")

        #self.connect(selection_model, QtCore.SIGNAL("selectionChanged ( QItemSelection, QItemSelection)"), self.item_changed)
        
#    def item_changed(self, index, index2):
        #index = index.indexes()[0]
        #print index.row()
        #print index.column()
            

if __name__ == "__main__":
    
    word_list = ['saffron', 'The dried, orange yellow plant used to as dye and as a cooking spice.'], \
             ['leaven', 'An agent, such as yeast, that cause batter or dough to rise..'], \
             ['coda', 'Musical conclusion of a movement or composition.'], \
             ['paladin', 'A heroic champion or paragon of chivalry.']

    crossword = Crossword(WIDTH, HEIGHT, ' ', 5000, word_list)
    crossword.compute_crossword(2)

    app = QtGui.QApplication(sys.argv)
    tw = CrossTableView(crossword)
    tw.show()
    sys.exit(app.exec_())
