# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapSetting.ui'
#
# Created: Sun Dec  2 18:34:13 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapSetting(object):
    def setupUi(self, MapSetting):
        MapSetting.setObjectName(_fromUtf8("MapSetting"))
        MapSetting.setEnabled(True)
        MapSetting.resize(400, 300)
        self.mapSettingButtonBox = QtGui.QDialogButtonBox(MapSetting)
        self.mapSettingButtonBox.setGeometry(QtCore.QRect(40, 260, 341, 32))
        self.mapSettingButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.mapSettingButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.mapSettingButtonBox.setObjectName(_fromUtf8("mapSettingButtonBox"))
        self.mf_name = QtGui.QLineEdit(MapSetting)
        self.mf_name.setGeometry(QtCore.QRect(60, 10, 321, 23))
        self.mf_name.setText(_fromUtf8(""))
        self.mf_name.setObjectName(_fromUtf8("mf_name"))
        self.mf_name_label = QtGui.QLabel(MapSetting)
        self.mf_name_label.setGeometry(QtCore.QRect(20, 10, 57, 15))
        self.mf_name_label.setObjectName(_fromUtf8("mf_name_label"))
        self.settingsForm = QtGui.QTabWidget(MapSetting)
        self.settingsForm.setGeometry(QtCore.QRect(10, 39, 381, 221))
        self.settingsForm.setObjectName(_fromUtf8("settingsForm"))
        self.outputTabForm = QtGui.QWidget()
        self.outputTabForm.setObjectName(_fromUtf8("outputTabForm"))
        self.mf_units = QtGui.QComboBox(self.outputTabForm)
        self.mf_units.setGeometry(QtCore.QRect(100, 53, 78, 24))
        self.mf_units.setEditable(False)
        self.mf_units.setObjectName(_fromUtf8("mf_units"))
        self.units_label = QtGui.QLabel(self.outputTabForm)
        self.units_label.setGeometry(QtCore.QRect(30, 60, 57, 15))
        self.units_label.setObjectName(_fromUtf8("units_label"))
        self.size_label = QtGui.QLabel(self.outputTabForm)
        self.size_label.setGeometry(QtCore.QRect(20, 33, 57, 15))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.size_label.setFont(font)
        self.size_label.setObjectName(_fromUtf8("size_label"))
        self.mf_sizewidth_label = QtGui.QLabel(self.outputTabForm)
        self.mf_sizewidth_label.setGeometry(QtCore.QRect(60, 34, 57, 15))
        self.mf_sizewidth_label.setObjectName(_fromUtf8("mf_sizewidth_label"))
        self.mf_sizewidth = QtGui.QSpinBox(self.outputTabForm)
        self.mf_sizewidth.setGeometry(QtCore.QRect(100, 30, 81, 23))
        self.mf_sizewidth.setMinimum(-1)
        self.mf_sizewidth.setMaximum(999999)
        self.mf_sizewidth.setObjectName(_fromUtf8("mf_sizewidth"))
        self.mf_sizeheight_label = QtGui.QLabel(self.outputTabForm)
        self.mf_sizeheight_label.setGeometry(QtCore.QRect(220, 32, 50, 20))
        self.mf_sizeheight_label.setObjectName(_fromUtf8("mf_sizeheight_label"))
        self.mf_sizeheight = QtGui.QSpinBox(self.outputTabForm)
        self.mf_sizeheight.setGeometry(QtCore.QRect(270, 31, 81, 23))
        self.mf_sizeheight.setMinimum(-1)
        self.mf_sizeheight.setMaximum(999999)
        self.mf_sizeheight.setObjectName(_fromUtf8("mf_sizeheight"))
        self.mf_default_outputformat = QtGui.QComboBox(self.outputTabForm)
        self.mf_default_outputformat.setGeometry(QtCore.QRect(150, 7, 121, 24))
        self.mf_default_outputformat.setObjectName(_fromUtf8("mf_default_outputformat"))
        self.mf_default_output_label = QtGui.QLabel(self.outputTabForm)
        self.mf_default_output_label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.mf_default_output_label.setObjectName(_fromUtf8("mf_default_output_label"))
        self.settingsForm.addTab(self.outputTabForm, _fromUtf8(""))
        self.debugTabForm = QtGui.QWidget()
        self.debugTabForm.setObjectName(_fromUtf8("debugTabForm"))
        self.settingsForm.addTab(self.debugTabForm, _fromUtf8(""))
        self.advancedTabForm = QtGui.QWidget()
        self.advancedTabForm.setAccessibleName(_fromUtf8(""))
        self.advancedTabForm.setObjectName(_fromUtf8("advancedTabForm"))
        self.settingsForm.addTab(self.advancedTabForm, _fromUtf8(""))

        self.retranslateUi(MapSetting)
        self.settingsForm.setCurrentIndex(0)
        QtCore.QObject.connect(self.mapSettingButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MapSetting.accept)
        QtCore.QObject.connect(self.mapSettingButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MapSetting.reject)
        QtCore.QMetaObject.connectSlotsByName(MapSetting)

    def retranslateUi(self, MapSetting):
        MapSetting.setWindowTitle(QtGui.QApplication.translate("MapSetting", "Map Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.mf_name_label.setText(QtGui.QApplication.translate("MapSetting", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsForm.setToolTip(QtGui.QApplication.translate("MapSetting", "<html><head/><body><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.units_label.setText(QtGui.QApplication.translate("MapSetting", "Units", None, QtGui.QApplication.UnicodeUTF8))
        self.size_label.setText(QtGui.QApplication.translate("MapSetting", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.mf_sizewidth_label.setText(QtGui.QApplication.translate("MapSetting", "width", None, QtGui.QApplication.UnicodeUTF8))
        self.mf_sizeheight_label.setText(QtGui.QApplication.translate("MapSetting", "height", None, QtGui.QApplication.UnicodeUTF8))
        self.mf_default_output_label.setText(QtGui.QApplication.translate("MapSetting", "Default output format", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsForm.setTabText(self.settingsForm.indexOf(self.outputTabForm), QtGui.QApplication.translate("MapSetting", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.debugTabForm.setToolTip(QtGui.QApplication.translate("MapSetting", "<html><head/><body><p>Set-up the debug level.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsForm.setTabText(self.settingsForm.indexOf(self.debugTabForm), QtGui.QApplication.translate("MapSetting", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.advancedTabForm.setToolTip(QtGui.QApplication.translate("MapSetting", "<html><head/><body><p>Advanced settings for map object (configuration files, specific parameters).</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsForm.setTabText(self.settingsForm.indexOf(self.advancedTabForm), QtGui.QApplication.translate("MapSetting", "Advanced", None, QtGui.QApplication.UnicodeUTF8))

