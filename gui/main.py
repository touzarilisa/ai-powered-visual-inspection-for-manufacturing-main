"""
This program serves as the main entry point for the GUI.
It uses Pyside2 engine from QML.
"""

# Imports
import os
import sys
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine





# Main
if __name__ == '__main__':
    # Create the application
    app = QGuiApplication(sys.argv)
    # Create the engine
    engine = QQmlApplicationEngine()  

    #engine.load(QUrl(QStringLiteral("main.qml")))
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())	
