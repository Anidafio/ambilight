import sys
from PyQt5 import QtWidgets
from config_app import AmbientLightConfigApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = AmbientLightConfigApp()
    main_app.gui.show()
    sys.exit(app.exec_())
