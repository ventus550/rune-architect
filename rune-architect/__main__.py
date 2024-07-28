from PyQt6.QtWidgets import QFileDialog
from collections import Counter
import pandas
from .layout import ApplicationLayout
from .gui.components import MessageBox
from .core.data import mapping, extract, transform
from .core.data.schema import WeightMinMax, DataFrame, Monsters, Runes
from .core.optimizer import Optimizer

flat_effects = [eff for eff in mapping.runes.effects.values() if not eff.endswith("%")]
data = pandas.DataFrame(
    {"weight": 1, "min": pandas.NA, "max": pandas.NA}, dtype="Int64", index=flat_effects
)
empty = "Empty"


class Application(ApplicationLayout):
    def __init__(self):
        super().__init__(minw=1200)
        self.json = None
        self.monsters: DataFrame[Monsters] = None
        self.runes: DataFrame[Runes] = None
        self.selected_monsters: DataFrame[Monsters] = None

        self.weight_min_max.data = data.T
        self.monster_selector.addItem("Monster")
        self.monster_selector.setDisabled(True)
        for sel in self.runesets_selectors:
            sel.addItems([empty, *sorted(mapping.runes.sets.values())])

        self.button.clicked.connect(self.select_data_file)

    def gatherSets(self):
        return dict(
            Counter(
                [sel.value for sel in self.runesets_selectors if sel.value != empty]
            )
        )

    def gatherWeightMinMax(self) -> DataFrame[WeightMinMax]:
        wmm = self.weight_min_max.data.astype("Int64").T
        wmm.weight = wmm.weight.fillna(0)
        return wmm

    def select_data_file(self, *args):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]  # Get the first selected file
                self.json = extract.json(file_path)
                self.enable_optimizer()

    def enable_optimizer(self):
        self.runes = extract.runes(self.json)
        self.monsters = extract.monsters(self.json)
        self.monster_selector.setEnabled(True)
        self.monster_selector.removeItem(0)
        self.monster_selector.addItems(sorted(self.monsters.name.dropna().values))
        self.button.setText("Optimize")
        self.button.clicked.disconnect(self.select_data_file)
        self.button.clicked.connect(self.optimize)

    def optimize(self):
        self.button.setDisabled(True)
        self.button.repaint()
        self.selected_monsters = transform.get_monsters_by_name(
            self.monsters, self.monster_selector.value
        )
        filtered_runes = self.runes
        if not self.allow_equipped_checkbox.isChecked():
            filtered_runes = transform.filter_equipped(
                self.runes, self.selected_monsters
            )
        self.worker = Optimizer(
            func=self.on_optimization_finish,
            runes=filtered_runes,
            monster=self.selected_monsters.iloc[:1],
            weight_min_max=self.gatherWeightMinMax(),
            sets=self.gatherSets(),
        )

    def on_optimization_finish(self, solution: DataFrame | None):
        self.button.setEnabled(True)
        if solution is not None:
            self.results.data = (
                transform.named_monster_runes_view(solution, self.monsters)
                .set_index("slot")
                .drop(columns="spd%")
            )
            summary_data = pandas.DataFrame(
                transform.flatten_runes(solution, self.selected_monsters)
                .apply(pandas.to_numeric, args=["coerce"])
                .select_dtypes(int)
                .sum()
            ).T
            summary_data["monster"] = self.monster_selector.value
            self.summary.data = summary_data.drop(columns="slot")

            self.worker.quit()
            self.worker.wait()
        else:
            MessageBox(self, "The formulated program is infeasible.").exec()


app = Application()
app.exec()
