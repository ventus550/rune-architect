from pathlib import Path


class settings:
    class application:
        name = "Rune Architect"
        height = 650
        width = 1200
        margin = 20
        icon = "icon.ico"
        logo = "logo.asvg"
        font = "recharge.otf"

    class directories:
        stylesheets = Path("gui/stylesheets")
        assets = Path("gui/assets")

    class theme:
        class background:
            container = "#2c313c"
            frames = "#343b48"

        class text:
            family = "recharge"

            class size:
                large = 16
                medium = 12
                normal = 10

            class color:
                important = "#f5f6f9"
                description = "#8a95aa"
                highlight = "#4f5b6e"
                warning = "#59000c"

        class items:
            radius = 5

            class color:
                primary = "#568af2"
                headers = "#1e2229"
