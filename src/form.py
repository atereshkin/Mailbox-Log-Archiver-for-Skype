# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Wed Jun 17 19:36:04 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("SkypeLogsLikeGTalk")
        Form.resize(400, 200)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.server_input = QtGui.QLineEdit(Form)
        self.server_input.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.server_input.setObjectName("server_input")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.server_input)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.port_input = QtGui.QSpinBox(Form)
        self.port_input.setMinimum(1)
        self.port_input.setMaximum(65535)
        self.port_input.setProperty("value", QtCore.QVariant(993))
        self.port_input.setObjectName("port_input")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.port_input)
        self.ssl_input = QtGui.QCheckBox(Form)
        self.ssl_input.setObjectName("ssl_input")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ssl_input)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #self.formLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.username_input = QtGui.QLineEdit(Form)
        self.username_input.setObjectName("username_input")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.username_input)
        self.password_input = QtGui.QLineEdit(Form)
        self.password_input.setEchoMode(QtGui.QLineEdit.Password)
        self.password_input.setObjectName("password_input")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.password_input)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.ok_button = QtGui.QPushButton(Form)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        self.cancel_button = QtGui.QPushButton(Form)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "SkypeLogsLikeGTalk", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.ssl_input.setText(QtGui.QApplication.translate("Form", "SSL(TLS)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("Form", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))



