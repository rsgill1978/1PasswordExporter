# Frequently Asked Questions (FAQ)

## Table of Contents

- [General Questions](#general-questions)
- [Installation and Requirements](#installation-and-requirements)
- [Usage and Operation](#usage-and-operation)
- [Security and Privacy](#security-and-privacy)
- [Data Export and Format](#data-export-and-format)
- [Import to Apple Passwords](#import-to-apple-passwords)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

---

## General Questions

### What does this script do?

This script converts a 1Password Unencrypted Export (`.1pux`) file into:
1. A CSV file that can be imported directly into Apple Passwords
2. Organized folders containing non-password data (credit cards, identities, documents, etc.)
3. Extracted file attachments from your vault

It automates the migration process from 1Password to Apple Passwords while preserving all your data.

### Why would I need this script?

You would use this script if you are:
- Migrating from 1Password to Apple Passwords
- Wanting to consolidate your passwords into Apple's ecosystem
- Needing to extract and organize your 1Password data
- Looking for a free alternative to paid password managers
- Preparing data for storage in another secure service (like NordLocker)

### Is this script safe to use?

Yes, the script is safe for the following reasons:
- Uses only Python standard library modules (no external dependencies)
- Does not connect to the internet or send data anywhere
- Does not modify your original 1Password vault
- Source code is fully readable and auditable
- Performs read-only operations on input files
- Creates new files without overwriting existing data

However, the output files contain sensitive data in plain text and must be handled securely.

### Is this script official or affiliated with 1Password or Apple?

No. This is an independent utility script created to facilitate migration between password managers. It is not endorsed, supported, or affiliated with 1Password or Apple Inc.

### Will this script work with future versions of 1Password or Apple Passwords?

The script is designed for 1Password export format version 3 (current as of 2025) and Apple Passwords CSV import format (iOS 18.0+, macOS Sequoia 15.0+).

If either company changes their format specifications, the script may require updates. Always verify the export and import work correctly with a test subset of your data.

---

## Installation and Requirements

### What do I need to run this script?

You need:
1. Python 3.6 or later installed on your computer
2. A `.1pux` export file from 1Password
3. At least 100MB of free disk space (varies with vault size)
4. A text editor or terminal application to run the script

No additional software or packages are required.

### How do I check if Python is installed?

Open a terminal or command prompt and type:

```bash
python3 --version
```

If Python is installed, you will see output like `Python 3.x.x`. If not, download it from [python.org](https://www.python.org/downloads/).

### Do I need to install any Python packages?

No. The script uses only standard library modules included with Python. No `pip install` commands are necessary.

### What operating systems are supported?

The script runs on:
- macOS (all versions with Python 3.6+)
- Windows (Windows 10/11 with Python 3.6+)
- Linux (all distributions with Python 3.6+)

However, importing the CSV into Apple Passwords requires:
- macOS Sequoia 15.0 or later, OR
- iOS 18.0 or later, OR
- iPadOS 18.0 or later

### Can I run this script on Windows and import to Apple Passwords?

Yes, but in two steps:
1. Run the script on Windows to generate the CSV
2. Transfer the `outputs/exported_passwords.csv` file to a Mac or iOS device
3. Import the CSV using Apple Passwords on that device

---

## Usage and Operation

### How do I get a .1pux file from 1Password?

1. Open 1Password 8 or later
2. Click File → Export → All Items
3. Choose format: "1Password Unencrypted Export (.1pux)"
4. Choose a save location
5. Confirm the export (1Password will warn about plain-text exposure)
6. Move the file to the `inputs/` directory

### What is the basic command to run the script?

```bash
python3 1password_exporter.py inputs/your_file.1pux
```

Replace `your_file.1pux` with the actual filename of your export.

### Where should I place my .1pux file?

Place it in the `inputs/` subdirectory within the `1PasswordExporter` folder. This keeps your workspace organized.

### How long does the script take to run?

Typical execution times:
- Small vault (<100 items): 5-10 seconds
- Medium vault (100-500 items): 10-30 seconds
- Large vault (500-2000 items): 30-90 seconds
- Very large vault (>2000 items): 2-5 minutes

Time varies based on the number of attachments and system performance.

### Can I process multiple .1pux files at once?

Not in the current version. Run the script separately for each file. The output from each run will overwrite previous results, so:
1. Process the first file
2. Move or rename the output files
3. Process the next file

Or consolidate exports in 1Password before exporting.

### What happens to my original .1pux file?

The script only reads the file and does not modify or delete it. You must manually delete it after successful import for security reasons.

### Where does the script create output files?

Output is created in the `outputs/` directory:
- `outputs/exported_passwords.csv` (Apple Passwords CSV file)
- `outputs/non_password_data/` folder with organized subfolders
- `outputs/non_password_data/attachments/` folder with extracted files

---

## Security and Privacy

### Are my passwords safe when using this script?

The passwords are as safe as the files themselves. Important security considerations:

**During export:**
- The `.1pux` file contains all passwords in plain text
- The CSV file contains all passwords in plain text
- Anyone with access to these files can read your passwords

**Protection measures:**
- The script does not send data over the network
- The script does not save data to any external location
- You control all input and output files

**Your responsibility:**
- Secure the directory (set appropriate file permissions)
- Delete files immediately after import
- Do not store files in cloud-synced folders
- Run the script offline if possible

### Should I run this script offline?

Yes, it is recommended to:
1. Disconnect from the internet
2. Run the export process
3. Import to Apple Passwords
4. Securely delete all files
5. Reconnect to the internet

This prevents any potential network-based attacks or accidental uploads to cloud services.

### How do I securely delete the files after import?

**macOS:**
```bash
# If srm is available (older macOS versions)
srm inputs/your_file.1pux outputs/exported_passwords.csv

# Or use rm and empty trash with secure empty
rm inputs/your_file.1pux outputs/exported_passwords.csv
```

**Linux:**
```bash
shred -vfz -n 5 inputs/your_file.1pux outputs/exported_passwords.csv
```

**Windows:**
```cmd
# Download sdelete from Microsoft Sysinternals
sdelete -p 5 inputs\your_file.1pux outputs\exported_passwords.csv
```

After deletion, restart your computer to clear memory.

### Can someone recover the deleted files?

Standard deletion (`rm`, `del`) may leave recoverable data. Use secure deletion tools mentioned above. For maximum security:
1. Use secure deletion tools
2. Restart the computer after deletion
3. Run on a system with full-disk encryption enabled (FileVault, BitLocker)

### What if I find a security issue?

Report security concerns responsibly:
1. Do not post sensitive details publicly
2. Include description of the issue
3. Provide steps to reproduce (without exposing passwords)
4. Suggest potential fixes if possible

---

## Data Export and Format

### What data is included in the CSV file?

The CSV contains only login items (categoryUuid: 001, 005, 110):
- Title (item name)
- URL (website address)
- Username (login name or email)
- Password (plain text)
- Notes (additional information)
- OTPAuth (two-factor authentication secrets)

### What data is NOT included in the CSV?

The following are exported to human-readable text files in `outputs/non_password_data/`:
- Credit cards
- Bank accounts
- Identities
- Secure notes
- Documents
- Passports
- Driver licenses
- SSH keys
- And 14 other non-password categories

### Why are non-password items saved as plain text files?

Plain text format is used because:
1. Apple Passwords CSV format only supports six columns (no custom fields)
2. Text files are instantly readable on any device (phone, desktop, tablet)
3. Easy to search using Spotlight, Windows Search, or file managers
4. Optimized for storage in NordLocker or other encrypted storage
5. Clean copy-paste of license keys and credentials without parsing
6. No special software needed to view or edit the data
7. Clean formatting with no redundant data type labels (e.g., "String:", "Date:", "URL:")
8. Smart field handling - dates formatted as YYYY-MM-DD, email addresses extracted directly

### What happens to file attachments?

All file attachments (documents, images, PDFs) are:
1. Extracted from the `.1pux` archive
2. Stored in the same folder as the item's text file
3. Preserved with original filenames
4. Saved without any modification
5. Listed in the text file for easy reference

Each non-password item gets its own folder containing a `.txt` file and any attachments.

### Are tags preserved?

Tags are not included in the exported text files as they are considered redundant metadata. The focus is on essential data (credentials, license keys, account numbers, etc.) without extraneous information. For password items in the CSV, tags can be manually added to the Notes field if needed.

### Is password history included?

No. Password history is excluded because:
- Apple Passwords does not support importing password history
- CSV format has no field for it
- Including it would significantly increase file sizes

### What about TOTP secrets for two-factor authentication?

TOTP secrets are included in the CSV's OTPAuth column as `otpauth://` URIs. Apple Passwords will automatically set up two-factor authentication for these items.

### Do I lose any data by using this script?

Some metadata is not preserved:
- Creation and modification timestamps
- Password history
- Item relationships and links
- Access history
- Custom icons (Apple Passwords uses website favicons)
- Vault sharing information

All actual data (passwords, credit cards, notes, documents) is fully preserved.

---

## Import to Apple Passwords

### How do I import the CSV to Apple Passwords?

**On macOS:**
1. Open the Passwords app
2. Authenticate with Touch ID or password
3. Go to File → Import Passwords
4. Select `outputs/exported_passwords.csv`
5. Review and confirm

**On iOS:**
1. Open Settings → Passwords
2. Authenticate with Face ID or passcode
3. Tap the "+" button → Import from CSV
4. Browse to the CSV file
5. Review and confirm

### What if the import fails?

Common causes and solutions:

**"Missing column labels":**
- Open CSV in text editor
- Verify first line is: `Title,URL,Username,Password,Notes,OTPAuth`
- Re-save as UTF-8 encoding

**"Could not import passwords":**
- Check file encoding (must be UTF-8 without BOM)
- Replace any curly quotes with straight quotes
- Ensure URLs include protocol (`https://` or `http://`)

**Some entries skipped:**
- Invalid URLs (missing protocol)
- Malformed TOTP URIs
- Duplicate entries (same URL + username)
- Check export summary for specific errors

### Can I test the import with a few items first?

Yes, it is highly recommended:
1. Open `outputs/exported_passwords.csv` in a text editor
2. Copy the header row and 5-10 data rows
3. Save as `outputs/test_passwords.csv`
4. Import the test file to Apple Passwords
5. Verify the entries appear correctly
6. If successful, import the full CSV

### How do I handle duplicate passwords?

During import, Apple Passwords will:
1. Detect duplicates (matching URL + username)
2. Prompt you to choose: Overwrite, Skip, or Merge
3. Review each carefully before confirming

To avoid duplicates:
- Export existing Apple Passwords entries first
- Manually merge in a spreadsheet
- Re-import the consolidated list

### Can I import to multiple devices?

Yes. Once imported to Apple Passwords on one device with iCloud Keychain enabled, the passwords will automatically sync to all your Apple devices signed in with the same Apple ID.

### What is the maximum number of entries I can import?

Apple Passwords can handle thousands of entries, but:
- Recommended maximum per CSV: 2000 entries
- Large imports may take several minutes
- Older devices may experience performance issues with very large files

If you have more than 2000 entries:
1. Split the CSV into multiple files (keep the header in each)
2. Import each file separately
3. Allow time for iCloud sync between imports

### Do I need to do anything after import?

After successful import:
1. Verify entries in Apple Passwords
2. Test autofill on a few websites
3. Check that TOTP codes work
4. Securely delete the CSV and 1pux files
5. Optionally restart your device to clear memory

---

## Troubleshooting

### The script says "command not found"

This means Python is not in your system PATH.

**Solutions:**
- Try `python` instead of `python3`
- Specify full path: `/usr/bin/python3 1password_exporter.py ...`
- Reinstall Python and ensure "Add to PATH" is checked

### I get a "No module named" error

If you see this error, it means a standard library module is missing or corrupted.

**Solution:**
- Reinstall Python from [python.org](https://www.python.org/)
- Ensure you download the full installer, not a minimal version

### The script runs but creates no output

Check for errors in the output. Common causes:
- Input file path is incorrect
- No items match the password categories
- Permissions issue (cannot write to outputs directory)

**Solution:**
```bash
# Check if output directory is writable
touch outputs/test_file.txt
rm outputs/test_file.txt

# Run script with full path
python3 /full/path/to/1password_exporter.py /full/path/to/file.1pux
```

### CSV looks corrupted or has strange characters

This is usually an encoding issue.

**Diagnosis:**
```bash
file outputs/exported_passwords.csv
```

Should show: `UTF-8 Unicode text`

**Solution:**
- Ensure your text editor supports UTF-8
- Do not open CSV in Excel (use Numbers, LibreOffice, or text editor)
- Re-run the script in a clean outputs directory

### Attachments are not being extracted

Check the export summary for specific error messages.

**Common causes:**
- Files not present in the `.1pux` archive (check with: `unzip -l file.1pux`)
- Corrupted archive
- Insufficient disk space

**Solution:**
- Re-export from 1Password
- Check available disk space: `df -h .`
- Verify archive integrity: `unzip -t file.1pux`

### Script crashes with "Memory Error"

This occurs with very large vaults on systems with limited RAM.

**Solutions:**
- Close other applications
- Export in smaller batches from 1Password
- Run on a system with more RAM
- Increase system swap space

### Import to Apple Passwords shows errors for some entries

**"Invalid URL" errors:**
- URLs must include protocol: `https://example.com` not `example.com`
- Fix by editing CSV and adding `https://` to URLs

**"Could not import" for specific entries:**
- Check for special characters that need escaping
- Ensure proper quoting of fields with commas
- Remove or escape any unmatched quotes

### How can I see more detailed error information?

Add debug output by editing the script:

1. Open `1password_exporter.py` in a text editor
2. Find the line `if __name__ == "__main__":`
3. Add above it:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
4. Save and re-run

This will show detailed processing information.

---

## Advanced Topics

### Can I modify the script to export additional fields?

Yes. The script is designed to be readable and modifiable. To add fields to the CSV:

1. Add field name to `fieldnames` list in `export_passwords_to_csv()`
2. Add extraction logic in the row dictionary
3. Note: Apple Passwords only supports six standard columns

### Can I use this script in an automated workflow?

Yes. The script:
- Returns exit code 0 on success, 1 on failure
- Outputs structured summary information
- Accepts command-line arguments
- Runs non-interactively

Example automated usage:
```bash
#!/bin/bash
python3 1password_exporter.py inputs/export.1pux
if [ $? -eq 0 ]; then
    echo "Export successful"
    # Additional processing here
else
    echo "Export failed"
    exit 1
fi
```

### Can I customize the output directory structure?

Yes. The script's `__init__` method defines output paths. Modify these to change structure:

```python
# Current default (outputs in outputs/ directory)
self.non_password_dir = os.path.join(self.output_dir, "non_password_data")

# Custom structure
self.non_password_dir = os.path.join(self.output_dir, "my_custom_folder")
```

### How do I handle very large vaults (>5000 items)?

For optimal performance with large vaults:

1. **Export in batches from 1Password:**
   - Create temporary vaults
   - Move 1000 items per vault
   - Export each vault separately

2. **Process each export:**
   ```bash
   python3 1password_exporter.py inputs/batch1.1pux
   mv outputs/exported_passwords.csv outputs/batch1_passwords.csv

   python3 1password_exporter.py inputs/batch2.1pux
   mv outputs/exported_passwords.csv outputs/batch2_passwords.csv
   ```

3. **Combine CSV files:**
   ```bash
   # Keep header from first file only
   cat outputs/batch1_passwords.csv > outputs/all_passwords.csv
   tail -n +2 outputs/batch2_passwords.csv >> outputs/all_passwords.csv
   ```

4. **Import combined CSV to Apple Passwords**

### What if I want to export to other password managers?

The script can be adapted for other formats:

**For LastPass:**
- Change CSV headers to: `url,username,password,extra,name,grouping,fav`

**For Bitwarden:**
- Headers: `folder,favorite,type,name,notes,fields,login_uri,login_username,login_password,login_totp`

**For Dashlane:**
- Headers: `name,url,login,password,note,category`

Modify the `export_passwords_to_csv()` method and adjust the fieldnames and row mapping.

### Can I validate the CSV before importing?

Yes, use command-line tools:

**Check structure:**
```bash
head -n 5 outputs/exported_passwords.csv
```

**Count entries:**
```bash
wc -l outputs/exported_passwords.csv
# Subtract 1 for header
```

**Verify no empty passwords:**
```bash
awk -F',' '$4==""' outputs/exported_passwords.csv
# Should show only header if all passwords present
```

**Check for invalid characters:**
```bash
grep -P '[^\x00-\x7F]' outputs/exported_passwords.csv
# Shows lines with non-ASCII characters
```

### How do I migrate just specific categories?

Modify the `is_password_item()` method to include only desired categories:

```python
def is_password_item(self, item: Dict[str, Any]) -> bool:
    category_uuid = item.get("categoryUuid", "")

    # Only export logins and servers
    password_categories = ["001", "110"]  # Remove "005" if you don't want Password items

    return category_uuid in password_categories
```

### What is the difference between 1pux and 1pif formats?

- **1pux**: Current format (1Password 8+), ZIP archive, version 3, JSON-based
- **1pif**: Legacy format (1Password 7 and earlier), plain text, JavaScript-like syntax

This script only supports 1pux. For 1pif files, use 1Password 7 to import and then export as 1pux.

### Can I run this script on a headless server?

Yes. The script has no GUI dependencies and runs entirely in the terminal. Ensure:
- Python 3.6+ is installed
- Input file is accessible
- Output directory has write permissions
- Sufficient disk space and memory

Perfect for automated migrations on servers or in Docker containers.

---

## Still Have Questions?

If your question is not answered here:

1. Check the [README.md](README.md) for detailed technical information
2. Review the [CHANGELOG.md](CHANGELOG.md) for version-specific details
3. Examine the script source code (heavily commented)
4. Test with a small subset of your data to understand behavior

For issues or bugs:
- Include your Python version
- Include your operating system
- Include relevant error messages
- Do NOT include actual passwords or sensitive data

---

**Last Updated:** 2025-11-25
**Version:** 1.2.0
