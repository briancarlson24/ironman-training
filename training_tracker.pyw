"""
Training tracker
================
PURPOSE
    A desktop window for tracking training toward the early-summer 2027
    marathon and a full Ironman (140.6) in fall 2027. It shows a grid with one column per day (the
    prior 6 days, today, and the next 7) and one row per item:
      - daily habits at the top (Meds, Water, Sleep 8hrs, Nutrition)
      - then one row per session type (Mobility, Strength A, Run/walk, ...)
      - then a Done row with each day's count
      - then a Notes row: click a day's pencil to write notes about it
    Tick a box when it's done; ticks and notes are saved to
    training_log.json next to this script. Click a cell's text, a row name, or a date to open a
    small details window. The bottom section always lists the Mobility,
    Strength A and Strength B exercises.

    The plan itself lives in a Markdown file (SCHEDULE_FILE below): the
    14-day cycle, progression, notes, daily habits, session details, how
    many days to show, and which sessions to pin at the bottom. Edit that
    file, then click Reload. Nothing about the plan is hard-coded here;
    this script only reads the file and draws it.

RUN
    Double-click the file (.pyw files run with no console window), or:
    C:\\Users\\brian\\AppData\\Local\\Programs\\Python\\Python310\\pythonw.exe
        "C:\\Users\\brian\\.claude\\Ironman Training\\training_tracker.pyw"

FILES
    training_tracker.pyw   this script
    training_log.json      your ticks, as a list of check records (see v19
                           and v20), and your notes, {"date": text}.
                           Created on the first tick. A damaged file is
                           renamed to training_log.damaged.json, not deleted.
    training_log.v1.json   copies of older-format logs, made once each when
    training_log.v2.json   they are converted to the current format.
    C:\\Users\\brian\\.claude\\profile\\fitness-training.md   the schedule

CHANGE LOG (all 2026-11-21)
    v1  First version, in D:\\DataEngineerTraining\\ironman.
        - Vertical list of day cards (7 days back, 28 ahead), a checkbox
          per session, exercise details in a right-hand panel.
        - Plan hard-coded in the script: 14-day cycle anchored on Mon
          2026-11-23, +5 min bike / +0.5 mi long run per cycle, every 3rd
          cycle at 70%, Wednesday swims from 2027-01-01.
        - Ticks saved to training_log.json (temp file + swap, so a crash
          can't corrupt it). Today button.
    v2  Plan moved out of the code into fitness-training.md, which the
        script reads and checks (clear error message naming the row to
        fix; the last good schedule stays on screen).
        - Added Open schedule and Reload buttons.
    v3  Moved to C:\\Users\\brian\\.claude\\Ironman Training.
    v4  Renamed .py -> .pyw so a double-click runs it with no black
        console window (Windows opens .pyw files with pyw.exe).
    v5  Pivoted to a grid: days across the top, one row per session type,
        frozen row-name column, Where row, Done row.
        - Added daily habit rows (Meds, Water, Sleep 8hrs), defined in the
          schedule file's Daily habits table.
        - Done cells turn green; today's column is highlighted.
        - Details panel moved below the grid.
        - Summary counts training and habits separately.
    v6  Narrower columns (amounts shortened to '45m' / '5mi').
        - Window shows 6 days back, today, 7 ahead ('Days back' / 'Days
          ahead' settings) and sizes itself to fit.
        - Strength A and B exercise lists always shown at the bottom
          ('Pinned details' setting); flex rules in the third column.
    v7  Removed the horizontal scrollbar (the mouse wheel still scrolls if
        the grid is ever wider than the window).
        - Removed the Where row (location still shows when you click a date).
        - Habit rows moved to the top of the grid.
        - Bottom section lists only the exercises, without the tips (the
          full text still shows when you click a Strength cell).
        - This full change log.
    v8  Habit checkboxes (Meds, Water, Sleep 8hrs) centered in their cells.
    v9  Schedule-file changes only (no code changes): Wednesday PM swims
        start now instead of January, and a Nutrition habit row after
        Sleep 8hrs.
    v10 Schedule-file change only: Stretch 1 and Stretch 2 combined into
        one 'Stretch' row (lower body Fridays, full body Sundays).
    v11 Bottom section is now Mobility | Strength A | Strength B (Mobility
        added to 'Pinned details'); the Flex rules column is gone (the
        rules are still in the schedule file).
        - Clicked details open in a small popup window by the mouse
          instead of the old third column. Escape or Close shuts it.
        - Bottom lists keep headings like 'STRETCH (30-45 sec each)'.
    v12 The Schedule and Log paths in the footer are clickable links.
        Warnings show after them.
        - Links and the Open schedule button open files in VS Code
          (Code.exe, so no console flash). Windows has no default app for
          .md/.json on this PC, so the old Open schedule button failed.
    v13 Schedule-file changes only: Strength A swaps step-ups for lateral
        lunges and single-leg calf raises for floor calf raises; weighted
        sit-ups at 60 lb. Strength B drops the bent-over reverse fly.
        Mobility's external rotation line joined onto one line.
    v14 Code review and simplification. Same look and behavior, except as
        noted. Code lines 557 -> 516; the bigger win is structure (fewer
        moving parts, no row-alignment workaround, named fields). The v13
        version is saved as training_tracker.v13.bak.
        - Fix: 'today' now rolls over at midnight if the window stays open
          (before, it kept highlighting yesterday until you clicked Reload).
        - Fix: a log file that is valid JSON but the wrong shape no longer
          crashes the app on startup; it's set aside like a damaged file.
        - Removed the sideways-scrolling machinery (Canvas, frozen name
          column, mouse-wheel binding, Today button). Since v7 the window
          sizes itself to fit every day, so it never scrolled. Row names
          and day cells now share one grid, which removes the code that
          kept two grids' rows lined up.
        - The schedule is a Schedule dataclass and each day a Day
          named tuple, so code reads sched.habits / day.tasks instead of
          sched["habits"] / self.days[d][1].
        - Grid drawn row type by row type (header, habits, sessions, Done)
          instead of one function branching on a 'kind' for every cell.
        - Removed unused code: the flex-rules text (no longer shown) and
          the WEEKDAYS list (strftime gives the weekday name).
    v15 Notes row under Done: a pencil per day opens a text box for notes
        about that day (Save or Ctrl+Enter; saving it empty deletes the
        note). Blue pencil = the day has a note. Notes are saved in
        training_log.json under "notes" (older logs without it still load)
        and also show when you click a date.
    v16 Hovering over a day's pencil shows its note in a small tooltip;
        moving the mouse away hides it. Days without a note show nothing.
    v17 Fix for two monitors: the note tooltip and the popups now open at
        the mouse pointer. Before, their position was capped to the main
        monitor's width, which pulled them onto the other screen when the
        tracker was on the second monitor. The tooltip also follows the
        mouse while it's over the pencil.
    v18 Hovering over a session cell's text ('5mi', 'AM', '30m') shows that
        session's details in the same tooltip at the mouse; clicking still
        opens the bigger popup. One shared hoverable() helper now drives
        both the note and session tooltips.
    v19 Check history (2026-11-21). The log keeps a record of every check
        instead of only the current state. Each record has:
            id            a random unique ID (uuid4)
            task          'date|session', e.g. '2026-11-21|meds'
            user          the Windows login name of whoever clicked
            checked_at    when the box was ticked (local time, to the second)
            unchecked_at  when it was unticked; null while still ticked
        Ticking adds a new record; unticking fills in unchecked_at on the
        open one; ticking again adds another new record. A box shows as
        ticked when its task has an open record (like an SCD2 table's
        current row, where end_date IS NULL).
        - Logs in the old format ("done": {task: time}) are converted on
          load: each tick becomes an open record with its original time and
          the current user. The old file is first copied to
          training_log.v1.json.
    v20 Check records are easier to report on (log file version 3).
        - 'task' ('2026-11-21|meds') is split into two fields: planned_date
          (the day the activity was planned for, i.e. the grid column) and
          item (the habit or session key). No more splitting a combined key.
        - Fields are saved in a fixed order instead of alphabetically:
              id, planned_date, item, user, checked_at, unchecked_at
        - Version 2 logs (with 'task') are converted on load; the old file
          is first copied to training_log.v2.json.
        - Fix: a converted log is saved as soon as the app opens. Before,
          the conversion stayed in memory until the next tick or note.
"""

