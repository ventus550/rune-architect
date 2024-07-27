from pathlib import Path


class settings:
    class application:
        name = "Rune Architect"
        height = 600
        width = 1200
        icon = "icon.ico"
        logo = "logo.asvg"
        font = "recharge.otf"
    class directories:
        stylesheets = Path("gui/stylesheets")
        assets = Path("gui/assets")

    class theme:
        class background:
            containers = "#59000c"
            frames = "#343b48"
            spans = "#3c4454"
            other = "#1e2229"

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
        class items:
            class color:
                context = "#568af2"
                hover = "#6c99f4"
                press = "#3f6fd1"
                secondary = "#2c313c"
