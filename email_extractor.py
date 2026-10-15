"""
Task 3: Task Automation with Python Scripts
Idea chosen: Extract all email addresses from a .txt file
            and save them to another file.

Concepts used: os, re, file handling

How to run:
    python email_extractor.py
"""

import os  # used to check that the input file exists
import re  # used to find email addresses (regular expressions)

# ---------- Settings (change these if you want) ----------
INPUT_FILE = "sample_emails.txt"      # the file we read from
OUTPUT_FILE = "extracted_emails.txt"  # the file we save results to

# A regular expression (pattern) that matches most email addresses:
#   name part  @  domain part  .  ending (like com, org, net)
EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


def read_file(path):
    """Open a text file and return everything inside it as one string."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def find_emails(text):
    """Find all email addresses in the text.

    Returns a list with no duplicates, keeping the original order.
    """
    all_matches = re.findall(EMAIL_PATTERN, text)

    unique_emails = []
    for email in all_matches:
        email = email.lower()  # treat Bob@x.com and bob@x.com as the same
        if email not in unique_emails:
            unique_emails.append(email)
    return unique_emails


def save_emails(emails, path):
    """Write each email on its own line in the output file."""
    with open(path, "w", encoding="utf-8") as file:
        for email in emails:
            file.write(email + "\n")


def main():
    print("=== Email Extractor ===")

    # Step 1: make sure the input file exists before we try to open it
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' was not found.")
        print("Put it in the same folder as this script and try again.")
        return

    # Step 2: read the file
    text = read_file(INPUT_FILE)

    # Step 3: find the emails
    emails = find_emails(text)

    # Step 4: save and report
    if not emails:
        print("No email addresses were found.")
        return

    save_emails(emails, OUTPUT_FILE)
    print(f"Found {len(emails)} unique email address(es):")
    for email in emails:
        print(" -", email)
    print(f"Saved to '{OUTPUT_FILE}'.")


# This runs main() only when we run this file directly
if __name__ == "__main__":
    main()
