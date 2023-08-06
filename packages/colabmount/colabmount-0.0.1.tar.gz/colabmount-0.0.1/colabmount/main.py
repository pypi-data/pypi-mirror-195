#!/usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import Iterable, Optional

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

GDRIVE_MOUNT_POINT = "/content/gdrive"
DEFAULT_BASE_DIRECTORY_CANDIDATES = (
    "/content/gdrive/MyDrive",
    "/content/gdrive/My Drive",
)


def mount_file(
    filename: str,
    create: bool,
    base_directory_candidates: Iterable[str] = DEFAULT_BASE_DIRECTORY_CANDIDATES,
    gdrive_mount_point: str = GDRIVE_MOUNT_POINT,
) -> Optional[Path]:
    try:
        from google.colab import drive
    except ImportError:
        print("Not running on Google Colab. Skipping Google Drive mount.")
        return None
    else:
        print("Running on Google Colab. Mounting Google Drive.")

    drive.mount(gdrive_mount_point)

    for base_directory_candidate in base_directory_candidates:
        assert base_directory_candidate.startswith(
            GDRIVE_MOUNT_POINT
        ), "Base directory candidates must be subdirectories of the gdrive mount point."
        assert isinstance(base_directory_candidate, str)

        log.debug(f"Checking for Google Drive directory: {base_directory_candidate}")
        if os.path.isdir(base_directory_candidate):
            log.debug(f"Found Google Drive directory: {base_directory_candidate}")
            google_drive_base = base_directory_candidate
            break
    else:
        raise FileNotFoundError(
            "Could not find a valid Google Drive directory. Tried {base_directory_candidates}"
        )

    file_path = Path(google_drive_base) / filename

    if file_path.exists():
        print(f"Found {filename} in Google Drive.")
        return file_path
    elif create:
        print(f"Could not find {filename} in Google Drive. Creating it.")
        with open(file_path, "w") as f:
            f.write("# Include your environment variables here.\n")
            f.write("SAMPLE_VAR=sample_value\n")

        color = "\033[94m"  # Blue
        message = (
            color
            + "\x1B[1m"
            + f"Please open {filename} in your Google Drive and add you environment variables, then re-run."
            + "\x1b[0m"
        )
        raise Exception(message)
    else:
        return None
