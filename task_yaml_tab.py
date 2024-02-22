from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from reload_label import *
from task_yaml_tab import *
import os

class TaskYamlViewerTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        self.layout = QVBoxLayout()

        self.reloadLabelRow = ReloadLabelRow()

        self.taskContent = QTextEdit()
        self.taskContent.setStyleSheet("background-color: #f0f0f0;")
        # self.syntaxHighlighter = YamlSyntaxHighlighter(self.taskContent.document())

        self.layout.addLayout(self.reloadLabelRow)
        self.layout.addWidget(self.taskContent)
        self.setLayout(self.layout)

    def load_task_yaml(self):
        project_directory = self.mainWindow.project_directory
        task_file_path = os.path.join(project_directory, "task.yaml")
        if os.path.exists(task_file_path):
            with open(task_file_path) as file:
                self.taskContent.setText(file.read())
                self.reloadLabelRow.update_reload_label()
        else:
            self.taskContent.setText("task.yaml not found in the selected directory.")