import getpass
import json
import os
import re
import shutil
import subprocess
import tkinter as tk
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).parent
LOG_FILE = HERE / "training_log.json"
LOG_VERSION = 3
# Field order for each check record, as written to the file.
CHECK_FIELDS = ("id", "planned_date", "item", "user", "checked_at", "unchecked_at")
SCHEDULE_FILE = Path.home() / ".claude" / "profile" / "fitness-training.md"
CYCLE_DAYS = 14


def find_vscode():
    """Path to Code.exe, found from the 'code' command on the PATH
    (...\\Microsoft VS Code\\bin\\code.cmd -> ...\\Microsoft VS Code\\Code.exe).
    Code.exe is used rather than code.cmd because a .cmd file flashes a
    console window. Returns None if VS Code isn't found."""
    cmd = shutil.which("code")
    exe = Path(cmd).parent.parent / "Code.exe" if cmd else None
    return exe if exe and exe.exists() else None


VSCODE = find_vscode()

# Colors: same dark palette as the stargazing widget.
BG, CARD, FG, DIM = "#10172a", "#1e293b", "#e2e8f0", "#94a3b8"
GOOD, ACCENT, WARN = "#4ade80", "#60a5fa", "#facc15"
TODAY_BG, DONE_BG, HOVER = "#1e3a5f", "#14532d", "#334155"
FONT = "Segoe UI"

# Grid sizes in pixels.
COL_W, LABEL_W, ROW_H, HEAD_H, SEP_H = 54, 120, 28, 40, 10
DETAIL_WRAP = 280  # text width of each column in the bottom section


# --- Reading the schedule file -----------------------------------------------
class ScheduleError(Exception):
    """Something in the Markdown file isn't in the expected shape."""


@dataclass
class Schedule:
    anchor: date          # Cycle day 1
    days_back: int
    days_ahead: int
    light_every: int      # every Nth cycle is lighter...
    light_scale: float    # ...at this fraction of normal volume
    cycle: list           # 14 lists of rows: {where, slot, key, task, starts}
    progression: dict     # {session key: (per cycle, cap or None, round to)}
    notes: list           # [(from date, to date, text)]
    habits: list          # [(key, name, details)]
    sessions: dict        # {session key: (title, details text)}, in file order
    pinned: list          # session keys listed at the bottom of the window


