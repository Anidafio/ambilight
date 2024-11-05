from PyQt5 import QtWidgets, QtGui
from gui.gui import GUI
from gui.overlay_window import OverlayWindow
import pystray
from PIL import Image as PILImage
from ambilight_logic.ambient_light_controller import AmbientLightController

class AmbientLightConfigApp:
    def __init__(self):
        self.overlay = None
        self.screen_width = QtWidgets.QApplication.primaryScreen().size().width()
        self.screen_height = QtWidgets.QApplication.primaryScreen().size().height()
        self.controller = None

        self.gui = GUI(
            start_callback=self.start_ambient_light,
            stop_callback=self.stop_ambient_light,
            show_overlay_callback=self.show_overlay,
            hide_overlay_callback=self.hide_overlay,
            update_overlay_callback=self.update_overlay,
            refresh_ports_callback=self.refresh_ports
        )

        # Set up the system tray icon
        self.setup_tray_icon()

    def calculate_zones(self):
        """Calculate the zones based on user settings."""
        zones = []
        zone_depth = self.gui.zone_depth_slider.value()
        horizontal_leds = self.gui.horizontal_leds_input.value()
        vertical_leds = self.gui.vertical_leds_input.value()
        edge_step = self.gui.edge_step_input.value()

        for i in reversed(range(horizontal_leds)):
            x = int(edge_step + i * (self.screen_width - 2 * edge_step) / horizontal_leds)
            y = self.screen_height - zone_depth
            zones.append((x, y, int((self.screen_width - 2 * edge_step) / horizontal_leds), zone_depth))

        for i in reversed(range(vertical_leds)):
            x = 0
            y = int(edge_step + i * (self.screen_height - 2 * edge_step) / vertical_leds)
            zones.append((x, y, zone_depth, int((self.screen_height - 2 * edge_step) / vertical_leds)))

        for i in range(horizontal_leds):
            x = int(edge_step + i * (self.screen_width - 2 * edge_step) / horizontal_leds)
            y = 0
            zones.append((x, y, int((self.screen_width - 2 * edge_step) / horizontal_leds), zone_depth))

        for i in range(vertical_leds):
            x = self.screen_width - zone_depth
            y = int(edge_step + i * (self.screen_height - 2 * edge_step) / vertical_leds)
            zones.append((x, y, zone_depth, int((self.screen_height - 2 * edge_step) / vertical_leds)))

        return zones

    def show_overlay(self):
        """Show the overlay window with calculated zones."""
        if self.overlay:
            self.overlay.close()

        zones = self.calculate_zones()
        self.overlay = OverlayWindow(zones, self.screen_width, self.screen_height)
        self.overlay.show()

    def hide_overlay(self):
        """Hide the overlay window."""
        if self.overlay:
            self.overlay.close()
            self.overlay = None

    def update_overlay(self):
        """Update the overlay window when settings change."""
        if self.gui.preview_checkbox.isChecked():
            self.show_overlay()

    def start_ambient_light(self):
        """Start the ambient light effect."""
        if not self.controller:
            target_fps = 30
            arduino_port = self.gui.port_dropdown.currentText()  # Get the selected port from the GUI
            if not arduino_port:
                print("No serial port selected!")
                return

            zones = self.calculate_zones()

            # Initialize the ambient light controller
            self.controller = AmbientLightController(
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                target_fps=target_fps,
                arduino_port=arduino_port,
                zones=zones
            )

            # Start the controller
            self.controller.start()
            self.gui.start_button.setEnabled(False)
            self.gui.stop_button.setEnabled(True)

    def stop_ambient_light(self):
        """Stop the ambient light effect."""
        if self.controller:
            self.controller.stop()
            self.controller = None
            self.gui.start_button.setEnabled(True)
            self.gui.stop_button.setEnabled(False)
            self.hide_overlay()

    def setup_tray_icon(self):
        """Configure the system tray icon."""
        image = PILImage.new("RGB", (64, 64), color="blue")
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.exit_app)
        )
        self.tray_icon = pystray.Icon("ambient_light_app", image, "Ambient Light", menu)
        self.tray_icon.run_detached()

    def show_window(self, icon, item):
        """Show the main GUI window."""
        self.gui.show()

    def exit_app(self, icon, item):
        """Exit the application."""
        self.stop_ambient_light()
        if self.overlay:
            self.overlay.close()
        icon.stop()
        QtWidgets.QApplication.instance().quit()

    def refresh_ports(self):
        """Refresh the serial ports in the GUI."""
        self.gui.refresh_ports()