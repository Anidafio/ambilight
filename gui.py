import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore

class GUI(QtWidgets.QWidget):
    def __init__(self, start_callback, stop_callback, show_overlay_callback, hide_overlay_callback, update_overlay_callback, refresh_ports_callback):
        super().__init__()
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.show_overlay_callback = show_overlay_callback
        self.hide_overlay_callback = hide_overlay_callback
        self.update_overlay_callback = update_overlay_callback
        self.refresh_ports_callback = refresh_ports_callback

        self.horizontal_leds = 18
        self.vertical_leds = 10
        self.edge_step = 50
        self.zone_depth = 50

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QGridLayout()

        # Number of LEDs on each side
        layout.addWidget(QtWidgets.QLabel("Horizontal LEDs:"), 0, 0)
        self.horizontal_leds_input = QtWidgets.QSpinBox()
        self.horizontal_leds_input.setValue(self.horizontal_leds)
        self.horizontal_leds_input.valueChanged.connect(self.update_overlay_callback)
        layout.addWidget(self.horizontal_leds_input, 0, 1)

        layout.addWidget(QtWidgets.QLabel("Vertical LEDs:"), 1, 0)
        self.vertical_leds_input = QtWidgets.QSpinBox()
        self.vertical_leds_input.setValue(self.vertical_leds)
        self.vertical_leds_input.valueChanged.connect(self.update_overlay_callback)
        layout.addWidget(self.vertical_leds_input, 1, 1)

        # Edge step from screen (in pixels)
        layout.addWidget(QtWidgets.QLabel("Edge Step (px):"), 2, 0)
        self.edge_step_input = QtWidgets.QSpinBox()
        self.edge_step_input.setValue(self.edge_step)
        self.edge_step_input.valueChanged.connect(self.update_overlay_callback)
        layout.addWidget(self.edge_step_input, 2, 1)

        # Zone depth slider
        layout.addWidget(QtWidgets.QLabel("Zone Depth:"), 3, 0)
        self.zone_depth_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.zone_depth_slider.setMinimum(10)
        self.zone_depth_slider.setMaximum(200)
        self.zone_depth_slider.setValue(self.zone_depth)
        self.zone_depth_slider.valueChanged.connect(self.update_overlay_callback)
        layout.addWidget(self.zone_depth_slider, 3, 1)

        # Preview Zones checkbox
        self.preview_checkbox = QtWidgets.QCheckBox("Preview Zones")
        self.preview_checkbox.stateChanged.connect(self.toggle_preview)
        layout.addWidget(self.preview_checkbox, 4, 0)

        # Serial port selection
        layout.addWidget(QtWidgets.QLabel("Arduino Port:"), 5, 0)
        self.port_dropdown = QtWidgets.QComboBox()
        self.refresh_ports()
        layout.addWidget(self.port_dropdown, 5, 1)

        # Refresh Ports Button
        refresh_button = QtWidgets.QPushButton("Refresh Ports")
        refresh_button.clicked.connect(self.refresh_ports_callback)
        layout.addWidget(refresh_button, 6, 0, 1, 2)

        # Start/Stop Buttons
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.start_callback)
        layout.addWidget(self.start_button, 7, 0)

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_callback)
        layout.addWidget(self.stop_button, 7, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        """Override close event to hide instead of closing."""
        event.ignore()  # Ignore the close event
        self.hide()     # Hide the window
        
    def refresh_ports(self):
        """Refresh the list of serial ports."""
        self.port_dropdown.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_dropdown.addItem(port.device)

    def toggle_preview(self):
        """Toggle preview display based on checkbox state."""
        if self.preview_checkbox.isChecked():
            self.show_overlay_callback()
        else:
            self.hide_overlay_callback()