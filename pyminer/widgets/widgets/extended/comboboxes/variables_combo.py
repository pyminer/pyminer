from typing import Any

from .combo import PMGComboCtrl


class Var():
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class PMGVariablesComboCtrl(PMGComboCtrl):
    def __init__(self, layout_dir: str, title: str, initial_value: Any = ""):
        """
        ComboBox control to select values
        Args:
            layout_dir:
            title:
            initial_value:
        """
        from utils import bind_panel_combo_ctrl_with_workspace
        super().__init__(layout_dir, title, initial_value, [""], [""])
        bind_panel_combo_ctrl_with_workspace(self)

    def get_value(self) ->str:
        return Var(super().get_value())
