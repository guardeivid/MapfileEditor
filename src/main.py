import sys
from PyQt4 import uic, QtGui, QtCore, Qt
import mapscript
from osgeo import gdal, ogr
import mapSettings, mf_debugLog

(Ui_MapfileEditor, QMainWindow) = uic.loadUiType('ui/mainwindow.ui')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MapfileEditorApplication(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super (MapfileEditorApplication, self).__init__(parent)
        self.createWidgets()
        
        # Global Configuration
        self.config = {}
        self.config["debug"] = mf_debugLog.debugObj()
        self.firstDir = '~/'
        
        # Constants []
        self.msLogical = {'MS_TRUE':1, 'MS_ON':1, 'MS_YES':1, 'MS_FALSE':0, 'MS_OFF':0, 'MS_NO':0}
        #TODO: use dict instead of list and use .keys() for ui part
        #self.units = ['inches', 'feet' ,'miles', 'meters', 'kilometers', 'dd', 'pixels', 'pourcentages', 'nauticalmiles']
        self.layerTypes = ['point', 'line', 'polygon', 'raster', 'annotation', 'query', 'circle', 'tileindex']
        self.connectionTypes = ['inline', 'shapefile', 'tiled shapefile', 'sde', 'ogr','postgis','wms', 'oracle spatial', 'wfs', 'graticule', 'mygis', 'raster']

        self.new()

        self.connect(self.ui.actionNew, QtCore.SIGNAL(_fromUtf8("activated()")), self.new)
        self.connect(self.ui.mf_tb_new, QtCore.SIGNAL(_fromUtf8("clicked()")), self.new)
        self.connect(self.ui.actionOpen, QtCore.SIGNAL(_fromUtf8("activated()")), self.open)
        self.connect(self.ui.mf_tb_open, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open)
        self.connect(self.ui.actionSave, QtCore.SIGNAL(_fromUtf8("activated()")), self.save)
        self.connect(self.ui.mf_tb_save, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save)
        self.connect(self.ui.actionSaveAs, QtCore.SIGNAL(_fromUtf8("activated()")), self.saveas)
        self.connect(self.ui.actionMapSetting, QtCore.SIGNAL(_fromUtf8("activated()")), self.mapSettingsWindows)
        self.connect(self.ui.mf_tb_mapparameter, QtCore.SIGNAL(_fromUtf8("clicked()")), self.mapSettingsWindows)
        self.connect(self.ui.mf_structure, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.openDialog)
        # Bug: not working
        self.connect(self.ui.mf_structure, QtCore.SIGNAL(_fromUtf8("entered(QModelIndex)")), self.openDialog)

        self.undoStack = QtGui.QUndoStack(self)
        #self.createUndoView()

        undoAction = self.undoStack.createUndoAction(self, QtCore.QCoreApplication.translate("MapFileEditor", "&Undo"));
        undoAction.setShortcuts(Qt.QKeySequence.Undo);

        redoAction = self.undoStack.createRedoAction(self, QtCore.QCoreApplication.translate("MapFileEditor", "&Redo"));
        redoAction.setShortcuts(Qt.QKeySequence.Redo);

        editMenu = self.menuBar().addMenu( QtCore.QCoreApplication.translate("MapFileEditor", "&Edit"));
        editMenu.addAction(undoAction);
        editMenu.addAction(redoAction);

    # ###########################
    # Settings Windows
    # ###########################
    def mapSettingsWindows(self):
        mapSettingsUi = mapSettings.MapSettings(self.map, self.config)
        self.map = mapSettingsUi.openMapSettings()

    # ##########################
    # Actions (Menu)
    # ##########################

    def new(self):
        # reste du mapfile
        self.map = mapscript.mapObj()
        self.updateMapStructure()

    def open(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(None, "Select one file to open", self.firstDir, "MapFile (*.map);;Text (*.txt);;All (*.*)"))
        self.map = mapscript.mapObj(self.filename)
        try:
            self.map = mapscript.mapObj(self.filename)
        except Exception:
            self.ui.statusbar.showMessage('Error: opening mapfile failed.')
        
        self.ui.statusbar.showMessage('Info: mapfile opened.')
        self.updateMapStructure()

    def save(self):
        self.map.save(self.filename)
        self.updateMapStructure()
        self.ui.statusbar.showMessage('Info: mapfile saved.')

    def saveas(self):
        self.filename = str(QtGui.QFileDialog.getSaveFileName(None, "Select you file to save", self.firstDir, "MapFile (*.map);;Text (*.txt);;All (*.*)"))

        self.map.save(self.filename)
        self.updateMapStructure()
        self.ui.statusbar.showMessage('Info: mapfile saved.')

    # ##########################
    # Common Method
    # ##########################
    def createUndoView(self):
        self.undoWindows = QtGui.QDialog()
        self.undoWindows.show()

        undoView = QtGui.QUndoView(self.undoWindows)
        undoView.setWindowTitle(QtCore.QCoreApplication.translate("MapFileEditor", "Command List"))
        undoView.show();
        undoView.setAttribute(Qt.Qt.WA_QuitOnClose, False);

    def updateMap(self):
        cloneMap = self.map.clone()
        cloneMap.setSize(500,500)
        if(cloneMap.extent.maxx == -1 or cloneMap.extent.maxy == -1 or cloneMap.extent.minx == -1 or cloneMap.extent.miny == -1):
            cloneMap.setExtent(-180,-90,180,90)

        try:
            imageObj = cloneMap.draw()
        except Exception: 
            self.ui.statusbar.showMessage("Error: map can't be draw")

        imageObj.save('/tmp/mapfileEditor.'+cloneMap.outputformat.extension)
        scene = QtGui.QGraphicsScene()
        pixMap = QtGui.QPixmap('/tmp/mapfileEditor.'+cloneMap.outputformat.extension)
        scene.addPixmap(pixMap)
        self.ui.mf_preview.setScene(scene)
        self.ui.mf_preview.show()

    def openDialog(self, item):
        if(item.row() == 0):
           self.mapSetting() 

    def updateMapStructure(self):
        # reset du model
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderItem(0, QtGui.QStandardItem('Key'))
        #self.model.setHorizontalHeaderItem(1, QtGui.QStandardItem('Value'))

        parentItem = self.model.invisibleRootItem()

        self.ui.statusbar.showMessage('Info: mapfile structure added.')
        mapItem = QtGui.QStandardItem('Map parameters')

        mapItem.setEditable(False)
        parentItem.appendRow(mapItem)

        #layersChild = QtGui.QStandardItem()
        layersItems = QtGui.QStandardItem('Layers')
        layersItems.setEditable(False)
        for index in range(self.map.numlayers):
            layer = self.map.getLayer(index)
            title = 'Layer #1 '+layer.name
            layerItem = QtGui.QStandardItem(title)
            layerItem.setToolTip(title)
            layerItem.setEditable(False)
            layerItem.setCheckable(True)
            layerItem.setCheckState(layer.status)
            layersItems.appendRow(layerItem)

        #layersChild.setChild(0, layersItems)
        parentItem.appendRow(layersItems)
        self.ui.mf_structure.setModel(self.model)
        self.ui.mf_structure.expandAll()
        #self.ui.view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.updateMap()

    def createWidgets(self):
        self.ui = Ui_MapfileEditor()
        self.ui.setupUi(self)

            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MapfileEditorApplication()
    myapp.show()
    sys.exit(app.exec_())

