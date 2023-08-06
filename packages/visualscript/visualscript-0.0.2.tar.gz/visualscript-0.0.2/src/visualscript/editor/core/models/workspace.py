import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMessageBox
from PyQt5.QtCore import Qt

from editor.core.models.scene import Scene
from editor.core.views.workspace import WorkspaceView

class WorkspaceWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.filename = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene()

        self.view = WorkspaceView(self.scene.graphics, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.has_been_modified

    def isFilenameSet(self):
        return self.filename is not None

    def selectedItems(self):
        return self.scene.selectedItems()

    def hasSelectedItems(self):
        return self.selectedItems() != []

    def canUndo(self):
        return self.scene.history.canUndo()

    def canRedo(self):
        return self.scene.history.canRedo()

    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        self.scene.clear()
        self.filename = None

    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.loadFromFile(filename)
        self.filename = filename
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()
        QApplication.restoreOverrideCursor()
        return True
        # except Exception as e:
        #     print(e)
        #     QApplication.restoreOverrideCursor()
        #     QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
        #     return False
        # finally:
        # QApplication.restoreOverrideCursor()


    def fileSave(self, filename=None):
        if filename is not None: self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True
