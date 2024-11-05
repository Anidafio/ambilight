import sys
import tkinter as tk
from PyQt5 import QtWidgets
from config_app import AmbientLightConfigApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    root = tk.Tk()
    config_app = AmbientLightConfigApp(root, app)
    
    root.mainloop()
    sys.exit(app.exec_())