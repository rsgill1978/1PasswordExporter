#!/usr/bin/env python3
"""
1Password to Apple Passwords Exporter

This script exports passwords from a 1Password .1pux file to an Apple Passwords-compatible CSV format.
Non-password data is organized into separate folders for later storage in NordLocker.

License: MIT License
Copyright (c) 2025 1Password Exporter Contributors
See LICENSE file for full license text.
"""

import zipfile
import json
import csv
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class PasswordExporter:
    """Main class for exporting 1Password data to Apple Passwords format."""

    # Category UUID mappings based on manual examination of 1pux file
    CATEGORY_NAMES = {
        "001": "Login",
        "002": "Credit Card",
        "003": "Secure Note",
        "004": "Identity",
        "005": "Password",
        "006": "Document",
        "100": "Software License",
        "101": "Bank Account",
        "103": "Driver License",
        "105": "Membership",
        "106": "Passport",
        "107": "Reward Program",
        "108": "Social Security Number",
        "109": "Wireless Router",
        "110": "Server",
        "112": "API Credential",
        "114": "SSH Key"
    }

    def __init__(self, input_file: str, output_dir: str = None):
        """Initialize the exporter with input file path."""
        self.input_file = input_file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = output_dir if output_dir else os.path.join(script_dir, "outputs")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Clean output directory if it exists
        if os.path.exists(self.output_dir):
            import shutil
            shutil.rmtree(self.output_dir)

        # Create output directories
        self.passwords_csv_path = os.path.join(self.output_dir, "exported_passwords.csv")
        self.non_password_dir = os.path.join(self.output_dir, "non_password_data")

        # Statistics
        self.stats = {
            "total_items": 0,
            "password_items": 0,
            "non_password_items": 0,
            "skipped_items": 0,
            "attachments_extracted": 0,
            "errors": []
        }

    def validate_input_file(self) -> bool:
        """Validate that the input file exists and is a valid .1pux file."""
        if not os.path.exists(self.input_file):
            print(f"Error: Input file '{self.input_file}' does not exist.")
            return False

        if not self.input_file.lower().endswith('.1pux'):
            print(f"Warning: Input file does not have .1pux extension.")

        if not zipfile.is_zipfile(self.input_file):
            print(f"Error: Input file is not a valid ZIP archive.")
            return False

        return True

    def create_output_directories(self):
        """Create necessary output directories."""
        os.makedirs(self.non_password_dir, exist_ok=True)

    def extract_username(self, item: Dict[str, Any]) -> str:
        """Extract username from login fields."""
        details = item.get("details", {})
        login_fields = details.get("loginFields", [])

        for field in login_fields:
            if field.get("designation") == "username":
                return field.get("value", "")

        return ""

    def extract_password(self, item: Dict[str, Any]) -> str:
        """Extract password from login fields."""
        details = item.get("details", {})
        login_fields = details.get("loginFields", [])

        for field in login_fields:
            if field.get("designation") == "password":
                return field.get("value", "")

        return ""

    def extract_url(self, item: Dict[str, Any]) -> str:
        """Extract primary URL from overview."""
        overview = item.get("overview", {})
        url = overview.get("url", "")

        if not url and overview.get("urls"):
            urls = overview.get("urls", [])
            if urls and len(urls) > 0:
                url = urls[0].get("url", "")

        return url if url else ""

    def extract_notes(self, item: Dict[str, Any]) -> str:
        """Extract notes from details."""
        details = item.get("details", {})
        return details.get("notesPlain", "")

    def extract_otp(self, item: Dict[str, Any]) -> str:
        """Extract OTP authentication URI from sections."""
        details = item.get("details", {})
        sections = details.get("sections", [])

        for section in sections:
            fields = section.get("fields", [])
            for field in fields:
                value = field.get("value", {})
                if isinstance(value, dict):
                    otp = value.get("totp", "")
                    if otp:
                        if otp.startswith("otpauth://"):
                            return otp
                        else:
                            return f"otpauth://totp/?secret={otp}"

        return ""

    def is_password_item(self, item: Dict[str, Any]) -> bool:
        """Determine if an item should be included in the passwords CSV."""
        category_uuid = item.get("categoryUuid", "")

        # Only export Login items to passwords CSV
        # 005 (Password) = unused generated passwords, not exported
        # 110 (Server) = exported to non_password_data instead
        password_categories = ["001"]  # Login only

        return category_uuid in password_categories

    def export_passwords_to_csv(self, items: List[Dict[str, Any]]):
        """Export password items to Apple Passwords CSV format."""
        password_items = [item for item in items if self.is_password_item(item)]

        # Track duplicate titles
        title_counts = {}

        with open(self.passwords_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

            writer.writeheader()

            for item in password_items:
                overview = item.get("overview", {})
                base_title = overview.get("title", "Untitled")

                # Handle duplicate titles
                if base_title in title_counts:
                    title_counts[base_title] += 1
                    title = f"{base_title}_{title_counts[base_title]}"
                else:
                    title_counts[base_title] = 1
                    title = base_title

                row = {
                    'Title': title,
                    'URL': self.extract_url(item),
                    'Username': self.extract_username(item),
                    'Password': self.extract_password(item),
                    'Notes': self.extract_notes(item),
                    'OTPAuth': self.extract_otp(item)
                }

                writer.writerow(row)

        # Count actual rows written (excluding header)
        self.stats["password_items"] = len(password_items)
        print(f"Exported {self.stats['password_items']} password items to: {self.passwords_csv_path}")

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be filesystem-safe."""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename[:200] if filename else "unnamed"

    def format_field_value(self, value: Any, indent: int = 0) -> str:
        """Format a field value for human-readable text output."""
        indent_str = "  " * indent

        if value is None:
            return f"{indent_str}(empty)"
        elif isinstance(value, dict):
            # Handle special field types - these are type-wrapped values from 1Password
            # Extract the actual value without showing the type wrapper

            if "concealed" in value:
                # Concealed field (password, PIN, etc.)
                return f"{indent_str}{value['concealed']}"
            elif "string" in value:
                # String field - extract value directly
                return f"{indent_str}{value['string']}"
            elif "date" in value:
                # Date field - format Unix timestamp as readable date
                try:
                    from datetime import datetime
                    date_val = int(value['date'])
                    formatted_date = datetime.fromtimestamp(date_val).strftime("%Y-%m-%d")
                    return f"{indent_str}{formatted_date}"
                except:
                    return f"{indent_str}{value['date']}"
            elif "monthYear" in value:
                # Month/Year field - format as MM/YYYY
                my = str(value['monthYear'])
                if len(my) == 6:
                    return f"{indent_str}{my[4:6]}/{my[0:4]}"
                return f"{indent_str}{my}"
            elif "url" in value:
                # URL field - extract URL directly
                return f"{indent_str}{value['url']}"
            elif "email" in value:
                # Email field - extract email address directly
                email_data = value['email']
                if isinstance(email_data, dict):
                    return f"{indent_str}{email_data.get('email_address', email_data.get('emailAddress', ''))}"
                return f"{indent_str}{email_data}"
            elif "phone" in value:
                # Phone field - extract phone number directly
                return f"{indent_str}{value['phone']}"
            elif "address" in value:
                # Address field - format address components
                addr = value['address']
                if isinstance(addr, dict):
                    # Format multi-line address
                    parts = []
                    if addr.get('street'): parts.append(addr['street'])
                    city_line = []
                    if addr.get('city'): city_line.append(addr['city'])
                    if addr.get('state'): city_line.append(addr['state'])
                    if addr.get('zip'): city_line.append(addr['zip'])
                    if city_line: parts.append(', '.join(city_line))
                    if addr.get('country'): parts.append(addr['country'])
                    return '\n'.join([f"{indent_str}{part}" for part in parts])
                return f"{indent_str}{addr}"
            elif "totp" in value:
                # TOTP field
                return f"{indent_str}{value['totp']}"
            elif "file" in value:
                # File attachment - don't display in field value
                file_info = value['file']
                return f"{indent_str}[Attachment: {file_info.get('fileName', 'unknown')}]"
            elif "creditCardNumber" in value:
                # Credit card number
                return f"{indent_str}{value['creditCardNumber']}"
            elif "creditCardType" in value:
                # Credit card type
                return f"{indent_str}{value['creditCardType']}"
            elif "gender" in value:
                # Gender field
                return f"{indent_str}{value['gender']}"
            elif "menu" in value:
                # Menu selection
                return f"{indent_str}{value['menu']}"
            elif "reference" in value:
                # Reference to another item
                return f"{indent_str}[Reference: {value['reference']}]"
            else:
                # Nested object without known type wrapper
                # Check if it's a simple key-value that should be extracted
                if len(value) == 1:
                    # Single key dict - might be a type wrapper we don't know about
                    key, val = list(value.items())[0]
                    # If the value is a simple type, just return it
                    if isinstance(val, (str, int, float, bool)):
                        return f"{indent_str}{val}"

                # Complex nested object - format recursively but skip type wrappers
                result = []
                for k, v in value.items():
                    # Skip common metadata fields
                    if k in ['provider', 'Provider']:
                        continue
                    formatted_key = k.replace("_", " ").replace("Address", "").replace("address", "").title().strip()
                    if not formatted_key:
                        continue
                    formatted_val = self.format_field_value(v, indent + 1)
                    # Only add if there's actual content
                    if formatted_val.strip() and formatted_val.strip() != "(empty)":
                        result.append(f"{indent_str}{formatted_key}:\n{formatted_val}")
                return "\n".join(result) if result else f"{indent_str}(empty)"
        elif isinstance(value, list):
            if not value:
                return f"{indent_str}(none)"
            return "\n".join([f"{indent_str}• {item}" for item in value])
        else:
            return f"{indent_str}{value}"

    def export_non_password_item(self, item: Dict[str, Any], category_name: str, zip_ref: zipfile.ZipFile):
        """Export a single non-password item as human-readable text with attachments in a folder."""
        category_dir = os.path.join(self.non_password_dir, self.sanitize_filename(category_name))
        os.makedirs(category_dir, exist_ok=True)

        overview = item.get("overview", {})
        title = overview.get("title", "Untitled")
        safe_title = self.sanitize_filename(title)

        # Create folder for this item (use title only, handle duplicates with counter)
        item_folder = os.path.join(category_dir, safe_title)

        # Handle duplicate folder names
        if os.path.exists(item_folder):
            counter = 2
            while os.path.exists(os.path.join(category_dir, f"{safe_title}_{counter}")):
                counter += 1
            item_folder = os.path.join(category_dir, f"{safe_title}_{counter}")

        os.makedirs(item_folder, exist_ok=True)

        # Create text filename using item title
        text_filename = f"{safe_title}.txt"
        text_path = os.path.join(item_folder, text_filename)

        # Build human-readable text content
        content_lines = []
        content_lines.append(f"{title}")
        content_lines.append("")

        # Basic metadata
        content_lines.append("BASIC INFORMATION")
        content_lines.append(f"Category: {category_name}")

        url = self.extract_url(item)
        if url:
            content_lines.append(f"URL: {url}")

        content_lines.append("")

        # Notes section
        notes = self.extract_notes(item)
        if notes:
            content_lines.append("NOTES")
            content_lines.append(notes)
            content_lines.append("")

        # Details section - parse all fields
        details = item.get("details", {})
        sections = details.get("sections", [])

        if sections:
            # Collect detail lines first to check if there's any content
            detail_lines = []

            for section in sections:
                section_title = section.get("title", "")
                section_lines = []

                fields = section.get("fields", [])
                for field in fields:
                    field_title = field.get("title", "")
                    field_value = field.get("value", "")

                    # Skip fields that are file attachments (they'll be listed in ATTACHMENTS section)
                    if isinstance(field_value, dict) and "file" in field_value:
                        continue

                    # Skip fields with no title (usually auto-generated fields)
                    if not field_title:
                        continue

                    # Format the field value first
                    formatted_value = self.format_field_value(field_value)

                    # Skip only if formatted value is empty, None, or placeholder text after formatting
                    if not formatted_value or formatted_value.strip() in ["", "(empty)", "None"]:
                        continue

                    section_lines.append(f"{field_title}: {formatted_value}")

                # Only add section if it has content
                if section_lines:
                    if section_title:
                        detail_lines.append(f"\n{section_title}:")
                    detail_lines.extend(section_lines)

            # Only add DETAILS header if there's actual content
            if detail_lines:
                content_lines.append("DETAILS")
                content_lines.extend(detail_lines)
                content_lines.append("")

        # Check for attachments and extract them to the same folder
        attachment_files = self.extract_attachment_to_folder(zip_ref, item, item_folder)

        if attachment_files:
            content_lines.append("ATTACHMENTS")
            content_lines.append(f"This item has {len(attachment_files)} attachment(s) in this folder:")
            content_lines.append("")
            for filename in attachment_files:
                content_lines.append(f"  • {filename}")
            content_lines.append("")

        # Write text file
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content_lines))

        self.stats["non_password_items"] += 1

    def extract_single_file(self, zip_ref: zipfile.ZipFile, document_id: str, filename: str, item_folder: str) -> Optional[str]:
        """Extract a single file from the archive. Returns the extracted filename or None."""
        try:
            # Try to find the file in the archive
            for zip_info in zip_ref.filelist:
                if zip_info.filename.startswith(f"files/{document_id}"):
                    safe_filename = self.sanitize_filename(filename)
                    output_path = os.path.join(item_folder, safe_filename)

                    # Handle duplicate filenames
                    counter = 1
                    base_name, ext = os.path.splitext(safe_filename)
                    while os.path.exists(output_path):
                        safe_filename = f"{base_name}_{counter}{ext}"
                        output_path = os.path.join(item_folder, safe_filename)
                        counter += 1

                    with zip_ref.open(zip_info.filename) as source, open(output_path, 'wb') as target:
                        target.write(source.read())

                    self.stats["attachments_extracted"] += 1
                    return safe_filename

            self.stats["errors"].append(f"Attachment not found in archive: {filename} (ID: {document_id})")
            return None

        except Exception as e:
            self.stats["errors"].append(f"Error extracting attachment {filename}: {str(e)}")
            return None

    def extract_attachment_to_folder(self, zip_ref: zipfile.ZipFile, item: Dict[str, Any], item_folder: str) -> List[str]:
        """Extract file attachments to the item's folder. Returns list of extracted filenames."""
        extracted_files = []
        details = item.get("details", {})

        # Extract from documentAttributes (Document category items)
        doc_attrs = details.get("documentAttributes")
        if doc_attrs:
            document_id = doc_attrs.get("documentId")
            filename = doc_attrs.get("fileName", "unknown")
            if document_id:
                result = self.extract_single_file(zip_ref, document_id, filename, item_folder)
                if result:
                    extracted_files.append(result)

        # Extract from field values in sections (e.g., Secure Notes with attachments)
        sections = details.get("sections", [])
        for section in sections:
            fields = section.get("fields", [])
            for field in fields:
                field_value = field.get("value", {})
                if isinstance(field_value, dict) and "file" in field_value:
                    file_info = field_value["file"]
                    document_id = file_info.get("documentId")
                    filename = file_info.get("fileName", "unknown")
                    if document_id:
                        result = self.extract_single_file(zip_ref, document_id, filename, item_folder)
                        if result:
                            extracted_files.append(result)

        return extracted_files

    def process_1pux_file(self):
        """Main processing function to parse and export 1pux data."""
        print(f"Processing 1Password export file: {self.input_file}")

        try:
            with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
                # Read and validate export attributes
                attributes = json.loads(zip_ref.read('export.attributes').decode('utf-8'))
                version = attributes.get("version")
                print(f"Export format version: {version}")

                if version != 3:
                    print(f"Warning: Expected format version 3, found {version}. Proceeding anyway...")

                # Read main data
                data = json.loads(zip_ref.read('export.data').decode('utf-8'))

                # Process all accounts and vaults
                all_items = []

                for account in data.get("accounts", []):
                    account_name = account.get("attrs", {}).get("accountName", "Unknown")
                    print(f"\nProcessing account: {account_name}")

                    for vault in account.get("vaults", []):
                        vault_name = vault.get("attrs", {}).get("name", "Unknown")
                        print(f"  Processing vault: {vault_name}")

                        items = vault.get("items", [])
                        all_items.extend(items)

                        for idx, item in enumerate(items):
                            self.stats["total_items"] += 1
                            category_uuid = item.get("categoryUuid", "unknown")
                            category_name = self.CATEGORY_NAMES.get(category_uuid, f"Category_{category_uuid}")

                            # Skip category 005 (Password) - unused generated passwords
                            if category_uuid == "005":
                                self.stats["skipped_items"] += 1
                                continue

                            if not self.is_password_item(item):
                                # Export non-password data (includes attachment extraction)
                                self.export_non_password_item(item, category_name, zip_ref)

                # Export all passwords to CSV
                self.export_passwords_to_csv(all_items)

        except Exception as e:
            print(f"Error processing 1pux file: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        return True

    def print_summary(self):
        """Print summary of export operation."""
        print("\n" + "="*60)
        print("EXPORT SUMMARY")
        print("="*60)
        print(f"Total items in .1pux file: {self.stats['total_items']}")
        print(f"Password items exported (CSV): {self.stats['password_items']}")
        print(f"Non-password items exported (text files): {self.stats['non_password_items']}")
        print(f"Items skipped (category 005 - unused passwords): {self.stats['skipped_items']}")
        print(f"Attachments extracted: {self.stats['attachments_extracted']}")

        if self.stats["errors"]:
            print(f"\nErrors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"][:10]:
                print(f"  - {error}")
            if len(self.stats["errors"]) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more")

        print("\nOutput locations:")
        print(f"  Passwords CSV: {self.passwords_csv_path}")
        print(f"  Non-password data: {self.non_password_dir}")
        print(f"    (Each item stored in its own folder with attachments)")
        print("="*60)

    def run(self) -> bool:
        """Execute the full export process."""
        if not self.validate_input_file():
            return False

        self.create_output_directories()

        success = self.process_1pux_file()

        if success:
            self.print_summary()

        return success


def generate_test_file(output_path: str = None) -> str:
    """Generate a dummy .1pux file for testing purposes."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if output_path is None:
        output_path = os.path.join(script_dir, "inputs", "test_data.1pux")

    # Ensure inputs directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create comprehensive test data with multiple item types
    test_data = {
        "accounts": [{
            "attrs": {
                "accountName": "Test User",
                "name": "Test User",
                "email": "test@example.com",
                "uuid": "TEST_ACCOUNT_UUID_123",
                "domain": "https://my.1password.com/"
            },
            "vaults": [{
                "attrs": {
                    "uuid": "TEST_VAULT_UUID_001",
                    "name": "Test Vault",
                    "desc": "Test vault for validation",
                    "avatar": "vault-avatar.png",
                    "type": "P"
                },
                "items": [
                    # Login item
                    {
                        "uuid": "test_login_001",
                        "favIndex": 1,
                        "createdAt": 1700000000,
                        "updatedAt": 1700100000,
                        "state": "active",
                        "categoryUuid": "001",
                        "overview": {
                            "title": "Example Website",
                            "subtitle": "user@example.com",
                            "url": "https://www.example.com",
                            "urls": [{"label": "", "url": "https://www.example.com"}],
                            "tags": ["work", "important"],
                            "ps": 100,
                            "pbe": 0.0,
                            "pgrng": True
                        },
                        "details": {
                            "loginFields": [
                                {
                                    "value": "user@example.com",
                                    "id": "username_field",
                                    "name": "username",
                                    "fieldType": "E",
                                    "designation": "username"
                                },
                                {
                                    "value": "SecureTestPass123!",
                                    "id": "password_field",
                                    "name": "password",
                                    "fieldType": "P",
                                    "designation": "password"
                                }
                            ],
                            "notesPlain": "This is a test login entry with *bold* and _italic_ markdown.",
                            "sections": [{
                                "title": "Additional Info",
                                "name": "Section_test_001",
                                "fields": [{
                                    "title": "Security Question",
                                    "id": "security_q_001",
                                    "value": "Mother's maiden name",
                                    "indexAtSource": 0,
                                    "guarded": False,
                                    "multiline": False,
                                    "dontGenerate": False,
                                    "inputTraits": {
                                        "keyboard": "default",
                                        "correction": "default",
                                        "capitalization": "default"
                                    }
                                }]
                            }],
                            "passwordHistory": [
                                {"value": "OldPassword123", "time": 1690000000},
                                {"value": "OlderPass456", "time": 1680000000}
                            ]
                        }
                    },
                    # Password item
                    {
                        "uuid": "test_password_002",
                        "favIndex": 0,
                        "createdAt": 1700000000,
                        "updatedAt": 1700000000,
                        "state": "active",
                        "categoryUuid": "005",
                        "overview": {
                            "title": "WiFi Password",
                            "tags": ["home"]
                        },
                        "details": {
                            "loginFields": [{
                                "value": "MyWiFiPassword2024",
                                "name": "password",
                                "fieldType": "P",
                                "designation": "password"
                            }],
                            "notesPlain": "Home network password"
                        }
                    },
                    # Credit Card item
                    {
                        "uuid": "test_card_003",
                        "favIndex": 0,
                        "createdAt": 1700000000,
                        "updatedAt": 1700000000,
                        "state": "active",
                        "categoryUuid": "002",
                        "overview": {
                            "title": "Test Visa Card",
                            "tags": ["finance"]
                        },
                        "details": {
                            "notesPlain": "Primary credit card",
                            "sections": [{
                                "title": "",
                                "name": "Section_card_details",
                                "fields": [
                                    {"title": "cardholder name", "value": "John Test Doe"},
                                    {"title": "type", "value": "Visa"},
                                    {"title": "number", "value": {"concealed": "4111111111111111"}},
                                    {"title": "cvv", "value": {"concealed": "123"}},
                                    {"title": "expiry date", "value": {"monthYear": 202612}}
                                ]
                            }]
                        }
                    },
                    # Secure Note item
                    {
                        "uuid": "test_note_004",
                        "favIndex": 0,
                        "createdAt": 1700000000,
                        "updatedAt": 1700000000,
                        "state": "active",
                        "categoryUuid": "003",
                        "overview": {
                            "title": "Important Notes",
                            "tags": ["personal"]
                        },
                        "details": {
                            "notesPlain": "This is a test secure note.\nLine 2 with more information.\nLine 3 with special chars: @#$%^&*()"
                        }
                    },
                    # Identity item
                    {
                        "uuid": "test_identity_005",
                        "favIndex": 0,
                        "createdAt": 1700000000,
                        "updatedAt": 1700000000,
                        "state": "active",
                        "categoryUuid": "004",
                        "overview": {
                            "title": "Personal Identity",
                            "tags": []
                        },
                        "details": {
                            "sections": [{
                                "title": "Identification",
                                "name": "Section_identity",
                                "fields": [
                                    {"title": "first name", "value": "John"},
                                    {"title": "last name", "value": "Doe"},
                                    {"title": "email", "value": "john.doe@example.com"},
                                    {"title": "phone", "value": "555-0123"}
                                ]
                            }]
                        }
                    }
                ]
            }]
        }]
    }

    # Create export attributes
    attributes = {
        "version": 3,
        "description": "1Password Unencrypted Export",
        "createdAt": 1700000000
    }

    # Write to ZIP file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('export.attributes', json.dumps(attributes, indent=2))
        zf.writestr('export.data', json.dumps(test_data, indent=2))

    print(f"✓ Generated test file: {output_path}")
    return output_path


def run_tests() -> bool:
    """Run automated tests on the exporter."""
    print("\n" + "="*60)
    print("RUNNING AUTOMATED TESTS")
    print("="*60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(script_dir, "inputs", "test_data.1pux")

    try:
        # Generate test file
        print("\n[1/3] Generating test data...")
        generate_test_file(test_file_path)

        # Run exporter
        print("\n[2/3] Running exporter on test data...")
        exporter = PasswordExporter(test_file_path)
        success = exporter.run()

        if not success:
            print("\n✗ TEST FAILED: Export process failed")
            return False

        # Validate outputs
        print("\n[3/3] Validating outputs...")
        outputs_dir = os.path.join(script_dir, "outputs")
        csv_path = os.path.join(outputs_dir, "exported_passwords.csv")
        non_password_dir = os.path.join(outputs_dir, "non_password_data")

        # Check CSV exists and has content
        if not os.path.exists(csv_path):
            print(f"✗ TEST FAILED: CSV file not found at {csv_path}")
            return False

        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:  # Header + at least one data row
                print(f"✗ TEST FAILED: CSV has insufficient data ({len(lines)} lines)")
                return False
            # Validate header
            expected_header = '"Title","URL","Username","Password","Notes","OTPAuth"'
            if not lines[0].strip().startswith(expected_header):
                print(f"✗ TEST FAILED: CSV header mismatch")
                print(f"   Expected: {expected_header}")
                print(f"   Got: {lines[0].strip()}")
                return False

        # Check non-password data directory exists
        if not os.path.exists(non_password_dir):
            print(f"✗ TEST FAILED: Non-password data directory not found")
            return False

        # Check that we have some category directories
        categories = [d for d in os.listdir(non_password_dir)
                     if os.path.isdir(os.path.join(non_password_dir, d))]
        if len(categories) == 0:
            print(f"✗ TEST FAILED: No category directories created")
            return False

        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED")
        print("="*60)
        print(f"  CSV file: {csv_path}")
        print(f"  Categories created: {len(categories)}")
        print(f"  CSV rows: {len(lines) - 1} (excluding header)")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_tests() -> bool:
    """Clean up test files and outputs."""
    print("\n" + "="*60)
    print("CLEANING UP TEST FILES")
    print("="*60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(script_dir, "inputs", "test_data.1pux")
    outputs_dir = os.path.join(script_dir, "outputs")

    cleaned = []
    errors = []

    try:
        # Remove test input file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            cleaned.append(test_file_path)
            print(f"✓ Removed: {test_file_path}")

        # Remove outputs directory
        if os.path.exists(outputs_dir):
            import shutil
            shutil.rmtree(outputs_dir)
            cleaned.append(outputs_dir)
            print(f"✓ Removed: {outputs_dir}")

        print("\n" + "="*60)
        print(f"✓ CLEANUP COMPLETE: {len(cleaned)} items removed")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n✗ CLEANUP FAILED: {str(e)}")
        return False


def main():
    """Main entry point for the script."""
    # Clear console
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

    print("1Password to Apple Passwords Exporter")
    print("="*60)

    # Check for special commands
    if len(sys.argv) >= 2:
        command = sys.argv[1].lower()

        if command == "--generate-test" or command == "-g":
            print("\nGenerating test file...")
            generate_test_file()
            sys.exit(0)

        elif command == "--test" or command == "-t":
            success = run_tests()
            sys.exit(0 if success else 1)

        elif command == "--cleanup" or command == "-c":
            success = cleanup_tests()
            sys.exit(0 if success else 1)

        elif command == "--test-all" or command == "-a":
            print("\nRunning full test cycle (generate → test → cleanup)...")
            test_success = run_tests()
            if test_success:
                cleanup_tests()
                print("\n✓ Full test cycle completed successfully!")
                sys.exit(0)
            else:
                print("\n✗ Tests failed. Skipping cleanup to preserve test artifacts.")
                sys.exit(1)

        elif command in ["--help", "-h", "help"]:
            print("\nUsage:")
            print("  python3 1password_exporter.py <input_file.1pux>")
            print("  python3 1password_exporter.py [options]")
            print("\nOptions:")
            print("  --generate-test, -g    Generate dummy test .1pux file")
            print("  --test, -t             Run automated tests")
            print("  --cleanup, -c          Clean up test files and outputs")
            print("  --test-all, -a         Run full test cycle (generate → test → cleanup)")
            print("  --help, -h             Show this help message")
            print("\nThe script will create in the outputs/ directory:")
            print("  - exported_passwords.csv (for Apple Passwords import)")
            print("  - non_password_data/ (organized non-password items)")
            print("    Each item gets its own folder with:")
            print("      • Human-readable .txt file")
            print("      • Any file attachments")
            sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 1password_exporter.py <input_file.1pux>")
        print("       python3 1password_exporter.py --help for more options")
        sys.exit(1)

    input_file = sys.argv[1]

    exporter = PasswordExporter(input_file)

    success = exporter.run()

    if success:
        print("\nExport completed successfully!")
        sys.exit(0)
    else:
        print("\nExport failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
