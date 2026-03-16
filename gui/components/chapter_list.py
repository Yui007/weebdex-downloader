"""Chapter list widget with selection support."""

from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.models import Chapter


class ChapterListWidget(QWidget):
    """Widget for displaying and selecting chapters."""
    
    selection_changed = pyqtSignal(int)  # number of selected chapters
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._chapters: List[Chapter] = []
        self._filtered_chapters: List[Chapter] = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the widget layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header with selection buttons
        header = QHBoxLayout()
        header.setSpacing(8)
        
        self.count_label = QLabel("0 chapters")
        self.count_label.setObjectName("sectionTitle")
        header.addWidget(self.count_label)
        
        header.addStretch()
        
        # Group filter
        group_label = QLabel("Group:")
        header.addWidget(group_label)
        
        self.group_filter = QComboBox()
        self.group_filter.setFixedWidth(200)
        self.group_filter.currentIndexChanged.connect(self._apply_group_filter)
        header.addWidget(self.group_filter)
        
        # Range input
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("e.g., 1-10 or 5")
        self.range_input.setFixedWidth(150)
        self.range_input.returnPressed.connect(self._apply_range_selection)
        header.addWidget(self.range_input)
        
        apply_btn = QPushButton("Apply")
        apply_btn.setObjectName("secondaryBtn")
        apply_btn.setFixedWidth(100)
        apply_btn.clicked.connect(self._apply_range_selection)
        header.addWidget(apply_btn)
        
        layout.addLayout(header)
        
        # Button row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.setObjectName("secondaryBtn")
        select_all_btn.clicked.connect(self.select_all)
        btn_row.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.setObjectName("secondaryBtn")
        deselect_all_btn.clicked.connect(self.deselect_all)
        btn_row.addWidget(deselect_all_btn)
        
        btn_row.addStretch()
        
        self.selected_label = QLabel("0 selected")
        self.selected_label.setStyleSheet("color: #e94560; font-weight: bold;")
        btn_row.addWidget(self.selected_label)
        
        layout.addLayout(btn_row)
        
        # Chapter list
        self.list_widget = QListWidget()
        self.list_widget.itemChanged.connect(self._on_item_changed)
        self.list_widget.setMinimumHeight(250)  # Ensure minimum visible height
        layout.addWidget(self.list_widget, 1)  # Give it stretch priority
    
    def set_chapters(self, chapters: List[Chapter]):
        """Populate the list with chapters."""
        self._chapters = chapters
        self._filtered_chapters = chapters
        
        # Populate group filter
        self._populate_group_filter()
        
        # Display chapters
        self._display_chapters()
    
    def _populate_group_filter(self):
        """Populate the group filter dropdown with unique groups."""
        # Collect all unique groups
        groups = set()
        for chapter in self._chapters:
            for group in chapter.groups:
                groups.add(group.name)
        
        # Sort groups alphabetically
        sorted_groups = sorted(groups)
        
        # Block signals while updating
        self.group_filter.blockSignals(True)
        self.group_filter.clear()
        
        # Add "All Groups" option
        self.group_filter.addItem("All Groups", None)
        
        # Add each group
        for group in sorted_groups:
            self.group_filter.addItem(group, group)
        
        self.group_filter.blockSignals(False)
    
    def _apply_group_filter(self):
        """Filter chapters by selected group."""
        selected_group = self.group_filter.currentData()
        
        if selected_group is None:
            # Show all chapters
            self._filtered_chapters = self._chapters
        else:
            # Filter by group
            self._filtered_chapters = [
                ch for ch in self._chapters
                if any(g.name == selected_group for g in ch.groups)
            ]
        
        self._display_chapters()
    
    def _display_chapters(self):
        """Display the filtered chapters in the list."""
        self.list_widget.clear()
        
        for i, chapter in enumerate(self._filtered_chapters):
            item = QListWidgetItem()
            
            # Build display text
            group_name = chapter.groups[0].name if chapter.groups else "Unknown"
            text = f"{i + 1}. {chapter.get_display_name()} - {group_name}"
            item.setText(text)
            
            # Store chapter data
            item.setData(Qt.ItemDataRole.UserRole, chapter)
            
            # Make checkable
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            
            self.list_widget.addItem(item)
        
        # Update count label to show filtered/total
        if len(self._filtered_chapters) < len(self._chapters):
            self.count_label.setText(
                f"{len(self._filtered_chapters)} / {len(self._chapters)} chapters"
            )
        else:
            self.count_label.setText(f"{len(self._chapters)} chapters")
        
        self._update_selected_count()
    
    def _apply_range_selection(self):
        """Apply selection based on range input."""
        text = self.range_input.text().strip()
        if not text:
            return
        
        total = len(self._filtered_chapters)
        
        # Handle "all"
        if text.lower() == "all":
            self.select_all()
            self.range_input.clear()
            return
        
        # Handle range "X-Y"
        if "-" in text:
            try:
                parts = text.split("-")
                start = int(parts[0]) - 1
                end = int(parts[1])
                
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if start <= i < end:
                        item.setCheckState(Qt.CheckState.Checked)
                    else:
                        item.setCheckState(Qt.CheckState.Unchecked)
                
                self.range_input.clear()
            except (ValueError, IndexError):
                pass
            return
        
        # Handle single number
        try:
            num = int(text) - 1
            if 0 <= num < total:
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if i == num:
                        item.setCheckState(Qt.CheckState.Checked)
                    else:
                        item.setCheckState(Qt.CheckState.Unchecked)
                self.range_input.clear()
        except ValueError:
            pass
    
    def select_all(self):
        """Select all chapters."""
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(Qt.CheckState.Checked)
    
    def deselect_all(self):
        """Deselect all chapters."""
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(Qt.CheckState.Unchecked)
    
    def _on_item_changed(self, item: QListWidgetItem):
        """Handle item checkbox change."""
        self._update_selected_count()
    
    def _update_selected_count(self):
        """Update the selected count label."""
        count = self.get_selected_count()
        self.selected_label.setText(f"{count} selected")
        self.selection_changed.emit(count)
    
    def get_selected_count(self) -> int:
        """Get number of selected chapters."""
        count = 0
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).checkState() == Qt.CheckState.Checked:
                count += 1
        return count
    
    def get_selected_chapters(self) -> List[Chapter]:
        """Get list of selected Chapter objects."""
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                chapter = item.data(Qt.ItemDataRole.UserRole)
                selected.append(chapter)
        return selected
    
    def clear(self):
        """Clear the list."""
        self._chapters = []
        self._filtered_chapters = []
        self.list_widget.clear()
        self.group_filter.clear()
        self.count_label.setText("0 chapters")
        self.selected_label.setText("0 selected")
        self.range_input.clear()
