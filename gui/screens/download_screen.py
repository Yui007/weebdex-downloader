"""Download screen with URL input, manga info, and chapter selection."""

from typing import Optional, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame, QMessageBox,
    QComboBox
)
from PyQt6.QtCore import Qt

from src.models import MangaInfo, Chapter
from src.config import get_config

from ..components.manga_card import MangaCard
from ..components.chapter_list import ChapterListWidget
from ..components.progress_widget import ProgressWidget
from ..workers.scraper_worker import ScraperWorker
from ..workers.download_worker import DownloadWorker


class DownloadScreen(QWidget):
    """Main download screen with URL input and chapter selection."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._manga_info: Optional[MangaInfo] = None
        self._chapters: List[Chapter] = []
        self._scraper_worker: Optional[ScraperWorker] = None
        self._download_worker: Optional[DownloadWorker] = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the screen layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Download Manga")
        header.setObjectName("title")
        layout.addWidget(header)
        
        subtitle = QLabel("Enter a weebdex.org manga URL to get started")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # URL input row
        url_row = QHBoxLayout()
        url_row.setSpacing(12)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://weebdex.org/title/...")
        self.url_input.returnPressed.connect(self._on_fetch_clicked)
        url_row.addWidget(self.url_input, 1)
        
        self.fetch_btn = QPushButton("Fetch")
        self.fetch_btn.setFixedWidth(100)
        self.fetch_btn.clicked.connect(self._on_fetch_clicked)
        url_row.addWidget(self.fetch_btn)
        
        layout.addLayout(url_row)
        
        # Filters row (hidden initially)
        self.filter_row = QHBoxLayout()
        self.filter_row.setSpacing(12)
        
        self.filter_label = QLabel("Filters:")
        self.filter_label.setObjectName("sectionTitle_small")
        self.filter_row.addWidget(self.filter_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.setPlaceholderText("Language")
        self.lang_combo.currentTextChanged.connect(self._apply_filters)
        self.filter_row.addWidget(self.lang_combo, 1)
        
        self.group_combo = QComboBox()
        self.group_combo.setPlaceholderText("Group")
        self.group_combo.currentTextChanged.connect(self._apply_filters)
        self.filter_row.addWidget(self.group_combo, 1)
        
        self.filter_row_widget = QWidget()
        self.filter_row_widget.setLayout(self.filter_row)
        self.filter_row_widget.hide()
        layout.addWidget(self.filter_row_widget)
        
        # Loading label (hidden by default)
        self.loading_label = QLabel("⏳ Fetching manga info...")
        self.loading_label.setStyleSheet("color: #fbbf24; font-size: 16px;")
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        
        # Manga card
        self.manga_card = MangaCard()
        self.manga_card.hide()
        self.content_layout.addWidget(self.manga_card)
        
        # Chapter list - give it stretch priority to expand
        self.chapter_list = ChapterListWidget()
        self.chapter_list.selection_changed.connect(self._on_selection_changed)
        self.chapter_list.hide()
        self.content_layout.addWidget(self.chapter_list, 1)  # stretch factor = 1
        
        # Download button row (below chapter list)
        self.download_row = QHBoxLayout()
        self.download_row.addStretch()
        
        self.download_btn = QPushButton("Download Selected")
        self.download_btn.setFixedWidth(200)
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self._on_download_clicked)
        self.download_row.addWidget(self.download_btn)
        
        self.download_row.addStretch()
        
        download_widget = QWidget()
        download_widget.setLayout(self.download_row)
        download_widget.hide()
        self.download_widget = download_widget
        self.content_layout.addWidget(download_widget)
        
        # Progress widget
        self.progress_widget = ProgressWidget()
        self.progress_widget.cancel_clicked.connect(self._on_cancel_clicked)
        self.content_layout.addWidget(self.progress_widget)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)
    
    def _on_fetch_clicked(self):
        """Handle fetch button click."""
        url = self.url_input.text().strip()
        if not url:
            return
        
        # Reset state
        self._reset_content()
        
        # Show loading
        self.loading_label.show()
        self.fetch_btn.setEnabled(False)
        self.fetch_btn.setText("Loading...")
        
        # Start worker
        self._scraper_worker = ScraperWorker(url)
        self._scraper_worker.finished.connect(self._on_fetch_finished)
        self._scraper_worker.error.connect(self._on_fetch_error)
        self._scraper_worker.start()
    
    def _on_fetch_finished(self, manga_info: MangaInfo, chapters: List[Chapter]):
        """Handle successful fetch."""
        self._manga_info = manga_info
        self._chapters = chapters
        
        # Update UI
        self.loading_label.hide()
        self.fetch_btn.setEnabled(True)
        self.fetch_btn.setText("Fetch")
        
        # Show manga info
        self.manga_card.set_manga(manga_info)
        self.manga_card.show()
        
        # Show chapters
        self.chapter_list.set_chapters(chapters)
        self.chapter_list.show()
        
        # Populate and show filters
        self._populate_filters(manga_info, chapters)
        self.filter_row_widget.show()
        
        # Show download button
        self.download_widget.show()
    
    def _populate_filters(self, manga_info: MangaInfo, chapters: List[Chapter]):
        """Populate filter dropdowns with available options."""
        # Block signals to avoid triggering _apply_filters while populating
        self.lang_combo.blockSignals(True)
        self.group_combo.blockSignals(True)
        
        self.lang_combo.clear()
        self.group_combo.clear()
        
        # Language combo
        self.lang_combo.addItem("All Languages")
        if manga_info.available_languages:
            for lang in sorted(manga_info.available_languages):
                self.lang_combo.addItem(lang.upper(), lang)
        
        # Group combo
        self.group_combo.addItem("All Groups")
        groups = set()
        for ch in chapters:
            for g in ch.groups:
                groups.add(g.name)
        
        for group_name in sorted(list(groups)):
            self.group_combo.addItem(group_name)
        
        self.lang_combo.blockSignals(False)
        self.group_combo.blockSignals(False)
    
    def _apply_filters(self):
        """Filter the chapter list based on dropdown selections."""
        if not self._chapters:
            return
            
        lang_idx = self.lang_combo.currentIndex()
        lang_filter = self.lang_combo.itemData(lang_idx) if lang_idx > 0 else None
        
        group_filter = self.group_combo.currentText()
        if group_filter == "All Groups":
            group_filter = None
            
        filtered = self._chapters
        
        if lang_filter:
            filtered = [ch for ch in filtered if ch.language == lang_filter]
            
        if group_filter:
            filtered = [
                ch for ch in filtered 
                if any(g.name == group_filter for g in ch.groups)
            ]
            
        self.chapter_list.set_chapters(filtered)
    
    def _on_fetch_error(self, message: str):
        """Handle fetch error."""
        self.loading_label.hide()
        self.fetch_btn.setEnabled(True)
        self.fetch_btn.setText("Fetch")
        
        QMessageBox.warning(self, "Error", message)
    
    def _on_selection_changed(self, count: int):
        """Handle chapter selection change."""
        self.download_btn.setEnabled(count > 0)
        self.download_btn.setText(f"Download ({count})" if count > 0 else "Download Selected")
    
    def _on_download_clicked(self):
        """Handle download button click."""
        selected = self.chapter_list.get_selected_chapters()
        if not selected or not self._manga_info:
            return
        
        # Disable controls
        self.download_btn.setEnabled(False)
        self.chapter_list.setEnabled(False)
        
        # Show progress
        self.progress_widget.reset()
        self.progress_widget.start(len(selected))
        
        # Start download worker
        config = get_config()
        self._download_worker = DownloadWorker(
            self._manga_info,
            selected,
            config
        )
        self._download_worker.progress.connect(self._on_download_progress)
        self._download_worker.finished.connect(self._on_download_finished)
        self._download_worker.error.connect(self._on_download_error)
        self._download_worker.start()
    
    def _on_download_progress(self, current: int, total: int, message: str):
        """Handle download progress update."""
        self.progress_widget.update_progress(current, total, message)
    
    def _on_download_finished(self, successful: int, failed: int):
        """Handle download completion."""
        self.progress_widget.finish(successful, failed)
        self._enable_controls()
    
    def _on_download_error(self, message: str):
        """Handle download error."""
        self.progress_widget.show_error(message)
        self._enable_controls()
    
    def _on_cancel_clicked(self):
        """Handle cancel button click."""
        if self._download_worker and self._download_worker.isRunning():
            self._download_worker.cancel()
    
    def _enable_controls(self):
        """Re-enable controls after download."""
        self.download_btn.setEnabled(True)
        self.chapter_list.setEnabled(True)
        self._on_selection_changed(self.chapter_list.get_selected_count())
    
    def _reset_content(self):
        """Reset the content area."""
        self._manga_info = None
        self._chapters = []
        self.manga_card.clear()
        self.manga_card.hide()
        self.chapter_list.clear()
        self.chapter_list.hide()
        self.download_widget.hide()
        self.filter_row_widget.hide()
        self.progress_widget.reset()
