"""Interactive prompts for Weebdex Downloader CLI."""

import re
from typing import List, Optional, Tuple

from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console

from ..models import Chapter
from ..config import Config, DownloadFormat, save_config
from .display import console, show_settings


def prompt_main_menu() -> int:
    """
    Display main menu and get user selection.
    
    Returns:
        1 = Download Manga
        2 = Settings
        3 = Exit
    """
    console.print("\n[bold cyan]Main Menu[/bold cyan]")
    console.print("[1] Download Manga by URL")
    console.print("[2] Settings")
    console.print("[3] Exit")
    console.print()
    
    while True:
        choice = Prompt.ask(
            "[bold]Select option[/bold]",
            choices=["1", "2", "3"],
            default="1"
        )
        return int(choice)


def prompt_url() -> Optional[str]:
    """
    Prompt for manga URL.
    
    Returns:
        URL string or None if cancelled
    """
    console.print("\n[dim]Enter the weebdex.org manga URL (or 'back' to return)[/dim]")
    url = Prompt.ask("[bold]Manga URL[/bold]")
    
    if url.lower() in ("back", "b", "cancel", "c", ""):
        return None
    
    return url.strip()


def parse_chapter_selection(
    selection: str,
    total_chapters: int
) -> Tuple[List[int], Optional[str]]:
    """
    Parse chapter selection input.
    
    Supports:
    - Single: "5" → [5]
    - Range: "1-10" → [1,2,3,...,10]
    - All: "all" or "a" → [1,2,...,total]
    
    Args:
        selection: User input string
        total_chapters: Total number of available chapters
        
    Returns:
        Tuple of (list of 1-indexed chapter numbers, error message or None)
    """
    selection = selection.strip().lower()
    
    # Handle "all"
    if selection in ("all", "a"):
        return list(range(1, total_chapters + 1)), None
    
    # Handle range "X-Y"
    range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", selection)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        
        if start < 1 or end > total_chapters:
            return [], f"Invalid range. Valid: 1-{total_chapters}"
        if start > end:
            return [], "Start must be less than or equal to end"
        
        return list(range(start, end + 1)), None
    
    # Handle single number
    if selection.isdigit():
        num = int(selection)
        if num < 1 or num > total_chapters:
            return [], f"Invalid chapter. Valid: 1-{total_chapters}"
        return [num], None
    
    return [], "Invalid format. Use: single (5), range (1-10), or 'all'"


def prompt_chapter_selection(
    chapters: List[Chapter]
) -> Optional[List[Chapter]]:
    """
    Prompt for chapter selection.
    
    Args:
        chapters: List of available chapters
        
    Returns:
        List of selected Chapter objects or None if cancelled
    """
    total = len(chapters)
    
    console.print(f"\n[dim]Select chapters to download (1-{total})[/dim]")
    console.print("[dim]Examples: '5' (single), '1-10' (range), 'all' (all chapters)[/dim]")
    console.print("[dim]Enter 'back' to return to menu[/dim]")
    console.print()
    
    while True:
        selection = Prompt.ask("[bold]Chapter selection[/bold]")
        
        if selection.lower() in ("back", "b", "cancel", "c"):
            return None
        
        indices, error = parse_chapter_selection(selection, total)
        
        if error:
            console.print(f"[red]{error}[/red]")
            continue
        
        # Convert 1-indexed to actual chapters
        selected = [chapters[i - 1] for i in indices]
        
        # Confirm selection
        if len(selected) > 1:
            chapter_range = f"{selected[0].get_display_name()} to {selected[-1].get_display_name()}"
            console.print(f"[dim]Selected {len(selected)} chapters: {chapter_range}[/dim]")
        else:
            console.print(f"[dim]Selected: {selected[0].get_display_name()}[/dim]")
        
        if Confirm.ask("Proceed with download?", default=True):
            return selected
        
        console.print("[dim]Selection cancelled. Enter new selection.[/dim]")


def prompt_filter_choice() -> bool:
    """
    Ask if user wants to filter chapters.
    """
    return Confirm.ask("\nDo you want to filter these chapters (by language/group)?", default=False)


