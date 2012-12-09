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
        
        # Constants []
        self.debugOn = True
        self.debug_output = 'shell'
        self.debug = 'INFO'
        self.history = []
        self.debugLevel = {'ERROR': 0, 'WARNING': 3, 'INFO': 5}
        self.msLogical = {'MS_TRUE':1, 'MS_ON':1, 'MS_YES':1, 'MS_FALSE':0, 'MS_OFF':0, 'MS_NO':0}
        self.units = ['inches', 'feet' ,'miles', 'meters', 'kilometers', 'dd', 'pixels', 'pourcentages', 'nauticalmiles']
        self.layerTypes = ['point', 'line', 'polygon', 'raster', 'annotation', 'query', 'circle', 'tileindex']
        self.connectionTypes = ['inline', 'shapefile', 'tiled shapefile', 'sde', 'ogr','postgis','wms', 'oracle spatial', 'wfs', 'graticule', 'mygis', 'raster']
        self.imageMode = ['PC256', 'RGB', 'RGBA', 'INT16', 'FLOAT32', 'FEATURE']
        self.imageTypes = ['jpeg' ,'pdf','png' ,'svg']
        self.firstDir = '~/'

        #get ESPG code and wkt proj4 string list 
        self.proj4List = self.getProjectionList()  

        self.new()

        self.connect(self.ui.actionNew, QtCore.SIGNAL(_fromUtf8("activated()")), self.new)
        self.connect(self.ui.mf_tb_new, QtCore.SIGNAL(_fromUtf8("clicked()")), self.new)
        self.connect(self.ui.actionOpen, QtCore.SIGNAL(_fromUtf8("activated()")), self.open)
        self.connect(self.ui.mf_tb_open, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open)
        self.connect(self.ui.actionSave, QtCore.SIGNAL(_fromUtf8("activated()")), self.save)
        self.connect(self.ui.mf_tb_save, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save)
        self.connect(self.ui.actionSaveAs, QtCore.SIGNAL(_fromUtf8("activated()")), self.saveas)
        self.connect(self.ui.actionMapSetting, QtCore.SIGNAL(_fromUtf8("activated()")), self.mapSetting)
        self.connect(self.ui.mf_tb_mapparameter, QtCore.SIGNAL(_fromUtf8("clicked()")), self.mapSetting)

    # ###########################
    # Settings Windows
    # ###########################
    def mapSetting(self):
        self.QMapSettingWindow = uic.loadUi('ui/mapSetting.ui')
        self.QMapSettingWindow.setModal(True)
        
        # Update form from MapFile
        try:
            self.QMapSettingWindow.mf_name.insert(self.map.name)
        except AttributeError:
            self.QMapSettingWindow.mf_name.insert(None)
       
        # MainTabform
        if(self.map.status == self.msLogical['MS_ON']):
             self.QMapSettingWindow.mf_map_status_on.setChecked(True)
             self.QMapSettingWindow.mf_map_status_off.setChecked(False)
        else:
            self.QMapSettingWindow.mf_map_status_on.setChecked(False)
            self.QMapSettingWindow.mf_map_status_off.setChecked(True)

        # -- outputformat list
        self.QMapSettingWindow.mf_map_outputformat.addItems(self.imageTypes)
        if (self.map.outputformat.name != '' and self.imageTypes.count(self.map.imagetype) == 0):
            self.QMapSettingWindow.mf_map_outputformat.addItem(self.map.outputformat.name)

        self.QMapSettingWindow.mf_map_outputformat.setCurrentIndex(self.QMapSettingWindow.mf_map_outputformat.findText(self.map.imagetype))

        self.QMapSettingWindow.mf_sizewidth.setValue(self.map.width)
        self.QMapSettingWindow.mf_sizeheight.setValue(self.map.height)
        self.QMapSettingWindow.mf_map_maxsize.setValue(self.map.maxsize)

        self.QMapSettingWindow.mf_map_units.addItems(self.units) #dd|feet|inches|kilometers|meters|miles|nauticalmiles
        self.QMapSettingWindow.mf_map_units.setCurrentIndex(self.map.units)
        # -- Projection
        if(str(self.map.getProjection()).startswith("+init=") or str(self.map.getProjection()) == ''):
            epsgCode = str(self.map.getProjection()).strip("+init=").upper()
        elif(str(self.map.getProjection()).startswith("+proj=")):
            wktProj = str(self.map.getProjection())
            # Change wktproj to EPSG/Name
            epsgCode = self.proj4List['epsgByWkt'][wktProj]

        if(epsgCode != ''):
            epsgName = self.proj4List['nameByEpsg'][epsgCode]
            currentProj = epsgName + " - " + epsgCode
        else:
            currentProj = ''

        self.QMapSettingWindow.mf_map_projection_btepsg.setChecked(True)
        self.QMapSettingWindow.mf_map_projection_btproj.setChecked(False)
        self.QMapSettingWindow.mf_map_projection.addItem(currentProj, 0)

        epsgList = QtCore.QStringList(list(set(self.proj4List["wktByCode"].keys()+self.proj4List["wktByName"].keys()+self.proj4List["wktByName"].values())))
        epsgCompleter = QtGui.QCompleter(epsgList)
        self.QMapSettingWindow.mf_map_projection.setCompleter(epsgCompleter)

        # ... change completer following mf_map_projection_btepsg/btproj
        self.connect(self.QMapSettingWindow.mf_map_projection_btepsg, QtCore.SIGNAL(_fromUtf8("clicked()")), self.switchProjection)
        self.connect(self.QMapSettingWindow.mf_map_projection_btproj, QtCore.SIGNAL(_fromUtf8("clicked()")), self.switchProjection)

        # -- extent
        self.connect(self.QMapSettingWindow.mf_map_extent_auto, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setExtentFields)
        self.connect(self.QMapSettingWindow.mf_map_extent_manuel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setExtentFields)

        if (self.map.extent.maxx != -1 and self.map.extent.maxy != -1 and self.map.extent.minx != -1 and self.map.extent.miny != -1):
            self.QMapSettingWindow.mf_map_extent_auto.setChecked(False)
            self.QMapSettingWindow.mf_map_extent_manuel.setChecked(True)
            self.QMapSettingWindow.mf_map_extent_manuel.setCheckable(True)
            self.setExtentFields()
            self.QMapSettingWindow.mf_map_extent_top.insert(str(self.map.extent.maxy))
            self.QMapSettingWindow.mf_map_extent_left.insert(str(self.map.extent.minx))
            self.QMapSettingWindow.mf_map_extent_bottom.insert(str(self.map.extent.miny))
            self.QMapSettingWindow.mf_map_extent_right.insert(str(self.map.extent.maxx))

        # PathesTabForm
        self.QMapSettingWindow.mf_map_shapepath.setText(self.map.shapepath)
        self.QMapSettingWindow.mf_map_fontset.setText(self.map.fontset.filename)
        self.QMapSettingWindow.mf_map_symbolset.setText(self.map.symbolset.filename)
        self.QMapSettingWindow.connect(self.QMapSettingWindow.mf_map_shapepath_browse, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openShapePath)
        self.QMapSettingWindow.connect(self.QMapSettingWindow.mf_map_fontset_browse, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openFontSet)
        self.QMapSettingWindow.connect(self.QMapSettingWindow.mf_map_symbolset_browse, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openSymbolSet)

        # advancedTabForm
        # outputFormatTabForm
        # OGCTabForm
        # debugTabForm
        
        if(self.map.debug != self.msLogical['MS_OFF']):
            self.QMapSettingWindow.mf_map_debug_on.setChecked(True)
            self.QMapSettingWindow.mf_map_debug_off.setChecked(False)
            self.QMapSettingWindow.mf_map_debug.setValue(self.map.debug)
        else:
            self.QMapSettingWindow.mf_map_debug_on.setChecked(False)
            self.QMapSettingWindow.mf_map_debug_off.setChecked(True)

        self.QMapSettingWindow.exec_()
        if(self.QMapSettingWindow.Accepted == True):
            self.saveMapSetting()

    def switchProjection(self):
        currentProj = str(self.QMapSettingWindow.mf_map_projection.currentText())
        if(self.QMapSettingWindow.mf_map_projection_btepsg.isChecked()):
            if(currentProj.startswith("EPSG:")):
                epsgCode = currentProj
                epsgName = self.proj4List["nameByEpsg"][currentProj]
            elif(currentProj.startswith("+proj=")):
                epsgCode = self.proj4List["epsgByWkt"][currentProj]
                epsgName = self.proj4List["nameByEpsg"][epsgCode]
            self.QMapSettingWindow.mf_map_projection.removeItem(0)
            self.QMapSettingWindow.mf_map_projection.addItem(epsgName + " - " + epsgCode, 0)
        elif(self.QMapSettingWindow.mf_map_projection_btproj.isChecked()):
            if(currentProj.startswith("EPSG:")):
                epsgCode = currentProj
            else:
                currentProj = currentProj.split(" - ")
                epsgCode = currentProj[1]
            wktProj = self.proj4List["wktByCode"][epsgCode]
            self.QMapSettingWindow.mf_map_projection.removeItem(0)
            self.QMapSettingWindow.mf_map_projection.addItem(wktProj, 0)

    def getProjectionList(self):
        wktByCode = {}
        wktByName = {}
        nameByEpsg = {}
        epsgByWkt = {}
        epsgFile = open('/usr/share/proj/epsg', 'r')
        epsgList = epsgFile.readlines()
        i = 0
        while i < len(epsgList):
            if(epsgList[i+1].startswith('# Unable to translate coordinate system EPSG:')):
                i+=3
                continue
            name = epsgList[i].strip('# ').strip('\n')
            line = epsgList[i+1].split('> ')
            projwkt = line[1].strip('  <>\n')
            code = line[0].strip('<')

            wktByCode["EPSG:"+code] = projwkt
            wktByName[name] = projwkt
            nameByEpsg["EPSG:"+code] = name
            epsgByWkt[projwkt] = "EPSG:"+code

            i+=2

        list = {"wktByCode": wktByCode, "wktByName": wktByName, 'wktByEpsg': epsgByWkt, 'nameByEpsg': nameByEpsg, 'epsgByWkt': epsgByWkt}
        return list

    def setExtentFields(self):
        enable = False
        if(self.QMapSettingWindow.mf_map_extent_manuel.isChecked()):
            enable = True
        
        self.QMapSettingWindow.mf_map_extent_top.setEnabled(enable)
        self.QMapSettingWindow.mf_map_extent_left.setEnabled(enable)
        self.QMapSettingWindow.mf_map_extent_bottom.setEnabled(enable)
        self.QMapSettingWindow.mf_map_extent_right.setEnabled(enable)

    def openShapePath(self):
        shapepath = str(QtGui.QFileDialog.getExistingDirectory())
        self.QMapSettingWindow.mf_map_shapepath.setText(shapepath)

    def openSymbolSet(self):
        symbolSetPath = str(QtGui.QFileDialog.getOpenFileName(None, "Select one file to open", self.firstDir, "Symbol file (*.sym);;Text (*.txt);;All (*.*)"))
        self.QMapSettingWindow.mf_map_symbolset.setText(symbolSetPath)
 
    def openFontSet(self):
        fontSetPath = str(QtGui.QFileDialog.getOpenFileName(None, "Select one file to open", self.firstDir, "Font file (*.font);;Text (*.txt);;All (*.*)"))
        self.QMapSettingWindow.mf_map_fontset.setText(fontSetPath)
 
    def saveMapSetting(self):

        # MainTabForm
        self.map.name = str(self.QMapSettingWindow.mf_name.text())
        self.map.setImageType(str(self.QMapSettingWindow.mf_map_outputformat.itemText(self.QMapSettingWindow.mf_map_outputformat.currentIndex())))
        self.map.width = self.QMapSettingWindow.mf_sizewidth.value()
        self.map.height = self.QMapSettingWindow.mf_sizeheight.value()

        if(self.QMapSettingWindow.mf_map_maxsize.value() != 2048):
            self.map.maxSize = self.QMapSettingWindow.mf_map_maxsize.value()
        
        self.map.units = self.QMapSettingWindow.mf_map_units.currentIndex();
        # -- Projection
        if (str(self.QMapSettingWindow.mf_map_projection.currentText()) != ''):
            if (self.QMapSettingWindow.mf_map_projection_btepsg.isChecked()):
                if (str(self.QMapSettingWindow.mf_map_projection.currentText()).startswith("EPSG:")):
                    wktProj = self.proj4List["wktByCode"][str(self.QMapSettingWindow.mf_map_projection.currentText())]
                elif (str(self.QMapSettingWindow.mf_map_projection.currentText()).startswith("+proj")):
                   wktProj = str(self.QMapSettingWindow.mf_map_projection.currentText())
                else:
                    currentProj = str(self.QMapSettingWindow.mf_map_projection.currentText()).split(" - ")
                    wktProj = self.proj4List["wktByName"][currentProj[0]] 
            elif (self.QMapSettingWindow.mf_map_projection_btproj.isChecked()):
                wktProj = str(self.QMapSettingWindow.mf_map_projection.currentText())
            self.map.setProjection(wktProj)

        if(self.QMapSettingWindow.mf_map_extent_manuel.isChecked()):
            self.debugLog('Extent: Save Manuel Extent')
            self.debugLog(str(self.QMapSettingWindow.mf_map_extent_left.text()))
            minx = str(self.QMapSettingWindow.mf_map_extent_left.text())
            miny = self.QMapSettingWindow.mf_map_extent_bottom.text()
            maxx = self.QMapSettingWindow.mf_map_extent_right.text()
            maxy = self.QMapSettingWindow.mf_map_extent_top.text()
            if(minx == ''):
                minx = -1
            if(miny == ''):
                miny = -1
            if(maxx == ''):
                maxx = -1
            if(maxy == ''):
                maxy = -1

            tmpExtent = {'minx':float(minx), 'miny': float(miny), 'maxx': float(maxx), 'maxy': float(maxy)}
        else:
            self.debugLog("Info: process calculation for max extent")
            tmpExtent = self.setExtentFromLayers()

        self.map.extent = mapscript.rectObj(tmpExtent['minx'], tmpExtent['miny'], tmpExtent['maxx'], tmpExtent['maxy'])

        # PathesTabForm
        if(str(self.QMapSettingWindow.mf_map_shapepath.text()) != ''):
            self.map.shapepath = str(self.QMapSettingWindow.mf_map_shapepath.text()) 
        # -- remove path using mappath
        if(str(self.QMapSettingWindow.mf_map_fontset.text()) != ''):
            self.map.setFontSet(str(self.QMapSettingWindow.mf_map_fontset.text()).replace(self.map.mappath,''))
        if(str(self.QMapSettingWindow.mf_map_symbolset.text()) != ''):
            self.map.setSymbolSet(str(self.QMapSettingWindow.mf_map_symbolset.text()).replace(self.map.mappath,''))

        # AdvancedTabform
        self.map.setRotation(float(self.QMapSettingWindow.mf_map_angle.value()))

        # OutputFormatTabForm
        #format = mapscript.outputFormatObj(self.QMapSettingWindow.mf_default_outputformat)
        #self.map.setOutputFormat(format)
        
        # OGCTabForm
        
        # debugTabForm
        if(self.QMapSettingWindow.mf_map_debug_on.isChecked() == 'True'):
            self.map.setConfigOption('MS_ERRORFILE', str(self.QMapSettingWindow.mf_map_config_errorfile.text()))
            if(self.QMapSettingWindow.mf_map_debug.value() == 0):
                self.map.debug = self.msLogical['MS_ON']
            else:
                self.map.debug = self.QMapSettingWindow.mf_map_debug.value()
        else:
            self.map.debug = self.msLogical['MS_OFF']
            #self.map.setConfigOption('MS_ERRORFILE', '')

        self.updateMapStructure()
        self.ui.statusbar.showMessage('Info: mapfile settings saved.')

    def setExtentFromLayers(self):
        """Get Max Extent from each layers"""
        maxExtent = {'minx':-1, 'miny':-1, 'maxx':-1, 'maxy':-1}
        for index in range(0,self.map.numlayers):
            self.debugLog("Extent: process for layer named" + layer.name)
            layer = self.map.getLayer(index) 
            extent = layer.getExtent().toString()
            if(maxExtent['minx'] > extent['minx']):
                maxExtent['minx'] = extent['minx']
            if(maxExtent['miny'] > extent['miny']):
                maxExtent['miny'] = extent['miny']
            if(maxExtent['maxx'] < extent['maxx']):
                maxExtent['maxx'] = extent['maxx']
            if(maxExtent['maxy'] < extent['maxy']):
                maxExtent['may'] = extent['maxy']
        return maxExtent

        
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
        
    def debugLog(self, string, level = 'ERROR'):
        if(self.debugOn and self.debug_output == 'shell'):
            if(self.debugLevel[self.debug] <= self.debugLevel[level]):
                print string
        elif(self.debugOn and self.debug_output == 'file'):
            if(self.debugLevel[self.debug] <= self.debugLevel[level]):
                print "Log debug file not supported"
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MapfileEditorApplication()
    myapp.show()
    sys.exit(app.exec_())

