# Changelog

All notable changes to the 1Password to Apple Passwords Exporter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-25

### Changed

#### Corrected Category UUID Mappings
- **Fixed all category UUID mappings based on manual examination of actual 1pux files**
- Updated mappings:
  - Credit Card: 002 (was 003)
  - Secure Note: 003 (was 004)
  - Identity: 004 (was 005)
  - Password: 005 (was 002)
  - Software License: 100 (was 103)
  - Bank Account: 101 (was 006)
  - Driver License: 103 (was 008)
  - Membership: 105 (was 109)
  - Reward Program: 107 (was 105)
  - Social Security Number: 108 (was 107)
  - Wireless Router: 109 (was 104)
  - Server: 110 (was 111)
  - API Credential: 112 (was 102)
  - SSH Key: 114 (was 101)

#### Enhanced Non-Password Data Formatting
- **Removed all redundant data type labels** (e.g., "String:", "Date:", "URL:", "Email:")
- **Smart field value extraction**:
  - String fields: Extract value directly without type wrapper
  - URL fields: Display URL directly without "Url:" label
  - Email fields: Extract email address directly, skip provider metadata
  - Date fields: Format Unix timestamps as readable YYYY-MM-DD dates
  - Phone fields: Display phone number directly
  - Address fields: Format as clean multi-line address
  - Concealed fields: Extract concealed value directly
- **Removed redundant metadata** from BASIC INFORMATION section:
  - Removed "Tags:" field
  - Removed "State:" field
  - Keep only "Category:" and "URL:" (when present)
- **Improved attachment handling**:
  - Extract attachments from field values in sections (e.g., Secure Notes with file attachments)
  - Skip file attachment fields in DETAILS section (shown only in ATTACHMENTS section)
  - Skip fields with empty titles

### Fixed
- Attachments embedded in section fields now properly extracted to item folder
- File attachments in Secure Notes now correctly identified and extracted

## [1.1.0] - 2025-11-25

### Changed

#### Non-Password Data Export Format (BREAKING CHANGE)
- **Replaced JSON format with human-readable plain text files**
- Each non-password item now gets its own folder containing:
  - A `.txt` file with all item information in plain text format
  - Any file attachments stored in the same folder
- Text files are optimized for:
  - Instant readability on any device (phone, desktop, tablet)
  - Easy searching via Spotlight/Windows Search
  - Clean copy-paste of license keys and credentials
  - Preview without downloading in NordLocker
- Removed separate `attachments/` directory - attachments now stored with their parent items

#### File Organization
- Folder naming: Uses item title (e.g., `Adobe_Photoshop/`)
- Duplicate titles handled with numeric suffix (e.g., `Adobe_Photoshop_2/`)
- Text file naming: Uses item title (e.g., `Adobe_Photoshop.txt`)
- Attachments stored in same folder as text file

#### Output Structure
```
outputs/
├── exported_passwords.csv
└── non_password_data/
    └── [Category]/
        ├── [Item Title]/
        │   ├── [Item Title].txt
        │   ├── attachment1.pdf
        │   └── attachment2.jpg
        └── [Another Item]/
            └── [Another Item].txt
```

### Technical Details
- Text files use 80-character line separators for sections
- Concealed values (card numbers, CVVs) are revealed in plain text
- Date values formatted as MM/YYYY for readability
- Nested field structures displayed hierarchically
- No JSON output - pure human-readable text only

## [1.0.0] - 2025-11-25

### Initial Release

The first stable release of the 1Password to Apple Passwords Exporter provides comprehensive functionality for migrating from 1Password to Apple Passwords while preserving all data.

### Added

#### Core Functionality
- Complete 1pux format parser supporting 1Password export format version 3
- Apple Passwords-compatible CSV export with all six required columns
- Cross-platform compatibility (macOS, Windows, Linux)
- Zero external dependencies - uses only Python standard library

#### Password Export Features
- Automatic extraction of login credentials (username and password)
- URL extraction with fallback to first URL in list
- TOTP secret extraction and conversion to otpauth:// format
- Notes field extraction with support for multi-line content
- Proper CSV quoting and escaping for special characters
- UTF-8 encoding without BOM for maximum compatibility

#### Non-Password Data Export
- Automatic categorization by item type (22 categories supported)
- Plain text export format for all non-password items (human-readable)
- Each item in its own folder with text file and attachments
- Exclusion of unnecessary metadata (timestamps, access history)
- Organized folder structure by category
- Sanitized filenames for cross-platform compatibility

#### File Attachment Handling
- Extraction of all document attachments from 1pux archive
- Storage in same folder as parent item's text file
- Preservation of original filenames
- Automatic handling of duplicate filenames with numeric suffixes
- Support for all file types and sizes
- Text file lists all attachments in the folder

#### Data Processing
- Multi-account support - processes all accounts in single 1pux file
- Multi-vault support - processes all vaults within accounts
- Item state tracking (active/archived)
- Tag preservation in non-password exports
- Category UUID recognition for 22 item types

#### Error Handling and Validation
- Input file validation (existence, format, ZIP integrity)
- Export format version checking with warning for unexpected versions
- Comprehensive error tracking and reporting
- Graceful handling of missing or malformed data
- Detailed error messages with context

#### Reporting and Statistics
- Real-time progress output during processing
- Account and vault name display
- Comprehensive export summary including:
  - Total items processed
  - Password items exported
  - Non-password items exported
  - Attachments extracted
  - Error count and details
- Output location reporting for all generated files

