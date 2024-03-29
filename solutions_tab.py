import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTabWidget, QLabel
import os
import statefulness
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class SolutionsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.task_directory = ""
        self.solution_paths = []

        main_layout = QVBoxLayout()

        # Create a horizontal layout for the button
        button_layout = QHBoxLayout()

        # Add a spacer on the left side
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.add_sol_btn = QPushButton("Add solution")
        self.add_sol_btn.clicked.connect(self.add_solution_path)
        button_layout.addWidget(self.add_sol_btn)

        main_layout.addLayout(button_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)


    def add_solution_path(self):
        if not os.path.exists(self.task_directory):
            return
        file_dialog = QFileDialog(self, "Select solution file")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            new_files = file_dialog.selectedFiles()
            self.solution_paths.extend(new_files)
            statefulness.save_task_dir_solutions(self.task_directory, self.solution_paths)
            self.refresh_tabs()

    def update_task_dir(self, dir_path):
        self.task_directory = dir_path
        self.solution_paths = statefulness.load_task_dir_solutions(dir_path)
        self.refresh_tabs()

    def remove_solution_path(self, path):
        print(f"removing {path} from {self.solution_paths}")
        self.solution_paths.remove(path)
        print(f"removed {path} from {self.solution_paths}")
        statefulness.save_task_dir_solutions(self.task_directory, self.solution_paths)
        self.refresh_tabs()

    def run_tests_button_handler(self, path):
        def handler():
            print(f"Running tests for {path}")
        return handler

    def make_remove_button_handler(self, path):
        def handler():
            reply = QMessageBox.question(self, 'Confirm Removal', f"Are you sure you want to remove the solution: {os.path.basename(path)}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.remove_solution_path(path)
        return handler

    def refresh_tabs(self):
        paths = self.solution_paths
        self.tabs.clear()
        for i in range(len(paths)):
            if not os.path.exists(paths[i]):
                print(f"Path {paths[i]} does not exist")
                continue
            path = paths[i]
            tab = QWidget()
            tabLayout = QVBoxLayout()

            labelsLayout = QHBoxLayout()
            full_path_label = QLabel("Path: "+os.path.abspath(path))
            run_tests_button = QPushButton("Run tests")
            remove_button = QPushButton("Remove")
            handler = self.make_remove_button_handler(path)
            remove_button.clicked.connect(handler)

            labelsLayout.addWidget(full_path_label)
            labelsLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            labelsLayout.addWidget(run_tests_button)
            labelsLayout.addWidget(remove_button)
            tabLayout.addLayout(labelsLayout)

            table = QTableWidget(0,7)
            table.setHorizontalHeaderLabels(["Test","Time","Memory","Stdin","Stdout","Stderr","Verdict"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            with open(path, "r") as sol_file:
                sol_file_content = sol_file.read()
            sol_file_content_sha256 = hashlib.sha256(sol_file_content.encode()).hexdigest()
            print(sol_file_content_sha256)
            results = statefulness.load_sol_test_results(self.task_directory,sol_file_content_sha256)
            for r in results:
                print(r)

            tabLayout.addWidget(table)
    
            tab.setLayout(tabLayout)
            self.tabs.addTab(tab, os.path.basename(path))
