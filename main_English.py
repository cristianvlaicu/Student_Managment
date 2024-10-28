# Importing the necessary modules from PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QVBoxLayout,
    QComboBox,
    QToolBar,
    QStatusBar,
    QMessageBox,
)
from PyQt6.QtGui import QAction, QIcon
import sys  # Importing the sys module
import sqlite3  # Importing the sqlite3 module for database interaction


class DatabaseConnection:  # Class to handle database connection
    def __init__(
        self, database_file="database.db"
    ):  # Constructor to initialize database file name
        self.database_file = database_file

    def connect(self):  # Method to establish a connection to the database
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):  # Main window class inheriting from QMainWindow
    def __init__(self):
        super().__init__()  # Calling the constructor of the parent class
        self.setWindowTitle(
            "Student Management System"
        )  # Setting the window title
        self.setMinimumSize(800, 600)  # Setting the minimum size of the window

        # Creating menu items
        file_menu_item = self.menuBar().addMenu("&File")  # Adding a File menu
        help_menu_item = self.menuBar().addMenu("&Help")  # Adding a Help menu
        edit_menu_item = self.menuBar().addMenu("&Edit")  # Adding an Edit menu

        # Creating actions for the menus
        add_student_action = QAction(
            QIcon("icons/add.png"), "Add Student", self
        )  # Action to add a student
        add_student_action.triggered.connect(
            self.insert
        )  # Connecting the action to the insert method
        file_menu_item.addAction(
            add_student_action
        )  # Adding the action to the File menu

        about_action = QAction(
            "About", self
        )  # Action to display an 'about' dialog
        help_menu_item.addAction(
            about_action
        )  # Adding the action to the Help menu
        about_action.setMenuRole(
            QAction.MenuRole.NoRole
        )  # Setting the menu role of the action
        about_action.triggered.connect(
            self.about
        )  # Connecting the action to the 'about method'

        search_action = QAction(
            QIcon("icons/search.png"), "Search", self
        )  # Action to search for a student
        edit_menu_item.addAction(
            search_action
        )  # Adding the action to the Edit menu
        search_action.triggered.connect(
            self.search
        )  # Connecting the action to the search method

        # Creating a table widget to display student data
        self.table = QTableWidget()  # Creating a QTableWidget object
        self.table.setColumnCount(
            4
        )  # Setting the number of columns in the table
        self.table.setHorizontalHeaderLabels(
            ("Id", "Name", "Course", "Mobile")
        )  # Setting the horizontal header labels
        self.table.verticalHeader().setVisible(
            False
        )  # Hiding the vertical header
        self.setCentralWidget(
            self.table
        )  # Setting the table as the central widget of the window

        # Creating a toolbar and adding actions to it
        toolbar = QToolBar()  # Creating a QToolBar object
        toolbar.setMovable(True)  # Allowing the toolbar to be moved
        self.addToolBar(toolbar)  # Adding the toolbar to the main window

        toolbar.addAction(
            add_student_action
        )  # Adding the add student action to the toolbar
        toolbar.addAction(
            search_action
        )  # Adding the search action to the toolbar

        # Creating a status bar
        self.statusbar = QStatusBar()  # Creating a QStatusBar object
        self.setStatusBar(
            self.statusbar
        )  # Setting the status bar for the main window

        # Connecting the cellClicked signal of the table to the cell_clicked method
        self.table.cellClicked.connect(
            self.cell_clicked
        )  # Connecting the cellClicked signal to the cell_clicked method

    def cell_clicked(self):  # Method to handle cell click event
        edit_button = QPushButton("Edit Record")  # Creating an edit button
        edit_button.clicked.connect(
            self.edit
        )  # Connecting the edit button to the edit method

        delete_button = QPushButton(
            "Delete Record"
        )  # Creating a delete button
        delete_button.clicked.connect(
            self.delete
        )  # Connecting the delete button to the delete method

        # Removing any existing buttons from the status bar
        children = self.findChildren(
            QPushButton
        )  # Finding all QPushButton children of the main window
        if children:
            for child in children:
                self.statusbar.removeWidget(
                    child
                )  # Removing each button from the status bar

        # Adding the edit and delete buttons to the status bar
        self.statusbar.addWidget(
            edit_button
        )  # Adding the edit button to the status bar
        self.statusbar.addWidget(
            delete_button
        )  # Adding the delete button to the status bar

    def load_data(
        self,
    ):  # Method to load data from the database into the table
        connection = (
            DatabaseConnection().connect()
        )  # Establishing a database connection
        result = connection.execute(
            "SELECT * FROM students"
        )  # Executing a SELECT query to fetch all student data
        self.table.setRowCount(
            0
        )  # Setting the row count of the table to 0 to clear any existing data
        for row_number, row_data in enumerate(
            result
        ):  # Iterating over the fetched data
            self.table.insertRow(
                row_number
            )  # Inserting a new row for each student
            for column_number, data in enumerate(
                row_data
            ):  # Iterating over the data for each student
                self.table.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )  # Setting the data in the table cell
        connection.close()  # Closing the database connection

    def insert(self):  # Function to open the insert dialog
        dialog = InsertDialog()  # Create an instance of the InsertDialog
        dialog.exec()  # Execute the dialog

    def search(self):  # Function to open the search dialog
        dialog = SearchDialog()  # Create an instance of the SearchDialog
        dialog.exec()  # Execute the dialog

    def edit(self):  # Function to open the edit dialog
        dialog = EditDialog()  # Create an instance of the EditDialog
        dialog.exec()  # Execute the dialog

    def delete(self):  # Function to open the delete dialog
        dialog = DeleteDialog()  # Create an instance of the DeleteDialog
        dialog.exec()  # Execute the dialog

    def about(self):  # Function to open the 'about dialog'
        dialog = AboutDialog()  # Create an instance of the AboutDialog
        dialog.exec()  # Execute the dialog


