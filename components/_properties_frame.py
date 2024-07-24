from typing import Any
from customtkinter import *
from .entry_field import EntryField
from .parameters import parameters

class PropertiesFrame(CTkFrame):
    def __init__(self, master, properties, column_placeholders=[], padx=5, pady=5, title="PropertiesFrame"):
        super().__init__(master=master)
        self.entries = {}
        self.properties = properties
        self.grid_columnconfigure(list(range(len(column_placeholders)+1)), weight=1)

        if (has_title := title is not None):
            CTkLabel(self, text=title, font=parameters.large_font, text_color=parameters.text_color).grid(row=0, column=0, columnspan=len(column_placeholders)+1, pady=pady*2)

        for i, p in enumerate(properties, start=has_title):
            CTkLabel(self, text=p, font=parameters.small_font).grid(row=i, column=0, padx=padx, pady=pady)
            rowents = self.entries[p] = []
            for col in column_placeholders:
                rowents.append(EntryField(self, placeholder_text=col, allow_letters=False, width=64, maxlen=5))
                rowents[-1].grid(row=i, column=len(rowents), padx=padx, pady=pady)

    def __getitem__(self, key: str) -> Any:
        return tuple(entry.get() for entry in self.entries[key])

    def items(self):
        return {property: self[property] for property in self.properties}

