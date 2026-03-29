"""
config.py — Central configuration for WUTS.
All paths, constants, and tunable parameters live here.
"""

import os

CONFIG = {
    # ── Paths ────────────────────────────────────────────────
    "SAVE_FOLDER":    r"C:\Users\mrtsh\Downloads\OneDrive - Botswana Accountancy College\Medicalss",
    "EXCEL_PATH":     r"C:\Users\mrtsh\Downloads\OneDrive - Botswana Accountancy College\PROTOTYPE\Medical_Examinations.xlsx",
    "HC_FOLDER":      r"C:\Users\mrtsh\Downloads\OneDrive - Botswana Accountancy College\Headcount",
    "CONFLICT_LOG":   r"C:\Users\mrtsh\Downloads\OneDrive - Botswana Accountancy College\PROTOTYPE\conflict_log.csv",

    # ── Email ────────────────────────────────────────────────
    "NOTIFY_EMAIL":   "bida23-114@thuto.bac.ac.bw",
    "NOTIFY_CC":      "",

    # ── Business Rules ───────────────────────────────────────
    "DAYS_WARNING":   30,
    "EXAM_INTERVALS": {
        "Executive":  365,
        "Top Brass":  365,
        "default":    730,
    },

    # ── Sheet Names ──────────────────────────────────────────
    "PERIODICS_SHEET": "DCC PERIODICS",
    "NEW_EMP_SHEET":   "New Employees",

    # ── Filename Noise Words (stripped when extracting name) ─
    "FILENAME_NOISE":  ["HHS", "form", "medical", "exam",
                        "examination", "report", "results"],

    # ── Email Time Window (hours) ────────────────────────────
    "EMAIL_HOURS": 24  ,
}
