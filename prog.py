#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,os, re
from PyQt4 import QtCore, QtGui
from gui import CrossTableView, LineEditDelegate
from main import Crossword
import pickle

HEIGHT = 12
WIDTH = 12
COL_WIDTH = 35
ROW_HIEGHT = 35
CONFIG_DAT = 'config.dat'

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(ApplicationWindow, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        ## menu ##
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.load_txt, QtCore.Qt.CTRL + QtCore.Qt.Key_H)
        self.file_menu.addAction('&Quit', self.quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)
        ## end menu ##

        self.main_widget = QtGui.QWidget(self)
        l = QtGui.QGridLayout(self.main_widget)
        

        self.label = QtGui.QTextEdit()
        self.compute = QtGui.QPushButton('Compute')
        #
        #crossword = Crossword(WIDTH, HEIGHT, ' ', 5000, word_list)
        #crossword.compute_crossword(2)
        #import pickle
        #self._crossword = pickle.load(open('dump_vert'))

        #print crossword.solution()
        #self._crossword = crossword
        
        self.table_view = CrossTableView()
        self.load_prev_crossword()

        ## what's word under select coords ###
        self._table_rows = self.built_ass_table(False, HEIGHT)
        self._table_cols = self.built_ass_table(True, WIDTH)
        #for n_row in range(HEIGHT):
        #    for word in self._crossword.current_word_list:
        #        if not word.vertical and word.row == n_row:
        #                #print 'rows: hoz', word.row, word.word, 'cur_row', n_row
        #                # append it
        #                self.append_to_indexed_dic(n_row,{word.word:word.clue},self._table_rows)
        #        elif word.vertical and word.row <= n_row < word.length + word.row:
        #                #print 'rows: vert', word.row, word.length, word.word, 'cur_row', n_row
        #                # word's letter on the row
        #                # append it
        #                self.append_to_indexed_dic(n_row,{word.word:word.clue},self._table_rows)
        # 
        #for n_col in range(WIDTH):
        #    for word in self._crossword.current_word_list:
        #        if word.vertical and word.col == n_col:
        #                # append it
        #                self.append_to_indexed_dic(n_col,{word.word:word.clue},self._table_cols)
        #        elif not word.vertical and word.col <= n_col < word.length + word.col:
        #                # word's letter on the col
        #                # append it
        #                self.append_to_indexed_dic(n_col,{word.word:word.clue},self._table_cols)
        
        #print '\nself._table_rows.items'
        #for k,v in self._table_rows.items():
        #    print k,v.keys()
            
        #print '\nself._table_cols.items'
        #for k,v in self._table_cols.items():
        #    print k,v.keys()
            

        #model = QtGui.QStandardItemModel(WIDTH, HEIGHT)
        #selection_model = QtGui.QItemSelectionModel(model)
        #self.table_view.setModel(model)
        #self.selection_model = QtGui.QItemSelectionModel(model)
        #self.table_view.setSelectionModel(self.selection_model)

        #delegate = LineEditDelegate(self.table_view, self._crossword)
        #self.table_view.setItemDelegate(delegate)
        
        self.label.setHtml(self.gen_html())

        l.addWidget(self.table_view, 0,0,2,1)
        l.addWidget(self.label, 0,1)
        l.addWidget(self.compute, 1,1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Viva!", 2000)

        #self.connect(self.selection_model, QtCore.SIGNAL("selectionChanged ( QItemSelection, QItemSelection)"), self.selected_item_changed)
        self.connect(self.compute, QtCore.SIGNAL("clicked()"), self.shuffle)

    def gen_html(self):
        html = '<html><body>'
        html += 'Horizontal<br>'
        hor = filter(lambda(x):not x.vertical,  self._crossword.current_word_list)
        for w in hor:
            html += w.clue.strip()
            html += '<br>'
        html += '<br>Vertical<br>'
        ver = filter(lambda(x):x.vertical,  self._crossword.current_word_list)
        for w in ver:
            html += w.clue.strip()
            html += '<br>'
        html += '</body></html>'
        return html 

    def built_ass_table(self,is_col_table,max):
        table = {}
        for n_row_col in range(max):
            for word in self._crossword.current_word_list:
                if is_col_table:
                    if word.vertical and word.col == n_row_col:
                        self.append_to_indexed_dic(n_row_col,{word.word:word.clue},table)
                    elif not word.vertical and word.col <= n_row_col < word.length + word.col:
                        # word's letter on the col
                        # append it
                        self.append_to_indexed_dic(n_row_col,{word.word:word.clue},table)
                else:
                    if not word.vertical and word.row == n_row_col:
                        #print 'rows: hoz', word.row, word.word, 'cur_row', n_row_col
                        # append it
                        self.append_to_indexed_dic(n_row_col,{word.word:word.clue},table)
                    elif word.vertical and word.row <= n_row_col < word.length + word.row:
                        #print 'rows: vert', word.row, word.length, word.word, 'cur_row', n_row_col
                        # word's letter on the row
                        # append it
                        self.append_to_indexed_dic(n_row_col,{word.word:word.clue},table) 
        return table

    def shuffle(self):
        self._crossword.compute_crossword(2)
        self.compute_new()

    def compute_new(self):
    
        ## debug ####################################
        #import pickle, os 
        #if self._crossword.current_word_list[0].vertical and not os.access('dump_vert', os.F_OK):
        #    pickle.dump(self._crossword, open('dump_vert', 'w'))
        #elif not self._crossword.current_word_list[0].vertical and not os.access('dump_hor', os.F_OK):
        #    pickle.dump(self._crossword, open('dump_hor', 'w'))
            
        #if not self._crossword or not  self._crossword.current_word_list[0].vertical:
        #    crossword = pickle.load(open('dump_vert'))
        #else:
        #    crossword = pickle.load(open('dump_hor'))
        #self._crossword = crossword

        print self._crossword.solution()
        ################################################

        #self.table_view = CrossTableView(self._self._crossword)
        try:
            self.table_view.model().clear()
        except AttributeError:
            pass
        #self.table_view.selectionModel().clear()
        #model2 = None
        model = QtGui.QStandardItemModel(WIDTH, HEIGHT)
        self.table_view.setModel(model)

        self.selection_model = QtGui.QItemSelectionModel(model)
        self.table_view.setSelectionModel(self.selection_model)

        delegate = LineEditDelegate(self.table_view, self._crossword)
        self.table_view.setItemDelegate(delegate)

        self.table_view.configure()

        self.connect(self.selection_model, QtCore.SIGNAL("selectionChanged ( QItemSelection, QItemSelection)"), self.selected_item_changed)

        self._table_rows = self.built_ass_table(False, HEIGHT)
        self._table_cols = self.built_ass_table(True, WIDTH)
        self.label.setHtml(self.gen_html())
        #return self._crossword

    def quit(self):
        pickle.dump(self._crossword, open(CONFIG_DAT, 'w'))
        self.close()

    def load_prev_crossword(self):
        if os.access(CONFIG_DAT, os.F_OK):
            self._crossword = pickle.load(open(CONFIG_DAT))
            self.compute_new()
        else:
            self.load_txt()

    def about(self):
        msg = QtGui.QMessageBox()
        msg.setText("Author: Vlad Bokov")
        msg.show()

    def load_txt(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, QtCore.QString("Open file"), os.getcwd(), QtCore.QString("Text files (*.txt)"))
        raw = open(fileName).read()
        words = re.findall('(\w+).*?=.*?(.*)', raw)

        crossword = Crossword(WIDTH, HEIGHT, ' ', 5000, words)
        self._crossword = crossword
        self._crossword.compute_crossword(2)
        self.compute_new()

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
        #print to_be_marked
        MARK_TAG_BEFORE='<i><font color="red">'
        MARK_TAG_AFTER='</font></i>'

        t = self.label.toPlainText()
        for m in to_be_marked:
            raw = m.strip()
            t = t.replace(raw, MARK_TAG_BEFORE+raw+MARK_TAG_AFTER)
            t = t.replace('\n', '<br>')
        self.label.setHtml('<html><body>'+t+'</body></html>')

    def append_to_indexed_dic(self, index, value, dic):
        if index not in dic:
            dic[index] = value
        elif index in dic: # and value not in dic[index]:
            dic[index].update(value)  


if __name__ == "__main__":
    
    word_list = ['saffron', 'The dried, orange yellow plant used to as dye and as a cooking spice.'], \
             ['leaven', 'An agent, such as yeast, that cause batter or dough to rise..'], \
             ['coda', 'Musical conclusion of a movement or composition.'], \
             ['paladin', 'A heroic champion or paragon of chivalry.']

    app = QtGui.QApplication(sys.argv)
    wd = ApplicationWindow()
    wd.show()
    sys.exit(app.exec_())
