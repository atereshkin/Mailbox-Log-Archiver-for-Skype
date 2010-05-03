"""
Copyright (C) 2009 Y-NODE Software
Author: Alexander Tereshkin <atereshkin@y-node.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys
import Skype4Py
import time

from PyQt4 import QtGui
from PyQt4.QtCore import QObject, SIGNAL, QCoreApplication, QSettings, QVariant


import form
import storage

from log import _init_logging
_init_logging(debug=True)

import logging
log = logging.getLogger('mlas')

class Plugin(object):
    
    def __init__(self, archiver):
        self.archiver = archiver
        self.skype= Skype4Py.Skype()
        self.skype.OnAttachmentStatus = self.on_attach
        self.skype.OnMessageStatus = self.on_message_status
        self.attach_unwearing()

    def on_attach(self, status):
        if status == Skype4Py.apiAttachAvailable:
            log.debug("Skype API attach available")
            self.attach_unwearing()
            
        if status == Skype4Py.apiAttachSuccess:
            log.debug("Skype API attached successfully")
            self.archive_all()
            

    def on_message_status(self, message, status):
        if status == 'SENT' or status == 'RECEIVED':
            log.debug('Adding message')
            self.archiver.add(message)

    def attach_unwearing(self):
        connected = False
        while not connected:
            try:
                log.debug("Trying to attach")
                self.skype.Attach()
                connected = True
            except:
                time.sleep(2)
                connected = False
        

    def archive_all(self):
        for msg in self.skype.Messages():
            self.archiver.add(msg)
    



class OptionsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = form.Ui_Form()
        self.ui.setupUi(self)
        self.init_events()
        self.settings = QSettings()
        self.load_settings()

    def init_events(self):
        QObject.connect(self.ui.ok_button, SIGNAL("clicked()"), self.ok)
        QObject.connect(self.ui.cancel_button, SIGNAL("clicked()"), self.cancel)


    def save_settings(self):
        self.settings.setValue("server", QVariant(self.ui.server_input.text()))
        self.settings.setValue("port", QVariant(self.ui.port_input.value()))
        self.settings.setValue("ssl", QVariant(self.ui.ssl_input.isChecked()))
        self.settings.setValue("username", QVariant(self.ui.username_input.text()))
        self.settings.sync()

    def load_settings(self):
        if self.settings.contains("username"):
            self.ui.password_input.setFocus()
        self.ui.server_input.setText(self.settings.value("server", QVariant('imap.gmail.com')).toString())
        self.ui.port_input.setValue(self.settings.value("port", QVariant(993)).toInt()[0])
        self.ui.ssl_input.setChecked(self.settings.value("ssl", QVariant(True)).toBool())
        self.ui.username_input.setText(self.settings.value("username", QVariant('')).toString())

    def ok(self):
        self.hide()
        
        self.save_settings()

        archiver = storage.IMAPMailArchiver(str(self.ui.server_input.text()),
                                            str(self.ui.port_input.value()),
                                            True,
                                            str(self.ui.username_input.text()),
                                            str(self.ui.password_input.text()))
        
        global plugin
        plugin = Plugin(archiver)



    def cancel(self):
        app.quit()


QCoreApplication.setOrganizationName("Y-NODE Software")
QCoreApplication.setOrganizationDomain("y-node.com")
QCoreApplication.setApplicationName("SkypeLogsLikeGTalk")

app = QtGui.QApplication(sys.argv)
dialog = OptionsDialog()
dialog.show()
sys.exit(app.exec_())

