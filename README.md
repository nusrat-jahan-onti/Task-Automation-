# Task 3: Task Automation with Python Scripts — Email Extractor

## Goal
Automate a small, repetitive real-life task: **find every email address inside a
`.txt` file and save them to another file.**

Doing this by hand (reading a long file and copying emails one by one) is slow
and easy to get wrong. This script does it in a second.

## Concepts Used
| Concept | Where it is used |
|---|---|
| `os` | `os.path.exists()` checks that the input file exists before opening it |
| `re` | `re.findall()` with a pattern finds all email addresses |
| File handling | `open()` with `"r"` to read and `"w"` to write, using `with` |
| Functions | The code is split into `read_file`, `find_emails`, `save_emails`, `main` |
| Lists and loops | Removing duplicates and printing results |

(`shutil` and `requests` were listed in the assignment, but they are for the
other ideas — moving files and scraping a page. This project picks the email
idea, so they are not needed.)

## Project Files
```
task3_email_extractor/
├── email_extractor.py     # the program
├── sample_emails.txt      # example input file
├── extracted_emails.txt   # output (created when you run the program)
└── README.md              # this documentation
```

## How to Run
1. Install Python 3 (https://www.python.org/downloads/).
2. Put all files in the same folder.
3. Open a terminal in that folder and run:
   ```
   python email_extractor.py
   ```
   (On some systems use `python3` instead of `python`.)
4. Open `extracted_emails.txt` to see the result.

To use your own file, change this line at the top of `email_extractor.py`:
```python
INPUT_FILE = "sample_emails.txt"
```

## Example Output
```
=== Email Extractor ===
Found 6 unique email address(es):
 - john.doe@example.com
 - billing@company.org
 - accounts@company.org
 - nusrat_99@gmail.com
 - rafi.ahmed@university.edu.bd
 - sara+notes@mail.net
Saved to 'extracted_emails.txt'.
```
Note: `JOHN.DOE@example.com` appears twice in the sample file, but it is saved
only once.

## How the Code Works (step by step)
1. **Check the file** — `os.path.exists` makes sure the input file is there. If
   not, the program prints a friendly error instead of crashing.
2. **Read the file** — the whole text is loaded into one string.
3. **Find emails** — the pattern
   `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` means:
   - some letters/numbers/symbols, then
   - an `@`, then
   - a domain name, then
   - a dot and an ending like `com` or `org`.
4. **Remove duplicates** — emails are made lowercase and each is added to the
   result list only once.
5. **Save** — each email is written on its own line in `extracted_emails.txt`.

## Rules Followed (from the assignment)
- Automates a small, real-life repetitive task.
- Uses one of the allowed ideas (extract emails from a `.txt` file to another file).
- Uses `os`, `re`, and file handling.
- Simple console program, no extra libraries to install.

## Limitations
- The pattern covers common emails but not every unusual format allowed by the
  email standard.
- Words like `hello@` (no domain) are correctly ignored.

## Ideas to Improve
- Ask the user for the file name with `input()`.
- Sort the emails alphabetically.
- Save to a `.csv` file as well.