def split_sections(text):
    """{'Settings': [lines...], ...}, keyed by each '## ' heading.
    '### ' sub-headings stay inside their parent section."""
    sections, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def read_table(sections, name, columns):
    """Turn the Markdown table in one section into a list of dicts,
    one per row, keyed by column name, like rows from a SELECT."""
    if name not in sections:
        raise ScheduleError(f"Missing section '## {name}'.")
    lines = [l.strip() for l in sections[name] if l.strip().startswith("|")]
    if not lines:
        raise ScheduleError(f"No table found under '## {name}'.")
    split = lambda l: [c.strip() for c in l.strip("|").split("|")]
    header = split(lines[0])
    missing = [c for c in columns if c not in header]
    if missing:
        raise ScheduleError(f"Table '{name}' is missing column(s): {', '.join(missing)}.")
    rows = []
    for line in lines[1:]:
        cells = split(line)
        if all(re.fullmatch(r":?-+:?", c) for c in cells):  # the |---|---| line
            continue
        cells += [""] * (len(header) - len(cells))          # pad short rows
        rows.append(dict(zip(header, cells)))
    return rows


def read_sessions(lines):
    """Parse '### key', then '**Title**', then a ``` code block, for each
    session. Returns them in file order, which is also the grid's row order."""
    sessions, key, title, body, in_block = {}, None, "", [], False
    for line in lines:
        if line.startswith("```"):
            if in_block and key:
                sessions[key] = (title or key, "\n".join(body).rstrip())
            in_block, body = not in_block, []
        elif in_block:
            body.append(line)
        elif line.startswith("### "):
            key, title = line[4:].strip(), ""
        elif line.startswith("**") and key:
            title = line.strip().strip("*")
    return sessions


def to_date(text, where):
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise ScheduleError(f"{where}: '{text}' is not a date like 2026-11-23.")


def to_number(text, where):
    try:
        return float(text.rstrip("%"))
    except ValueError:
        raise ScheduleError(f"{where}: '{text}' is not a number.")


def load_schedule(path=SCHEDULE_FILE):
    """Read and check the whole schedule file. Raises ScheduleError with a
    message that says which part of the file to fix."""
    if not path.exists():
        raise ScheduleError(f"Schedule file not found: {path}")
    sections = split_sections(path.read_text(encoding="utf-8"))

    settings = {r["Setting"]: r["Value"]
                for r in read_table(sections, "Settings", ["Setting", "Value"])}
    try:
        anchor = to_date(settings["Cycle day 1"], "Settings")
        days_back, days_ahead, light_every = (
            int(to_number(settings[name], "Settings"))
            for name in ("Days back", "Days ahead", "Light cycle every"))
        light_scale = to_number(settings["Light cycle volume"], "Settings") / 100
    except KeyError as missing:
        raise ScheduleError(f"Settings table is missing the {missing} row.")

    sessions = read_sessions(sections.get("Session details", []))

    def check_session(key, where):
        if key not in sessions:
            raise ScheduleError(f"{where}: no '### {key}' section under Session details.")

    pinned = [k.strip() for k in settings.get("Pinned details", "").split(",") if k.strip()]
    for key in pinned:
        check_session(key, "Settings, Pinned details")

    # The 14-day cycle: one list of rows per day, like GROUP BY Day.
    cycle = [[] for _ in range(CYCLE_DAYS)]
    cols = ["Day", "Weekday", "Where", "Slot", "Session", "Task", "Starts"]
    for n, r in enumerate(read_table(sections, "14-day cycle", cols), start=1):
        where = f"14-day cycle, row {n}"
        day = int(to_number(r["Day"], where))
        if not 1 <= day <= CYCLE_DAYS:
            raise ScheduleError(f"{where}: Day must be 1-{CYCLE_DAYS}, not {day}.")
        expected = (anchor + timedelta(days=day - 1)).strftime("%a")
        if r["Weekday"] != expected:
            raise ScheduleError(f"{where}: Day {day} is a {expected} "
                                f"(counting from Cycle day 1), not {r['Weekday']}.")
        check_session(r["Session"], where)
        if any(t["key"] == r["Session"] for t in cycle[day - 1]):
            raise ScheduleError(f"{where}: Day {day} already has a "
                                f"'{r['Session']}' session (one per day).")
        cycle[day - 1].append({
            "where": r["Where"], "slot": r["Slot"], "key": r["Session"], "task": r["Task"],
            "starts": to_date(r["Starts"], where) if r["Starts"] else None,
        })

    progression = {}
    for r in read_table(sections, "Progression", ["Session", "Per cycle", "Cap", "Round to"]):
        where = f"Progression, '{r['Session']}'"
        progression[r["Session"]] = (
            to_number(r["Per cycle"] or "0", where),
            to_number(r["Cap"], where) if r["Cap"] else None,
            to_number(r["Round to"] or "1", where),
        )

    notes = [(to_date(r["From"], "Notes"), to_date(r["To"], "Notes"), r["Note"])
             for r in read_table(sections, "Notes", ["From", "To", "Note"])]

    habits = []  # optional section
    if "Daily habits" in sections:
        for r in read_table(sections, "Daily habits", ["Habit", "Key", "Details"]):
            key = r["Key"]
            if not key or key in sessions or key in [h[0] for h in habits]:
                raise ScheduleError(f"Daily habits: key '{key}' is blank or used twice.")
            habits.append((key, r["Habit"], r["Details"]))

    return Schedule(anchor, days_back, days_ahead, light_every, light_scale,
                    cycle, progression, notes, habits, sessions, pinned)


