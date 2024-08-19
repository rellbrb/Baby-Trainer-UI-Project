import sys  # Import sys to handle system-specific parameters and functions
from PyQt6.QtWidgets import (  # Import necessary widgets from PyQt6
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
    QFormLayout, QLabel, QTabWidget, QLineEdit, QComboBox, QGridLayout
)
from PyQt6.QtGui import QIcon   # Used for window icons (if any)
from PyQt6.QtCore import Qt, QTimer  # Core elements like Qt identifiers and Timer
import pyqtgraph as pg  # For creating scientific graphics
import numpy as np  # For numerical operations

# Define a class for the second window, intended for simple training scenarios
class Window2(QMainWindow):  
    def __init__(self, fullname="", personal_id="", occupation="", difficulty=""):
        super().__init__()  # Initialize the superclass
        self.setWindowTitle('Simple training')  # Set the window title
        self.window2_main_layout = QVBoxLayout()  # Vertical layout for widgets
        self.tabs = QTabWidget()  # Tab widget for multiple plots or views
        self.create_force_tab()  # Method to create a tab with a force plot
        self.tabs.addTab(self.force_tab, 'Force')  # Add the force tab to the tab widget
        self.window2_main_layout.addWidget(self.tabs)

        # Method to display user information
        self.display_input_info(fullname, personal_id, occupation, difficulty)

        # Buttons to start and stop the simulation
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_plot)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_plot)
        self.window2_main_layout.addWidget(self.start_button)
        self.window2_main_layout.addWidget(self.stop_button)

        # Timer to update plots periodically
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)

        # Set up the central widget and layout
        w2 = QWidget()
        w2.setLayout(self.window2_main_layout)
        self.setCentralWidget(w2)

        self.data_index = 0  # Index to manage the data progression in plots
        
        # Light indicator for visual feedback
        self.light_indicator = QLabel()
        self.light_indicator.setFixedSize(60, 60)
        self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        self.window2_main_layout.addWidget(self.light_indicator)

    # Display static user information
    def display_input_info(self, fullname, personal_id, occupation, difficulty):
        info_label = QLabel(f"Full Name: {fullname}\n"
                            f"Personal ID: {personal_id}\n"
                            f"Occupation: {occupation}\n"
                            f"Difficulty: {difficulty}")
        self.window2_main_layout.addWidget(info_label)

    # Create a tab with a force plot
    def create_force_tab(self):
        self.force_tab = QWidget()
        layout = QVBoxLayout()
        self.force_plot_widget = pg.PlotWidget()
        self.force_plot_widget.setTitle('Force vs. Time')
        self.force_plot_widget.setLabel('left', 'Force', units='N')
        self.force_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.force_plot_widget)
        self.force_tab.setLayout(layout)
        self.force_plot_widget.addLine(y=0.5, pen='g')  # Horizontal threshold line
        
    # Start the data plot updating process
    def start_plot(self):
        if not self.plot_timer.isActive():
            self.plot_timer.start(100)  # Update every 100 milliseconds

    # Stop the data plot updating process
    def stop_plot(self):
        if self.plot_timer.isActive():
            self.plot_timer.stop()

    # Method to update the plot data
    def update_plots(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x + self.data_index / 10.0)  # Simulated sine wave data
        
        # Dynamically update the plot
        if hasattr(self, 'force_data_line'):
            self.force_plot_widget.removeItem(self.force_data_line)
        self.force_data_line = self.force_plot_widget.plot(x, y, pen='r')
        
        # Adjust the light indicator based on data values
        current_tab = self.tabs.currentWidget()
        if current_tab == self.force_tab and y[-1] > 0.5:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        else:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: green;")
        self.data_index += 1
        
       
