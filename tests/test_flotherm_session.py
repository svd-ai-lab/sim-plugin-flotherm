"""Session lifecycle regressions for the Flotherm driver."""
from __future__ import annotations

import pytest

from sim_plugin_flotherm import FlothermDriver


def test_no_gui_mode_is_rejected() -> None:
    driver = FlothermDriver()

    with pytest.raises(RuntimeError, match="does not support ui_mode='no_gui'"):
        driver.launch(ui_mode="no_gui")
