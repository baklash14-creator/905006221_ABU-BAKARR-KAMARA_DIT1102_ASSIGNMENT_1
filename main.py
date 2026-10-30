"""Student Learning Portal - PROG211 Object-Oriented Programming 1 (Individual Assignment).

Domain : Education - Student Learning Portal
Run    : python main.py
Needs  : Python 3 only. No installs, no browser, no hosting.

Digital Public Goods (DPG) alignment:
  - Open-source : published on GitHub under the MIT licence.
  - Inclusive   : plain text menu, numbered choices, clear messages, no images.
  - Privacy     : no names or contact details. Learners have only an anonymous
                  ID and a class level.
  - Modular     : the classes (Task 1/3) are separate from the menu (user interface).
"""
import os

# =====================================================================
# TASK 1 + TASK 3: CLASSES, ATTRIBUTES, METHODS
# =====================================================================


class Course:
    """A course that learners can enrol in."""

    # Tuple of tuples (optional extra marks): (code, title, total lessons, pass mark %)
    CATALOG = (
        ("MTH101", "Mathematics", 8, 50),
        ("ENG101", "English Language", 6, 50),
        ("SCI101", "Integrated Science", 7, 50),
        ("ICT101", "Computer Basics", 5, 60),
        ("AGR101", "Agricultural Science", 6, 50),
    )

    def __init__(self, code, title, total_lessons, pass_mark):
        self.code = code
        self.title = title
        self.total_lessons = total_lessons
        self.pass_mark = pass_mark

    # ---- class methods ----
    @classmethod
    def from_catalog(cls, code):
        """Create a Course object from the catalog by its code."""
        for c, title, lessons, mark in cls.CATALOG:
            if c == code:
                return cls(c, title, lessons, mark)
        raise ValueError(f"Unknown course: {code}")

    @classmethod
    def codes(cls):
        return [row[0] for row in cls.CATALOG]

    # ---- instance method ----
    def display_info(self):
        return f"{self.code} - {self.title}: {self.total_lessons} lessons, pass mark {self.pass_mark}%"


class Student:
    """An anonymous learner on the portal."""

    LEVELS = ("Primary 1-3", "Primary 4-6", "JSS 1", "JSS 2", "JSS 3",
              "SSS 1", "SSS 2", "SSS 3", "Adult learner")
    _counter = 0  # class attribute: number of students created

    def __init__(self, level):
        if not self.is_valid_level(level):
            raise ValueError("Invalid class level.")
        self.student_id = self.generate_id()
        self.level = level
        self.records = {}  # course code -> {"lessons": int, "scores": [int]}

    # ---- class methods ----
    @classmethod
    def generate_id(cls):
        cls._counter += 1
        return f"ST-{cls._counter:04d}"

    @classmethod
    def total_created(cls):
        return cls._counter

    # ---- static methods ----
    @staticmethod
    def is_valid_level(value):
        return value in Student.LEVELS

    @staticmethod
    def grade_letter(average):
        if average >= 80:
            return "A"
        if average >= 65:
            return "B"
        if average >= 50:
            return "C"
        if average >= 40:
            return "D"
        return "F"

    # ---- instance methods ----
    def is_enrolled(self, course):
        return course.code in self.records

    def enroll(self, course):
        """Object interaction: Student <-> Course."""
        if self.is_enrolled(course):
            raise ValueError(f"Already enrolled in {course.title}.")
        self.records[course.code] = {"lessons": 0, "scores": []}
        return f"Enrolled in {course.title}."

    def _record(self, course):
        if not self.is_enrolled(course):
            raise ValueError(f"Enrol in {course.title} first.")
        return self.records[course.code]

    def complete_lesson(self, course):
        rec = self._record(course)
        if rec["lessons"] >= course.total_lessons:
            raise ValueError("All lessons are already completed.")
        rec["lessons"] += 1
        return f"Lesson {rec['lessons']}/{course.total_lessons} completed."

    def add_score(self, course, score):
        rec = self._record(course)
        try:
            score = int(score)
        except (TypeError, ValueError):
            raise ValueError("Score must be a whole number.")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")
        rec["scores"].append(score)
        return f"Score {score} saved for {course.title}."

    def progress_percent(self, course):
        if not self.is_enrolled(course):
            return 0
        return round(100 * self.records[course.code]["lessons"] / course.total_lessons)

    def average_score(self, course):
        if not self.is_enrolled(course):
            return None
        scores = self.records[course.code]["scores"]
        return round(sum(scores) / len(scores)) if scores else None

    def status(self, course):
        if not self.is_enrolled(course):
            return "Not enrolled"
        avg = self.average_score(course)
        done = self.records[course.code]["lessons"] >= course.total_lessons
        if done and avg is not None and avg >= course.pass_mark:
            return "Passed"
        if done:
            return "Finished"
        return "In progress"

    def display_info(self):
        return f"{self.student_id} | {self.level} | enrolled in {len(self.records)} course(s)"


