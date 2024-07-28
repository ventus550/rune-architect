from pathlib import Path


class settings:
    class application:
        name = "Rune Architect"
        height = 660
        width = 1400
        margin = 30
        icon = "icon.ico"
        logo = "logo.asvg"
        font = "recharge.otf"

    class directories:
        stylesheets = Path("rune-architect/gui/stylesheets")
        assets = Path("rune-architect/gui/assets")
    class theme:
        class background:
            container = "#1e2229"
            frames = "#f5f6f9"

        class text:
            family = "recharge"

            class size:
                large = 16
                medium = 14
                normal = 12

            class color:
                important = "#f5f6f9"
                description = "#8a95aa"
                highlight = "#4f5b6e"
                warning = "#59000c"

        class items:
            radius = 5

            class color:
                primary = "#8c0101"
                headers = "#1e2229"
