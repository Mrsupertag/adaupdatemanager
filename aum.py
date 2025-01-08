import flet as ft
import requests
import semver  # Ensure this library is installed: pip install semver

# Configuration variables
MINOR_REPO_API_URL = "https://api.github.com/repos/2048hertz/ada-minor-update-repo/releases"
MAJOR_REPO_API_URL = "https://api.github.com/repos/2048hertz/ada-major-update-repo/releases"
MAJOR_REPO_UPDATES_BRANCH = "updates"
CURRENT_MINOR_VERSION = "0"  # Placeholder for the current minor version
CURRENT_MAJOR_VERSION = "0"  # Placeholder for the current major version

def main(page: ft.Page):
    page.title = "Ada Update Manager"
    page.window_width = 800
    page.window_height = 600
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
        button_bg = ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_900
        button_fg = ft.colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE
        check_button.bgcolor = button_bg
        check_button.color = button_fg
        theme_button.bgcolor = button_bg
        theme_button.color = button_fg
        exit_button.bgcolor = button_bg
        exit_button.color = button_fg

    def fetch_latest_release(repo_api_url, branch=None):
        headers = {"Accept": "application/vnd.github.v3+json"}
        params = {"per_page": 1}
        if branch:
            params["target_commitish"] = branch
        response = requests.get(repo_api_url, headers=headers, params=params)
        if response.status_code == 200:
            releases = response.json()
            if releases:
                latest_release = releases[0]
                return latest_release["tag_name"], latest_release["assets"]
        return None, None

    def download_update_script(assets, download_path="update.sh"):
        for asset in assets:
            if asset["name"] == "update.sh":
                download_url = asset["browser_download_url"]
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(download_path, "wb") as file:
                        file.write(response.content)
                    return True
        return False

    def check_updates(e):
        global CURRENT_MINOR_VERSION
        global CURRENT_MAJOR_VERSION

        status_text.value = "Checking for updates..."
        page.update()

        # Check for minor updates
        minor_version, minor_assets = fetch_latest_release(MINOR_REPO_API_URL)
        if minor_version and semver.compare(minor_version, CURRENT_MINOR_VERSION) > 0:
            if download_update_script(minor_assets):
                CURRENT_MINOR_VERSION = minor_version
                status_text.value = f"Minor update to version {CURRENT_MINOR_VERSION} downloaded."
            else:
                status_text.value = "Failed to download minor update script."
        else:
            status_text.value = "No minor updates available."

        # Check for major updates
        major_version, major_assets = fetch_latest_release(MAJOR_REPO_API_URL, MAJOR_REPO_UPDATES_BRANCH)
        if major_version and semver.compare(major_version, CURRENT_MAJOR_VERSION) > 0:
            if download_update_script(major_assets):
                CURRENT_MAJOR_VERSION = major_version
                status_text.value = f"Major update to version {CURRENT_MAJOR_VERSION} downloaded."
            else:
                status_text.value = "Failed to download major update script."
        else:
            status_text.value = "No major updates available."

        # Update the version display
        version_display.value = f"Current Version: {CURRENT_MAJOR_VERSION}"
        page.update()

    def exit_app(e):
        page.window_close()

    # Header
    header = ft.Text(
        value="Update Manager",
        size=36,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Version display
    version_display = ft.Text(
        value=f"Current Version: {CURRENT_MAJOR_VERSION}",
        size=14,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # Status text
    status_text = ft.Text(
        value="Welcome to the Update Manager",
        weight=ft.FontWeight.BOLD,
        size=16
    )

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