# Define a class for an intermediate training window
class Window3(QMainWindow):
    def __init__(self, fullname="", personal_id="", occupation="", difficulty=""):
        super().__init__()
        self.setWindowTitle('Intermediate Training')
        self.window3_main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        # Create tabs for different types of data visualization
        self.create_force_tab()
        self.create_angular_displacement_tab()
        self.create_combined_tab()
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.force_tab, 'Force')
        self.tabs.addTab(self.angular_tab, 'Angular Displacement')
        self.tabs.addTab(self.combined_tab, 'Combined View')
        self.window3_main_layout.addWidget(self.tabs)

        # Display user information at the top of the window
        self.display_input_info(fullname, personal_id, occupation, difficulty)

        # Start and stop buttons for the data updates
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_plot)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_plot)
        self.window3_main_layout.addWidget(self.start_button)
        self.window3_main_layout.addWidget(self.stop_button)

        # Timer for periodic updates of the plots
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)

        # Setting up the layout and widgets
        w3 = QWidget()
        w3.setLayout(self.window3_main_layout)
        self.setCentralWidget(w3)

        self.data_index = 0  # Index for controlling the simulation's data flow
        self.plot_data = {}  # Store references to plotted data for updates

        # Visual indicator (light) for threshold crossing alerts
        self.light_indicator = QLabel()
        self.light_indicator.setFixedSize(60, 60)
        self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        self.window3_main_layout.addWidget(self.light_indicator)

    # Display static user information in a consistent format
    def display_input_info(self, fullname, personal_id, occupation, difficulty):
        info_label = QLabel(f"Full Name: {fullname}\n"
                            f"Personal ID: {personal_id}\n"
                            f"Occupation: {occupation}\n"
                            f"Difficulty: {difficulty}")
        self.window3_main_layout.addWidget(info_label)

    # Simplified example of creating a plot tab for force data
    def create_force_tab(self):
        self.force_tab = QWidget()
        layout = QVBoxLayout()
        self.force_plot_widget = pg.PlotWidget()
        self.force_plot_widget.setTitle('Force vs. Time')
        self.force_plot_widget.setLabel('left', 'Force', units='N')
        self.force_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.force_plot_widget)
        self.force_tab.setLayout(layout)
        self.force_plot_widget.addLine(y=0.5, pen='g')  # Threshold line

    # Creating tab and plot for angular displacement data
    def create_angular_displacement_tab(self):
        self.angular_tab = QWidget()
        layout = QVBoxLayout()
        self.angular_plot_widget = pg.PlotWidget()
        self.angular_plot_widget.setTitle('Angular Displacement vs. Time')
        self.angular_plot_widget.setLabel('left', 'Angular Displacement', units='deg')
        self.angular_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.angular_plot_widget)
        self.angular_tab.setLayout(layout)
        self.angular_plot_widget.addLine(y=0.5, pen='g')  # Threshold line

    # Creating a combined view that includes both force and angular displacement in a grid layout
    def create_combined_tab(self):
        self.combined_tab = QWidget()
        grid_layout = QGridLayout()
        self.combined_force_plot_widget = pg.PlotWidget()
        self.combined_force_plot_widget.setTitle('Force vs. Time')
        self.combined_angular_plot_widget = pg.PlotWidget()
        self.combined_angular_plot_widget.setTitle('Angular Displacement vs. Time')
        grid_layout.addWidget(self.combined_force_plot_widget, 0, 0)
        grid_layout.addWidget(self.combined_angular_plot_widget, 0, 1)
        self.combined_tab.setLayout(grid_layout)
        # Adding threshold lines for the combined view plots
        self.combined_force_plot_widget.addLine(y=0.5, pen='g')
        self.combined_angular_plot_widget.addLine(y=0.5, pen='g')

    # Function to start data plotting
    def start_plot(self):
        if not self.plot_timer.isActive():
            self.plot_timer.start(100)  # Update every 100 milliseconds

    # Function to stop data plotting
    def stop_plot(self):
        if self.plot_timer.isActive():
            self.plot_timer.stop()

    # Update data plots periodically based on the timer
    def update_plots(self):
        x = np.linspace(0, 10, 100)
        y_force = np.sin(x + self.data_index / 10.0)  # Dynamic data for force graph
        y_angular = np.cos(x + self.data_index / 10.0)  # Dynamic data for angular displacement graph

        # Dynamically update both individual and combined view plots
        if hasattr(self, 'force_data_line'):
            self.force_plot_widget.removeItem(self.force_data_line)
            self.combined_force_plot_widget.removeItem(self.force_data_line_combined)
        self.force_data_line = self.force_plot_widget.plot(x, y_force, pen='r')
        self.force_data_line_combined = self.combined_force_plot_widget.plot(x, y_force, pen='r')

        if hasattr(self, 'angular_data_line'):
            self.angular_plot_widget.removeItem(self.angular_data_line)
            self.combined_angular_plot_widget.removeItem(self.angular_data_line_combined)
        self.angular_data_line = self.angular_plot_widget.plot(x, y_angular, pen='b')
        self.angular_data_line_combined = self.combined_angular_plot_widget.plot(x, y_angular, pen='b')

        # Update light indicator based on the current tab and the last data point
        current_tab = self.tabs.currentWidget()
        if current_tab == self.force_tab and y_force[-1] > 0.5:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        elif current_tab == self.angular_tab and y_angular[-1] > 0.5:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        else:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: green;")

        self.data_index += 1
        

