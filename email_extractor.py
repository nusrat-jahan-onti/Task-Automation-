"""
CodeAlpha Python Programming - TASK 3: Task Automation with Python Scripts
==========================================================================
Idea chosen : Extract all email addresses from a .txt file
              and save them to another file.
Key concepts: os, re, file handling

Smart Email Extractor - what this program does:
    1. Asks for a .txt file OR a whole folder of .txt files (input()).
    2. Finds every email address in them (re).
    3. Cleans the results: removes duplicates, rejects broken emails,
       counts how many times each email appears, sorts A-Z.
    4. Optionally keeps only emails from one domain (e.g. gmail.com).
    5. Saves everything inside an "output" folder (os):
           extracted_emails.txt  - one email per line
           extracted_emails.csv  - email, domain, times found, source files
           report.txt            - summary with statistics

How to run:
    python email_extractor.py
"""

import csv  # used only to write the .csv file neatly
import os   # folders, paths and checking that files exist
import re   # finding email addresses (regular expressions)

# ---------- Settings ----------
DEFAULT_INPUT = "sample_data"   # used if the user just presses Enter
OUTPUT_FOLDER = "output"        # all results are saved here
OUTPUT_TXT = os.path.join(OUTPUT_FOLDER, "extracted_emails.txt")
OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, "extracted_emails.csv")
OUTPUT_REPORT = os.path.join(OUTPUT_FOLDER, "report.txt")

# Pattern for most email addresses:
#   name part  @  domain part  .  ending (like com, org, net)
EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


# ---------------------------------------------------------------
# Step 1: getting the files
# ---------------------------------------------------------------
def ask_for_input():
    """Ask the user for a file or folder. Pressing Enter uses the default."""
    answer = input(f"Enter a .txt file or a folder name [{DEFAULT_INPUT}]: ").strip()
    if answer == "":
        answer = DEFAULT_INPUT
    return answer


def get_txt_files(path):
    """Return a list of .txt files for the given path.

    - If path is a file   -> a list with just that file.
    - If path is a folder -> every .txt file inside it (sorted).
    - If path doesn't exist -> None.
    """
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        files = []
        for name in sorted(os.listdir(path)):
            if name.lower().endswith(".txt"):
                files.append(os.path.join(path, name))
        return files
    return None


def read_file(path):
    """Open a text file and return everything inside it as one string."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


# ---------------------------------------------------------------
# Step 2: finding and cleaning emails
# ---------------------------------------------------------------
def clean_email(raw_email):
    """Make an email lowercase and reject obviously broken ones.

    Returns the cleaned email, or None if it should be ignored.
    """
    email = raw_email.lower()
    local_part = email.split("@")[0]

    if ".." in email:                                   # john..doe@x.com
        return None
    if local_part.startswith(".") or local_part.endswith("."):
        return None
    return email


def get_domain(email):
    """Return the part after the @ sign  (john@gmail.com -> gmail.com)."""
    return email.split("@")[1]


def collect_emails(files):
    """Read every file and collect the emails.

    Returns three things:
        results  - dictionary: email -> {"count": number, "files": [names]}
        scanned  - how many files were read successfully
        skipped  - list of files that could not be read
    """
    results = {}
    scanned = 0
    skipped = []

    for path in files:
        try:
            text = read_file(path)
        except (OSError, UnicodeDecodeError):
            skipped.append(path)  # unreadable file - skip it, don't crash
            continue

        scanned += 1
        file_name = os.path.basename(path)

        for raw in re.findall(EMAIL_PATTERN, text):
            email = clean_email(raw)
            if email is None:
                continue
            if email not in results:
                results[email] = {"count": 0, "files": []}
            results[email]["count"] += 1
            if file_name not in results[email]["files"]:
                results[email]["files"].append(file_name)

    return results, scanned, skipped


def filter_by_domain(results, domain):
    """Keep only the emails that belong to the given domain."""
    domain = domain.lower().strip()
    filtered = {}
    for email, info in results.items():
        if get_domain(email) == domain:
            filtered[email] = info
    return filtered


def count_domains(results):
    """Count how many unique emails each domain has.

    Returns a list of (domain, count) sorted from most to least.
    """
    counts = {}
    for email in results:
        domain = get_domain(email)
        counts[domain] = counts.get(domain, 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


# ---------------------------------------------------------------
# Step 3: saving the results
# ---------------------------------------------------------------
def save_as_txt(emails, path):
    """Write each email on its own line in a .txt file."""
    with open(path, "w", encoding="utf-8") as file:
        for email in emails:
            file.write(email + "\n")


def save_as_csv(emails, results, path):
    """Write a table (opens in Excel) with details for each email."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Email", "Domain", "Times Found", "Found In"])
        for number, email in enumerate(emails, start=1):
            info = results[email]
            writer.writerow([
                number,
                email,
                get_domain(email),
                info["count"],
                "; ".join(info["files"]),
            ])


