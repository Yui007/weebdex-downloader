"""Dark theme styling for the GUI."""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor


# Color palette
COLORS = {
    "background": "#1a1a2e",
    "surface": "#16213e",
    "surface_light": "#1f2b4d",
    "accent": "#e94560",
    "accent_hover": "#ff6b6b",
    "text": "#ffffff",
    "text_secondary": "#a0a0a0",
    "border": "#2a2a4a",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "error": "#ef4444",
}


DARK_THEME = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}

QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}}

/* Sidebar */
#sidebar {{
    background-color: {COLORS['surface']};
    border-right: 1px solid {COLORS['border']};
}}

#sidebar QPushButton {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    color: {COLORS['text_secondary']};
    font-size: 14px;
}}

#sidebar QPushButton:hover {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text']};
}}

#sidebar QPushButton:checked {{
    background-color: {COLORS['accent']};
    color: {COLORS['text']};
}}

/* Input fields */
QLineEdit {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text']};
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

QLineEdit::placeholder {{
    color: {COLORS['text_secondary']};
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS['accent']};
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: {COLORS['text']};
    font-size: 14px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

QPushButton#secondaryBtn {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
}}

QPushButton#secondaryBtn:hover {{
    background-color: {COLORS['surface_light']};
    border-color: {COLORS['accent']};
}}

/* Scroll area */
QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollBar:vertical {{
    background-color: {COLORS['surface']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* List widgets */
QListWidget {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
}}

QListWidget::item {{
    background-color: transparent;
    border-radius: 6px;
    padding: 8px;
    margin: 2px;
}}

QListWidget::item:hover {{
    background-color: {COLORS['surface_light']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

/* Checkboxes */
QCheckBox {{
    spacing: 8px;
    color: {COLORS['text']};
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['surface']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['accent']};
}}

/* Combo boxes */
QComboBox {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text']};
}}

QComboBox:hover {{
    border-color: {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['accent']};
}}

/* Spin boxes */
QSpinBox {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 12px;
    color: {COLORS['text']};
}}

QSpinBox:hover {{
    border-color: {COLORS['accent']};
}}

/* Progress bar */
QProgressBar {{
    background-color: {COLORS['surface']};
    border: none;
    border-radius: 10px;
    height: 20px;
    text-align: center;
    color: {COLORS['text']};
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 10px;
}}

/* Labels */
QLabel {{
    color: {COLORS['text']};
    background-color: transparent;
}}

QLabel#title {{
    font-size: 24px;
    font-weight: bold;
}}

QLabel#subtitle {{
    font-size: 16px;
    color: {COLORS['text_secondary']};
}}

QLabel#sectionTitle {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS['accent']};
}}

QLabel#sectionTitle_small {{
    font-size: 14px;
    font-weight: bold;
    color: {COLORS['accent']};
}}

/* Cards */
QFrame#card {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
}}

/* Status bar */
QStatusBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
}}

/* Group boxes */
QGroupBox {{
    background-color: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 24px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {COLORS['accent']};
}}

/* Tool tips */
QToolTip {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 6px;
}}
"""


def apply_theme(app: QApplication) -> None:
    """Apply the dark theme to the application."""
    app.setStyleSheet(DARK_THEME)
    
    # Set palette for native widgets
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["background"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["surface"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["surface_light"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS["surface"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS["text"]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["text"]))
    
    app.setPalette(palette)
