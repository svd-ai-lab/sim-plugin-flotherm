"""Session lifecycle regressions for the Flotherm driver."""
from __future__ import annotations

from pathlib import Path

import pytest

from sim_plugin_flotherm import FlothermDriver
from sim_plugin_flotherm._helpers import (
    detect_job_state,
    is_process_alive,
    read_solve_log,
)


def test_no_gui_mode_is_rejected() -> None:
    driver = FlothermDriver()

    with pytest.raises(RuntimeError, match="does not support ui_mode='no_gui'"):
        driver.launch(ui_mode="no_gui")


def test_is_process_alive_handles_empty_pid() -> None:
    assert is_process_alive(None) is False


def test_read_solve_log_detects_normal_exit(tmp_path: Path) -> None:
    project_dir = "Demo.ABC"
    logit = (
        tmp_path / project_dir / "DataSets" / "BaseSolution" / "PDTemp" / "logit"
    )
    logit.parent.mkdir(parents=True)
    logit.write_text(
        "solver output\nstatus 3 normal exit from main program MAINUU.\n",
        encoding="utf-8",
    )

    out = read_solve_log(str(tmp_path), project_dir)

    assert out["exists"] is True
    assert out["state"] == "succeeded"
    assert "normal exit" in out["tail"]


def test_read_solve_log_accepts_non_three_normal_exit(tmp_path: Path) -> None:
    project_dir = "Demo.ABC"
    logit = (
        tmp_path / project_dir / "DataSets" / "BaseSolution" / "PDTemp" / "logit"
    )
    logit.parent.mkdir(parents=True)
    logit.write_text(
        "solver output\nstatus 7 normal exit from main program MAINUU.\n",
        encoding="utf-8",
    )

    assert read_solve_log(str(tmp_path), project_dir)["state"] == "succeeded"


def test_detect_job_state_uses_logit_completion_even_when_process_alive(
    tmp_path: Path,
) -> None:
    project_dir = "Demo.ABC"
    logit = (
        tmp_path / project_dir / "DataSets" / "BaseSolution" / "PDTemp" / "logit"
    )
    logit.parent.mkdir(parents=True)
    logit.write_text(
        "solver output\nstatus 3 normal exit from main program MAINUU.\n",
        encoding="utf-8",
    )

    state, reasons = detect_job_state(
        workspace=str(tmp_path),
        project_dir=project_dir,
        pre_solve_snapshot={},
        process_pid=None,
        elapsed_s=1,
        timeout_s=30,
    )

    assert state == "succeeded"
    assert any("PDTemp/logit state: succeeded" in reason for reason in reasons)
