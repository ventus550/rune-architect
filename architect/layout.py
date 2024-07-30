from .gui.components import (
	Window,
	Container,
	TitleBar,
	DataFrame,
	Button,
	Dropdown,
    CheckBox,
    QSizePolicy,
    Qt
)
from .gui.components.alignment import *
from .settings import settings


class ApplicationLayout(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        window: Container = Container(
            shadow=True,
            margin=5,
            spacing=10,
            bg_color=settings.theme.background.container
        )
        self.addWidget(window)
        
        window[None] = TitleBar(self, height=50, logo_image="icon.svg")

        window[None] = container = Container(
            bg_color=settings.theme.background.frames,
            cstretch=[0],
            rstretch=[3],
            spacing=20,
            margin=settings.application.margin
        )

        container[0, 0] = self.button = Button(text="Load json data", height=40)
        
        container[1, 0, 2, 1] = self.weight_min_max = DataFrame[AlignTop](maxlen=5, numeric=True)
        self.weight_min_max.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
        container[0, 1] = environment = Container[AlignCenter](cstretch=0, margin=0, spacing=10)
        environment[0, 0] = self.monster_selector = Dropdown(width=300)
        environment[0, 1] = self.allow_equipped_checkbox = CheckBox("Equipped")

        container[1, 1] = runesets = Container[AlignTop](margin=0, spacing=15)
        self.runesets_selectors = [
            Dropdown(),
            Dropdown(),
            Dropdown(),
        ]
        runesets[None] = self.runesets_selectors[0]
        runesets[None] = self.runesets_selectors[1]
        runesets[None] = self.runesets_selectors[2]

        container[2, 0, 1, 2] = self.summary = DataFrame[AlignTop](editable=False)
        self.summary.verticalHeader().setVisible(False)

        container[3, 0, 1, 2] = self.results = DataFrame(editable=False)
        self.results.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)