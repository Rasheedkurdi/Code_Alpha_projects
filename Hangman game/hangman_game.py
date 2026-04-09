import flet as ft
import random
import string


def main(page: ft.Page):
    page.title = "Hangman Game"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 820
    page.window.height = 750
    page.window.resizable = True

    word_list = [
        "PYTHON", "JAVASCRIPT", "PROGRAMMING", "DEVELOPER",
        "COMPUTER", "FRAMEWORK", "INTERFACE", "APPLICATION",
    ]

    hangman_stages = [
        "   ------\n   |    |\n   |\n   |\n   |\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |\n   |\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |    |\n   |\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |   /|\n   |\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |   /|\\\n   |\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |   /|\\\n   |   /\n   |\n=========",
        "   ------\n   |    |\n   |    O\n   |   /|\\\n   |   / \\\n   |\n=========",
    ]

    # Game state
    secret_word = ""
    guessed_letters: set = set()
    incorrect_guesses = 0
    max_incorrect = 6

    # UI elements
    word_display = ft.Text(value="", size=36, weight=ft.FontWeight.BOLD)
    status_text = ft.Text(
        value="", size=16, color=ft.Colors.BLUE_200,
        text_align=ft.TextAlign.CENTER,
    )
    hangman_text = ft.Text(
        value=hangman_stages[0], size=16,
        font_family="Consolas", color=ft.Colors.WHITE70,
    )
    hangman_box = ft.Container(
        content=hangman_text,
        bgcolor=ft.Colors.ON_INVERSE_SURFACE,
        padding=16, border_radius=10,
        margin=ft.Margin(top=0, right=0, bottom=12, left=0),
    )

    # --- Build letter buttons with on_click=None (assigned in start_game) ---
    def make_letter_btn(char: str) -> ft.Container:
        return ft.Container(
            content=ft.Text(char, size=14, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE),
            data=char,
            width=50, height=42,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=6,
            alignment=ft.Alignment(0, 0),
            ink=False,
            on_click=None,  # assigned in start_game() after letter_click is defined
        )

    all_buttons: dict = {ch: make_letter_btn(ch) for ch in string.ascii_uppercase}
    alphabet = list(string.ascii_uppercase)

    letters_row1 = ft.Row(
        controls=[all_buttons[ch] for ch in alphabet[:9]],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )
    letters_row2 = ft.Row(
        controls=[all_buttons[ch] for ch in alphabet[9:18]],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )
    letters_row3 = ft.Row(
        controls=[all_buttons[ch] for ch in alphabet[18:]],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )

    # --- New Game button ---
    new_game_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.WHITE, size=20),
                ft.Text("New Game", size=15, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE),
            ],
            tight=True, spacing=8,
        ),
        bgcolor=ft.Colors.BLUE_700,
        padding=ft.Padding(top=12, bottom=12, left=26, right=26),
        border_radius=10,
        ink=True,
        on_click=lambda _: start_game(),
    )

    # --- Word list panel (visible on open / game over, hidden during play) ---
    word_list_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("📋 Possible Words", size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_300),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(w, size=13, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_GREY_800,
                            padding=ft.Padding(top=6, bottom=6, left=14, right=14),
                            border_radius=20,
                            margin=ft.Margin(top=3, bottom=3, left=4, right=4),
                        )
                        for w in word_list
                    ],
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor=ft.Colors.ON_INVERSE_SURFACE,
        padding=16,
        border_radius=12,
        width=700,
        visible=True,   # shown before game starts
    )

    # --- Game logic (letter_click defined BEFORE all_buttons get on_click) ---
    def update_word_display():
        display = [ch if ch in guessed_letters else "_" for ch in secret_word]
        word_display.value = "  ".join(display)
        if "_" not in display:
            status_text.value = "🎉 CONGRATULATIONS! YOU WON! 🎉"
            status_text.color = ft.Colors.GREEN_400
            end_game()

    def end_game():
        for btn in all_buttons.values():
            btn.on_click = None
            btn.ink = False
        word_list_panel.visible = True   # show word list again after game ends
        page.update()

    def letter_click(e):
        nonlocal incorrect_guesses
        letter: str = e.control.data
        if letter in guessed_letters:
            return
        e.control.on_click = None
        e.control.ink = False
        guessed_letters.add(letter)

        if letter in secret_word:
            e.control.bgcolor = ft.Colors.GREEN_700
            update_word_display()
        else:
            e.control.bgcolor = ft.Colors.RED_700
            incorrect_guesses += 1
            hangman_text.value = hangman_stages[incorrect_guesses]
            status_text.value = f"Wrong: {incorrect_guesses} / {max_incorrect}"
            status_text.color = ft.Colors.WHITE70
            if incorrect_guesses >= max_incorrect:
                status_text.value = f"💀 GAME OVER! The word was: {secret_word} 💀"
                status_text.color = ft.Colors.RED_400
                end_game()
        page.update()

    def start_game():
        nonlocal secret_word, guessed_letters, incorrect_guesses
        secret_word = random.choice(word_list).upper()
        guessed_letters = set()
        incorrect_guesses = 0

        hangman_text.value = hangman_stages[0]
        status_text.value = "Guess the hidden word — one letter at a time!"
        status_text.color = ft.Colors.BLUE_200

        # Hide word list during gameplay
        word_list_panel.visible = False

        # Assign click handler now that letter_click exists
        for btn in all_buttons.values():
            btn.bgcolor = ft.Colors.BLUE_GREY_700
            btn.ink = True
            btn.on_click = letter_click

        update_word_display()
        page.update()

    # Build scrollable page
    page.add(
        ft.Column(
            controls=[
                ft.Text("🎮 HANGMAN 🎮", size=40, weight=ft.FontWeight.W_900,
                        color=ft.Colors.BLUE_400),
                hangman_box,
                status_text,
                word_display,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                letters_row1,
                ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                letters_row2,
                ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                letters_row3,
                ft.Divider(height=14, color=ft.Colors.TRANSPARENT),
                new_game_btn,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                word_list_panel,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
            expand=True,
        )
    )

    # Do NOT call start_game() on load — show word list first
    status_text.value = "Press  ▶ New Game  to start playing!"
    status_text.color = ft.Colors.BLUE_200
    word_display.value = ""
    page.update()


if __name__ == "__main__":
    ft.run(main)
