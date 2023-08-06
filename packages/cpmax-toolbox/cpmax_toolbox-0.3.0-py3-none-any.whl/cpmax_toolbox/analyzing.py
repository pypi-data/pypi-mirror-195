import pandas as pd
from pathlib import Path
import numpy as np
from scipy import signal

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("pdf")

from rich.progress import track
from cpmax_toolbox.file_repair import repair_file, parse_path

import typing


def filter_measurement(
    df: pd.DataFrame, fs=500, n_min: float = 0, n_max: float = 100, thres: float = 5000
) -> pd.DataFrame:
    def filt_ax(df):
        hit_thres = False
        for col in df.columns:
            hit_thres = hit_thres or (
                ((df[col].max() - df[col].mean()) > thres)
                or ((df[col].mean() - df[col].min()) > thres)
            )

        n = 60 * fs / len(df)
        out_of_nrange = n < n_min or n > n_max

        df["okay"] = 1 - (hit_thres or out_of_nrange)
        return df

    df_temp = df.copy()

    """ remove rotations where any max > thres """
    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    df_temp["okay"] = False

    dfs = df_temp.groupby("Revolutions", group_keys=True).apply(filt_ax)
    df_temp = dfs.reset_index(drop=True)

    return df_temp[df_temp["okay"].astype(bool)].reset_index(drop=True)[
        ["Axial", "Radial", "Torsional", "Trigger"]
    ]  # type:ignore - suppress type error from pylance


def calculate_angle_dependency(
    df: typing.Union[pd.DataFrame, Path, str],
    remove_mean: bool = True,
    angle_points=512,
    show_track=False,
) -> pd.DataFrame:
    if isinstance(df, str):
        df = parse_path(df)

    if isinstance(df, Path):
        try:
            df = pd.read_csv(df, skiprows=3, sep="\t")
        except:
            df = pd.read_csv(repair_file(df), skiprows=3, sep="\t")

    col_soll = {"Axial", "Radial", "Torsional", "Trigger"}
    col_ist = set(df.columns)
    if col_ist != col_soll:
        raise ValueError(f"columns in Dataframe not matching {{{', '.join(col_soll)}}}")

    df_temp = df.copy()
    if remove_mean:
        for ax in ["Axial", "Radial", "Torsional"]:
            df_temp[ax] = df_temp[ax] - df_temp[ax].mean()

    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    dfs = []

    if show_track:
        gen = lambda x: track(x, "calculating angle dependency...")
    else:
        gen = lambda x: x

    for i in gen(range(df_temp["Revolutions"].max())):
        dfi = df_temp[df_temp["Revolutions"] == i]
        keys = ["Axial", "Radial", "Torsional", "Trigger"]
        data = {}
        for k in keys:
            if k == "Trigger":
                data[k] = ((angle_points - 1) * [0]) + [1]
            else:
                data[k] = signal.resample(dfi[k], angle_points)

        dfs.append(pd.DataFrame(data))
    df_temp = pd.concat(dfs, ignore_index=True)
    return df_temp


def create_specs(
    df_meas: pd.DataFrame,
    output_pdf: typing.Union[Path, None] = None,
    prefix="",
    fs=512,
    xmin=0,
    xmax=5,
) -> None:
    """fft calculation and plot -> vibA design"""
    # fft_freqs = np.fft.fftfreq(int(len(df_meas)), 1/fs)[: len(df_meas) // 2]
    data = {"f": np.fft.fftfreq(int(len(df_meas)), 1 / fs)[: len(df_meas) // 2]}
    for ax in ["Axial", "Radial"]:
        data[ax] = (
            2 * np.abs(np.fft.fft(df_meas[ax]))[: len(df_meas) // 2] / len(df_meas)
        )

    df_fft = pd.DataFrame(data=data)

    fig, axs = plt.subplots(2, 1, sharey=True)
    colors = ["#ffa500", "#9acd32"]
    for i, ax in enumerate(["Axial", "Radial"]):
        axs[i].plot(df_fft["f"], df_fft[ax], label=ax, color=colors[i])
        axs[i].axis(xmin=xmin, xmax=xmax, ymin=0)
        axs[i].set_xlabel("Order / Frequency [Hz]")
        axs[i].set_ylabel("Amplitude [mm/s²]")
        axs[i].grid()
        axs[i].legend(loc="upper right")

    if output_pdf:
        fig.set_size_inches(10, 10)
        if output_pdf.is_dir():
            r_max = df_fft[np.abs(df_fft["f"] - 1) < df_fft["f"][1]].max()
            output_pdf = output_pdf / (
                prefix
                + f"__res_{df_fft['f'][1]:.5f}P__Ax_{r_max['Axial']:.2f}mms2__Rad_{r_max['Radial']:.2f}mms2.pdf"
            )

        fig.savefig(
            output_pdf,  # type:ignore - suppress pylint warning message (Path -> str not compatible)
            bbox_inches="tight",
            dpi=600,
        )
    else:
        plt.show()