def prompt_language_filter(languages: List[str]) -> Optional[str]:
    """
    Prompt for language filter.
    """
    options = ["All"] + sorted([l.upper() for l in languages])
    console.print("\n[dim]Select language filter:[/dim]")
    for i, lang in enumerate(options):
        console.print(f"[{i}] {lang}")
    
    choice = IntPrompt.ask(
        "\n[bold]Select language[/bold]",
        choices=[str(i) for i in range(len(options))],
        default=0
    )
    
    if choice == 0:
        return None
    return options[choice].lower()


def prompt_group_filter(groups: List[str]) -> Optional[str]:
    """
    Prompt for group filter.
    """
    options = ["All"] + sorted(groups)
    console.print("\n[dim]Select scanlation group filter:[/dim]")
    for i, group in enumerate(options):
        console.print(f"[{i}] {group}")
    
    choice = IntPrompt.ask(
        "\n[bold]Select group[/bold]",
        choices=[str(i) for i in range(len(options))],
        default=0
    )
    
    if choice == 0:
        return None
    return options[choice]


def prompt_settings_menu(config: Config) -> Config:
    """
    Display settings menu and allow modifications.
    
    Args:
        config: Current configuration
        
    Returns:
        Updated configuration
    """
    while True:
        console.print("\n")
        show_settings(config)
        
        console.print("\n[bold cyan]Settings Menu[/bold cyan]")
        console.print("[1] Download Format (PDF/CBZ/Images)")
        console.print("[2] Keep Images After Conversion")
        console.print("[3] Concurrent Chapters")
        console.print("[4] Concurrent Images")
        console.print("[5] Max Chapters Display")
        console.print("[6] Enable Detailed Logs")
        console.print("[7] Download Path")
        console.print("[8] Back to Main Menu")
        console.print()
        
        choice = Prompt.ask(
            "[bold]Select option[/bold]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="8"
        )
        
        if choice == "1":
            # Download format
            console.print("\n[dim]Select download format:[/dim]")
            console.print("[1] Images (save as image files)")
            console.print("[2] PDF (combine into PDF)")
            console.print("[3] CBZ (comic book archive with metadata)")
            
            fmt_choice = Prompt.ask(
                "[bold]Format[/bold]",
                choices=["1", "2", "3"],
                default="1"
            )
            format_map = {"1": "images", "2": "pdf", "3": "cbz"}
            config.download_format = format_map[fmt_choice]
            save_config(config)
            console.print("[green]✓ Download format updated[/green]")
            
        elif choice == "2":
            # Keep images
            config.keep_images = Confirm.ask(
                "Keep images after PDF/CBZ conversion?",
                default=config.keep_images
            )
            save_config(config)
            console.print("[green]✓ Setting updated[/green]")
            
        elif choice == "3":
            # Concurrent chapters
            config.concurrent_chapters = IntPrompt.ask(
                "Concurrent chapter downloads (1-10)",
                default=config.concurrent_chapters
            )
            config.concurrent_chapters = max(1, min(10, config.concurrent_chapters))
            save_config(config)
            console.print("[green]✓ Concurrent chapters updated[/green]")
            
        elif choice == "4":
            # Concurrent images
            config.concurrent_images = IntPrompt.ask(
                "Concurrent image downloads (1-20)",
                default=config.concurrent_images
            )
            config.concurrent_images = max(1, min(20, config.concurrent_images))
            save_config(config)
            console.print("[green]✓ Concurrent images updated[/green]")
            
        elif choice == "5":
            # Max chapters display
            console.print("[dim]0 = Show all chapters[/dim]")
            config.max_chapters_display = IntPrompt.ask(
                "Max chapters to display",
                default=config.max_chapters_display
            )
            config.max_chapters_display = max(0, config.max_chapters_display)
            save_config(config)
            console.print("[green]✓ Display limit updated[/green]")
            
        elif choice == "6":
            # Enable logs
            config.enable_logs = Confirm.ask(
                "Enable detailed logging?",
                default=config.enable_logs
            )
            save_config(config)
            console.print("[green]✓ Logging setting updated[/green]")
            
        elif choice == "7":
            # Download path
            new_path = Prompt.ask(
                "Download path",
                default=config.download_path
            )
            config.download_path = new_path
            save_config(config)
            console.print("[green]✓ Download path updated[/green]")
            
        elif choice == "8":
            break
    
    return config
