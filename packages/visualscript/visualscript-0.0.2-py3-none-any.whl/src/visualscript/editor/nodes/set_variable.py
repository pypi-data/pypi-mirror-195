from typing import Any
from PyQt5.QtCore import Qt
from editor.nodes.executable import ExecutableNode
from editor.config import register_node

@register_node()
class SetVariableNode(ExecutableNode):
    title = "New Variable"
    category = "Default"

    def __init__(self, scene, title=title, input_types=[], output_types=[]):
        super().__init__(scene, "", [Any, *input_types], output_types)
        self.graphics.update_title(title)
        self.save_variable()
        self.graphics.mouseDoubleClickEvent = self.edit_title
        self.add_signals({self.graphics.title_item.UnfocusSignal: self.save_variable,
                          self.graphics.title_item.KeyPressSignal: self.graphics.refresh_shape})

    def edit_title(self, event):
        title_item = self.graphics.title_item
        title_item.textCursor().setVisualNavigation(True)
        title_item.setTextInteractionFlags(Qt.TextEditorInteraction)

    def save_variable(self):
        new_title = self.graphics.title_item.toPlainText()
        if self.title == "New Variable":
            if self.scene.module.__dict__.__contains__(self.title):
                self.scene.module.__dict__.pop(self.title)
        if new_title != self.title:
            self.title = new_title
            self.graphics.update_title()
        if not self.scene.module.__dict__.__contains__(self.title):
            self.scene.module.__dict__[self.title] = None
            self.scene.getAttributeBrowser().reload(self.scene.module)

    async def execute(self):
        self.scene.module.__dict__[self.title] = self.get_input_value(1)
        await super().execute()
