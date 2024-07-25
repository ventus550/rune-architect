from pathlib import Path


class settings:
    app_name = "Rune Architect"
    stylesheets_directory = Path("gui/stylesheets")
    assets_directory = Path("gui/assets")
    font_path = assets_directory / "recharge.otf"
    app_height = 600
    app_width = 800


class theme:
    dark_one = "#59000c"
    dark_two = "#1e2229"
    dark_three = "#21252d"
    dark_four = "#272c36"
    bg_one = "#2c313c"
    bg_two = "#343b48"
    bg_three = "#3c4454"
    icon_color = "#c3ccdf"
    icon_hover = "#dce1ec"
    icon_pressed = "#6c99f4"
    icon_active = "#f5f6f9"
    context_color = "#568af2"
    context_hover = "#6c99f4"
    context_pressed = "#3f6fd1"
    text_title = "#dce1ec"
    text_foreground = "#8a95aa"
    text_description = "#4f5b6e"
    text_active = "#dce1ec"
    monospace_font = "Consolas"
    white = "#f5f6f9"
    pink = "#ff007f"
    green = "#00ff7f"
    red = "#941801"
    yellow = "#f1fa8c"
    font_family = "recharge"
    title_size = 10
    text_size = 9