def save_report(path, source, scanned, skipped, emails, results,
                total_found, total_unique, domain_filter):
    """Write a short summary report about the run."""
    duplicates = total_found - total_unique
    top_email = max(emails, key=lambda e: results[e]["count"])

    with open(path, "w", encoding="utf-8") as file:
        file.write("CodeAlpha Python Programming - Task 3\n")
        file.write("Smart Email Extractor - Report\n")
        file.write("=" * 40 + "\n")
        file.write(f"Source               : {source}\n")
        file.write(f"Files scanned        : {scanned}\n")
        file.write(f"Files skipped        : {len(skipped)}\n")
        file.write(f"Emails found (total) : {total_found}\n")
        file.write(f"Unique emails        : {total_unique}\n")
        file.write(f"Duplicates removed   : {duplicates}\n")
        if domain_filter:
            file.write(f"Domain filter        : {domain_filter}\n")
        file.write(f"Emails saved         : {len(emails)}\n")
        file.write(
            f"Most repeated email  : {top_email} "
            f"({results[top_email]['count']} times)\n"
        )
        file.write("\nEmails per domain:\n")
        for domain, count in count_domains({e: results[e] for e in emails}):
            file.write(f"  {domain:<25} {count}\n")


# ---------------------------------------------------------------
# The main program
# ---------------------------------------------------------------
def main():
    print("=== CodeAlpha Task 3: Smart Email Extractor ===")

    # Step 1: ask what to scan and make sure it exists
    source = ask_for_input()
    files = get_txt_files(source)

    if files is None:
        print(f"Error: '{source}' was not found.")
        print("Check the name and try again (it must be in this folder).")
        return
    if len(files) == 0:
        print(f"No .txt files were found in '{source}'.")
        return

    # Step 2: read the files and find the emails
    results, scanned, skipped = collect_emails(files)
    total_found = sum(info["count"] for info in results.values())
    print(f"\nScanned {scanned} file(s). Found {total_found} email(s), "
          f"{len(results)} unique.")
    if skipped:
        print("Skipped (could not read):", ", ".join(skipped))

    if not results:
        print("No email addresses were found.")
        return

    # Step 3: optional filter by domain
    domain_filter = input("Keep only one domain? (e.g. gmail.com, Enter to skip): ").strip()
    if domain_filter:
        results_to_save = filter_by_domain(results, domain_filter)
        if not results_to_save:
            print(f"No emails from '{domain_filter}' were found.")
            return
    else:
        results_to_save = results

    emails = sorted(results_to_save)  # alphabetical order (A to Z)

    # Step 4: save everything inside the output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    save_as_txt(emails, OUTPUT_TXT)
    save_as_csv(emails, results_to_save, OUTPUT_CSV)
    save_report(OUTPUT_REPORT, source, scanned, skipped, emails,
                results_to_save, total_found, len(results), domain_filter)

    # Step 5: show the result on screen
    print(f"\nEmails saved ({len(emails)}, sorted A-Z):")
    for email in emails:
        times = results_to_save[email]["count"]
        print(f" - {email}  (found {times}x)")

    print("\nEmails per domain:")
    for domain, count in count_domains(results_to_save):
        print(f"   {domain:<25} {count}")

    print(f"\nSaved to the '{OUTPUT_FOLDER}' folder:")
    print(f"   {OUTPUT_TXT}")
    print(f"   {OUTPUT_CSV}")
    print(f"   {OUTPUT_REPORT}")


# This runs main() only when we run this file directly
if __name__ == "__main__":
    main()
