# sim-plugin-flotherm

[Simcenter Flotherm](https://plm.sw.siemens.com/en-US/simcenter/mechanical-simulation/flotherm/) driver for [sim-cli](https://github.com/svd-ai-lab/sim-cli), distributed as an out-of-tree plugin via Python `entry_points`.

Flotherm is closed-source commercial thermal-CFD software from Siemens. This plugin **does not bundle any vendor binaries, SDKs, or licenses** — users must install Simcenter Flotherm separately and supply their own license. See [LICENSE-NOTICE.md](LICENSE-NOTICE.md).

The driver is Windows-only — Flotherm itself only ships on Windows, and the driver uses `pywinauto` GUI automation (Flotherm has no headless batch API for first-time project setup).

## Install

```bash
pip install git+https://github.com/svd-ai-lab/sim-plugin-flotherm@main
```

After install, sim-cli auto-discovers the driver:

```bash
sim drivers | grep flotherm
sim run --solver flotherm path/to/project.pack
```

## How it works

The plugin registers via two entry-point groups:

```toml
[project.entry-points."sim.drivers"]
flotherm = "sim_plugin_flotherm:FlothermDriver"

[project.entry-points."sim.skills"]
flotherm = "sim_plugin_flotherm:skills_dir"
```

`sim.drivers` exposes the driver class; `sim.skills` exposes a directory of skill files bundled inside the wheel (workflows, FloSCRIPT XSD schemas, version-specific quirks).

## Develop

```bash
git clone https://github.com/svd-ai-lab/sim-plugin-flotherm
cd sim-plugin-flotherm
uv sync --extra test
uv run --extra test python -m pytest
```

Note: Tier-4 (real Flotherm) tests require Windows + a licensed Simcenter Flotherm install. Tier-1 / Tier-2 tests (detect, lint, FloSCRIPT/FloXML builders) run on macOS / Linux.

## License

Apache-2.0 for the plugin code itself. See [LICENSE](LICENSE) and [LICENSE-NOTICE.md](LICENSE-NOTICE.md).
