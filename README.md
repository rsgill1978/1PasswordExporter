# 1Password to Apple Passwords Exporter | Free Migration Tool 🔐

**Migrate from 1Password to Apple Passwords in minutes** - A free, open-source Python tool that converts 1Password `.1pux` exports to Apple Passwords CSV format. Export passwords, credit cards, secure notes, and attachments with zero data loss.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/rsgill1978/1PasswordExporter)
[![Support](https://img.shields.io/badge/Support-Buy%20Me%20a%20Coffee-yellow.svg)](https://www.buymeacoffee.com/rsgill)

**Keywords**: 1Password exporter, Apple Passwords migration, password manager migration, 1Password to Apple Passwords, .1pux converter, password export tool, 1Password alternative, iCloud Keychain import, password migration tool, free password exporter

## Quick Start Guide

**Ready to migrate from 1Password to Apple Passwords?** Follow these steps:

1. **Download this tool**: Click the green **Code** button above → **Download ZIP** → Extract it
2. **Export from 1Password**: File → Export → All Items → Choose `.1pux` format
3. **Run the script**: `python3 1password_exporter.py inputs/your_export.1pux`
4. **Import to Apple Passwords**: Open Passwords app → File → Import Passwords

**No installation required** - Uses only Python standard library (3.6+).

[📖 Detailed Instructions](#usage) | [🧪 Test Before Using](#testing) | [💝 Support This Project](#support-this-project)

---

## Table of Contents

- [Quick Start Guide](#quick-start-guide)
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Testing](#testing)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Technical Details](#technical-details)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Support This Project](#support-this-project)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Why Choose This 1Password Exporter?**

Switching from 1Password to Apple Passwords (macOS Sequoia 15.0+, iOS 18.0+)? This free, open-source migration tool provides a complete solution for transferring your entire password vault while preserving all your data.

**What It Does:**
1. ✅ **Exports passwords** - Creates Apple Passwords-compatible CSV files with login credentials, URLs, and TOTP codes
2. ✅ **Preserves non-password data** - Converts credit cards, identities, secure notes, licenses, and documents to human-readable text files
3. ✅ **Extracts attachments** - Saves all file attachments alongside their parent items
4. ✅ **Handles large vaults** - Processes thousands of items from multiple accounts and vaults
5. ✅ **Cross-platform** - Works on macOS, Windows, and Linux with zero dependencies

**Perfect for**: 1Password users migrating to Apple's free Passwords app, users seeking iCloud Keychain alternatives, or anyone wanting to export 1Password data for backup purposes.

## Features

### Password Export
- Exports login credentials in Apple Passwords-compatible CSV format
- Preserves usernames, passwords, URLs, notes, and TOTP secrets
- Handles special characters and multi-line notes correctly
- Ensures proper CSV quoting for Apple Passwords compatibility

### Non-Password Data Organization
- Extracts and organizes items by category (Credit Cards, Identities, Documents, etc.)
- Exports data as **human-readable plain text files** for secure storage
- Each item gets its own folder containing a .txt file and any attachments
- Excludes unnecessary metadata (timestamps, access history)
- Maintains logical folder structure for efficient data management

### File Attachment Handling
- Extracts all file attachments alongside their parent items
- Each item's attachments stored in the same folder as its text file
- Preserves original filenames
- Handles duplicate filenames automatically

### Cross-Platform Compatibility
- Pure Python implementation (no platform-specific dependencies)
- Works on macOS, Windows, and Linux
- Uses standard library modules only
- Compatible with Python 3.6 and later

### Error Handling and Reporting
- Validates input file format
- Provides detailed progress information
- Reports errors with context
- Generates comprehensive export summary

## Why Migrate to Apple Passwords?

**Considering switching from 1Password?** Here's why users choose Apple Passwords:

- ✅ **Free** - No subscription fees (included with macOS Sequoia 15.0+ and iOS 18.0+)
- ✅ **Native integration** - Built into macOS, iOS, iPadOS, and visionOS
- ✅ **iCloud sync** - Automatic synchronization across all Apple devices
- ✅ **Family Sharing** - Share passwords with family members at no extra cost
- ✅ **Privacy-focused** - End-to-end encryption with Apple's privacy commitment
- ✅ **AutoFill** - Works seamlessly with Safari and third-party apps

**This tool vs alternatives:** Unlike manual CSV editing or paid migration services, this free open-source tool preserves ALL your data including attachments, secure notes, and TOTP codes.

## Requirements

### System Requirements
- Python 3.6 or later
- Operating System: macOS, Windows, or Linux
- Minimum 100MB free disk space (varies with vault size)
- Sufficient RAM to process the 1pux file (typically 512MB minimum)

### Python Dependencies
This script uses only Python standard library modules:
- `zipfile` - For extracting 1pux archive
- `json` - For parsing 1Password data structures
- `csv` - For generating Apple Passwords CSV
- `os` and `pathlib` - For file system operations
- `re` - For filename sanitization
- `sys` - For command-line arguments
- `datetime` - For timestamp generation

No external packages or installation required.

## Installation

### Automated Setup (Recommended)

For one-click installation and configuration, use the automated setup scripts in the `setup/` directory:

**macOS:**
```bash
cd setup
./setup_macos.sh
```

**Linux Mint / Ubuntu:**
```bash
cd setup
./setup_linux.sh
```

**Windows (PowerShell):**
```powershell
cd setup
.\setup_windows.ps1
```

The setup scripts will:
- Verify Python 3.6+ and pip are installed
- Install development tools (pylint, flake8, black, mypy)
- Auto-install 20+ VSCode extensions
- Run automated tests to verify everything works
- Display next steps

**Setup time: 2-5 minutes**

### Manual Installation

If you prefer manual setup or the automated script fails:

1. Download or clone the script to your desired location
2. Ensure Python 3.6 or later is installed on your system
3. Make the script executable (optional, Unix-like systems):

```bash
chmod +x 1password_exporter.py
```

### Verification

Verify your Python installation:

```bash
python3 --version
```

You should see output like `Python 3.x.x` where x is 6 or higher.

## Testing

The script includes a built-in test suite to verify functionality before using it with your real data. The test suite generates dummy 1Password data, processes it, and validates the output.

### Quick Test (Recommended)

Run the complete test cycle with a single command:

```bash
python3 1password_exporter.py --test-all
```

This will:
1. Generate a dummy `.1pux` test file with sample data
2. Process the test file and create output
3. Verify the output is correct
4. Clean up all test files automatically

**Expected output:**
```
Generating test .1pux file...
✓ Test file generated: inputs/test_export.1pux

Running automated tests...
Processing: inputs/test_export.1pux
✓ Tests passed successfully

Cleaning up test files...
✓ Cleanup complete
```

### Individual Test Commands

For more control, you can run test steps individually:

**Generate test data only:**
```bash
python3 1password_exporter.py --generate-test
```

Creates `inputs/test_export.1pux` with sample data including:
- Login items (with usernames, passwords, URLs, TOTP)
- Credit cards (with card numbers, expiry dates)
- Secure notes (with text content)
- Software licenses (with attachments)
- Identities (with personal information)

**Run tests only:**
```bash
python3 1password_exporter.py --test
```

Processes the test file and validates output structure. Requires `inputs/test_export.1pux` to exist (generate it first).

**Clean up test files:**
```bash
python3 1password_exporter.py --cleanup
```

Removes:
- `inputs/test_export.1pux`
- `outputs/exported_passwords.csv`
- `outputs/non_password_data/` directory and all contents

### Alternative Test Flags

The following shorthand flags are also supported:

```bash
python3 1password_exporter.py -a    # Same as --test-all
python3 1password_exporter.py -g    # Same as --generate-test
python3 1password_exporter.py -t    # Same as --test
python3 1password_exporter.py -c    # Same as --cleanup
```

### When to Run Tests

- **Before first use**: Verify the script works on your system
- **After Python upgrade**: Ensure compatibility with new Python version
- **After modifying the script**: Validate your changes didn't break functionality
- **When troubleshooting**: Isolate whether issues are with the script or your data

### Test Data Contents

The generated test file includes realistic sample data:
- Multiple accounts and vaults
- Various item types (22 different categories)
- Special characters in passwords and notes
- TOTP secrets in otpauth:// format
- Multi-line notes with Markdown
- Concealed fields (credit card numbers, CVVs)
- File attachments (dummy PDF and image files)
- Duplicate item names (to test deduplication)

The test data is completely synthetic and safe to examine.

## Usage

### Step 1: Export from 1Password

1. Open 1Password 8 or later
2. Go to File → Export → All Items
3. Choose format: "1Password Unencrypted Export (.1pux)"
4. Save the file (it will have a UUID-based name like `ABCDEF123456.1pux`)
5. Move the `.1pux` file to the `inputs` directory

**Important**: The `.1pux` file is completely unencrypted and contains all your passwords in plain text. Handle it securely.

### Step 2: Run the Exporter

Navigate to the script directory and run:

```bash
python3 1password_exporter.py inputs/your_export_file.1pux
```

#### Example

```bash
cd /Users/username/Desktop/Passwords/1PasswordExporter
python3 1password_exporter.py inputs/ABCDEF123456.1pux
```

### Step 3: Import to Apple Passwords

1. Open the Passwords app (macOS Sequoia 15.0+) or Settings → Passwords (iOS 18.0+)
2. Authenticate with Face ID, Touch ID, or passcode
3. Select File → Import Passwords (macOS) or "+" → Import from CSV (iOS)
4. Navigate to `outputs/exported_passwords.csv` in the script directory
5. Review the import preview and confirm
6. Wait for synchronization to complete

### Step 4: Secure Cleanup

After successful import:

```bash
# Delete the sensitive files
rm inputs/your_export_file.1pux
rm outputs/exported_passwords.csv

# Optional: Securely delete on macOS
srm inputs/your_export_file.1pux outputs/exported_passwords.csv
```

## Output Structure

The script creates the following directory structure:

```
1PasswordExporter/
├── 1password_exporter.py          # The main script
├── .gitignore                      # Git ignore file (excludes inputs and outputs)
├── inputs/                         # Place your .1pux files here
│   └── your_export.1pux
└── outputs/                        # All output files
    ├── exported_passwords.csv      # Apple Passwords import file
    └── non_password_data/          # Organized non-password items
        ├── Credit Card/
        │   ├── Visa Personal/
        │   │   ├── Visa_Personal.txt           # Human-readable info
        │   │   └── receipt.pdf                 # Attachment (if any)
        │   └── Mastercard Business/
        │       └── Mastercard_Business.txt
        ├── Software License/
        │   ├── Adobe Photoshop/
        │   │   ├── Adobe_Photoshop.txt
        │   │   ├── license_cert.pdf
        │   │   └── activation_code.txt
        │   └── Microsoft Office/
        │       └── Microsoft_Office.txt
        ├── Identity/
        │   └── Personal Info/
        │       ├── Personal_Info.txt
        │       └── id_scan.jpg
        ├── Secure Note/
        ├── Bank Account/
        ├── Driver License/
        └── Passport/
```

### File Formats

#### exported_passwords.csv

Apple Passwords-compatible CSV with six columns:
- `Title`: Item name
- `URL`: Website URL or identifier
- `Username`: Login username
- `Password`: Plain text password
- `Notes`: Additional information
- `OTPAuth`: TOTP URI for two-factor authentication

#### Text Files

Non-password items are exported as human-readable plain text files. Each item gets its own folder containing:

1. **A .txt file** named after the item (e.g., `Adobe_Photoshop.txt`)
2. **Any file attachments** stored in the same folder

**Example text file format:**

```
Adobe Photoshop CC 2024

BASIC INFORMATION
Category: Software License
URL: https://adobe.com

NOTES
Annual subscription - renews March 2026
Login: john.doe@example.com

DETAILS
license key: XXXX-XXXX-XXXX-XXXX-XXXX
version: CC 2024

Customer:
licensed to: John Doe
registered email: john.doe@example.com

Order:
purchase date: 2024-03-15
order number: ORD-123456789

ATTACHMENTS
This item has 3 attachment(s) in this folder:

  • license_certificate.pdf
  • purchase_receipt.pdf
  • installation_guide.pdf
```

**Key features:**
- **Clean formatting** - no redundant data type labels (e.g., "String:", "Date:", "URL:")
- **Instantly readable** on any device (phone, desktop, tablet)
- **No special software needed** - opens in any text viewer
- **Searchable** by Spotlight/Windows Search
- **Copy-paste friendly** - license keys and credentials copy cleanly
- **Cloud storage friendly** - can preview without downloading
- **Smart field handling** - dates formatted as YYYY-MM-DD, attachments listed separately

## Technical Details

For comprehensive technical documentation, see:
- **[1Password .1pux Format Specification](docs/1pux/1pux.md)** - Complete technical details of the .1pux file format
- **[Apple Passwords CSV Import Format](docs/ApplePasswords/ApplePasswords.md)** - Detailed CSV format requirements for Apple Passwords

### 1pux Format Processing

The `.1pux` file is a standard ZIP archive containing:

1. `export.attributes` - Export metadata (version, timestamp)
2. `export.data` - Main JSON payload with accounts, vaults, and items
3. `files/` - Directory containing file attachments

The script processes the structure: Accounts → Vaults → Items

### Category Classification

Items are classified by their `categoryUuid` field:

| Category UUID | Category Name | Export Destination |
|--------------|---------------|-------------------|
| 001 | Login | passwords CSV |
| 005 | Password | passwords CSV |
| 110 | Server | passwords CSV |
| 002 | Credit Card | non_password_data |
| 003 | Secure Note | non_password_data |
| 004 | Identity | non_password_data |
| 006 | Document | non_password_data |
| 100 | Software License | non_password_data |
| 101 | Bank Account | non_password_data |
| 103 | Driver License | non_password_data |
| 105 | Membership | non_password_data |
| 106 | Passport | non_password_data |
| 107 | Reward Program | non_password_data |
| 108 | Social Security Number | non_password_data |
| 109 | Wireless Router | non_password_data |
| 112 | API Credential | non_password_data |
| 114 | SSH Key | non_password_data |

### Data Extraction Logic

#### Username Extraction
Searches `loginFields` array for field with `designation: "username"`.

#### Password Extraction
Searches `loginFields` array for field with `designation: "password"`.

#### URL Extraction
Uses `overview.url` or first entry in `overview.urls` array.

#### OTP Extraction
Scans all sections for fields containing TOTP secrets, formats as `otpauth://` URI.

#### Notes Extraction
Retrieves `details.notesPlain` which supports Markdown formatting.

### File Attachment Extraction

Attachments are stored in the 1pux archive as:
```
files/<documentId>___<fileName>
```

The script:
1. Reads `documentAttributes` from item details
2. Locates files by `documentId` prefix in the archive
3. Extracts to category-specific folders
4. Handles filename conflicts with numeric suffixes

### Filename Sanitization

Filenames are sanitized for cross-platform compatibility:
- Removes invalid characters: `< > : " / \ | ? *`
- Strips leading/trailing dots and spaces
- Truncates to 200 characters
- Provides fallback names for empty titles

### CSV Generation

The CSV follows Apple Passwords requirements:
- UTF-8 encoding without BOM
- Comma delimiter
- All fields quoted (`csv.QUOTE_ALL`)
- CRLF line terminators (automatic on Windows)
- Exact header order: `Title,URL,Username,Password,Notes,OTPAuth`

## Security Considerations

### Sensitive Data Handling

**Critical Security Warnings:**

1. **Plain Text Exposure**: Both `.1pux` files and the generated CSV contain passwords in plain text
2. **File System Security**: Ensure export directory has appropriate permissions (chmod 700 on Unix)
3. **Memory Exposure**: The script loads data into memory; close other applications on shared systems
4. **Network Isolation**: Run the script offline to prevent potential network-based attacks
5. **Secure Deletion**: Use secure deletion tools after import completion

### Recommended Security Practices

#### Before Export
- Ensure your device is not infected with malware
- Close unnecessary applications
- Disable cloud sync for the output directory
- Work in a private environment

#### During Export
- Do not leave computer unattended
- Do not run on shared or public computers
- Monitor system activity for unusual processes

#### After Export
- Verify successful import to Apple Passwords
- Use secure deletion tools:
  - macOS: `srm` (if available) or FileVault secure empty trash
  - Linux: `shred` or `wipe`
  - Windows: `sdelete` or built-in secure delete
- Clear clipboard if any passwords were copied
- Restart computer to clear memory (optional but recommended for sensitive vaults)

### File Permissions

The script does not automatically set restrictive permissions. Manually secure the directory:

```bash
# Unix-like systems
chmod 700 1PasswordExporter
chmod 700 1PasswordExporter/inputs
chmod 700 1PasswordExporter/outputs
chmod 600 inputs/*.1pux
chmod 600 outputs/exported_passwords.csv
```

## Troubleshooting

### Common Issues

#### Error: Input file does not exist
**Cause**: Incorrect file path or filename
**Solution**:
- Verify the file is in the `inputs/` directory
- Check for typos in the filename
- Use absolute path if needed: `/full/path/to/file.1pux`

#### Error: Input file is not a valid ZIP archive
**Cause**: Corrupted or incomplete download
**Solution**:
- Re-export from 1Password
- Verify file size (should be at least several KB)
- Check file integrity: `unzip -t your_file.1pux`

#### Warning: Expected format version 3, found X
**Cause**: Different 1pux format version (future or older)
**Solution**:
- Script proceeds anyway but verify output
- Report issue if export fails
- Update 1Password to latest version

#### Partial import or missing items
**Cause**:
- Invalid URL formats
- Malformed TOTP URIs
- Unsupported characters in CSV

**Solution**:
- Check `outputs/exported_passwords.csv` in text editor
- Verify URLs include protocol (`https://`)
- Review error messages in export summary
- Split large CSV files (<2000 entries per file)

#### Attachments not extracted
**Cause**: Missing files in 1pux archive or corrupted entries
**Solution**:
- Check export summary for specific error messages
- Verify attachments exist in original 1Password vault
- Try exporting individual items with attachments

#### Script crashes or hangs
**Cause**: Insufficient memory for large vaults
**Solution**:
- Close other applications
- Process vault in smaller batches (export subsets from 1Password)
- Increase system swap space
- Use a system with more RAM

### Debug Mode

For detailed debugging, modify the script to add verbose output:

```python
# Add at the beginning of process_1pux_file method
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Validation

Verify CSV format before importing:

```bash
# Check CSV structure
head -n 5 outputs/exported_passwords.csv

# Count entries
wc -l outputs/exported_passwords.csv

# Verify encoding
file outputs/exported_passwords.csv
# Should show: UTF-8 Unicode text
```

### Apple Passwords Import Errors

If Apple Passwords reports errors:

1. **Missing column labels**: Verify first line is exactly `Title,URL,Username,Password,Notes,OTPAuth`
2. **Garbled characters**: Convert to UTF-8 without BOM
3. **Some entries skipped**: Check URL validity (must include `https://` or `http://`)
4. **Duplicate entries**: Apple Passwords may skip duplicates; manually merge if needed

## Known Limitations

### Current Limitations

1. **Password History**: Not included in CSV export (space constraints)
2. **Custom Icons**: Not extracted (Apple Passwords uses favicons)
3. **Linked Items**: References between items are not preserved
4. **Shared Vaults**: All items treated equally (sharing info not in Apple Passwords)
5. **Passkeys**: Not supported by CSV import format
6. **Wi-Fi Credentials**: Cannot be imported via CSV to Apple Passwords

### Apple Passwords CSV Import Constraints

1. **File Size**: Recommended maximum 2000 entries per CSV
2. **No Hierarchy**: All items imported to flat list (no folders)
3. **No Custom Fields**: Only six standard columns supported
4. **URL Format**: Must include protocol or autofill may not work
5. **No Metadata**: Creation dates, modification dates not preserved
6. **Character Limits**:
   - Titles: 255 characters
   - URLs: 2048 characters
   - Passwords: 128 characters

### Platform-Specific Notes

#### macOS
- Requires macOS Sequoia 15.0 or later
- Uses standalone Passwords.app
- Best import performance

#### iOS/iPadOS
- Requires iOS 18.0 or later
- Import via Settings → Passwords
- May be slower for large files (>1000 entries)

#### Windows/Linux
- Cannot directly import to Apple Passwords
- Use generated CSV as intermediate format
- Transfer CSV to macOS/iOS device for import

## Support This Project

If this tool saved you time and money, consider buying me a coffee:

**[☕ Buy Me a Coffee](https://www.buymeacoffee.com/rsgill)** ← Click here to support

<a href="https://www.buymeacoffee.com/rsgill" target="_blank"><img src=".github/assets/buymeacoffee-qr.png" alt="Buy Me a Coffee QR Code" width="200"></a>

Or scan the QR code above. Your support helps maintain and improve this tool!

## Contributing

This is a standalone utility script. Contributions, bug reports, and feature requests are welcome.

### Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version (`python3 --version`)
- 1Password version used for export
- Error messages (full output)
- Approximate vault size (number of items)

Do not include actual passwords or sensitive data in reports.

### Development

The script is designed to be self-contained with no external dependencies for ease of distribution and security auditing.

When modifying:
1. Maintain Python 3.6+ compatibility
2. Use only standard library modules
3. Follow existing code style
4. Test with various vault sizes and item types
5. Ensure cross-platform compatibility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Users are responsible for:
- Securing sensitive data throughout the export process
- Complying with applicable data protection regulations
- Verifying export completeness and accuracy
- Proper disposal of temporary files

For full license text and conditions, please refer to the [LICENSE](LICENSE) file.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Frequently Asked Questions

### Common Migration Questions

**Q: Can I migrate from 1Password to Apple Passwords for free?**
A: Yes! This tool is completely free and open-source. Apple Passwords is also free (included with macOS Sequoia 15.0+ and iOS 18.0+).

**Q: Will I lose any data when exporting from 1Password?**
A: No. This tool exports ALL data including passwords, TOTP codes, credit cards, secure notes, identities, documents, and file attachments.

**Q: Is it safe to export my 1Password data?**
A: The .1pux file is unencrypted, so treat it carefully. Follow our [security best practices](#security-considerations). Delete the export file immediately after successful import.

**Q: How long does the migration take?**
A: For most users, 5-10 minutes total. Export from 1Password (2 min) → Run script (1 min) → Import to Apple Passwords (2-5 min).

**Q: Can I migrate TOTP/2FA codes?**
A: Yes! The tool exports TOTP secrets in the correct format for Apple Passwords.

**Q: What about my credit cards and secure notes?**
A: Non-password items are exported as organized, human-readable text files perfect for secure storage (NordLocker, encrypted drives, etc.).

See [FAQ.md](FAQ.md) for more questions and detailed answers.

---

**Version**: 1.2.0
**Last Updated**: 2025-11-25
**Python Compatibility**: 3.6+
**Platform**: Cross-platform (macOS, Windows, Linux)

**Found this helpful?** [☕ Buy me a coffee](https://www.buymeacoffee.com/rsgill)
