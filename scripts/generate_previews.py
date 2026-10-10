"""Render real XJTU-MPE previews from a locally downloaded recording.

Requires numpy, pandas and matplotlib. The event input is the byte range
90,000,000–91,799,999 of data/900W/1/event.csv; partial boundary lines are
discarded. No raw recording is added to the website repository.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("input", type=Path)
parser.add_argument("--output", type=Path, default=Path("static/images"))
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)

BG, TEXT, GRID = "#101e31", "#c8d4e5", "#2c3c51"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
    "xtick.color": TEXT, "ytick.color": TEXT, "text.color": TEXT,
    "savefig.facecolor": BG,
})

lines = (args.input / "event-slice.csv").read_text().splitlines()
events = np.array([line.split(",") for line in lines[1:-1]], dtype=np.int64)
t0 = int(events[0, 0])
window = events[(events[:, 0] >= t0) & (events[:, 0] < t0 + 10_000)]
fig, ax = plt.subplots(figsize=(9, 5.1), dpi=160)
for polarity, color, label in [(0, "#70c3ff", "Negative (p = 0)"), (1, "#f3ba73", "Positive (p = 1)")]:
    points = window[window[:, 3] == polarity]
    ax.scatter(points[:, 1], points[:, 2], s=1.6, c=color, alpha=.8, linewidths=0, label=label, rasterized=True)
ax.set_xlim(375, 937)
ax.set_ylim(637, 75)
ax.set_aspect("equal")
ax.set_xlabel("Sensor x (pixels)")
ax.set_ylabel("Sensor y (pixels)")
ax.legend(loc="upper right", facecolor=BG, edgecolor=GRID, markerscale=4, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(pad=2)
fig.savefig(args.output / "event-preview.png")
plt.close(fig)

parameters = pd.read_csv(args.input / "para.csv", encoding="utf-8-sig", skiprows=[1])
time = parameters["timestamp"].to_numpy() / 1e6
power = parameters["laser_power"].to_numpy() * 6
fig, ax = plt.subplots(figsize=(9, 5.1), dpi=160)
ax.plot(time, power, color="#f3ba73", linewidth=2)
ax.fill_between(time, power, color="#f3ba73", alpha=.08)
ax.axvspan(t0 / 1e6, (t0 + 10_000) / 1e6, color="#70c3ff", alpha=.7, label="Event preview window")
ax.set_xlabel("Recording timestamp (s)")
ax.set_ylabel("Total laser power (W)")
ax.set_ylim(-30, 1050)
ax.set_xlim(time[0], time[-1])
ax.grid(axis="y", color=GRID, linewidth=.6)
ax.legend(loc="upper right", facecolor=BG, edgecolor=GRID, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(pad=2)
fig.savefig(args.output / "power-preview.png")
plt.close(fig)

scan = np.loadtxt(args.input / "3dscan.asc", usecols=(0, 1, 2))
sample = scan[::40]
fig = plt.figure(figsize=(9, 5.1), dpi=160)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(BG)
scatter = ax.scatter(*sample.T, c=sample[:, 2], cmap="cividis", s=1.5, linewidths=0, rasterized=True,
                     norm=Normalize(*np.quantile(scan[:, 2], [.01, .99])))
ax.set_box_aspect((6, 1.3, 1))
ax.view_init(elev=28, azim=-76)
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.pane.fill = False
    axis.pane.set_edgecolor(GRID)
    axis._axinfo["grid"]["color"] = GRID
ax.set_xlabel("Scan x", labelpad=10)
ax.set_yticks([])
ax.set_zticks([])
ax.set_ylabel("")
ax.set_zlabel("")
ax.tick_params(colors=TEXT, labelsize=8)
fig.subplots_adjust(left=0, right=.93, bottom=.08, top=.98)
colorbar = fig.colorbar(scatter, ax=ax, shrink=.5, pad=.03, aspect=18)
colorbar.set_label("Scan z coordinate")
colorbar.outline.set_edgecolor(GRID)
fig.savefig(args.output / "scan-preview.png")
plt.close(fig)

base = "https://huggingface.co/datasets/ahqiutkp/XJTU-MPE/resolve/main/data/900W/1/"
provenance = {
    "recording": "900W/1", "retrieved": "2026-10-10",
    "source_urls": {file: base + file for file in ["event.csv", "para.csv", "3dscan.asc"]},
    "event_byte_range": [90_000_000, 91_799_999],
    "event_window_us": [t0, t0 + 10_000],
    "event_count": len(window),
    "parameter_count": len(parameters),
    "scan_point_count": len(scan),
    "displayed_scan_point_count": len(sample),
    "scan_sampling": "Every 40th point in file order; original XYZ coordinates, no plane fitting.",
    "power_conversion": "laser_power multiplied by 6 to match nominal total power in watts.",
    "sha256": {name: hashlib.sha256((args.input / name).read_bytes()).hexdigest()
               for name in ["event-slice.csv", "para.csv", "3dscan.asc"]},
}
(args.output / "preview-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
print(json.dumps({key: provenance[key] for key in ["event_window_us", "event_count", "scan_point_count"]}))