class AboutDialog(QMessageBox):  # Class for the 'about dialog'
    def __init__(self):  # Constructor for the AboutDialog class
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("About")  # Set the window title
        content = """  # Content of the about dialog
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)  # Set the text of the dialog


class EditDialog(QDialog):  # Class for the edit dialog
    def __init__(self):  # Constructor for the EditDialog class
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("Update Student Data")  # Set the window title
        self.setFixedWidth(300)  # Set the fixed width of the dialog
        self.setFixedHeight(300)  # Set the fixed height of the dialog

        layout = QVBoxLayout()  # Create a vertical layout

        # Get student name from selected row
        index = (
            main_window.table.currentRow()
        )  # Get the index of the selected row
        student_name = main_window.table.item(
            index, 1
        ).text()  # Get the student name from the selected row

        # Get id from selected row
        self.student_id = main_window.table.item(
            index, 0
        ).text()  # Get the student id from the selected row

        # Add student name widget
        self.student_name = QLineEdit(
            student_name
        )  # Create a line edit widget for the student name
        self.student_name.setPlaceholderText(
            "Name"
        )  # Set the placeholder text for the student name widget
        layout.addWidget(
            self.student_name
        )  # Add the student name widget to the layout

        # Add combo box of courses
        course_name = main_window.table.item(
            index, 2
        ).text()  # Get the course name from the selected row
        self.course_name = (
            QComboBox()
        )  # Create a combo box widget for the course name
        courses = [
            "Biology",
            "Math",
            "Astronomy",
            "Physics",
        ]  # List of courses
        self.course_name.addItems(courses)  # Add the courses to the combo box
        self.course_name.setCurrentText(
            course_name
        )  # Set the current text of the combo box to the course name
        layout.addWidget(self.course_name)  # Add the combo box to the layout

        # Add mobile widget
        mobile = main_window.table.item(
            index, 3
        ).text()  # Get the mobile number from the selected row
        self.mobile = QLineEdit(
            mobile
        )  # Create a line edit widget for the mobile number
        self.mobile.setPlaceholderText(
            "Mobile"
        )  # Set the placeholder text for the mobile number widget
        layout.addWidget(
            self.mobile
        )  # Add the mobile number widget to the layout

        # Add a submitted button
        button = QPushButton("Update")  # Create a push button widget
        button.clicked.connect(
            self.update_student
        )  # Connect the button's clicked signal to the update_student method
        layout.addWidget(button)  # Add the button to the layout

        self.setLayout(layout)  # Set the layout of the dialog

    def update_student(self):  # Method to update the student data
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",  # Execute the update query
            (
                self.student_name.text(),  # Get the student name from the student name widget
                self.course_name.itemText(
                    self.course_name.currentIndex()
                ),  # Get the course name from the combo box
                self.mobile.text(),  # Get the mobile number from the mobile number widget
                self.student_id,
            ),
        )  # Get the student id
        connection.commit()  # Commit the changes to the database
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

        # Refresh the table
        main_window.load_data()  # Reload the data in the table


class DeleteDialog(QDialog):  # Class for the delete dialog
    def __init__(self):  # Constructor for the DeleteDialog class
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle("Delete Student Data")  # Set the window title

        layout = QGridLayout()  # Create a grid layout
        confirmation = QLabel(
            "Are you sure you want to delete?"
        )  # Create a label widget for the confirmation message
        yes = QPushButton("Yes")  # Create a push button widget for yes
        no = QPushButton("No")  # Create a push button widget for no

        layout.addWidget(
            confirmation, 0, 0, 1, 2
        )  # Add the confirmation label to the layout
        layout.addWidget(yes, 1, 0)  # Add the yes button to the layout
        layout.addWidget(no, 1, 1)  # Add the no button to the layout
        self.setLayout(layout)  # Set the layout of the dialog

        yes.clicked.connect(
            self.delete_student
        )  # Connect the yes button's clicked signal to the delete_student method

    def delete_student(self):
        # Get selected row index and student id
        index = (
            main_window.table.currentRow()
        )  # Get the currently selected row index
        student_id = main_window.table.item(
            index, 0
        ).text()  # Get the student ID from the first column

        connection = sqlite3.connect("database.db")  # Connect to the database
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute(
            "DELETE from students WHERE id = ?", (student_id,)
        )  # Execute the DELETE statement
        connection.commit()  # Commit the changes to the database
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
        main_window.load_data()  # Reload the data in the table

        self.close()  # Close the dialog

        confirmation_widget = QMessageBox()  # Create a message box
        confirmation_widget.setWindowTitle(
            "Success"
        )  # Set the title of the message box
        confirmation_widget.setText(
            "The record was deleted successfully!"
        )  # Set the message
        confirmation_widget.exec()  # Show the message box


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Insert Student Data"
        )  # Set the title of the window
        self.setFixedWidth(300)  # Set the width of the window
        self.setFixedHeight(300)  # Set the height of the window

        layout = QVBoxLayout()  # Create a vertical layout

        # Add student name widget
        self.student_name = (
            QLineEdit()
        )  # Create a line edit for the student name
        self.student_name.setPlaceholderText(
            "Name"
        )  # Set the placeholder text
        layout.addWidget(self.student_name)  # Add the line edit to the layout

        # Add combo box of courses
        self.course_name = QComboBox()  # Create a combo box for the courses
        courses = [
            "Biology",
            "Math",
            "Astronomy",
            "Physics",
        ]  # Create a list of courses
        self.course_name.addItems(courses)  # Add the courses to the combo box
        layout.addWidget(self.course_name)  # Add the combo box to the layout

        # Add mobile widget
        self.mobile = QLineEdit()  # Create a line edit for the mobile number
        self.mobile.setPlaceholderText("Mobile")  # Set the placeholder text
        layout.addWidget(self.mobile)  # Add the line edit to the layout

        # Add a submitted button
        button = QPushButton("Register")  # Create a button
        button.clicked.connect(
            self.add_student
        )  # Connect the button to the add_student method
        layout.addWidget(button)  # Add the button to the layout

        self.setLayout(layout)  # Set the layout for the window

    def add_student(self):
        name = (
            self.student_name.text()
        )  # Get the student name from the line edit
        course = self.course_name.itemText(
            self.course_name.currentIndex()
        )  # Get the selected course from the combo box
        mobile = self.mobile.text()  # Get the mobile number from the line edit
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",  # Execute the INSERT statement
            (name, course, mobile),
        )
        connection.commit()  # Commit the changes to the database
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
        main_window.load_data()  # Reload the data in the table


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")  # Set the title of the window
        self.setFixedWidth(300)  # Set the width of the window
        self.setFixedHeight(300)  # Set the height of the window

        # Create layout and input widget
        layout = QVBoxLayout()  # Create a vertical layout
        self.student_name = (
            QLineEdit()
        )  # Create a line edit for the student name
        self.student_name.setPlaceholderText(
            "Name"
        )  # Set the placeholder text
        layout.addWidget(self.student_name)  # Add the line edit to the layout

        # Create button
        button = QPushButton("Search")  # Create a button
        button.clicked.connect(
            self.search
        )  # Connect the button to the search method
        layout.addWidget(button)  # Add the button to the layout

        self.setLayout(layout)  # Set the layout for the window

    def search(self):
        name = (
            self.student_name.text()
        )  # Get the student name from the line edit
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor object
        result = cursor.execute(
            "SELECT * FROM students WHERE name = ?", (name,)
        )  # Execute the SELECT statement
        rows = list(result)  # Convert the result to a list
        print(rows)  # Print the rows
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString
        )  # Find the items in the table
        for item in items:  # Iterate over the items
            print(item)  # Print the item
            main_window.table.item(item.row(), 1).setSelected(
                True
            )  # Select the item

        cursor.close()  # Close the cursor
        connection.close()  # Close the connection


app = QApplication(sys.argv)  # Create a QApplication object
main_window = MainWindow()  # Create a MainWindow object
main_window.show()  # Show the main window
main_window.load_data()  # Load the data in the table
sys.exit(app.exec())  # Start the event loop
