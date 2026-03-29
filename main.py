"""
╔══════════════════════════════════════════════════════════════╗
║        Wellness Updating and Tracking System (WUTS)          ║
║                      main.py — CLI Entry                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
from datetime import datetime

# Ensure local modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from config         import CONFIG
from ui             import WUTSConsole
from modules.email_processor    import EmailProcessor
from modules.pdf_extractor      import PDFExtractor
from modules.excel_updater      import ExcelUpdater
from modules.headcount          import HeadcountReconciler
from modules.notifications      import NotificationService
from modules.conflict_logger    import ConflictLogger

# ──────────────────────────────────────────────────────────────
def run_process_emails(ui, outlook):
    ui.section("Process Inbox Emails")
    processor = EmailProcessor(
        outlook_app   = outlook,
        pdf_extractor = PDFExtractor(),
        excel_updater = ExcelUpdater(),
        reconciler    = HeadcountReconciler(),
        notifier      = NotificationService(outlook),
        ui            = ui
    )
    processor.run()

def run_headcount(ui, outlook):
    ui.section("Headcount Reconciliation")
    path = ui.prompt_path("Enter path to headcount file (.xlsx/.xls/.csv)")
    if not path:
        ui.warn("No path provided — returning to menu")
        return
    reconciler = HeadcountReconciler(ui=ui)
    new_c, exit_c = reconciler.reconcile(path)
    notifier = NotificationService(outlook, ui=ui)
    notifier.send_headcount_notification(new_c, exit_c, os.path.basename(path))

def run_send_booking_alerts(ui, outlook):
    ui.section("Send Booking Alerts")
    notifier = NotificationService(outlook, ui=ui)
    notifier.send_booking_notification()

def run_view_conflicts(ui):
    ui.section("View Conflict Log")
    logger = ConflictLogger(ui=ui)
    logger.display()

def run_manual_pdf(ui, outlook):
    ui.section("Manual PDF Processing")
    path = ui.prompt_path("Enter path to PDF file")
    if not path or not path.lower().endswith(".pdf"):
        ui.warn("Invalid path — returning to menu")
        return
    extractor = PDFExtractor(ui=ui)
    updater   = ExcelUpdater(ui=ui)
    data      = extractor.extract(path)
    updater.update(data)

def run_full_cycle(ui, outlook):
    ui.section("Full Cycle Run")
    ui.info("Running all steps: inbox → headcount → booking alerts")
    run_process_emails(ui, outlook)
    run_send_booking_alerts(ui, outlook)

# ──────────────────────────────────────────────────────────────
MENU_OPTIONS = [
    ("Process Inbox Emails",        run_process_emails,      True ),
    ("Headcount Reconciliation",    run_headcount,           True ),
    ("Send Booking Alerts",         run_send_booking_alerts, True ),
    ("Manual PDF Processing",       run_manual_pdf,          True),
    ("View Conflict Log",           run_view_conflicts,      False),
    ("Full Cycle Run",              run_full_cycle,          True ),
    ("Exit",                        None,                    False),
]

# ──────────────────────────────────────────────────────────────
def connect_outlook(ui):
    try:
        import win32com.client
        ui.info("Connecting to Outlook...")
        outlook   = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        time.sleep(2)
        ui.success("Outlook connected")
        return outlook, namespace
    except Exception as e:
        ui.warn(f"Could not connect to Outlook: {e}")
        ui.warn("Email-dependent features will be unavailable")
        return None, None

# ──────────────────────────────────────────────────────────────
def main():
    ui = WUTSConsole()
    ui.banner()

    outlook, _ = connect_outlook(ui)

    while True:
        ui.menu(MENU_OPTIONS)
        choice = ui.prompt_choice(len(MENU_OPTIONS))

        if choice is None:
            continue

        label, fn, needs_outlook = MENU_OPTIONS[choice]

        if fn is None:  # Exit
            ui.goodbye()
            break

        if needs_outlook and outlook is None:
            ui.warn(f"'{label}' requires an Outlook connection. "
                    "Please restart with Outlook open.")
            continue

        try:
            if needs_outlook:
                fn(ui, outlook)
            else:
                fn(ui)
        except KeyboardInterrupt:
            ui.warn("Operation cancelled — returning to menu")
        except Exception as e:
            ui.error(f"Unexpected error in '{label}': {e}")

        ui.pause()

if __name__ == "__main__":
    main()
