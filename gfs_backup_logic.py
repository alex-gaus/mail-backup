import os
import datetime
import argparse
from imapbackup38 import run_imapbackup

def main():
    print("### STARTING gfs_backup_logic ###")
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="IMAP Email Backup with GFS Rotation")
    parser.add_argument("-s", "--server", required=True, help="IMAP server address")
    parser.add_argument("-u", "--user", required=True, help="IMAP username")
    parser.add_argument("-p", "--password", required=True, help="IMAP password")
    parser.add_argument("-d", "--base_dir", required=True, help="Base directory for backups")

    args = parser.parse_args()

    # Get current date
    today = datetime.date.today()
    month = today.strftime("%Y-%m")
    year = today.strftime("%Y")

    # Define backup paths
    DAILY_DIR = os.path.join(args.base_dir, f"daily/")
    MONTHLY_DIR = os.path.join(args.base_dir, f"monthly/{month}-{today}")
    YEARLY_DIR = os.path.join(args.base_dir, f"yearly/{year}-{month}-{today}")

    # Decide which backup to run
    if today.day == 1 and today.month == 1:  # Every January 1st
        path = YEARLY_DIR
    elif today.day == 1:  # Every 1st of the month
        path = MONTHLY_DIR
    else:  # Every week
        path = DAILY_DIR

    # Ensure backup directory exists
    os.makedirs(path, exist_ok=True)

    # Configure IMAP backup
    config = {
    "basedir": path,
    "server": args.server,           # IMAP server (must be set by user)
    "user": args.user,             # IMAP username (must be set by user)
    "pass": args.password,             # IMAP password (must be set by user)
    "overwrite": False,       # Append to existing mbox files (False) or overwrite (True)
    "usessl": False,          # Use SSL for IMAP connection
    "thunderbird": True,     # Thunderbird compatibility mode
    "nospinner": True,       # Disable spinner UI
    "icloud": False,          # iCloud-specific settings
    "port": 143,             # IMAP port (default: 993 for SSL, 143 for non-SSL)
    "keyfilename": None,      # SSL key file (if applicable)
    "certfilename": None,     # SSL certificate file (if applicable)
    "folders": None,          # Specific folders to backup (None = all folders)
    "exclude-folders": None,  # Excluded folders
    "timeout": 60             # Timeout in seconds (default: 60)
}

    print(f"Starting with agruments: user: {args.user}, server: {args.server}, path: {path}")
    # Run the backup
    run_imapbackup(config)
    print("/n### SCRIPT DONE! ###")
if __name__ == "__main__":
    main()