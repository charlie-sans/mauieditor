## .net maui gui designer Wysiwyg

import os
import sys
import json
import time
import PySide6
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebChannel import *
from PySide6.QtNetwork import *
from PySide6.QtPrintSupport import *
from PySide6.QtSvg import *
from PySide6.Qt3DCore import *
from PySide6.Qt3DRender import *
from PySide6.Qt3DExtras import *
# list of CSharp controls
items = [
    ("Button", "<Button />"),
    ("Label", "<Label />"),
    ("Textbox", "<Textbox />"),
    ("Checkbox", "<Checkbox />"),
    ("Radio Button", "<RadioButton />"),
    ("Listbox", "<Listbox />"),
    ("Combobox", "<Combobox />"),
    ("Image", "<Image />"),
    ("Video", "<Video />"),
    ("Audio", "<Audio />"),
    ("Webview", "<Webview />"),
    ("Canvas", "<Canvas />"),
    ("Chart", "<Chart />"),
    ("Table", "<Table />"),
    ("Grid", "<Grid />"),
    ("Panel", "<Panel />"),
    ("Groupbox", "<Groupbox />"),
    ("Tab", "<Tab />"),
    ("Accordion", "<Accordion />"),
    ("Progressbar", "<Progressbar />"),
    ("Slider", "<Slider />"),
    ("Spinner", "<Spinner />"),
    ("Calendar", "<Calendar />"),
    ("Clock", "<Clock />"),
    ("Map", "<Map />"),
    ("QR Code", "<QRCode />"),
    ("Barcode", "<Barcode />"),
    ("Color Picker", "<ColorPicker />"),
    ("Date Picker", "<DatePicker />"),
    ("Time Picker", "<TimePicker />"),
    ("File Picker", "<FilePicker />"),
    ("Treeview", "<Treeview />"),
    ("Menu", "<Menu />"),
    ("Toolbar", "<Toolbar />"),
    ("Statusbar", "<Statusbar />"),
    ("Dialog", "<Dialog />"),
    ("Tooltip", "<Tooltip />"),
    ("Notification", "<Notification />"),
    ("Toast", "<Toast />"),
    
]

class CustomWidget(QGraphicsItem):
        def __init__(self):
            super().__init__()
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
            self.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.setAcceptHoverEvents(True)
            self.cornerGrabber = QRectF(-10, -10, 20, 20)
            self.centerGrabber = QRectF(-5, -5, 10, 10)
            self.rect = QRectF(0, 0, 100, 100)
            self.text = ""  # Initialize text
            self.resizeMode = None  # Initialize resizeMode

        def boundingRect(self):
            return self.rect

        def paint(self, painter, option, widget):
            painter.drawRect(self.rect)
            painter.fillRect(self.cornerGrabber, Qt.red)
            painter.fillRect(self.centerGrabber, Qt.blue)
            painter.drawText(self.rect, Qt.AlignCenter, self.text)  # Draw the text

        def itemChange(self, change, value):
            if change == QGraphicsItem.ItemPositionChange:
                self.cornerGrabber.moveTopLeft(self.rect.topLeft())
                self.centerGrabber.moveCenter(self.rect.center())
            
            return super().itemChange(change, value)

        def hoverMoveEvent(self, event):
            if self.cornerGrabber.contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.centerGrabber.contains(event.pos()):
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                if self.cornerGrabber.contains(event.pos()):
                    self.setCursor(Qt.SizeFDiagCursor)
                    self.resizeMode = "corner"
                elif self.centerGrabber.contains(event.pos()):
                    self.setCursor(Qt.SizeAllCursor)
                    self.resizeMode = "center"
                else:
                    self.setCursor(Qt.ClosedHandCursor)
                    self.resizeMode = None
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            if self.resizeMode == "corner":
                self.rect.setBottomRight(event.pos())
            elif self.resizeMode == "center":
                delta = event.pos() - event.lastPos()
                self.rect.translate(delta)
            else:
                super().mouseMoveEvent(event)

        def mouseReleaseEvent(self, event):
            self.setCursor(Qt.ArrowCursor)
            self.resizeMode = None
            super().mouseReleaseEvent(event)
            
        def setText(self, text):
            self.text = text
            

class CustomView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WYSIWYG GUI Editor")

        self.resize(800, 600)
        self.drawcanvas()
        
        
    def drawcanvas(self):
        # buttons and lists that can be dragged and dropped
        self.sidebar = QDockWidget("Sidebar", self)
        self.sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
        self.sidebar.setWidget(QListWidget())
        self.sidebar.setFloating(False)
        self.sidebar.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.sidebar.setFixedWidth(200)
        
        # add items to the listbox 
        self.sidebar.widget().addItems([i[0] for i in items])
        
        # canvas setup for drag and drop
        self.canvas = QGraphicsScene()
        self.view = QGraphicsView(self.canvas)
        self.setCentralWidget(self.view)
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.view.setAcceptDrops(True)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.TextAntialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.menuBar.setNativeMenuBar(True)
        self.menuBar.setCornerWidget(QPushButton("Save"))
        self.menuBar.setCornerWidget(QPushButton("Load"))
        self.menuBar.setCornerWidget(QPushButton("Preview"))
        self.menuBar.setCornerWidget(QPushButton("Export"))
        self.menuBar.setCornerWidget(QPushButton("Settings"))
        
        
        # setup menu options
        # Add menu items to an already set addAction()
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction("New")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        Exportmenu = fileMenu.addMenu("Export")
        Exportmenu.addAction("Export to C#")
        
        # setup bindings
        self.sidebar.widget().itemClicked.connect(self.addwidget)
        self.view.dropEvent = self.dropEvent
        self.view.dragEnterEvent = self.dragEnterEvent
        self.view.dragMoveEvent = self.dragMoveEvent
        
        # bind the menu buttons
        
        Exportmenu.triggered.connect(self.exporttoxaml)
        
        # self.view.mousePressEvent = self.mousePressEvent
        # self.view.mouseMoveEvent = self.mouseMoveEvent
        # self.view.mouseReleaseEvent = self.mouseReleaseEvent
        
    def addwidget(self, item):
        # add widget to canvas
        widget = CustomWidget()
        widget.setPos(0, 0)
        self.canvas.addItem(widget)
        # set widget text
        widget.setText(items[self.sidebar.widget().row(item)][1])
        # set widget size
        widget.rect = QRectF(0, 0, 100, 100)
        widget.update()
        
    def exporttoxaml(self):
        # export to xaml
        
        for item in self.canvas.items():
            print(item)
        
        
        
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()