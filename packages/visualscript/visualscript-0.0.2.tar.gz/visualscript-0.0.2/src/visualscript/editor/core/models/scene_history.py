from editor.core.utils import dumpException

DEBUG = False

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        self.history_limit = 512

        # listeners
        self._history_modified_listeners = []
        self._history_stored_listeners = []
        self._history_restored_listeners = []

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def storeInitialHistoryStamp(self):
        self.storeHistory("Initial History Stamp")

    def addHistoryModifiedListener(self, callback):
        self._history_modified_listeners.append(callback)

    def addHistoryStoredListener(self, callback):
        self._history_stored_listeners.append(callback)

    def addHistoryRestoredListener(self, callback):
        self._history_restored_listeners.append(callback)

    def canUndo(self):
        return self.history_current_step > 0

    def canRedo(self):
        return self.history_current_step + 1 < len(self.history_stack)

    def undo(self):
        if DEBUG: print("UNDO")

        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def redo(self):
        if DEBUG: print("REDO")
        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def restoreHistory(self):
        if DEBUG: print("Restoring history",
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])
        for callback in self._history_modified_listeners: callback()
        for callback in self._history_restored_listeners: callback()

    def storeHistory(self, desc, setModified=False):
        if setModified:
            self.scene.has_been_modified = True

        if DEBUG:
            print("Storing history", '"%s"' % desc, ".... current_step: @%d" % self.history_current_step, "(%d)" % len(self.history_stack))

        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print("  -- setting step to:", self.history_current_step)

        # always trigger history modified (for i.e. updateEditMenu)
        for callback in self._history_modified_listeners: callback()
        for callback in self._history_stored_listeners: callback()

    def createHistoryStamp(self, desc):
        sel_obj = []
        for item in self.scene.selectedItems():
            sel_obj.append(item.id)
        # for item in self.scene.graphics.selectedItems():
        #     if hasattr(item, 'node'):
        #         sel_obj['nodes'].append(item.node.id)
            # elif isinstance(item, QDMGraphicsEdge):
            #     sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj,
        }

        return history_stamp

    def restoreHistoryStamp(self, history_stamp):
        self.scene.deserialize(history_stamp['snapshot'])

        for item_id in history_stamp['selection']:
            for item in self.scene.items:
                if item.id == item_id:
                    item.graphics.setSelected(True)
                    break

