"""
ui.py — WUTS Console Interface
Handles all terminal rendering: banner, menus, prompts, status messages.
"""

import os
import sys
from datetime import datetime

# ── ANSI colour helpers ────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Palette
    TEAL    = "\033[38;5;38m"
    CYAN    = "\033[38;5;45m"
    WHITE   = "\033[97m"
    GREY    = "\033[38;5;245m"
    GREEN   = "\033[38;5;82m"
    YELLOW  = "\033[38;5;220m"
    RED     = "\033[38;5;196m"
    BLUE    = "\033[38;5;75m"
    MAGENTA = "\033[38;5;177m"

    BG_DARK = "\033[48;5;234m"
    BG_TEAL = "\033[48;5;23m"

def c(colour, text):
    return f"{colour}{text}{C.RESET}"

def width():
    try:
        return min(os.get_terminal_size().columns, 80)
    except Exception:
        return 72

# ──────────────────────────────────────────────────────────────
class WUTSConsole:

    def _line(self, char="─", colour=C.TEAL):
        print(c(colour, char * width()))

    def banner(self):
        w = width()
        os.system("cls" if os.name == "nt" else "clear")
        print()
        self._line("═", C.CYAN)
        print(c(C.BOLD + C.CYAN,
                "  ██╗    ██╗██╗   ██╗████████╗███████╗"))
        print(c(C.BOLD + C.CYAN,
                "  ██║    ██║██║   ██║╚══██╔══╝██╔════╝"))
        print(c(C.BOLD + C.TEAL,
                "  ██║ █╗ ██║██║   ██║   ██║   ███████╗"))
        print(c(C.BOLD + C.TEAL,
                "  ██║███╗██║██║   ██║   ██║   ╚════██║"))
        print(c(C.BOLD + C.WHITE,
                "  ╚███╔███╔╝╚██████╔╝   ██║   ███████║"))
        print(c(C.BOLD + C.WHITE,
                "   ╚══╝╚══╝  ╚═════╝    ╚═╝   ╚══════╝"))
        print()
        title = "Wellness Updating and Tracking System"
        pad   = (w - len(title)) // 2
        print(c(C.BOLD + C.WHITE, " " * pad + title))
        version_line = "v1.0  ·  Debswana Corprate Centre"
        pad2  = (w - len(version_line)) // 2
        print(c(C.GREY, " " * pad2 + version_line))
        self._line("═", C.CYAN)
        now = datetime.now().strftime("%A, %d %B %Y  %H:%M")
        print(c(C.DIM + C.GREY, f"  Session started: {now}"))
        print()

    def menu(self, options):
        self._line()
        print(c(C.BOLD + C.WHITE, "  MAIN MENU"))
        self._line()
        for i, (label, _, _) in enumerate(options):
            num    = c(C.BOLD + C.TEAL,  f"  [{i + 1}]")
            is_exit = label == "Exit"
            colour  = C.RED if is_exit else C.WHITE
            sep     = c(C.GREY, "  ·  ")
            icons   = {
                "Process Inbox Emails":     "📥",
                "Headcount Reconciliation": "📊",
                "Send Booking Alerts":      "🔔",
                "Manual PDF Processing":    "📄",
                "View Conflict Log":        "⚠️ ",
                "Full Cycle Run":           "🔄",
                "Exit":                     "🚪",
            }
            icon = icons.get(label, "  ")
            print(f"{num}{sep}{icon}  {c(colour, label)}")
        self._line()

    def prompt_choice(self, n):
        try:
            raw = input(c(C.BOLD + C.CYAN, "  → Select option: ")).strip()
            val = int(raw) - 1
            if 0 <= val < n:
                return val
            self.warn(f"Please enter a number between 1 and {n}")
            return None
        except (ValueError, EOFError):
            self.warn("Invalid input")
            return None

    def prompt_path(self, prompt_text):
        try:
            raw = input(c(C.CYAN, f"  → {prompt_text}: ")).strip()
            return raw if raw else None
        except EOFError:
            return None

    def section(self, title):
        print()
        self._line("─", C.TEAL)
        print(c(C.BOLD + C.CYAN, f"  ▶  {title.upper()}"))
        self._line("─", C.TEAL)

    def info(self, msg):
        print(c(C.BLUE,   f"  ℹ  {msg}"))

    def success(self, msg):
        print(c(C.GREEN,  f"  ✔  {msg}"))

    def warn(self, msg):
        print(c(C.YELLOW, f"  ⚠  {msg}"))

    def error(self, msg):
        print(c(C.RED,    f"  ✖  {msg}"))

    def result(self, label, value, colour=C.WHITE):
        print(f"  {c(C.GREY, label + ':')}  {c(colour, str(value))}")

    def table_row(self, cols, widths, colours=None):
        row = ""
        for i, (col, w) in enumerate(zip(cols, widths)):
            colour = colours[i] if colours else C.WHITE
            row += c(colour, str(col).ljust(w))
        print("  " + row)

    def pause(self):
        print()
        input(c(C.DIM + C.GREY, "  Press Enter to return to menu..."))
        os.system("cls" if os.name == "nt" else "clear")
        self.banner()

    def goodbye(self):
        print()
        self._line("═", C.CYAN)
        print(c(C.BOLD + C.TEAL,
                "  Thank you for using WUTS. Stay well. 💙"))
        self._line("═", C.CYAN)
        print()
