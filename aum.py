import flet as ft

CURRENT_VERSION = "0.1"

def main(page: ft.Page):
    page.title = "Ada Update Manager"
    page.window_width = 400
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.bgcolor = ft.colors.BLACK
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.bgcolor = ft.colors.WHITE
            page.theme_mode = ft.ThemeMode.LIGHT
        update_button_colors()
        page.update()

    def update_button_colors():
        check_button.bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_900
        check_button.color = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE

        theme_button.bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_900
        theme_button.color = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE

        exit_button.bgcolor = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_900
        exit_button.color = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE

    def check_updates(e):
        status_text.value = "Checking for updates..."
        page.update()
        # Placeholder for actual update logic
        status_text.value = "No updates available."  # Replace with real status
        page.update()

    def exit_app(e):
        page.window_close()

    # Header
    header = ft.Text(
        value="Update Manager",
        size=128,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Version display
    version_display = ft.Text(
        value=f"Current Version: {CURRENT_VERSION}",
        size=14,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # Status text
    status_text = ft.Text(value="Welcome to the Update Manager", weight=ft.FontWeight.BOLD, size=36)

    # Buttons
    check_button = ft.ElevatedButton(
        text="Check for Updates", 
        on_click=check_updates, 
        bgcolor=ft.colors.GREY_900, 
        color=ft.colors.WHITE, 
        width=300, 
        height=60
    )
    theme_button = ft.ElevatedButton(
        text="Toggle Theme", 
        on_click=toggle_theme, 
        bgcolor=ft.colors.GREY_900, 
        color=ft.colors.WHITE, 
        width=300, 
        height=60
    )
    exit_button = ft.ElevatedButton(
        text="Exit", 
        on_click=exit_app, 
        bgcolor=ft.colors.GREY_900, 
        color=ft.colors.WHITE, 
        width=300, 
        height=60
    )

    # Layout
    page.add(
        ft.Column(
            [
                header,
                version_display,
                ft.Divider(),
                status_text,
                ft.Divider(),
                check_button,
                theme_button,
                exit_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        )
    )

    # Set initial button styles
    update_button_colors()

# Run the app
ft.app(target=main)