# =====================================================================
# TASK 2: ONE DATA STRUCTURE (a dictionary, unique ID as the key)
# =====================================================================

registry = {}


def add_record(registry, student):
    """Add a Student to the dictionary, keyed by its unique ID."""
    registry[student.student_id] = student
    return student


def display_records(registry):
    """Display all records from the dictionary as a table."""
    print(f"{BOLD}{'ID':<10}{'Class level':<18}{'Courses':>8}{RESET}")
    print("-" * 36)
    for s in registry.values():
        print(f"{s.student_id:<10}{s.level:<18}{len(s.records):>8}")
    print("-" * 36)
    print(f"{len(registry)} learner(s) in total")


def enrolment_summary(registry):
    """How many learners are enrolled in each course."""
    return {code: sum(1 for s in registry.values() if code in s.records)
            for code in Course.codes()}


# =====================================================================
# TERMINAL INTERFACE (look and feel)
# =====================================================================

os.system("")  # switches on ANSI colours in the Windows terminal
RESET, BOLD = "\033[0m", "\033[1m"
GREEN, RED, YELLOW, CYAN, DIM = "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[2m"
WIDTH = 62


def line(char="="):
    print(CYAN + char * WIDTH + RESET)


def banner(title, sub=""):
    print()
    line("=")
    print(f"{CYAN}{BOLD}{title.center(WIDTH)}{RESET}")
    if sub:
        print(f"{DIM}{sub.center(WIDTH)}{RESET}")
    line("=")


def heading(title):
    print(f"\n{BOLD}{CYAN}--- {title} ---{RESET}")


def ok(message):
    print(f"{GREEN}[OK] {message}{RESET}")


def fail(message):
    print(f"{RED}[!] {message}{RESET}")


def pause():
    input(f"\n{DIM}Press Enter to return to the menu...{RESET}")


def bar(percent, size=20):
    filled = round(size * percent / 100)
    return "[" + "#" * filled + "-" * (size - filled) + f"] {percent:3d}%"


def status_colour(status):
    colour = {"Passed": GREEN, "In progress": YELLOW}.get(status, DIM)
    return f"{colour}{status}{RESET}"


def seed_demo_data():
    """A few anonymous sample learners so the program is not empty at the start."""
    for level in ("JSS 2", "SSS 1", "Adult learner"):
        add_record(registry, Student(level))
    first = registry["ST-0001"]
    maths = Course.from_catalog("MTH101")
    first.enroll(maths)
    first.complete_lesson(maths)
    first.add_score(maths, 72)


def choose(title, options):
    """Show a numbered list and return the chosen item, or None."""
    heading(title)
    for i, option in enumerate(options, 1):
        print(f"  {YELLOW}{i}{RESET}. {option}")
    pick = input(f"\n{BOLD}Choose a number (Enter to cancel): {RESET}").strip()
    if pick.isdigit() and 1 <= int(pick) <= len(options):
        return options[int(pick) - 1]
    return None