class Window4(QMainWindow): 
    # Initialize the Advanced Training window with personal details as arguments
    def __init__(self, fullname="", personal_id="", occupation="", difficulty=""):
        super().__init__()
        self.setWindowTitle('Advanced Training')
        self.window4_main_layout = QVBoxLayout()

        # Tabs to organize different types of data visualization
        self.tabs = QTabWidget()
        self.create_force_tab()
        self.create_pressure_tab()
        self.create_angular_displacement_tab()
        self.create_combined_tab()
        self.tabs.addTab(self.combined_tab, 'Combined View')
        self.tabs.addTab(self.force_tab, 'Force')
        self.tabs.addTab(self.pressure_tab, 'Pressure')
        self.tabs.addTab(self.angular_tab, 'Angular Displacement')

        self.window4_main_layout.addWidget(self.tabs)

        # Display personal and training details
        self.display_input_info(fullname, personal_id, occupation, difficulty)

        # Control buttons for starting and stopping the training
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_plot)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_plot)
        self.window4_main_layout.addWidget(self.start_button)
        self.window4_main_layout.addWidget(self.stop_button)

        # Timer to handle real-time updates to the plots
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)

        # Setup the main layout
        w4 = QWidget()
        w4.setLayout(self.window4_main_layout)
        self.setCentralWidget(w4)

        self.data_index = 0  # Index to manage the simulation's progression

        # Light indicator for threshold breaches
        self.light_indicator = QLabel()
        self.light_indicator.setFixedSize(60, 60)
        self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        self.window4_main_layout.addWidget(self.light_indicator)

    # Display static user information clearly
    def display_input_info(self, fullname, personal_id, occupation, difficulty):
        info_label = QLabel(f"Full Name: {fullname}\n"
                            f"Personal ID: {personal_id}\n"
                            f"Occupation: {occupation}\n"
                            f"Difficulty: {difficulty}")
        self.window4_main_layout.addWidget(info_label)

    # Create tabs for different metrics (force, pressure, etc.)
    def create_force_tab(self):
        self.force_tab = QWidget()
        layout = QVBoxLayout()
        self.force_plot_widget = pg.PlotWidget()
        self.force_plot_widget.setTitle('Force vs. Time')
        self.force_plot_widget.setLabel('left', 'Force', units='N')
        self.force_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.force_plot_widget)
        self.force_tab.setLayout(layout)
        self.force_plot_widget.addLine(y=0.5, pen='g')  # Threshold line for visualization

    def create_pressure_tab(self):
        self.pressure_tab = QWidget()
        layout = QVBoxLayout()
        self.pressure_plot_widget = pg.PlotWidget()
        self.pressure_plot_widget.setTitle('Pressure vs. Time')
        self.pressure_plot_widget.setLabel('left', 'Pressure', units='Pa')
        self.pressure_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.pressure_plot_widget)
        self.pressure_tab.setLayout(layout)
        self.pressure_plot_widget.addLine(y=100, pen='b')  # Pressure threshold

    def create_angular_displacement_tab(self):
        self.angular_tab = QWidget()
        layout = QVBoxLayout()
        self.angular_plot_widget = pg.PlotWidget()
        self.angular_plot_widget.setTitle('Angular Displacement vs. Time')
        self.angular_plot_widget.setLabel('left', 'Angular Displacement', units='deg')
        self.angular_plot_widget.setLabel('bottom', 'Time', units='s')
        layout.addWidget(self.angular_plot_widget)
        self.angular_tab.setLayout(layout)
        self.angular_plot_widget.addLine(y=0.5, pen='g')  # Angular displacement threshold

    # Combined tab showing all metrics together for comparison
    def create_combined_tab(self):
        self.combined_tab = QWidget()
        grid_layout = QGridLayout()
        self.combined_force_plot_widget = pg.PlotWidget()
        self.combined_force_plot_widget.setTitle('Force vs. Time')
        self.combined_pressure_plot_widget = pg.PlotWidget()
        self.combined_pressure_plot_widget.setTitle('Pressure vs. Time')
        self.combined_angular_plot_widget = pg.PlotWidget()
        self.combined_angular_plot_widget.setTitle('Angular Displacement vs. Time')
        grid_layout.addWidget(self.combined_force_plot_widget, 0, 0)
        grid_layout.addWidget(self.combined_pressure_plot_widget, 0, 1)
        grid_layout.addWidget(self.combined_angular_plot_widget, 1, 0)
        self.combined_tab.setLayout(grid_layout)

    # Methods to start and stop the real-time data plot updates
    def start_plot(self):
        if not self.plot_timer.isActive():
            self.plot_timer.start(100)  # Timer interval in milliseconds

    def stop_plot(self):
        if self.plot_timer.isActive():
            self.plot_timer.stop()

    # Update the plots based on the timer; manage data and visuals
    def update_plots(self):
        x = np.linspace(0, 10, 100)
        y_force = np.sin(x + self.data_index / 10.0) * 0.4 + 0.5
        y_pressure = np.cos(x + self.data_index / 10.0) * 80 + 100
        y_angular = np.sin(x + self.data_index / 10.0) * 0.4 + 0.5

        # Update all plots; check and update light based on threshold values
        self.force_plot_widget.plot(x, y_force, clear=True, pen='r')
        self.pressure_plot_widget.plot(x, y_pressure, clear=True, pen='b')
        self.angular_plot_widget.plot(x, y_angular, clear=True, pen='g')

        current_tab = self.tabs.currentWidget()
        if current_tab == self.force_tab and y_force[-1] > 0.5:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        elif current_tab == self.pressure_tab and y_pressure[-1] > 100:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        elif current_tab == self.angular_tab and y_angular[-1] > 0.5:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: red;")
        else:
            self.light_indicator.setStyleSheet("border-radius: 10px; background-color: green;")

        self.data_index += 1
        
        # Update force data in the individual and combined tab
        if hasattr(self, 'force_data_line'):
            self.force_plot_widget.removeItem(self.force_data_line)
            self.combined_force_plot_widget.removeItem(self.force_data_line_combined)
        self.force_data_line = self.force_plot_widget.plot(x, y_force, pen='r')
        self.force_data_line_combined = self.combined_force_plot_widget.plot(x, y_force, pen='r')

        # Update angular data in the individual and combined tab
        if hasattr(self, 'angular_data_line'):
            self.angular_plot_widget.removeItem(self.angular_data_line)
            self.combined_angular_plot_widget.removeItem(self.angular_data_line_combined)
        self.angular_data_line = self.angular_plot_widget.plot(x, y_angular, pen='b')
        self.angular_data_line_combined = self.combined_angular_plot_widget.plot(x, y_angular, pen='b')

        # Update pressure data in the individual and combined tab
        if hasattr(self, 'pressure_data_line'):
            self.pressure_plot_widget.removeItem(self.pressure_data_line)
            self.combined_pressure_plot_widget.removeItem(self.pressure_data_line_combined)
        self.pressure_data_line = self.pressure_plot_widget.plot(x, y_angular, pen='b')
        self.pressure_data_line_combined = self.combined_pressure_plot_widget.plot(x, y_pressure, pen='g')
        
