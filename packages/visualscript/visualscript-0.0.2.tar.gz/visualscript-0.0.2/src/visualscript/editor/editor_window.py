import os, json

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from editor.core.utils import dumpException
from editor.workspace_window import WorkspaceWindow

def loadStylesheets(*args):
    res = ''
    for arg in args:
        file = QFile(arg)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        res += "\n" + str(stylesheet, encoding='utf-8')
    QApplication.instance().setStyleSheet(res)

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.initUI()

    def initUI(self):
        # stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss")
        )

        self.empty_icon = QIcon(".")

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        self.createAttributeBrowser()
        self.setShortcutEnabled(True)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.setWindowTitle("Models Circuit Editor")
        self.show()

    def createAttributeBrowser(self):
        from editor.core.models.properties_widget import PropertiesWidget
        self.attributeBrowser = PropertiesWidget()
        self.attributeDock = QDockWidget()
        self.attributeDock.setWindowTitle("Attributes Window")
        self.attributeDock.setWidget(self.attributeBrowser)
        self.attributeDock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.attributeDock)

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            event.accept()

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...", triggered=self.onFileSaveAs)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation", triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Y', statusTip="Redo last operation", triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', self, shortcut='Ctrl+X', statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', self, shortcut='Ctrl+C', statusTip="Copy to clipboard", triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', self, shortcut='Ctrl+V', statusTip="Paste from clipboard", triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items", triggered=self.onEditDelete)

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

    def getActiveWorkspace(self) -> WorkspaceWindow:
        active_workspace = self.mdiArea.activeSubWindow()
        if active_workspace:
            return active_workspace.widget()
        return None

    def isModified(self):
        return self.getActiveWorkspace().scene.isModified()

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to lose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.showMaximized()
            self.getActiveWorkspace().view.scenePosChanged.connect(self.onScenePosChanged)
        except Exception as e:
            dumpException(e)

    def onFileOpen(self, file_paths=None):
        if not file_paths:
            file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open graph from file',
                                                         filter=self.tr("Python Scripts (*.py *.vpy)"))

        for path in file_paths:
            path = os.path.join(os.curdir, path)
            if path:
                existing = self.findMdiChild(path)
                if existing:
                    self.mdiArea.setActiveSubWindow(existing)
                else:
                    new_workspace = WorkspaceWindow(self)
                    if new_workspace.fileLoad(path):
                        self.statusBar().showMessage("File %s loaded" % path, 5000)
                        new_workspace.setTitle()
                        subwnd = self.createMdiChild(new_workspace)
                        subwnd.show()
                        self.getActiveWorkspace().view.scenePosChanged.connect(self.onScenePosChanged)
                    else:
                        new_workspace.close()

    def createMenus(self):
        menubar = self.menuBar()

        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def onFileSave(self):
        active_workspace = self.getActiveWorkspace()
        if active_workspace is not None:
            if not active_workspace.isFilenameSet(): return self.onFileSaveAs()

            active_workspace.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % active_workspace.filename, 5000)
            active_workspace.setTitle()

            # support for MDI app
            # if hasattr(active_workspace, "setTitle"):
            # else: self.setTitle()
            return True

    def onFileSaveAs(self):
        current_nodeeditor = self.getActiveWorkspace()
        if current_nodeeditor is not None:
            fname, fformat = QFileDialog.getSaveFileName(self, 'Save visual script',
                                                         filter=self.tr("Visual Python Scripts (*.vpy);;"
                                                                        "All Files (*.*)"))

            if fname == '':
                return False

            extension = fformat.split('.')
            extension = '.' + extension[1].strip(')') if len(extension) == 2 else ''
            if fname.endswith(extension):
                fname = fname[:-len(extension)]

            if extension != '':
                fname += extension

            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.filename, 5000)
            current_nodeeditor.setTitle()

            # support for MDI app
            # if hasattr(current_nodeeditor, "setTitle"):
            # else: self.setTitle()
            return True

    def onEditUndo(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.history.undo()

    def onEditRedo(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.history.redo()

    def onEditDelete(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.getView().deleteSelected()

    def onEditCut(self):
        if self.getActiveWorkspace():
            data = self.getActiveWorkspace().scene.clipboard.serializeSelected(cut=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getActiveWorkspace():
            data = self.getActiveWorkspace().scene.clipboard.serializeSelected(cut=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getActiveWorkspace():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            self.getActiveWorkspace().scene.clipboard.deserializeFromClipboard(data)

    def updateMenus(self):
        # print("update Menus")
        active = self.getActiveWorkspace()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        active = self.getActiveWorkspace()
        hasMdiChild = (active is not None)

        self.actPaste.setEnabled(hasMdiChild)

        hasSelectedItems = hasMdiChild and active.hasSelectedItems()
        self.actCut.setEnabled(hasSelectedItems)
        self.actCopy.setEnabled(hasSelectedItems)
        self.actDelete.setEnabled(hasSelectedItems)

        self.actUndo.setEnabled(hasMdiChild and active.canUndo())
        self.actRedo.setEnabled(hasMdiChild and active.canRedo())

    def updateWindowMenu(self):
        self.windowMenu.clear()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getActiveWorkspace())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        self.toolbar = QToolBar()
        self.toolbar.setWindowTitle("Execution Toolbar")
        self.compileAction = self.toolbar.addAction("Compile")
        self.compileAction.triggered.connect(lambda: self.Compile())
        self.addToolBar(self.toolbar)

    def Compile(self):
        editor_widget = self.getActiveWorkspace()
        self.running = not self.running
        text = "Stop" if self.running else "Compile"
        self.compileAction.setText(text)
        if editor_widget:
            if self.running:
                editor_widget.Compile()
            else:
                editor_widget.Stop()

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else WorkspaceWindow(self)
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)