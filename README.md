# CodeAlpha Python Programming — Task 3: Task Automation with Python Scripts

**Project:** Smart Email Extractor
**Task number:** Task 3 (CodeAlpha Python Programming)

## Goal
Automate a small, repetitive real-life task: **find every email address inside
`.txt` files and save them to another file.**

Copying emails by hand from many files is slow and easy to get wrong. This
program scans a file (or a whole folder of files), cleans the results, and saves
them in three ready-to-use files.

## Task Rules Followed (from CodeAlpha Task 3)
| Rule | How this project follows it |
|---|---|
| Automate a small, real-life repetitive task | Extracts emails from text files automatically |
| Pick one of the given ideas | Idea chosen: *Extract all email addresses from a `.txt` file and save them to another file* |
| Key concepts: `os`, `re`, file handling | `os` handles files/folders, `re` finds the emails, `open()` reads and writes files |
| Keep it simple | One Python file, console only, no extra installs |

(`shutil` and `requests` belong to the other two ideas — moving `.jpg` files and
scraping a web page — so they are not needed here.)

## Features
| Feature | What it does |
|---|---|
| File **or folder** input | Type one `.txt` file or a folder; every `.txt` inside is scanned |
| Email finder | Uses a regular expression to find emails |
| Cleaning | Lowercases emails, removes duplicates, rejects broken ones like `john..doe@x.com` |
| Counting | Shows how many times each email appeared and in which file(s) |
| Sorted A–Z | Final list is alphabetical |
| Domain filter | Optionally keep only one domain, e.g. `gmail.com` |
| Domain statistics | Shows how many emails each domain has |
| Three output files | `.txt` list, `.csv` table, and a `report.txt` summary |
| Safe error handling | Missing file, empty folder, no emails, unreadable file — all handled with a friendly message |

## Concepts Used
| Concept | Where it is used |
|---|---|
| `os` | `os.path.isfile/isdir`, `os.listdir`, `os.path.join`, `os.makedirs` |
| `re` | `re.findall()` with an email pattern |
| File handling | `open()` with `"r"` and `"w"`, always inside `with` |
| `input()` | Asks for the file/folder and the optional domain filter |
| Dictionaries | Store each email's count and source files |
| Lists, loops, `if/else` | Cleaning, sorting, printing |
| Functions | One small function per job (`read_file`, `clean_email`, `collect_emails`, …) |
| `try/except` | Skips files that cannot be read instead of crashing |
| `csv` module (extra) | Writes the `.csv` file neatly |

## Project Files
```
task3_email_extractor/
├── email_extractor.py          # the program
├── README.md                   # this documentation
├── sample_data/                # example input files
│   ├── team_list.txt
│   ├── newsletter.txt
│   └── notes_no_emails.txt     # has no emails (tests that case)
└── output/                     # created when you run the program
    ├── extracted_emails.txt
    ├── extracted_emails.csv
    └── report.txt
```

## How to Run
1. Install Python 3 (https://www.python.org/downloads/).
2. Keep the folder structure above (script next to `sample_data`).
3. Open a terminal in the project folder and run:
   ```
   python email_extractor.py
   ```
   (On some systems use `python3`.)
4. When asked for a file or folder, type a name or press **Enter** to scan `sample_data`.
5. When asked for a domain filter, type e.g. `gmail.com`, or press **Enter** to skip.
6. Open the `output` folder to see your results.

To scan your own emails, put your `.txt` files in a folder and type that folder's name.

## Example Run
```
=== CodeAlpha Task 3: Smart Email Extractor ===
Enter a .txt file or a folder name [sample_data]:
Scanned 3 file(s). Found 12 email(s), 9 unique.
Keep only one domain? (e.g. gmail.com, Enter to skip):

Emails saved (9, sorted A-Z):
 - accounts@company.org  (found 1x)
 - billing@company.org  (found 1x)
 - john.doe@example.com  (found 3x)
 - mim@university.edu.bd  (found 1x)
 - nusrat_99@gmail.com  (found 2x)
 - rafi.ahmed@university.edu.bd  (found 1x)
 - sara+notes@mail.net  (found 1x)
 - support@company.org  (found 1x)
 - tanvir.hossain@gmail.com  (found 1x)

Emails per domain:
   company.org               3
   gmail.com                 2
   university.edu.bd         2
   example.com               1
   mail.net                  1

Saved to the 'output' folder:
   output/extracted_emails.txt
   output/extracted_emails.csv
   output/report.txt
```

### What the output files look like
**extracted_emails.csv** (opens in Excel)
```
No,Email,Domain,Times Found,Found In
1,accounts@company.org,company.org,1,team_list.txt
3,john.doe@example.com,example.com,3,newsletter.txt; team_list.txt
...
```
**report.txt**
```
Files scanned        : 3
Emails found (total) : 12
Unique emails        : 9
Duplicates removed   : 3
Most repeated email  : john.doe@example.com (3 times)
```

## How the Code Works (step by step)
1. **Ask** — `ask_for_input()` gets a file or folder name.
2. **Find files** — `get_txt_files()` returns the list of `.txt` files (or `None` if the path doesn't exist).
3. **Read and search** — `collect_emails()` opens each file and runs
   `re.findall` with the pattern `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}`
   (name, `@`, domain, dot, ending like `com`).
4. **Clean** — `clean_email()` lowercases and rejects broken emails; a dictionary
   keeps one entry per email with its count and source files.
5. **Filter (optional)** — `filter_by_domain()` keeps one domain only.
6. **Sort** — `sorted()` puts emails in A–Z order.
7. **Save** — `os.makedirs` creates `output/`, then the `.txt`, `.csv` and report are written.

## Limitations
- Scans only the `.txt` files directly inside the folder (not sub-folders).
- The pattern covers common emails but not every unusual format the email standard allows.
- Text like `hello@` or `user@domain` (no `.com`-style ending) is correctly ignored.

## Author
Created as part of the CodeAlpha Python Programming internship — Task 3.
