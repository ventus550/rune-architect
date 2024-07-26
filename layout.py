from gui.components import (
	ApplicationWindow,
	Container,
	TitleBar,
	DataFrame,
	Button,
	Dropdown,
    CheckBox,
    QSizePolicy,
)
from gui.components.alignment import *
from gui.components.settings import theme, settings
from itertools import product

import numpy, pandas

data = pandas.DataFrame(numpy.random.randint(0, 100, (12, 3)), columns=["Weight", "Min", "Max"])


class ApplicationLayout(ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        window: Container = Container(shadow=True, margin=10, spacing=10, bg_color=theme.bg_one)
        self.addWidget(window)
        
        window[None] = TitleBar(self, height=50)

        window[None] = container = Container(bg_color=theme.bg_two, cstretch=[0], rstretch=[2])

        container[0, 0] = self.button = Button(text="Load json data", height=50)
        container[1, 0, 2, 1] = self.weight_min_max = DataFrame[AlignTop](maxlen=3, numeric=True)
    
        container[0, 1] = environment = Container[AlignTop](cstretch=0, margin=4, spacing=10)
        environment[0, 0] = self.monster_selector = Dropdown(width=200)
        environment[0, 1] = self.allow_equipped_checkbox = CheckBox("Equipped")

        container[1, 1] = runesets = Container[AlignTop](margin=5, spacing=4)
        self.runesets_selectors = [
            Dropdown(),
            Dropdown(),
            Dropdown(),
        ]
        runesets[None] = self.runesets_selectors[0]
        runesets[None] = self.runesets_selectors[1]
        runesets[None] = self.runesets_selectors[2]
        
        
        container[2, 0, 1, 2] = self.results = DataFrame(data, editable=False)
        self.results.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
