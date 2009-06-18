import sys
import Skype4Py

from PyQt4 import QtGui
from PyQt4.QtCore import QObject, SIGNAL, QCoreApplication, QSettings, QVariant


import form
import storage

class Plugin(object):
    
    def __init__(self, archiver):
        self.archiver = archiver
        self.skype= Skype4Py.Skype()
        self.skype.Attach();
        self.skype.OnAttachmentStatus = self.on_attach;
        self.skype.OnMessageStatus = self.on_message_status;


    def on_attach(status):
        if status == Skype4Py.apiAttachAvailable:
            self.skype.Attach()
            
        if status == Skype4Py.apiAttachSuccess:
            pass


    def on_message_status(message, status):
        if status == 'SENT' or status == 'RECEIVED':
            self.archiver.add(message)



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

        archiver = storage.IMAPMailArchiver(self.ui.server_input.text(),
                                            self.ui.port_input.value(),
                                            True,
                                            self.ui.username_input.text(),
                                            self.ui.password_input.text())
        
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