# --- Turning the schedule into one day's plan --------------------------------
class Day(NamedTuple):
    location: str
    tasks: dict    # {session key: (slot, label)}
    notes: list    # note texts for this date
    cycle_day: int  # 0-13


def tasks_for(sched, d):
    """Work out one date's plan.

    divmod rounds down for negative numbers too, so dates before Cycle day 1
    land in cycle -1, -2, ... with the right day of the cycle. Earlier
    cycles use the starting numbers.
    """
    cycle, cycle_day = divmod((d - sched.anchor).days, CYCLE_DAYS)
    p = max(cycle, 0)
    light = p > 0 and (p + 1) % sched.light_every == 0
    scale = sched.light_scale if light else 1.0

    def grow(number, rule):
        """'{30}' in a task -> this cycle's number: add, cap, scale, round."""
        per_cycle, cap, step = rule
        value = number + per_cycle * p
        if cap is not None:
            value = min(value, cap)
        return f"{round(value * scale / step) * step:g}"

    rows = sched.cycle[cycle_day]
    tasks = {}
    for r in rows:
        if r["starts"] is None or d >= r["starts"]:
            rule = sched.progression.get(r["key"], (0, None, 1))
            label = re.sub(r"\{([\d.]+)\}", lambda m: grow(float(m.group(1)), rule), r["task"])
            tasks[r["key"]] = (r["slot"], label)

    notes = [text for start, end, text in sched.notes if start <= d <= end]
    if light:
        notes.append(f"Lighter week: about {sched.light_scale:.0%} volume.")
    return Day(rows[0]["where"] if rows else "", tasks, notes, cycle_day)


def short_title(title):
    """'Indoor bike (easy)' -> 'Indoor bike';  'Strength A: lower...' -> 'Strength A'"""
    return title.split(":")[0].split(" (")[0].strip()


def cell_text(slot, label):
    """What fits in a narrow grid cell: the amount if there is one
    ('30m' for minutes, '5mi' for miles), otherwise the time of day ('AM'/'PM')."""
    m = re.search(r"(\d+(?:\.\d+)?)[ -](min|mi)", label)
    if not m:
        return slot
    return m.group(1) + ("m" if m.group(2) == "min" else "mi")


def exercises_only(text):
    """Keep list lines ('- Goblet squat...', '1. Wall calf stretch'), their
    wrapped continuation lines, and ALL-CAPS headings; drop the tips."""
    def is_heading(line):
        """'ANKLES' or 'STRETCH (30-45 sec each)': all caps before any '('."""
        head = line.split("(")[0].strip()
        return any(c.isalpha() for c in head) and head == head.upper()

    keep, in_item = [], False
    for line in text.splitlines():
        if re.match(r"\s*(-|\d+\.)\s", line):     # a list item
            keep.append(line)
            in_item = True
        elif in_item and line.startswith("    ") and line.strip():
            keep.append(line)                      # the item wraps onto this line
        else:
            in_item = False
            if is_heading(line):
                keep.append(line)
    return "\n".join(keep)


def task_id(d, key):
    """Stable ID for the log file, e.g. '2026-11-23|mobility'."""
    return f"{d.isoformat()}|{key}"


# --- Saving and loading ticks ------------------------------------------------
def now():
    """Local time to the second, e.g. '2026-11-21T13:11:05'."""
    return datetime.now().isoformat(timespec="seconds")


def current_user():
    """The Windows login name, e.g. 'brian'."""
    try:
        return getpass.getuser()
    except Exception:  # no login name in the environment (rare)
        return "unknown"


def new_check(tid, checked_at=None, user=None, check_id=None, unchecked_at=None):
    """One check record, with its fields in CHECK_FIELDS order. By default:
    a new ID, the current user, ticked now, not yet unticked."""
    planned_date, item = tid.split("|", 1)
    return {"id": check_id or str(uuid.uuid4()),
            "planned_date": planned_date,
            "item": item,
            "user": user or current_user(),
            "checked_at": checked_at or now(),
            "unchecked_at": unchecked_at}


def check_task(c):
    """A record's task ID ('2026-11-21|meds'), used to match it to a grid cell."""
    return f"{c['planned_date']}|{c['item']}"


def backup_file(version):
    """Where an older-format log is copied before conversion, e.g. training_log.v1.json."""
    return LOG_FILE.with_name(f"training_log.v{version}.json")


