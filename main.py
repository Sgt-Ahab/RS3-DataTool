import sys
from PySide6.QtWidgets import (
    QApplication,
    )
from PySide6.QtGui import QIcon
from resource_paths import resource_path 
from main_window import MainWindow
from styles.app_style import APP_STYLE

def getWindowIcon():
    primary_icon = resource_path("assets/R.png")
    fallback_icon = resource_path("assets/icon.png")

    if primary_icon.exists():
        return QIcon(str(primary_icon))

    if fallback_icon.exists():
        return QIcon(str(fallback_icon))

    return QIcon()

app = QApplication(sys.argv)
app.setStyleSheet(APP_STYLE)

app_icon = getWindowIcon()
app.setWindowIcon(app_icon)

window = MainWindow()
window.setWindowIcon(app_icon)
window.show()
sys.exit(app.exec())