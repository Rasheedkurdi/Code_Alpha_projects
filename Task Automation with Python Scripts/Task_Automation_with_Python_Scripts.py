import flet as ft
import os
import shutil
import re
import requests
from datetime import datetime

def main(page: ft.Page):
    # ==========================
    # Page Configuration
    # ==========================
    page.title = "Task Automation Suite"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 900
    page.window_height = 700
    page.padding = 0
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Inter")
    
    # Custom color palette
    BG_COLOR = "#0f172a"          # Slate 900
    SURFACE_COLOR = "#1e293b"     # Slate 800
    PRIMARY_COLOR = "#6366f1"     # Indigo 500
    PRIMARY_HOVER = "#4f46e5"     # Indigo 600
    ACCENT_COLOR = "#10b981"      # Emerald 500
    TEXT_COLOR = "#f8fafc"        # Slate 50
    TEXT_MUTED = "#94a3b8"        # Slate 400
    
    page.bgcolor = BG_COLOR

    # ==========================
    # Snackbars for feedback
    # ==========================
    def show_snack(message, is_error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=TEXT_COLOR, weight=ft.FontWeight.W_500),
            bgcolor="#ef4444" if is_error else ACCENT_COLOR,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=8),
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()

    # ==========================
    # Common UI Components
    # ==========================
    def create_header(title, subtitle, icon_name):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon_name, size=32, color=PRIMARY_COLOR),
                        padding=12,
                        bgcolor="#1e1b4b", # Indigo 950
                        border_radius=12,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                            ft.Text(subtitle, size=14, color=TEXT_MUTED),
                        ],
                        spacing=2,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            margin=ft.Margin.only(bottom=24)
        )

    def create_textfield(label, hint="", default_val="", multiline=False):
        return ft.TextField(
            label=label,
            hint_text=hint,
            value=default_val,
            border_color=SURFACE_COLOR,
            focused_border_color=PRIMARY_COLOR,
            bgcolor="#0f172a",
            color=TEXT_COLOR,
            border_radius=8,
            multiline=multiline,
            min_lines=3 if multiline else 1,
            max_lines=10 if multiline else 1,
            expand=True
        )

    def create_button(text, icon, on_click):
        return ft.Button(
            content=ft.Row([ft.Icon(icon, size=18), ft.Text(text, weight=ft.FontWeight.W_600)], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(
                color=TEXT_COLOR,
                bgcolor={ft.ControlState.DEFAULT: PRIMARY_COLOR, ft.ControlState.HOVERED: PRIMARY_HOVER},
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=16,
                elevation=4
            ),
            on_click=on_click,
            height=50,
            width=200
        )

    # ==========================
    # Task 1: Move JPG Files
    # ==========================
    def move_jpg_files(e):
        src = src_input.value.strip()
        dest = dest_input.value.strip()
        
        if not src or not dest:
            show_snack("Please provide both source and destination folders.", True)
            return
            
        if not os.path.exists(src):
            show_snack(f"Source folder '{src}' does not exist!", True)
            return
            
        if not os.path.exists(dest):
            try:
                os.makedirs(dest)
            except Exception as ex:
                show_snack(f"Failed to create destination folder: {ex}", True)
                return
                
        try:
            jpg_files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg'))]
            if not jpg_files:
                show_snack("No .jpg files found in source folder!", True)
                return
                
            moved_count = 0
            for file in jpg_files:
                shutil.move(os.path.join(src, file), os.path.join(dest, file))
                moved_count += 1
                
            show_snack(f"Successfully moved {moved_count} JPG files to '{dest}'")
            # Clear inputs
            src_input.value = ""
            dest_input.value = ""
            page.update()
        except Exception as ex:
            show_snack(f"Error moving files: {ex}", True)

    src_picker = ft.FilePicker()
    dest_picker = ft.FilePicker()

    async def browse_src(e):
        path = await src_picker.get_directory_path()
        if path:
            src_input.value = path
            src_input.update()

    async def browse_dest(e):
        path = await dest_picker.get_directory_path()
        if path:
            dest_input.value = path
            dest_input.update()

    src_input = create_textfield("Source Folder Path", "e.g. C:/Users/Downloads")
    dest_input = create_textfield("Destination Folder Path", "e.g. C:/Users/Pictures")

    task1_view = ft.Container(
        content=ft.Column([
            create_header("Move JPG Files", "Organize your images by moving all .jpg files from one folder to another.", ft.Icons.PHOTO_LIBRARY),
            ft.Row([src_input, ft.IconButton(icon=ft.Icons.FOLDER_OPEN, on_click=browse_src, icon_color=PRIMARY_COLOR, tooltip="Browse Source Folder")]),
            ft.Row([dest_input, ft.IconButton(icon=ft.Icons.FOLDER_OPEN, on_click=browse_dest, icon_color=PRIMARY_COLOR, tooltip="Browse Destination Folder")]),
            ft.Container(height=10),
            create_button("Move Files", ft.Icons.DRIVE_FILE_MOVE, move_jpg_files)
        ]),
        padding=40,
        expand=True
    )

    # ==========================
    # Task 2: Extract Emails
    # ==========================
    def extract_emails(e):
        input_file = email_in_input.value.strip()
        output_file = email_out_input.value.strip() or "emails_found.txt"
        
        if not input_file:
            show_snack("Please provide an input text file path.", True)
            return
            
        if not os.path.exists(input_file):
            show_snack(f"File '{input_file}' does not exist!", True)
            return
            
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, content)
            
            unique_emails = []
            seen = set()
            for email in emails:
                if email.lower() not in seen:
                    unique_emails.append(email)
                    seen.add(email.lower())
            
            if not unique_emails:
                show_snack("No email addresses found in the file!", True)
                return
                
            # Create a nice preview in the UI
            preview_text = "\n".join(unique_emails[:5])
            if len(unique_emails) > 5:
                preview_text += f"\n... and {len(unique_emails) - 5} more."
                
            email_result.value = f"Found {len(unique_emails)} emails:\n{preview_text}"
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(f"Email addresses extracted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("="*50 + "\n\n")
                for i, email in enumerate(unique_emails, 1):
                    file.write(f"{i}. {email}\n")
            
            show_snack(f"Saved {len(unique_emails)} emails to {output_file}")
            page.update()
        except Exception as ex:
            show_snack(f"Error processing file: {ex}", True)

    email_in_picker = ft.FilePicker()
    email_out_picker = ft.FilePicker()

    async def browse_email_in(e):
        files = await email_in_picker.pick_files(allowed_extensions=["txt", "csv"])
        if files and len(files) > 0:
            email_in_input.value = files[0].path
            email_in_input.update()

    async def browse_email_out(e):
        path = await email_out_picker.save_file(allowed_extensions=["txt"])
        if path:
            email_out_input.value = path
            email_out_input.update()

    email_in_input = create_textfield("Input Text File Path", "e.g. C:/Users/data.txt")
    email_out_input = create_textfield("Output File Path (Optional)", "Defaults to emails_found.txt")
    email_result = ft.Text("", color=TEXT_MUTED, selectable=True)
    
    task2_view = ft.Container(
        content=ft.Column([
            create_header("Extract Emails", "Scan a text file and extract all valid email addresses.", ft.Icons.MARK_EMAIL_READ),
            ft.Row([email_in_input, ft.IconButton(icon=ft.Icons.FILE_OPEN, on_click=browse_email_in, icon_color=PRIMARY_COLOR, tooltip="Browse Input File")]),
            ft.Row([email_out_input, ft.IconButton(icon=ft.Icons.SAVE, on_click=browse_email_out, icon_color=PRIMARY_COLOR, tooltip="Select Output Destination")]),
            ft.Container(height=10),
            create_button("Extract Now", ft.Icons.SEARCH, extract_emails),
            ft.Container(height=20),
            ft.Container(
                content=email_result,
                padding=15,
                bgcolor="#0f172a",
                border_radius=8,
                visible=True
            )
        ]),
        padding=40,
        expand=True
    )

    # ==========================
    # Task 3: Scrape Webpage Title
    # ==========================
    def scrape_title(e):
        url = url_input.value.strip()
        
        if not url:
            show_snack("Please provide a URL.", True)
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        scraper_progress.visible = True
        page.update()
            
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            title_match = re.search(r'<title.*?>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
            
            if title_match:
                title = title_match.group(1).strip()
                title_result.value = title
                title_result_container.visible = True
                show_snack("Webpage title scraped successfully!")
                
                # Automatically format a filename if we want to save
                # We won't prompt, we'll give them a button to save
                def save_title_to_file(e):
                    filename = f"webpage_title_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    try:
                        with open(filename, 'w', encoding='utf-8') as file:
                            file.write(f"URL: {url}\n")
                            file.write(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            file.write("="*50 + "\n")
                            file.write(f"Title: {title}\n")
                        show_snack(f"Saved to {filename}")
                    except Exception as err:
                        show_snack(f"Error saving: {err}", True)
                        
                save_title_btn.on_click = save_title_to_file
                save_title_btn.visible = True
            else:
                show_snack("Could not find a <title> tag in the page.", True)
                
        except requests.exceptions.RequestException as ex:
            show_snack(f"Error fetching webpage: {ex}", True)
        except Exception as ex:
            show_snack(f"Unexpected error: {ex}", True)
        finally:
            scraper_progress.visible = False
            page.update()

    url_input = create_textfield("Webpage URL", "e.g. https://python.org")
    scraper_progress = ft.ProgressBar(visible=False, color=ACCENT_COLOR, bgcolor=SURFACE_COLOR)
    title_result = ft.Text("", size=18, weight=ft.FontWeight.W_500, color=ACCENT_COLOR, selectable=True)
    title_result_container = ft.Container(
        content=ft.Column([
            ft.Text("Scraped Title:", size=14, color=TEXT_MUTED),
            title_result
        ]),
        padding=15, 
        bgcolor="#0f172a", 
        border_radius=8, 
        visible=False,
        border=ft.Border.all(1, SURFACE_COLOR)
    )
    save_title_btn = ft.TextButton("Save to File", icon=ft.Icons.SAVE, visible=False)

    task3_view = ft.Container(
        content=ft.Column([
            create_header("Scrape Title", "Retrieve the HTML title of any public webpage.", ft.Icons.LANGUAGE),
            url_input,
            ft.Container(height=10),
            ft.Row([
                create_button("Fetch Title", ft.Icons.DOWNLOAD, scrape_title),
            ]),
            ft.Container(height=10),
            scraper_progress,
            ft.Container(height=10),
            title_result_container,
            save_title_btn
        ]),
        padding=40,
        expand=True
    )

    # ==========================
    # Task 4: Create Sample Files
    # ==========================
    def create_samples(e):
        try:
            # Create sample emails
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
                
            # Create sample images
            sample_folder = "sample_images"
            if not os.path.exists(sample_folder):
                os.makedirs(sample_folder)
            for i in range(1, 4):
                with open(os.path.join(sample_folder, f"image{i}.jpg"), 'w') as f:
                    f.write(f"Placeholder for image{i}.jpg")
            
            sample_status.value = (
                "✅ Created 'sample_emails.txt' (Use this for the Email Extractor)\n"
                "✅ Created 'sample_images/' with 3 mock JPGs (Use this for the JPG Mover)"
            )
            sample_status.color = ACCENT_COLOR
            show_snack("Sample files generated successfully!")
            
            # Pre-fill inputs for convenience
            src_input.value = os.path.abspath(sample_folder)
            dest_input.value = os.path.abspath("moved_images")
            email_in_input.value = os.path.abspath("sample_emails.txt")
            
            page.update()
        except Exception as ex:
            show_snack(f"Error creating samples: {ex}", True)

    sample_status = ft.Text("", size=14, color=TEXT_MUTED)

    task4_view = ft.Container(
        content=ft.Column([
            create_header("Test Setup", "Generate sample files and folders to instantly test these tools.", ft.Icons.SCIENCE),
            ft.Text(
                "Click below to magically create 'sample_emails.txt' and a 'sample_images' folder in the current directory. "
                "Inputs for other tools will be automatically populated with these paths!",
                color=TEXT_MUTED,
                size=15
            ),
            ft.Container(height=20),
            create_button("Generate Samples", ft.Icons.ROCKET_LAUNCH, create_samples),
            ft.Container(height=20),
            sample_status
        ]),
        padding=40,
        expand=True
    )

    # ==========================
    # Navigation & Layout
    # ==========================
    
    views = [task1_view, task2_view, task3_view, task4_view]
    
    def on_nav_change(e):
        selected_index = e.control.selected_index
        for i, view in enumerate(views):
            view.visible = (i == selected_index)
            
        header_title.value = [
            "JPG Organizer", 
            "Email Extractor", 
            "Webpage Scraper", 
            "Environment Setup"
        ][selected_index]
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=SURFACE_COLOR,
        indicator_color=PRIMARY_COLOR,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.PHOTO_LIBRARY_OUTLINED, 
                selected_icon=ft.Icons.PHOTO_LIBRARY, 
                label="JPGs"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.EMAIL_OUTLINED, 
                selected_icon=ft.Icons.EMAIL, 
                label="Emails"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.WEB_OUTLINED, 
                selected_icon=ft.Icons.WEB, 
                label="Web"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SCIENCE_OUTLINED, 
                selected_icon=ft.Icons.SCIENCE, 
                label="Setup"
            ),
        ],
        on_change=on_nav_change,
        expand=False
    )
    
    # Initial setup
    for i, view in enumerate(views):
        view.visible = (i == 0)

    header_title = ft.Text("JPG Organizer", size=20, weight=ft.FontWeight.W_600, color=TEXT_COLOR)

    # Top app bar
    app_bar = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME, color=PRIMARY_COLOR, size=24),
                ft.Text("PyAuto Suite", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR)
            ]),
            ft.Container(
                content=ft.Text("v1.0 Flet Edition", size=12, color=TEXT_MUTED),
                padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                bgcolor=SURFACE_COLOR,
                border_radius=20
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=20, vertical=15),
        bgcolor=SURFACE_COLOR,
        border=ft.Border.only(bottom=ft.BorderSide(1, "#334155"))
    )

    main_content = ft.Container(
        content=ft.Stack(controls=views),
        expand=True,
        bgcolor=BG_COLOR,
        border_radius=ft.BorderRadius.only(top_left=20),
        margin=ft.Margin.only(top=0),
    )

    layout = ft.Column(
        controls=[
            app_bar,
            ft.Row(
                controls=[
                    rail,
                    main_content
                ],
                expand=True,
                spacing=0
            )
        ],
        expand=True,
        spacing=0
    )

    page.add(layout)
    
if __name__ == "__main__":
    ft.run(main)
