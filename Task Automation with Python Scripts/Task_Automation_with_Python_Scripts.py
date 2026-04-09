import os
import shutil
import re
import requests
from pathlib import Path
from datetime import datetime

# ============================================
# TASK 1: Move all .jpg files to a new folder
# ============================================
def move_jpg_files():
    """Move all .jpg files from source folder to destination folder"""
    print("\n" + "="*50)
    print("📸 TASK 1: Move JPG Files")
    print("="*50)
    
    # Get folder paths from user
    source_folder = input("Enter source folder path: ").strip()
    dest_folder = input("Enter destination folder path: ").strip()
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"❌ Source folder '{source_folder}' does not exist!")
        return
    
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print(f"✅ Created destination folder: {dest_folder}")
    
    # Find and move JPG files
    jpg_files = []
    for file in os.listdir(source_folder):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            jpg_files.append(file)
    
    if not jpg_files:
        print("❌ No .jpg files found in source folder!")
        return
    
    print(f"\nFound {len(jpg_files)} JPG file(s):")
    for file in jpg_files:
        print(f"  - {file}")
    
    # Move files
    confirm = input(f"\nMove these {len(jpg_files)} files? (yes/no): ").lower()
    if confirm in ['yes', 'y']:
        moved_count = 0
        for file in jpg_files:
            source_path = os.path.join(source_folder, file)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(source_path, dest_path)
            moved_count += 1
            print(f"✅ Moved: {file}")
        
        print(f"\n✅ Successfully moved {moved_count} JPG files to '{dest_folder}'")
    else:
        print("❌ Operation cancelled.")

# ============================================
# TASK 2: Extract email addresses from text file
# ============================================
def extract_emails():
    """Extract all email addresses from a .txt file and save to another file"""
    print("\n" + "="*50)
    print("📧 TASK 2: Extract Email Addresses")
    print("="*50)
    
    # Get file paths
    input_file = input("Enter input text file path: ").strip()
    output_file = input("Enter output file path (default: emails_found.txt): ").strip()
    
    if not output_file:
        output_file = "emails_found.txt"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ File '{input_file}' does not exist!")
        return
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regular expression pattern for email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, content)
        
        # Remove duplicates while preserving order
        unique_emails = []
        seen = set()
        for email in emails:
            if email.lower() not in seen:
                unique_emails.append(email)
                seen.add(email.lower())
        
        if not unique_emails:
            print("❌ No email addresses found in the file!")
            return
        
        # Save to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"Email addresses extracted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("="*50 + "\n\n")
            for i, email in enumerate(unique_emails, 1):
                file.write(f"{i}. {email}\n")
        
        print(f"\n✅ Found {len(unique_emails)} unique email address(es):")
        for email in unique_emails[:10]:  # Show first 10
            print(f"  - {email}")
        if len(unique_emails) > 10:
            print(f"  ... and {len(unique_emails) - 10} more")
        
        print(f"\n💾 Emails saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")

# ============================================
# TASK 3: Scrape webpage title
# ============================================
def scrape_webpage_title():
    """Scrape and save the title of a webpage"""
    print("\n" + "="*50)
    print("🌐 TASK 3: Scrape Webpage Title")
    print("="*50)
    
    # Get URL from user
    url = input("Enter webpage URL (e.g., https://example.com): ").strip()
    
    # Add https:// if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Send HTTP request
        print(f"⏳ Fetching: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Extract title using regex (simpler than parsing HTML)
        title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
        
        if title_match:
            title = title_match.group(1).strip()
            print(f"\n✅ Page Title: {title}")
            
            # Ask to save
            save_option = input("\nSave title to file? (yes/no): ").lower()
            if save_option in ['yes', 'y']:
                filename = f"webpage_title_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"URL: {url}\n")
                    file.write(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write("="*50 + "\n")
                    file.write(f"Title: {title}\n")
                
                print(f"💾 Title saved to: {filename}")
        else:
            print("❌ Could not find title tag in the webpage!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching webpage: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# ============================================
# BONUS TASK: Create sample files for testing
# ============================================
def create_sample_files():
    """Create sample files to test the automation tasks"""
    print("\n" + "="*50)
    print("🧪 Create Sample Test Files")
    print("="*50)
    
    # Create sample text file with emails
    sample_text = """Sample text with email addresses:
    
    Contact us at: support@example.com
    John Doe: john.doe@gmail.com
    Jane Smith: jane.smith@company.co.uk
    Sales department: sales@example.com
    
    Other emails:
    - info@testsite.org
    - admin@mywebsite.net
    - john.doe@gmail.com (duplicate)
    
    Invalid: notanemail, name@domain, user@.com
    """
    
    with open("sample_emails.txt", "w", encoding='utf-8') as file:
        file.write(sample_text)
    print("✅ Created: sample_emails.txt")
    
    # Create sample folder with dummy JPG files
    sample_folder = "sample_images"
    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)
        # Create empty placeholder files (since we can't create actual images)
        for i in range(1, 4):
            with open(os.path.join(sample_folder, f"image{i}.jpg"), 'w') as f:
                f.write(f"Placeholder for image{i}.jpg")
        print(f"✅ Created: {sample_folder}/ with 3 sample .jpg files")
    
    print("\n🎯 Sample files created! You can now test the automation tasks.")
    print("   - Task 1: Move JPGs from 'sample_images/' to a new folder")
    print("   - Task 2: Extract emails from 'sample_emails.txt'")
    print("   - Task 3: Test with any website (e.g., https://python.org)")

# ============================================
# Main Menu
# ============================================
def main():
    """Main menu to select automation task"""
    while True:
        print("\n" + "="*50)
        print("🤖 TASK AUTOMATION SUITE")
        print("="*50)
        print("1. 📸 Move all .jpg files to a new folder")
        print("2. 📧 Extract email addresses from text file")
        print("3. 🌐 Scrape webpage title")
        print("4. 🧪 Create sample test files")
        print("5. 🚪 Exit")
        print("="*50)
        
        choice = input("Select task (1-5): ").strip()
        
        if choice == '1':
            move_jpg_files()
        elif choice == '2':
            extract_emails()
        elif choice == '3':
            scrape_webpage_title()
        elif choice == '4':
            create_sample_files()
        elif choice == '5':
            print("\n👋 Thank you for using Task Automation Suite!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-5.")
        
        # Ask to continue
        if choice != '5':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()