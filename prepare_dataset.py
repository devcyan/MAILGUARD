import tarfile
import csv
import os
from email import policy
from email.parser import BytesParser

DATA_DIR = "data"

HAM_ARCHIVE = os.path.join(
    DATA_DIR, "20030228_easy_ham_2.tar.bz2"
)

SPAM_ARCHIVE = os.path.join(
    DATA_DIR, "20050311_spam_2.tar.bz2"
)

OUTPUT_FILE = os.path.join(DATA_DIR, "spam.csv")


def extract_email_text(raw_email):
    try:
        message = BytesParser(
            policy=policy.default
        ).parsebytes(raw_email)

        parts = []

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        parts.append(part.get_content())
                    except Exception:
                        pass
        else:
            if message.get_content_type() == "text/plain":
                try:
                    parts.append(message.get_content())
                except Exception:
                    pass

        return "\n".join(parts).strip()

    except Exception:
        return ""


def process_archive(archive_path, label, writer):
    count = 0

    with tarfile.open(archive_path, "r:bz2") as archive:

        for member in archive.getmembers():

            if not member.isfile():
                continue

            file = archive.extractfile(member)

            if file is None:
                continue

            raw_email = file.read()

            text = extract_email_text(raw_email)

            if text:
                writer.writerow([label, text])
                count += 1

    return count


def main():

    print("Preparing MailGuard dataset...")
    print()

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(["label", "text"])

        ham_count = process_archive(
            HAM_ARCHIVE,
            "ham",
            writer
        )

        spam_count = process_archive(
            SPAM_ARCHIVE,
            "spam",
            writer
        )

    print(f"Ham emails  : {ham_count}")
    print(f"Spam emails : {spam_count}")
    print(f"Total       : {ham_count + spam_count}")
    print()
    print(f"Dataset saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()