def ask_student():
    sid = input(f"{BOLD}Learner ID (e.g. ST-0001): {RESET}").strip().upper()
    student = registry.get(sid)
    if student is None:
        fail("Learner not found.")
    return student


def ask_course():
    labels = [Course.from_catalog(c).display_info() for c in Course.codes()]
    picked = choose("Choose a course", labels)
    if picked is None:
        return None
    return Course.from_catalog(picked.split(" - ")[0])


# ---------- menu actions ----------
def add_student():
    level = choose("Choose a class level", list(Student.LEVELS))
    if level is None:
        return
    student = add_record(registry, Student(level))
    ok(f"Learner {student.student_id} created ({student.level}).")


def list_students():
    heading("All learners")
    if registry:
        display_records(registry)
    else:
        print("No learners yet.")


def show_student():
    student = ask_student()
    if student is None:
        return
    heading(f"Progress for {student.student_id} ({student.level})")
    for code in Course.codes():
        course = Course.from_catalog(code)
        print(f"\n{BOLD}{course.title}{RESET} {DIM}({course.code}){RESET}")
        if not student.is_enrolled(course):
            print(f"  {DIM}Not enrolled{RESET}")
            continue
        avg = student.average_score(course)
        avg_text = f"{avg}% (grade {Student.grade_letter(avg)})" if avg is not None else "no scores yet"
        print(f"  Lessons : {student.records[code]['lessons']}/{course.total_lessons}  "
              f"{bar(student.progress_percent(course))}")
        print(f"  Average : {avg_text}")
        print(f"  Status  : {status_colour(student.status(course))}")


def do_action(action):
    student = ask_student()
    if student is None:
        return
    course = ask_course()
    if course is None:
        return
    try:
        if action == "enroll":
            ok(student.enroll(course))
        elif action == "lesson":
            ok(student.complete_lesson(course))
        else:
            ok(student.add_score(course, input(f"{BOLD}Quiz score (0-100): {RESET}")))
    except ValueError as err:
        fail(str(err))


def show_summary():
    heading("Enrolment summary")
    print(f"{BOLD}{'Course':<24}{'Lessons':>8}{'Pass':>7}{'Enrolled':>10}{RESET}")
    print("-" * 49)
    for code, count in enrolment_summary(registry).items():
        c = Course.from_catalog(code)
        print(f"{c.title:<24}{c.total_lessons:>8}{str(c.pass_mark) + '%':>7}{count:>10}")
    print("-" * 49)


MENU = (
    ("Add learner", add_student),
    ("List learners", list_students),
    ("Show learner progress", show_student),
    ("Enrol learner in a course", lambda: do_action("enroll")),
    ("Complete a lesson", lambda: do_action("lesson")),
    ("Save a quiz score", lambda: do_action("score")),
    ("Enrolment summary", show_summary),
)
QUIT_NUMBER = len(MENU) + 1  # Quit is the last option (8)


def show_menu():
    banner("STUDENT LEARNING PORTAL", "PROG211 - Object-Oriented Programming 1")
    for i, (label, _) in enumerate(MENU, 1):
        print(f"   {YELLOW}{i}{RESET}.  {label}")
    print(f"   {RED}{QUIT_NUMBER}{RESET}.  Quit")
    line("-")
    print(f"{DIM}{len(registry)} learner(s) loaded - no personal data stored{RESET}")


def main():
    seed_demo_data()
    while True:
        show_menu()
        pick = input(f"{BOLD}Choose an option (1-{QUIT_NUMBER}): {RESET}").strip()
        if pick == str(QUIT_NUMBER):
            print(f"\n{GREEN}Thank you for using the Student Learning Portal. Goodbye!{RESET}\n")
            break
        if pick.isdigit() and 1 <= int(pick) <= len(MENU):
            MENU[int(pick) - 1][1]()
        else:
            fail(f"Please enter a number from 1 to {QUIT_NUMBER}.")
        pause()


if __name__ == "__main__":
    main()
