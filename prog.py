#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, re
from PyQt4 import QtCore, QtGui
from gui import CrossTableView, LineEditDelegate
from main import Crossword

HEIGHT = 12
WIDTH = 12
COL_WIDTH = 35
ROW_HIEGHT = 35

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(ApplicationWindow, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QGridLayout(self.main_widget)


        self.label = QtGui.QTextEdit()
        self.compute = QtGui.QPushButton('Compute')
        self.compute_new()

        l.addWidget(self.table_view, 0,0,2,1)
        l.addWidget(self.label, 0,1)
        l.addWidget(self.compute, 1,1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Viva!", 2000)

        self.connect(self.table_view.selectionModel(), QtCore.SIGNAL("selectionChanged ( QItemSelection, QItemSelection)"), self.selected_item_changed)
        self.connect(self.compute, QtCore.SIGNAL("clicked()"), self.compute_new)

    def compute_new(self):
        crossword = Crossword(WIDTH, HEIGHT, ' ', 5000, word_list)
        crossword.compute_crossword(2)
        print crossword.solution()

        self._crossword = crossword
        ### what's word under select coords ###
        self._table_rows = {}
        for n_row in range(HEIGHT):
            for word in self._crossword.current_word_list:
                if not word.vertical and word.row == n_row:
                        #print 'rows: hoz', word.row, word.word, 'cur_row', n_row
                        # append it
                        self.append_to_indexed_dic(n_row,{word.word:word.clue},self._table_rows)
                elif word.vertical and word.row <= n_row < word.length + word.row:
                        #print 'rows: vert', word.row, word.length, word.word, 'cur_row', n_row
                        # word's letter on the row
                        # append it
                        self.append_to_indexed_dic(n_row,{word.word:word.clue},self._table_rows)
        
        self._table_cols = {}
        for n_col in range(WIDTH):
            for word in self._crossword.current_word_list:
                if word.vertical and word.col == n_col:
                        # append it
                        self.append_to_indexed_dic(n_col,{word.word:word.clue},self._table_cols)
                elif not word.vertical and word.col <= n_col < word.length + word.col:
                        # word's letter on the col
                        # append it
                        self.append_to_indexed_dic(n_col,{word.word:word.clue},self._table_cols)
        
        #print 'self._table_rows.items'
        #for k,v in self._table_rows.items():
        #    print k,v     
            
        #print 'self._table_cols.items'
        #for k,v in self._table_cols.items():
        #    print k,v     
            
        #    
        #    self._table.update({(word.row, word.col):word.clue})

        self.table_view = CrossTableView(self._crossword)
        #self.table_view.model().clear()
        delegate = LineEditDelegate(self.table_view, crossword)
        self.table_view.setItemDelegate(delegate)
        
        #self.label = QtGui.QLabel('\n'.join([x.clue for x in self._crossword.current_word_list]))
        html = '<html><body>'
        #html += '<style type="text/css"> p.marked {font-size:larger} </style>'
        html += 'Horizontal<br>'
        hor = filter(lambda(x):not x.vertical,  self._crossword.current_word_list)
        for w in hor:
            html += w.clue
            html += '<br>'
        html += '<br>Vertical<br>'
        ver = filter(lambda(x):x.vertical,  self._crossword.current_word_list)
        for w in ver:
            html += w.clue
            html += '<br>'
        html += '</body></html>'
        self.label.setHtml(html)

    def selected_item_changed(self, index, index2):
        curr_index = index.indexes()[0]
        try:
            to_be_marked_by_row = self._table_rows[curr_index.row()]
        except KeyError:
            pass
        try:
            to_be_marked_by_col = self._table_cols[curr_index.column()]
        except KeyError:
            pass
        to_be_marked = [to_be_marked_by_row[v] for v in  filter(lambda x: x in to_be_marked_by_col, to_be_marked_by_row)]
        #print [to_be_marked_by_row[x] for x in to_be_marked]
        MARK_TAG_BEFORE='<span style=" font-style:italic; color:#ff0000;">'
        MARK_TAG_AFTER='</span>'
        self.label.setHtml(self.label.toHtml().replace(MARK_TAG_BEFORE, ''))
        self.label.setHtml(self.label.toHtml().replace(MARK_TAG_AFTER, ''))

        for m in to_be_marked:
            self.label.setHtml(self.label.toHtml().replace(m, MARK_TAG_BEFORE+m+MARK_TAG_AFTER))
        #print self.label.toHtml()

    def append_to_indexed_dic(self, index, value, dic):
        #index += 1 # WHY?!
        if index not in dic:
            dic[index] = value
        elif index in dic: # and value not in dic[index]:
            dic[index].update(value)  


if __name__ == "__main__":
    
    word_list = ['saffron', 'The dried, orange yellow plant used to as dye and as a cooking spice.'], \
             ['leaven', 'An agent, such as yeast, that cause batter or dough to rise..'], \
             ['coda', 'Musical conclusion of a movement or composition.'], \
             ['paladin', 'A heroic champion or paragon of chivalry.']

    #crossword = Crossword(WIDTH, HEIGHT, ' ', 5000, word_list)
    #crossword.compute_crossword(2)

    app = QtGui.QApplication(sys.argv)
    wd = ApplicationWindow()
    wd.show()
    sys.exit(app.exec_())