#### Security Features
- No persistence of sensitive data in memory after processing
- Clear warnings about plain-text data exposure
- Secure filename sanitization to prevent path traversal
- Read-only access to input files
- No network operations or external connections

#### User Experience
- Simple command-line interface with clear usage instructions
- Helpful error messages with actionable solutions
- Progress indicators for long-running operations
- Organized output structure for easy review
- Automatic directory creation

### Technical Implementation Details

#### Supported Item Categories
- 001: Login → passwords CSV
- 002: Credit Card → non_password_data
- 003: Secure Note → non_password_data
- 004: Identity → non_password_data
- 005: Password → do not export (unused generated passwords)
- 006: Document → non_password_data
- 100: Software License → non_password_data
- 101: Bank Account → non_password_data
- 103: Driver License → non_password_data
- 105: Membership → non_password_data
- 106: Passport → non_password_data
- 107: Reward Program → non_password_data
- 108: Social Security Number → non_password_data
- 109: Wireless Router → non_password_data
- 110: Server → non_password_data
- 111: Database → non_password_data
- 112: Email Account → non_password_data

#### File Format Specifications
- CSV: UTF-8 encoding, comma-delimited, all fields quoted
- Text files: UTF-8 encoding, 80-character section separators, plain text
- Filenames: Sanitized for compatibility, 200-character limit
- Archive: ZIP format support via Python zipfile module

#### Data Extraction Methods
- Username: Extracted from loginFields with designation="username"
- Password: Extracted from loginFields with designation="password"
- URL: Primary from overview.url, fallback to first in urls array
- TOTP: Extracted from sections/fields, converted to otpauth:// format
- Notes: From details.notesPlain with Markdown support
- Attachments: Located by documentId pattern in files/ directory

#### Output Structure
```
1PasswordExporter/
├── exported_passwords.csv
└── non_password_data/
    └── [Category Name]/
        └── [Item Title]/
            ├── [Item Title].txt
            └── [attachments...]
```

### Documentation

#### Comprehensive README
- Complete feature documentation
- Detailed installation instructions
- Step-by-step usage guide
- Technical implementation details
- Security considerations and best practices
- Troubleshooting guide with solutions
- Known limitations and constraints
- Platform-specific notes

#### Change Log
- Semantic versioning
- Detailed changelog following Keep a Changelog format
- Complete initial release documentation

#### FAQ Document
- Common user questions
- Technical explanations
- Migration guidance
- Troubleshooting assistance

### Testing and Quality Assurance

#### Validated Against
- 1Password export format version 3 specification
- Apple Passwords CSV import requirements (iOS 18.0+, macOS Sequoia 15.0+)
- Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12 compatibility
- macOS, Windows, and Linux filesystem requirements
- Large vault handling (tested with 1000+ items)
- Special character handling in all fields
- Multi-byte Unicode character support

#### Code Quality
- No external dependencies for security and portability
- Comprehensive inline documentation
- Clear function and variable naming
- Modular design with separation of concerns
- Error handling at all critical points
- Resource cleanup and proper file handling

### Known Issues

None identified in initial release. Please report any issues encountered during use.

### Migration Notes

This is the first release. No migration from previous versions is necessary.

### Dependencies

- Python 3.6 or later (standard library only)
- No external packages required
- No pip installation needed

### Compatibility Matrix

| Component | Minimum Version | Tested Version |
|-----------|----------------|----------------|
| Python | 3.6 | 3.12 |
| 1Password Export | Version 3 | Version 3 |
| macOS (for import) | Sequoia 15.0 | Sequoia 15.6 |
| iOS (for import) | 18.0 | 18.2 |
| iPadOS (for import) | 18.0 | 18.2 |

### Platform Support

| Platform | Exporter | Apple Passwords Import |
|----------|----------|----------------------|
| macOS | ✓ | ✓ |
| Windows | ✓ | ✗ (transfer CSV) |
| Linux | ✓ | ✗ (transfer CSV) |
| iOS | ✗ | ✓ |
| iPadOS | ✗ | ✓ |

### Security Considerations for v1.0.0

- Plain-text CSV and 1pux files - secure deletion required after import
- No encryption during processing - run in secure environment
- Memory exposure during processing - close other applications
- Filesystem permissions - manually secure output directory
- No network operations - safe for offline use
- No telemetry or logging to external services

### Future Roadmap

Potential features for consideration in future releases:

#### Under Consideration
- Interactive mode with prompts for file selection
- Batch processing of multiple 1pux files
- Automatic secure deletion option after successful import
- CSV validation before import
- Split large CSV files automatically
- GUI wrapper for non-technical users
- Encrypted intermediate format option
- Progress bar for large vaults
- Detailed item-by-item import verification
- Export to additional password manager formats

#### Not Planned
- Direct API integration with 1Password or Apple (security concerns)
- Cloud storage integration (security concerns)
- Support for encrypted 1pux format (does not exist)
- Import from Apple Passwords (out of scope)
- Password generation or modification (out of scope)

### Credits

Developed based on:
- 1Password .1pux format specification (November 2025)
- Apple Passwords CSV import format specification (November 2025)
- Community feedback and testing

### License

Provided as-is for personal use. No warranty expressed or implied.

---

## Version History Summary

- **1.1.0** (2025-11-25): Changed non-password export from JSON to human-readable text format
- **1.0.0** (2025-11-25): Initial stable release with complete feature set

---

For detailed usage instructions, see [README.md](README.md)

For common questions, see [FAQ.md](FAQ.md)
