# Student Learning Portal (PROG211 - Object-Oriented Programming 1)

A single-file **Python program** with a terminal menu where anonymous learners enrol in courses, complete lessons and record quiz scores. Domain: **Education - Student Learning Portal**.

## How to run

You only need Python 3. No installs, no browser and no hosting.

```bash
python main.py
```

Type a number from the menu and press Enter.

## Assignment mapping

| Task | Where in `main.py` |
|------|--------------------|
| **Task 1 - Classes, attributes, methods, object interaction** | `Course` and `Student` classes. `Student.enroll(course)`, `complete_lesson(course)` and `add_score(course, score)` show the two objects interacting. |
| **Task 2 - One data structure** | A **dictionary** (`registry`) stores `Student` objects with their unique ID as the key. `add_record()` and `display_records()` add and display records. |
| **Task 2 - Tuples (optional)** | `Course.CATALOG` and `Student.LEVELS` are tuples. |
| **Task 3 - Instance methods** | `enroll()`, `complete_lesson()`, `add_score()`, `progress_percent()`, `average_score()`, `status()`, `display_info()` |
| **Task 3 - Class methods** | `@classmethod` `Course.from_catalog()`, `Student.generate_id()`, `Student.total_created()` |
| **Static methods** | `@staticmethod` `Student.is_valid_level()` and `Student.grade_letter()` |

## How it meets Digital Public Goods (DPG) standards

- **Open-source:** the code is published on GitHub under the MIT licence.
- **Inclusive and accessible:** plain text menu with numbered choices, clear success and error messages, no images, and it runs on any computer with Python, including low-power machines.
- **Privacy-respecting:** no names, phone numbers, addresses or other personal data are collected. A learner has only an anonymous ID (e.g. `ST-0001`) and a class level.
- **Modular and reusable:** the classes are separate from the menu code, so they can be reused in another interface such as a website or app.

## Example usage (sample input / output)

**Input:** choose `1` (Add learner), pick level `4` (JSS 2).

**Output:**
```
[OK] Learner ST-0004 created (JSS 2).
```

**Input:** choose `4` (Enrol), enter `ST-0004`, pick course `1`.

**Output:**
```
[OK] Enrolled in Mathematics.
```

**Input:** choose `6` (Save a quiz score), enter `ST-0004`, course `1`, score `150`.

**Output:**
```
[!] Score must be between 0 and 100.
```

**Input:** choose `3` (Show learner progress), enter `ST-0001`.

**Output:**
```
Mathematics (MTH101)
  Lessons : 1/8  [##------------------]  12%
  Average : 72% (grade B)
  Status  : In progress
```

## Notes

Data is held in memory, so it resets when the program closes. This keeps the project simple and avoids storing personal data.

## Licence

MIT
