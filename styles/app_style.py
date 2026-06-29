APP_STYLE = """
QMainWindow {
    background-color: #1f2428;
}

QWidget {
    background-color: #1f2428;
    color: #e6edf3;
    font-family: Segoe UI;
    font-size: 13px;
}

QLabel {
    color: #e6edf3;
}

QLabel#ResultPanel {
    background-color: #11161a;
    color: #f0f6fc;
    border: 1px solid #3d4650;
    border-radius: 6px;
    padding: 10px;
    font-family: Consolas;
    font-size: 13px;
}

QPlainTextEdit#ResultPanel {
    background-color: #11161a;
    color: #f0f6fc;
    border: 1px solid #3d4650;
    border-radius: 6px;
    padding: 10px;
    font-family: Consolas;
    font-size: 13px;
    selection-background-color: #d6b35a;
    selection-color: #11161a;
}

QLabel#StatusLabel {
    color: #a98c45;
    font-weight: bold;
}

QLineEdit {
    background-color: #11161a;
    color: #f0f6fc;
    border: 1px solid #3d4650;
    border-radius: 6px;
    padding: 7px;
    selection-background-color: #d6b35a;
    selection-color: #11161a;
}

QLineEdit:focus {
    border: 1px solid #d6b35a;
}

QPushButton {
    background-color: #2f3a44;
    color: #f0f6fc;
    border: 1px solid #4b5563;
    border-radius: 6px;
    padding: 8px 14px;
}

QPushButton:hover {
    background-color: #3a4652;
    border: 1px solid #d6b35a;
    color: #f1d27a;
}

QPushButton:pressed {
    background-color: #242c33;
    color: #d6b35a;
}

QPushButton:disabled {
    background-color: #1b2025;
    color: #6b7280;
    border: 1px solid #2b333b;
}

QListWidget {
    background-color: #11161a;
    color: #f0f6fc;
    border: 1px solid #3d4650;
    border-radius: 6px;
    padding: 6px;
    outline: none;
}

QListWidget::item {
    padding: 6px;
    border: none;
    outline: none;
}

QListWidget::item:hover {
    background-color: #2f3a44;
}

QListWidget::item:selected {
    background-color: #3a4652;
    color: #f1d27a;
    border-left: 3px solid #d6b35a;
    outline: none;
}

QListWidget::item:selected:focus {
    background-color: #3a4652;
    color: #f1d27a;
    border-left: 3px solid #d6b35a;
    outline: none;
}

QScrollBar:vertical {
    background: #11161a;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #4b5563;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #6b7280;
}


QTabWidget::pane {
    border: 0px;
    margin: 0px;
    padding: 0px;
    background-color: #1f2428;
}

QTabWidget::tab-bar {
    left: 0px;
}

QTabWidget {
    border: none;
}

QTabBar {
    background-color: #1f2428;
    border: 0px;
    margin: 0px;
    padding: 0px;
}

QTabBar::tab {
    background-color: #20272d;
    color: #d6b35a;
    border: 1px solid #2f3a44;
    padding: 8px 4px;
    min-width: 28px;
    min-height: 82px;
}

QTabBar::tab:selected {
    background-color: #11161a;
    color: #f1d27a;

    border-top: 1px solid #d6b35a;
    border-bottom: 1px solid #d6b35a;
    border-left: 0px;
    border-right: 2px solid #d6b35a;
}

QTabBar::tab:hover {
    background-color: #2f3a44;
    color: #f1d27a;
    border: 1px solid #a98c45;
}

QGroupBox {
    background-color: #1f2428;
    border: 1px solid #3d4650;
    border-radius: 6px;
    margin-top: 12px;
    padding: 12px;
    color: #d6b35a;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0px 6px;
    background-color: #1f2428;
    color: #f1d27a;
}

"""