def load_log():
    """Return ([check records], {date: note text}, warning).
    Missing file = nothing done yet. Older logs without notes are fine.
    Older formats are converted to check records, after copying the file:
        v1  "done": {task: time ticked}
        v2  "checks" with a combined 'task' field"""
    if not LOG_FILE.exists():
        return [], {}, ""
    try:
        data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        notes = data.get("notes", {})
        if "checks" not in data:
            # v1: make each tick a record. Like an INSERT ... SELECT from the
            # old table into the new one.
            done = data["done"]
            if not isinstance(done, dict):
                raise TypeError
            old_version = 1
            checks = [new_check(tid, ticked) for tid, ticked in sorted(done.items())]
        else:
            rows = data["checks"]
            if not (isinstance(rows, list) and all(isinstance(c, dict) for c in rows)):
                raise TypeError
            old_version = 2 if any("task" in c for c in rows) else None
            # Rebuild every record so its fields are in CHECK_FIELDS order.
            # v2 rows have 'task'; v3 rows already have planned_date and item.
            checks = [new_check(c["task"] if "task" in c else check_task(c),
                                checked_at=c["checked_at"], user=c.get("user"),
                                check_id=c.get("id"), unchecked_at=c["unchecked_at"])
                      for c in rows]
        if not isinstance(notes, dict):
            raise TypeError
        if old_version:
            if not backup_file(old_version).exists():
                shutil.copy2(LOG_FILE, backup_file(old_version))  # once per old version
            # Write the converted log now, so the file is in the current
            # format as soon as the app opens (not only after the next tick).
            save_log(checks, notes)
        return checks, notes, ""
    except (ValueError, KeyError, TypeError, AttributeError):
        # Don't silently lose a damaged file: set it aside and start fresh.
        backup = LOG_FILE.with_suffix(".damaged.json")
        LOG_FILE.replace(backup)
        return [], {}, f"Log file was unreadable; moved to {backup.name}."


def save_log(checks, notes):
    """Write to a temp file first, then swap it in, so a crash mid-save
    can't leave a half-written log behind. Keys are written in the order
    they were built (CHECK_FIELDS for records), not alphabetically."""
    tmp = LOG_FILE.with_suffix(".tmp")
    data = {"version": LOG_VERSION, "checks": checks, "notes": dict(sorted(notes.items()))}
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(LOG_FILE)


