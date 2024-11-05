import tkinter as tk
import pystray
from PIL import Image as PILImage
from overlay_window import OverlayWindow
from gui import GUI
from ambient_light_controller import AmbientLightController

class AmbientLightConfigApp:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.overlay = None  # To manage the overlay window
        self.controller = None

        self.gui = GUI(
            master=root,
            start_callback=self.start_ambient_light,
            stop_callback=self.stop_ambient_light,
            show_overlay_callback=self.show_overlay,
            hide_overlay_callback=self.hide_overlay,
            update_overlay_callback=self.update_overlay
        )
        self.gui.pack()

        # Configure system tray icon
        self.setup_tray_icon()

        # Adjust window size to fit screen
        self.root.geometry("600x400")
        
    def calculate_zones(self, screen_width, screen_height):
        """Calculate the zones based on user settings, including edge step."""
        zones = []
        zone_depth = self.gui.zone_depth.get()
        horizontal_leds = self.gui.horizontal_leds.get()
        vertical_leds = self.gui.vertical_leds.get()
        edge_step = self.gui.edge_step.get()  # Edge step in pixels
        
        # Calculate bottom row (horizontal)
        for i in reversed(range(horizontal_leds)):
            x = int(edge_step + i * (screen_width - 2 * edge_step) / horizontal_leds)
            y = screen_height - zone_depth
            width = int((screen_width - 2 * edge_step) / horizontal_leds)
            height = zone_depth
            zones.append((x, y, width, height))

        # Calculate left column (vertical) from bottom to top
        for i in reversed(range(vertical_leds)):
            x = 0
            y = int(edge_step + i * (screen_height - 2 * edge_step) / vertical_leds)
            width = zone_depth
            height = int((screen_height - 2 * edge_step) / vertical_leds)
            zones.append((x, y, width, height))

        # Calculate top row (horizontal)
        for i in range(horizontal_leds):
            x = int(edge_step + i * (screen_width - 2 * edge_step) / horizontal_leds)
            y = 0
            width = int((screen_width - 2 * edge_step) / horizontal_leds)
            height = zone_depth
            zones.append((x, y, width, height))

        # Calculate right column (vertical)
        for i in range(vertical_leds):
            x = screen_width - zone_depth
            y = int(edge_step + i * (screen_height - 2 * edge_step) / vertical_leds)
            width = zone_depth
            height = int((screen_height - 2 * edge_step) / vertical_leds)
            zones.append((x, y, width, height))

        return zones

    def show_overlay(self):
        """Show the overlay with zones on the screen."""
        if self.overlay:
            self.overlay.hide()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        zones = self.calculate_zones(screen_width, screen_height)

        # Create and display overlay window with calculated zones
        self.overlay = OverlayWindow(zones, screen_width, screen_height)
        self.overlay.show()

    def hide_overlay(self):
        """Hide the overlay if it is currently displayed."""
        if self.overlay:
            self.overlay.hide()

    def update_overlay(self):
        """Update the overlay when zone depth or edge step changes."""
        if self.gui.preview_enabled.get():  # Only update if preview is enabled
            self.show_overlay()
            
    def start_ambient_light(self):
        """Start the ambient light controller with current settings."""
        if not self.controller:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            target_fps = 30
            arduino_port = self.gui.port_var.get()  # Get the selected port from the GUI
            if not arduino_port:
                print("No serial port selected!")
                return

            zones = self.calculate_zones(screen_width, screen_height)

            # Initialize the ambient light controller
            self.controller = AmbientLightController(
                screen_width=screen_width,
                screen_height=screen_height,
                target_fps=target_fps,
                arduino_port=arduino_port,
                zones=zones
            )

            # Start the controller
            self.controller.start()
            self.gui.start_button.config(state=tk.DISABLED)
            self.gui.stop_button.config(state=tk.NORMAL)

    def stop_ambient_light(self):
        """Stop the ambient light controller if it is running."""
        if self.controller:
            self.controller.stop()
            self.controller = None
            self.gui.start_button.config(state=tk.NORMAL)
            self.gui.stop_button.config(state=tk.DISABLED)

    def setup_tray_icon(self):
        """Configure the system tray icon."""
        image = PILImage.new("RGB", (64, 64), color="blue")
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.exit_app)
        )
        self.tray_icon = pystray.Icon("ambient_light_app", image, "Ambient Light", menu)
        self.tray_icon.run_detached()

    def minimize_to_tray(self):
        """Minimize the application to the system tray instead of closing."""
        self.root.withdraw()  # Hide the window instead of closing
        self.tray_icon.visible = True  # Ensure the tray icon is visible

    def show_window(self, icon, item):
        """Show the main GUI window from the system tray icon."""
        self.root.after(0, self._show_gui)  # Schedule the GUI to show on the main thread

    def _show_gui(self):
        """Helper method to show the GUI window on the main thread."""
        if not self.root.winfo_viewable():  # Check if the window is not currently shown
            self.root.deiconify()  # Show the window
            self.root.lift()  # Bring it to the front
        self.tray_icon.visible = False  # Hide the tray icon once the window is shown

    def exit_app(self, icon, item):
        """Exit the application."""
        if self.overlay:
            self.overlay.hide()
        icon.stop()
        self.root.quit()