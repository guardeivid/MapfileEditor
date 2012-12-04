import sys
from PyQt4 import uic, QtGui, QtCore
import mapscript 

(Ui_MapfileEditor, QMainWindow) = uic.loadUiType('ui/mainwindow.ui')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MapfileEditorApplication(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super (MapfileEditorApplication, self).__init__(parent)
        self.createWidgets()
        
        # Constants
        self.filename = '/home/yves/mapfile.map'
        self.history = []
        self.units = ['dd', 'feet', 'inches', 'meters', 'miles', 'nauticalmiles', 'pixels']
        self.layerTypes = ['point', 'line', 'polygon', 'raster', 'annotation', 'query', 'circle', 'tileindex']
        self.connectionTypes = ['inline', 'shapefile', 'tiled shapefile', 'sde', 'ogr','postgis','wms', 'oracle spatial', 'wfs', 'graticule', 'mygis', 'raster']
        self.imageTypes = ['jpeg' ,'pdf','png' ,'svg']
        
        self.new()

        self.connect(self.ui.actionNew, QtCore.SIGNAL(_fromUtf8("activated()")), self.new)
        self.connect(self.ui.mf_tb_new, QtCore.SIGNAL(_fromUtf8("clicked()")), self.new)
        self.connect(self.ui.actionOpen, QtCore.SIGNAL(_fromUtf8("activated()")), self.open)
        self.connect(self.ui.mf_tb_open, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open)
        self.connect(self.ui.actionSave, QtCore.SIGNAL(_fromUtf8("activated()")), self.save)
        self.connect(self.ui.mf_tb_save, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save)
        self.connect(self.ui.actionMapSetting, QtCore.SIGNAL(_fromUtf8("activated()")), self.mapSetting)
        self.connect(self.ui.mf_tb_mapparameter, QtCore.SIGNAL(_fromUtf8("clicked()")), self.mapSetting)

    # ###########################
    # Settings Windows
    # ###########################
    def mapSetting(self):
        QMapSettingWindow = uic.loadUi('ui/mapSetting.ui')
        QMapSettingWindow.setModal(True)
  
        # Update form from MapFile
        QMapSettingWindow.mf_name.insert(self.map.name)
        QMapSettingWindow.mf_sizewidth.setValue(self.map.width)
        QMapSettingWindow.mf_sizeheight.setValue(self.map.height)
        QMapSettingWindow.mf_units.addItems(self.units) #dd|feet|inches|kilometers|meters|miles|nauticalmiles
        QMapSettingWindow.mf_units.setCurrentIndex(self.map.units)
        # -- outputformat list
        QMapSettingWindow.mf_default_outputformat.addItems(self.imageTypes)
        if (self.map.outputformat.name != '' and self.imageTypes.count(self.map.imagetype) == 0):
            QMapSettingWindow.mf_default_outputformat.addItem(name)

        QMapSettingWindow.mf_default_outputformat.setCurrentIndex(QMapSettingWindow.mf_default_outputformat.findText(self.map.imagetype))

        QMapSettingWindow.exec_()
        if(QMapSettingWindow.Accepted == True):
            self.saveMapSetting(QMapSettingWindow)

    def saveMapSetting(self, QMapSettingWindow):

        # Save form to MapFile
        Qtext = QMapSettingWindow.mf_name.text()
        self.map.name = str(Qtext)
        self.map.width = QMapSettingWindow.mf_sizewidth.value()
        self.map.height = QMapSettingWindow.mf_sizeheight.value()

        self.updateMapStructure()
        self.ui.statusbar.showMessage('Info: mapfile settings saved.')

    def createWidgets(self):
        self.ui = Ui_MapfileEditor()
        self.ui.setupUi(self)

    # ##########################
    # Actions (Menu)
    # ##########################

    def new(self):
        # reste du mapfile
        self.map = mapscript.mapObj()
        self.updateMapStructure()

    def open(self):
        try:
            self.map = mapscript.mapObj('/mnt/home_new/Documents/Developpement/Langage/Python/mapfile-editor/MapfileEditor/data/world_mapfile.map')
        finally:
            self.ui.statusbar.showMessage('Error: opening mapfile failed.')

        self.ui.statusbar.showMessage('Info: mapfile opened.')
        self.updateMapStructure()

    def save(self):
        self.map.save(self.filename)
        self.updateMapStructure()
        self.ui.statusbar.showMessage('Info: mapfile saved.')

    # ##########################
    # Common Method
    # ##########################
    def updateMap(self):
        cloneMap = self.map.clone()
        cloneMap.setSize(500,500)
        cloneMap.setExtent(-180,-90,180,90)
        try:
            imageObj = cloneMap.draw()
        finally:
            self.ui.statusbar.showMessage("Error: map can't be draw")

        imageObj.save('/tmp/mapfileEditor.'+cloneMap.outputformat.extension)
        scene = QtGui.QGraphicsScene()
        pixMap = QtGui.QPixmap('/tmp/mapfileEditor.'+cloneMap.outputformat.extension)
        scene.addPixmap(pixMap)
        self.ui.mf_preview.setScene(scene)
        self.ui.mf_preview.show()

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
            layersItems.appendRow(layerItem)

        #layersChild.setChild(0, layersItems)
        parentItem.appendRow(layersItems)
        self.ui.mf_structure.setModel(self.model)
        self.ui.mf_structure.expandAll()
        #self.ui.view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.updateMap()
        


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MapfileEditorApplication()
    myapp.show()
    sys.exit(app.exec_())