# --- The window --------------------------------------------------------------
class TrainingTracker:
    def __init__(self, root):
        self.root = root
        self.checks, self.notes, warning = load_log()
        # Tasks ticked right now: those with an open record (unchecked_at is
        # null). Kept as a set so the grid and counts can look them up fast.
        self.ticked = {check_task(c) for c in self.checks if c["unchecked_at"] is None}
        self.sched = None
        self.popup = None  # the details window, while one is open
        self.tip = None    # the hover tooltip for a note, while one is showing

        root.title("Training tracker")
        root.configure(bg=BG, padx=14, pady=12)

        # Header: title, plus buttons on the right.
        top = tk.Frame(root, bg=BG)
        top.pack(fill="x")
        tk.Label(top, text="Training tracker", font=(FONT, 13, "bold"),
                 bg=BG, fg=FG).pack(side="left")
        for text, command in [("Reload", self.reload),
                              ("Open schedule", lambda: self.open_file(SCHEDULE_FILE))]:
            self.button(top, text, command, CARD).pack(side="right", padx=(6, 0))
        self.summary = tk.Label(root, font=(FONT, 10), bg=BG, fg=FG, anchor="w")
        self.summary.pack(fill="x", pady=(2, 8))

        # The grid: column 0 = row names, columns 1.. = days.
        self.table = tk.Frame(root, bg=BG)
        self.table.pack(anchor="w")

        # Below: the pinned sessions' exercise lists (Mobility, Strength A, ...).
        self.pinned_frame = tk.Frame(root, bg=CARD, padx=12, pady=10)
        self.pinned_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Footer: clickable links to the two files, then any warning message.
        footer = tk.Frame(root, bg=BG)
        footer.pack(fill="x", pady=(8, 0))
        for caption, path in [("Schedule:", SCHEDULE_FILE), ("Log:", LOG_FILE)]:
            tk.Label(footer, text=caption, font=(FONT, 8), bg=BG,
                     fg=DIM).pack(side="left", padx=(0, 3))
            link = tk.Label(footer, text=str(path), font=(FONT, 8, "underline"),
                            bg=BG, fg=ACCENT, cursor="hand2")
            link.bind("<Button-1>", lambda e, p=path: self.open_file(p))
            link.pack(side="left", padx=(0, 16))
        self.status = tk.Label(footer, font=(FONT, 8), bg=BG, fg=DIM, anchor="w")
        self.status.pack(side="left", fill="x")

        self.reload()
        if warning:
            self.set_status(warning, warn=True)
        self.watch_date()

    # --- Small widget helpers ----------------------------------------------------
    def button(self, parent, text, command, bg):
        return tk.Button(parent, text=text, command=command, font=(FONT, 8),
                         relief="flat", bg=bg, fg=FG, activebackground=HOVER,
                         activeforeground=FG)

    def put(self, widget, row, col):
        """Place a widget in the grid. The 1-pixel gap shows as grid lines."""
        widget.grid(row=row, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))
        return widget

    def clickable(self, widget, on_click):
        widget.config(cursor="hand2")
        widget.bind("<Button-1>", lambda e: on_click())
        return widget

    def detail_column(self, parent, wrap=DETAIL_WRAP):
        """A bold title plus a block of wrapped text."""
        labels = [tk.Label(parent, font=(FONT, size, weight), bg=CARD, fg=FG,
                           anchor="nw", justify="left", wraplength=wrap)
                  for size, weight in [(10, "bold"), (9, "normal")]]
        labels[0].pack(fill="x")
        labels[1].pack(fill="both", expand=True, pady=(4, 0))
        return labels

    def column_bg(self, d):
        return TODAY_BG if d == self.today else CARD

    # --- Loading and drawing -----------------------------------------------------
    def reload(self):
        """(Re)read the schedule file and redraw everything."""
        try:
            sched = load_schedule()
        except ScheduleError as err:
            # Keep showing the last good schedule (if any) and say what's wrong.
            self.set_status(f"Schedule problem: {err}  (fix the file, then Reload)",
                            warn=True)
            if self.sched is None:
                self.show_message("Couldn't read the schedule",
                                  f"{err}\n\nFile:\n{SCHEDULE_FILE}")
            return
        self.sched = sched
        self.today = date.today()
        first = self.today - timedelta(days=sched.days_back)
        dates = [first + timedelta(days=i)
                 for i in range(sched.days_back + sched.days_ahead + 1)]
        self.days = {d: tasks_for(sched, d) for d in dates}  # each day's plan, once
        self.draw_grid()
        self.draw_pinned()
        self.update_summary()
        self.set_status("")  # clear any old warning

    def watch_date(self):
        """Once a minute: if the date has changed (the window was left open
        past midnight), redraw so 'today' moves to the new day."""
        if self.sched is not None and date.today() != self.today:
            self.reload()
        self.root.after(60_000, self.watch_date)

    def draw_grid(self):
        self.hide_tip()  # its icon is about to be redrawn
        for widget in self.table.winfo_children():
            widget.destroy()
        self.table.columnconfigure(0, minsize=LABEL_W)
        for c in range(1, len(self.days) + 1):
            self.table.columnconfigure(c, minsize=COL_W)

        def row_name(row, text, on_click=None, bold=True):
            label = tk.Label(self.table, text=text, bg=BG, anchor="w",
                             fg=FG if bold else DIM,
                             font=(FONT, 9, "bold" if bold else "normal"))
            label.grid(row=row, column=0, sticky="nsew")
            if on_click:
                self.clickable(label, on_click)

        # Only session types that appear in the dates shown, in file order.
        used = {key for day in self.days.values() for key in day.tasks}
        session_keys = [k for k in self.sched.sessions if k in used]
        habits = self.sched.habits
        habit_rows = range(1, 1 + len(habits))
        sep_row = 1 + len(habits)  # an empty, short row between the two groups
        session_rows = range(sep_row + 1, sep_row + 1 + len(session_keys))
        done_row = sep_row + 1 + len(session_keys)
        notes_row = done_row + 1

        self.table.rowconfigure(0, minsize=HEAD_H)
        self.table.rowconfigure(sep_row, minsize=SEP_H)
        for r in [*habit_rows, *session_rows, done_row, notes_row]:
            self.table.rowconfigure(r, minsize=ROW_H)

        for r, (key, name, details) in zip(habit_rows, habits):
            row_name(r, name, lambda n=name, t=details: self.show_message(n, t))
        for r, key in zip(session_rows, session_keys):
            row_name(r, short_title(self.sched.sessions[key][0]),
                     lambda k=key: self.show_session(k))
        row_name(done_row, "Done", bold=False)
        row_name(notes_row, "Notes", bold=False)

        self.done_labels = {}  # {date: label in the Done row}
        self.note_icons = {}   # {date: pencil icon in the Notes row}
        for c, (d, day) in enumerate(self.days.items(), start=1):
            bg = self.column_bg(d)
            # Header: weekday and date; '•' if the day has notes.
            text = d.strftime("%a\n%b %d").replace(" 0", " ") + (" •" if day.notes else "")
            fg = ACCENT if d == self.today else (DIM if d < self.today else FG)
            self.clickable(self.put(tk.Label(self.table, text=text, bg=bg, fg=fg,
                                             font=(FONT, 8, "bold")), 0, c),
                           lambda d=d: self.show_day(d))
            for r, (key, name, details) in zip(habit_rows, habits):
                self.checkbox_cell(r, c, d, key)
            for r, key in zip(session_rows, session_keys):
                if key in day.tasks:
                    self.checkbox_cell(r, c, d, key, cell_text(*day.tasks[key]))
                else:
                    self.put(tk.Frame(self.table, bg=bg), r, c)  # nothing planned
            self.done_labels[d] = self.put(
                tk.Label(self.table, bg=bg, font=(FONT, 9, "bold")), done_row, c)
            self.update_count(d)
            icon = self.note_icons[d] = self.clickable(self.put(
                tk.Label(self.table, text="✎", bg=bg, font=(FONT, 12)), notes_row, c),
                lambda d=d: self.edit_note(d))
            self.hoverable(icon, lambda d=d: ("", self.notes.get(d.isoformat())))
            self.update_note_icon(d)

    def checkbox_cell(self, row, col, d, key, text=""):
        """One tickable cell. Habit cells: just a centered checkbox. Session
        cells: a checkbox plus short text ('30m') that shows the session's
        details on hover and opens them in a popup on click."""
        tid = task_id(d, key)
        var = tk.BooleanVar(value=tid in self.ticked)
        cell = self.put(tk.Frame(self.table), row, col)
        box = tk.Checkbutton(cell, variable=var, selectcolor=BG,
                             highlightthickness=0, bd=0, fg=GOOD)
        widgets = [cell, box]
        if text:
            box.pack(side="left", padx=(1, 0))
            label = self.clickable(tk.Label(cell, text=text, font=(FONT, 8)),
                                   lambda: self.show_message(*self.session_details(key, d)))
            self.hoverable(label, lambda: self.session_details(key, d))
            label.pack(side="left")
            widgets.append(label)
        else:
            box.pack(expand=True)

        def paint():
            """Ticked cells turn green; otherwise the column's normal color."""
            bg = DONE_BG if var.get() else self.column_bg(d)
            for w in widgets:
                w.config(bg=bg)
            box.config(activebackground=bg)
            if text:
                widgets[2].config(fg=GOOD if var.get() else FG)

        def on_toggle():
            self.toggle(d, tid, var.get())
            paint()

        box.config(command=on_toggle)
        paint()

    def draw_pinned(self):
        """Always-visible exercise lists for the 'Pinned details' sessions."""
        for widget in self.pinned_frame.winfo_children():
            widget.destroy()
        for key in self.sched.pinned:
            column = tk.Frame(self.pinned_frame, bg=CARD)
            column.pack(side="left", fill="y", padx=(0, 20))
            title, text = self.detail_column(column)
            session_title, body = self.sched.sessions[key]
            title.config(text=session_title)
            text.config(text=exercises_only(body))

    # --- Ticks and counts --------------------------------------------------------
    def toggle(self, d, tid, is_done):
        """Ticking adds a new check record. Unticking closes the open one by
        filling in unchecked_at; the record itself is kept as history."""
        if is_done:
            if tid not in self.ticked:
                self.checks.append(new_check(tid))
                self.ticked.add(tid)
        else:
            stamp = now()
            # Close every open record for this task. Normally there's only
            # one, but this also tidies up a hand-edited file with two.
            for c in self.checks:
                if check_task(c) == tid and c["unchecked_at"] is None:
                    c["unchecked_at"] = stamp
            self.ticked.discard(tid)
        self.save()
        self.update_count(d)
        self.update_summary()

    def save(self):
        try:
            save_log(self.checks, self.notes)
        except OSError as err:
            self.set_status(f"Could not save: {err}", warn=True)

    def ids(self, d, sessions=True, habits=True):
        """Tickable IDs for one day: its sessions and/or its habits."""
        keys = []
        if sessions:
            keys += self.days[d].tasks
        if habits:
            keys += [key for key, _, _ in self.sched.habits]
        return [task_id(d, key) for key in keys]

    def count(self, ids):
        """(how many are ticked, how many there are), like SUM(done), COUNT(*)."""
        return sum(tid in self.ticked for tid in ids), len(ids)

    def update_count(self, d):
        n, total = self.count(self.ids(d))
        self.done_labels[d].config(text=f"{n}/{total}",
                                   fg=GOOD if total and n == total else DIM)

    def update_summary(self):
        past = [d for d in self.days if d <= self.today]
        train_done, train_total = self.count(
            [tid for d in past for tid in self.ids(d, habits=False)])
        habit_done, habit_total = self.count(
            [tid for d in past for tid in self.ids(d, sessions=False)])
        upcoming = sum(len(day.tasks) for d, day in self.days.items()
                       if self.today < d <= self.today + timedelta(days=7))
        self.summary.config(
            text=f"Last {len(past)} days incl. today:  training {train_done}/{train_total}"
                 f"  ·  habits {habit_done}/{habit_total}"
                 f"        Next 7 days: {upcoming} sessions planned")

    # --- Details popup -------------------------------------------------------------
    def session_details(self, key, d=None):
        """(title, text) for a session; with a date, headed by that day's plan."""
        title, text = self.sched.sessions[key]
        if d is not None:
            slot, label = self.days[d].tasks[key]
            title, text = f"{d:%a %b %d}  ·  {slot}  ·  {label}", f"{title}\n\n{text}"
        return title, text

    def show_session(self, key, d=None):
        self.show_message(*self.session_details(key, d))

    def show_day(self, d):
        day = self.days[d]
        lines = [f"Where: {day.location}"] if day.location else []
        lines += [f"Note: {n}" for n in day.notes] + [""]
        mark = lambda key: "[x]" if task_id(d, key) in self.ticked else "[ ]"
        lines += [f"{mark(key)} {slot}  {label}" for key, (slot, label) in day.tasks.items()]
        lines += [f"{mark(key)}     {name}" for key, name, _ in self.sched.habits]
        if d.isoformat() in self.notes:
            lines += ["", "My notes:", self.notes[d.isoformat()]]
        self.show_message(f"{d:%A, %B %d}  ·  day {day.cycle_day + 1} of {CYCLE_DAYS}",
                          "\n".join(lines))

    def new_popup(self, title):
        """A small window that replaces any open one. Escape closes it.
        Fill it, then call place_popup()."""
        self.hide_tip()  # a click opens a popup; don't leave the tooltip too
        if self.popup is not None and self.popup.winfo_exists():
            self.popup.destroy()
        win = self.popup = tk.Toplevel(self.root, bg=CARD, padx=14, pady=10)
        win.title(title)
        win.transient(self.root)  # stays on top of the tracker, no taskbar entry
        win.resizable(False, False)
        win.bind("<Escape>", lambda e: win.destroy())
        return win

    def place_popup(self, win):
        """Open just below-right of the mouse pointer, on whichever monitor
        it's on. (Not clamped to the main screen's size: on a second monitor
        that would pull the window back onto the main one.)"""
        win.geometry(f"+{win.winfo_pointerx() + 12}+{win.winfo_pointery() + 12}")
        win.focus_set()

    def show_message(self, title, text):
        """Show details in a popup next to the mouse."""
        win = self.new_popup("Details")
        title_label, text_label = self.detail_column(win, wrap=420)
        title_label.config(text=title)
        text_label.config(text=text)
        self.button(win, "Close", win.destroy, BG).pack(anchor="e", pady=(8, 0))
        self.place_popup(win)

    # --- Daily notes ---------------------------------------------------------------
    def edit_note(self, d):
        """A popup with a text box for the day's note. Save (or Ctrl+Enter)
        stores it; saving an empty box deletes the note."""
        key = d.isoformat()
        win = self.new_popup("Notes")
        tk.Label(win, text=f"Notes for {d:%A, %B %d}", font=(FONT, 10, "bold"),
                 bg=CARD, fg=FG, anchor="w").pack(fill="x")
        box = tk.Text(win, width=50, height=8, wrap="word", font=(FONT, 10),
                      bg=BG, fg=FG, insertbackground=FG, relief="flat", padx=6, pady=4)
        box.pack(pady=(6, 0))
        box.insert("1.0", self.notes.get(key, ""))

        def save():
            text = box.get("1.0", "end").strip()
            if text:
                self.notes[key] = text
            else:
                self.notes.pop(key, None)
            self.save()
            self.update_note_icon(d)
            win.destroy()

        buttons = tk.Frame(win, bg=CARD)
        buttons.pack(fill="x", pady=(8, 0))
        self.button(buttons, "Save", save, BG).pack(side="right", padx=(6, 0))
        self.button(buttons, "Cancel", win.destroy, BG).pack(side="right")
        tk.Label(buttons, text="Ctrl+Enter to save", font=(FONT, 8), bg=CARD,
                 fg=DIM).pack(side="left")
        box.bind("<Control-Return>", lambda e: (save(), "break")[1])
        self.place_popup(win)
        box.focus_set()

    # --- Hover tooltips ------------------------------------------------------------
    def hoverable(self, widget, get_tip):
        """Show a tooltip at the mouse while it's over the widget.
        get_tip() returns (title, text) when the mouse arrives; if the
        text is empty (e.g. a day with no note), nothing is shown."""
        widget.bind("<Enter>", lambda e: self.show_tip(*get_tip(), e.x_root, e.y_root))
        widget.bind("<Motion>", lambda e: self.move_tip(e.x_root, e.y_root))
        widget.bind("<Leave>", lambda e: self.hide_tip())

    def show_tip(self, title, text, x, y):
        """A borderless window (overrideredirect) at the mouse, so it looks
        like a tooltip: an optional bold title, then the text."""
        self.hide_tip()
        if not text:
            return
        tip = self.tip = tk.Toplevel(self.root, bg=CARD, padx=10, pady=8,
                                     highlightthickness=1, highlightbackground=DIM)
        tip.overrideredirect(True)  # no title bar or border
        tip.attributes("-topmost", True)
        title_label, text_label = self.detail_column(tip, wrap=380)
        title_label.config(text=title)
        text_label.config(text=text)
        if not title:
            title_label.pack_forget()
        self.move_tip(x, y)

    def move_tip(self, x, y):
        """Keep the tooltip just below-right of the mouse pointer.

        x and y are screen coordinates of the pointer. On a second monitor
        they can be beyond the main screen's width (or negative), so they
        are used as-is, not clamped to the main screen."""
        if self.tip is not None:
            self.tip.geometry(f"+{x + 14}+{y + 18}")

    def hide_tip(self):
        if self.tip is not None:
            self.tip.destroy()
            self.tip = None

    def update_note_icon(self, d):
        """Blue pencil if the day has a note, grey if not."""
        self.note_icons[d].config(fg=ACCENT if d.isoformat() in self.notes else DIM)

    # --- Files and status ----------------------------------------------------------
    def open_file(self, path):
        """Open a file in VS Code, or failing that its default Windows app.
        (Windows has no default app for .md and .json on this PC.)"""
        if not path.exists():
            self.set_status(f"{path.name} doesn't exist yet "
                            f"(the log is created on your first tick).", warn=True)
            return
        try:
            if VSCODE is not None:
                subprocess.Popen([str(VSCODE), str(path)])
            else:
                os.startfile(path)
        except OSError as err:
            self.set_status(f"Couldn't open {path.name}: {err}", warn=True)

    def set_status(self, text, warn=False):
        self.status.config(text=text, fg=WARN if warn else DIM)


# --- Start the app -----------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    TrainingTracker(root)
    root.geometry("+40+30")  # size to fit the content, near the top-left
    root.minsize(600, 400)
    root.mainloop()  # hands control to tkinter until the window is closed