# Define the main window for user input
class Window1(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.setWindowTitle('Training Program')  # Set the title of the window
        self.window1_main_layout = QVBoxLayout()  # Create a vertical layout for the main window

        # Create labels and input fields for user information
        self.fullname_label = QLabel('Full Name:')  # Label for full name
        self.fullname_input = QLineEdit()  # Input field for full name
        self.personal_id_label = QLabel('Personal ID:')  # Label for personal ID
        self.personal_id_input = QLineEdit()  # Input field for personal ID
        self.occupation_label = QLabel('Occupation:')  # Label for occupation
        self.occupation_input = QLineEdit()  # Input field for occupation
        self.difficulty_label = QLabel('Difficulty:')  # Label for difficulty level
        self.difficulty_combo = QComboBox()  # Dropdown menu for difficulty level
        self.difficulty_combo.addItems(['Easy', 'Intermediate', 'Advanced'])

        # Add labels and input fields to the main layout
        self.window1_main_layout.addWidget(self.fullname_label)
        self.window1_main_layout.addWidget(self.fullname_input)
        self.window1_main_layout.addWidget(self.personal_id_label)
        self.window1_main_layout.addWidget(self.personal_id_input)
        self.window1_main_layout.addWidget(self.occupation_label)
        self.window1_main_layout.addWidget(self.occupation_input)
        self.window1_main_layout.addWidget(self.difficulty_label)
        self.window1_main_layout.addWidget(self.difficulty_combo)

        # Create a button to start the training
        self.start_training_button = QPushButton('Start Training')
        self.start_training_button.clicked.connect(self.start_training)

        # Add the button to the layout
        self.window1_main_layout.addWidget(self.start_training_button)

        # Create a central widget and set the layout for the main window
        window1_widget = QWidget()
        window1_widget.setLayout(self.window1_main_layout)
        self.setCentralWidget(window1_widget)  # Set the central widget for the main window

    def start_training(self):
        # Retrieve user information from the input fields
        fullname = self.fullname_input.text()
        personal_id = self.personal_id_input.text()
        occupation = self.occupation_input.text()
        difficulty = self.difficulty_combo.currentText()

        # Determine which training window to open based on the selected difficulty level
        if difficulty == 'Easy':
            self.open_window2(fullname, personal_id, occupation, difficulty)
        elif difficulty == 'Intermediate':
            self.open_window3(fullname, personal_id, occupation, difficulty)
        elif difficulty == 'Advanced':
            self.open_window4(fullname, personal_id, occupation, difficulty)

    def open_window2(self, fullname, personal_id, occupation, difficulty):
        self.window2 = Window2(fullname, personal_id, occupation, difficulty)
        self.window2.show()

    def open_window3(self, fullname, personal_id, occupation, difficulty):
        self.window3 = Window3(fullname, personal_id, occupation, difficulty)
        self.window3.show()

    def open_window4(self, fullname, personal_id, occupation, difficulty):
        self.window4 = Window4(fullname, personal_id, occupation, difficulty)
        self.window4.show()

# Define the main window for the application startup page
class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the constructor of the base class (QMainWindow)
        self.setWindowTitle('Start-up Page')
        self.window1 = Window1()
      
        # Create a vertical layout for the main window
        l = QVBoxLayout()
        
        # Create and customize labels for the main window title and subtitle
        mainwindow_title = QLabel("Baby Trainer!")
        mainfont = mainwindow_title.font()
        mainfont.setPointSize(80)
        mainwindow_title.setFont(mainfont)
        mainwindow_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        l.addWidget(mainwindow_title)
        
        mainwindow_subtitle = QLabel('Goodluck')
        subfont = mainwindow_subtitle.font()
        subfont.setPointSize(10)
        mainwindow_subtitle.setFont(subfont)
        mainwindow_subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter) #aligns the label to the cennter of the page
        l.addWidget(mainwindow_subtitle)   #adds the labe

        # Create a button for the window
        mainbutton = QPushButton("Start")
        mainbutton.clicked.connect(self.toggle_window1)  # Connect the button's click event to toggle_window1 method
        l.addWidget(mainbutton, alignment= Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter) # Add the button to the layout

        l.addStretch()
        w = QWidget()  # Create a new QWidget
        w.setLayout(l)  # Set the layout for the QWidget
        self.setCentralWidget(w)  # Set the QWidget as the central widget of the QMainWindow
        
    # Method to toggle the visibility of window1
    def toggle_window1(self):
        self.close()  # Close the main window
        self.window1.show()  # Show window1
        
        
# Main function to start the application
def main():
    app = QApplication(sys.argv)  # Create a PyQt application
    window = MainWindow1()  # Create an instance of the main window
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start the event loop


if __name__ == '__main__':
    main()  # Run the main function to start the application
