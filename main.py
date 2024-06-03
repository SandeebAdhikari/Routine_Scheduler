import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class TextWrapDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        # Draw background
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            painter.fillRect(option.rect, option.palette.base())

        # Draw text
        text = index.data(Qt.DisplayRole)
        doc = QTextDocument()
        doc.setTextWidth(option.rect.width())
        doc.setHtml(text)
        painter.translate(option.rect.topLeft())
        doc.drawContents(painter)

        painter.restore()

    def sizeHint(self, option, index):
        text = index.data(Qt.DisplayRole)
        doc = QTextDocument()
        doc.setHtml(text)
        return QSize(int(doc.idealWidth()), int(doc.size().height()))


class TaskScheduler(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Task Scheduler and Reminder')
        
        main_vertical_layout = QVBoxLayout()
        
        main_horizontal_layout = QHBoxLayout()
        
        
        left_layout = QVBoxLayout()
        
        self.top_left_taskInput = QTextEdit(self)
        self.top_left_taskInput.setPlaceholderText('Enter a new task')
        
        self.top_left_addButton = QPushButton('Add Task', self)
        self.top_left_addButton.clicked.connect(self.addTask)
        
        left_layout.addWidget(self.top_left_taskInput)
        left_layout.addWidget(self.top_left_addButton)
        
        right_layout = QVBoxLayout()
        
        self.time = QTimeEdit(self)
        self.time.setDisplayFormat("HH:mm")
        
        
        self.top_right_calendar = QCalendarWidget()
        self.top_right_calendar.setGridVisible(True)
        self.top_right_calendar.clicked.connect(self.selectDate)
        
        right_layout.addWidget(self.time)
        right_layout.addWidget(self.top_right_calendar)
        
        main_horizontal_layout.addLayout(left_layout)
        main_horizontal_layout.addLayout(right_layout)
        
        main_vertical_layout.addLayout(main_horizontal_layout)
        
        self.tree_taskList = QTreeWidget()
        self.tree_taskList.setHeaderLabels(["Date", "Time", "Task"])
        self.tree_taskList.setColumnWidth(0, 200)  # Set the Date column width
        self.tree_taskList.setColumnWidth(0, 200)
        self.tree_taskList.setColumnWidth(1, 300)
        self.tree_taskList.header().setSectionResizeMode(QHeaderView.Interactive)  # Allow resizing
        self.tree_taskList.setItemDelegate(TextWrapDelegate(self.tree_taskList))
        
        main_vertical_layout.addWidget(self.tree_taskList)
        

        #self.setLayout(main_horizontal_layout)
        self.setLayout(main_vertical_layout)
    
    def selectDate(self, date):
        self.selected_date = date 
             
    def addTask(self):
        task = self.top_left_taskInput.toPlainText()
        if task and self.selected_date:
            QTreeWidgetItem(self.tree_taskList,[self.selected_date.toString(), self.time.time().toString(), task])
            self.top_left_taskInput.clear()
            self.selected_date = None
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    scheduler = TaskScheduler()
    scheduler.show()
    sys.exit(app.exec_())