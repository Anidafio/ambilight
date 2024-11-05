from PyQt5 import QtWidgets, QtCore, QtGui

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, zones, screen_width, screen_height):
        super().__init__()
        self.zones = zones
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set window properties for transparent overlay
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # Set window size to match the screen
        self.setGeometry(0, 0, screen_width, screen_height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0, 150))  # Semi-transparent green for rectangles
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw each zone as a rectangle
        for (x, y, width, height) in self.zones:
            painter.drawRect(x, y, width, height)
    
    def hide(self):
        """Close the overlay window."""
        self.close()