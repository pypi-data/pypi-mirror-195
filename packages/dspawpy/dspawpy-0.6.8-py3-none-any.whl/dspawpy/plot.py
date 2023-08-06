# -*- coding: utf-8 -*-

import math
import json
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import h5py
from scipy.interpolate import interp1d
from dspawpy.io.read import load_h5

import os


def get_subfolders_quantum_totals(directory: str):
    """返回铁电极化计算任务的子目录、量子数、极化总量；
    请勿创建其他子目录，否则会被错误读取

    Parameters
    ----------
    directory：str
        铁电极化计算任务主目录

    Returns
    -------
    subfolders : list
        子目录列表
    quantum : np.ndarray
        量子数，xyz三个方向, shape=(1, 3)
    totals : np.ndarray
        极化总量，xyz三个方向, shape=(len(subfolders), 3)

    Examples
    --------
    >>> from dspawpy.plot import get_subfolders_quantum_totals
    >>> directory = '.' # current directory
    >>> subfolders, quantum, totals = get_subfolders_quantum_totals(directory)
    >>> subfolders
    ['S00', 'S01', 'S06', 'S02', 'S07', 'S03', 'S08', 'S04', 'S10', 'S09', 'S05', 'S11']
    >>> quantum
    array([60.06722499, 60.38782135, 62.58443595])
    >>> totals
    array([[-4.28508315e-05, -8.71560447e+00, -1.95833103e-06],
           [-2.67572295e-05,  6.03528774e+00, -3.07857463e-06],
           [-2.14180047e-05,  5.74655747e+00,  1.54336369e-05],
           [-6.11371699e-05,  1.92736107e+01, -2.87951455e-05],
           [ 3.98336164e-05,  1.72479105e+01, -2.75634797e-06],
           [ 1.20422859e-05, -2.89108722e+01, -1.72015009e-05],
           [ 5.23329032e-05,  2.89106070e+01, -5.19480945e-06],
           [-2.86362371e-05, -1.72479598e+01, -3.61790588e-05],
           [-5.52844691e-05, -6.03482453e+00, -2.71118952e-05],
           [-3.63338519e-05, -1.92737729e+01, -6.94462350e-06],
           [ 9.30116520e-06, -5.74668477e+00,  2.91334059e-05],
           [-4.53814037e-05,  8.71545041e+00,  1.18885825e-06]])
    """

    subfolders = next(os.walk(directory))[1]
    if os.path.exists(f"{subfolders[0]}/polarization.json"):
        # quantum number if constant across the whole calculation,
        # so, read only once
        with open(f"{subfolders[0]}/polarization.json", "r") as f:
            quantum = json.load(f)["PolarizationInfo"]["Quantum"]
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            with open("%s/polarization.json" % fd, "r") as f:
                data = json.load(f)
            total = data["PolarizationInfo"]["Total"]
            print("Total: ", total)
            totals[i] = float(total)

    elif os.path.exists(f"{subfolders[0]}/scf.h5"):
        # quantum number if constant across the whole calculation,
        # so, read only once
        quantum = np.array(
            h5py.File(f"{subfolders[0]}/scf.h5").get("/PolarizationInfo/Quantum")
        )
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            data = h5py.File("./%s/scf.h5" % fd)
            total = np.array(data.get("/PolarizationInfo/Total"))
            totals[i] = total
    else:
        raise ValueError("no polarization.json or scf.h5 file found")

    return subfolders, quantum, totals


def plot_polarization_figure(
    directory: str, show: bool = True, fig_name: str = "pol.png"
):
    """绘制铁电极化结果图

    Parameters
    ----------
    directory : str
        铁电极化计算任务主目录
    show : bool, optional
        是否交互显示图片, by default True
    fig_name : str, optional
        图片保存路径, by default 'pol.png'

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------
    >>> from dspawpy.plot import plot_polarization_figure
    >>> directory = '.' # current directory
    >>> plot_polarization_figure(directory, fig_name='pol.png')
    --> saved to pol.png
    """
    subfolders, quantum, totals = get_subfolders_quantum_totals(directory)

    fig, axes = plt.subplots(1, 3, sharey=True)
    xyz = ["x", "y", "z"]
    for j in range(3):
        axes[j].plot(subfolders, totals[:, j], ".")
        for r in range(3):
            totals_up = totals + quantum * r
            totals_down = totals - quantum * r
            axes[j].plot(subfolders, totals_up[:, j], ".")
            axes[j].plot(subfolders, totals_down[:, j], ".")
        axes[j].set_title("P%s" % xyz[j])
        axes[j].xaxis.set_ticks(subfolders)  # 设置x轴刻度
        axes[j].set_xticklabels(labels=subfolders, rotation=90)
        axes[j].grid(axis="x", color="gray", linestyle=":", linewidth=0.5)

    plt.tight_layout()
    if fig_name:
        plt.savefig(fig_name)
        print(f"--> saved to {fig_name}")
    if show:
        plt.show()

    return axes


def getEwtData(nk, nb, celtot, proj_wt, ef, de, dele):
    emin = np.min(celtot) - de
    emax = np.max(celtot) - de

    emin = np.floor(emin - 0.2)
    emax = max(math.ceil(emax) * 1.0, 5.0)

    nps = int((emax - emin) / de)

    X = np.zeros((nps + 1, nk))
    Y = np.zeros((nps + 1, nk))

    X2 = []
    Y2 = []
    Z2 = []

    for ik in range(nk):
        for ip in range(nps + 1):
            omega = ip * de + emin + ef
            X[ip][ik] = ik
            Y[ip][ik] = ip * de + emin
            ewts_value = 0
            for ib in range(nb):
                smearing = dele / np.pi / ((omega - celtot[ib][ik]) ** 2 + dele**2)
                ewts_value += smearing * proj_wt[ib][ik]
            if ewts_value > 0.01:
                X2.append(ik)
                Y2.append(ip * de + emin)
                Z2.append(ewts_value)

    Z2_half = max(Z2) / 2

    for i, x in enumerate(Z2):
        if x > Z2_half:
            Z2[i] = Z2_half

    plt.scatter(X2, Y2, c=Z2, cmap="hot")
    plt.xlim(0, 200)
    plt.ylim(emin - 0.5, 15)
    ax = plt.gca()
    plt.colorbar()
    ax.set_facecolor("black")

    return plt


def plot_potential_along_axis(potential_dir: str, axis=2, smooth=False, smooth_frac=0.8, **kwargs):
    """绘制沿着某个轴向的势能曲线

    Parameters
    ----------
    potential_dir : str
        势能文件路径
    axis : int, optional
        沿着哪个轴向绘制势能曲线, 默认2
    smooth : bool, optional
        是否平滑, 默认False
    smooth_frac : float, optional
        平滑系数, 默认0.8
    **kwargs : dict
        其他参数, 传递给 matplotlib.pyplot.plot

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理
    """
    if potential_dir.endswith(".h5"):
        potential = load_h5(potential_dir)
        grid = potential["/AtomInfo/Grid"]
        # pot = np.asarray(potential["/Potential/TotalElectrostaticPotential"]).reshape(grid, order="F")
        # DS-PAW 数据写入h5 列优先
        # h5py 从h5读取数据 默认行优先
        # np.array(data_list) 默认行优先
        # 所以这里先以 行优先 把 “h5 行优先 读进来的数据” 转成一维， 再以 列优先 转成 grid 对应的维度
        tmp_pot = np.asarray(
            potential["/Potential/TotalElectrostaticPotential"]
        ).reshape([-1, 1], order="C")
        pot = tmp_pot.reshape(grid, order="F")
    elif potential_dir.endswith(".json"):
        with open(potential_dir, "r") as f:
            potential = json.load(f)

        grid = potential["AtomInfo"]["Grid"]
        pot = np.asarray(potential["Potential"]["TotalElectrostaticPotential"]).reshape(
            grid, order="F"
        )
    else:
        print(f'only support .h5 or .json file, but got {potential_dir}')
        return

    all_axis = [0, 1, 2]
    all_axis.remove(axis)
    y = np.mean(pot, tuple(all_axis))
    x = np.arange(len(y))
    if smooth:
        s = sm.nonparametric.lowess(y, x, frac=smooth_frac)
        plt.plot(s[:, 0], s[:, 1], label="macroscopic average", **kwargs)

    plt.plot(x, y, label="planar electrostatic", **kwargs)
    return plt


def plot_optical(optical_dir: str, key: str, index: int = 0):
    """TODO

    Args:
        optical_h5: optical.h5 filename
        key: "AbsorptionCoefficient","ExtinctionCoefficient","RefractiveIndex","Reflectance"
        index:

    结果:

    """
    if optical_dir.endswith("h5"):
        data_all = load_h5(optical_dir)
        energy = data_all["/OpticalInfo/EnergyAxe"]
        data = data_all["/OpticalInfo/" + key]
    elif optical_dir.endswith("json"):
        with open(optical_dir, "r") as fin:
            data_all = json.load(fin)

        energy = data_all["OpticalInfo"]["EnergyAxe"]
        data = data_all["OpticalInfo"][key]
    else:
        print("file - " + optical_dir + " :  Unsupported format!")
        return

    data = np.asarray(data).reshape(len(energy), 6)[:, index]

    inter_f = interp1d(energy, data, kind="cubic")
    energy_spline = np.linspace(energy[0], energy[-1], 2001)
    data_spline = inter_f(energy_spline)

    plt.plot(energy_spline, data_spline, c="b")
    plt.xlabel("Photon energy (eV)")
    plt.ylabel("%s %s" % (key, r"$\alpha (\omega )(cm^{-1})$"))


def plot_bandunfolding(band_dir: str, ef=0.0, de=0.05, dele=0.06):
    """TODO

    Parameters
    ----------
    band_dir : str
        _description_
    ef : float, optional
        _description_, by default 0.0
    de : float, optional
        _description_, by default 0.05
    dele : float, optional
        _description_, by default 0.06

    Returns
    -------
    _type_
        _description_
    """
    if band_dir.endswith(".h5"):
        band = load_h5(band_dir)
        number_of_band = band["/BandInfo/NumberOfBand"][0]
        number_of_kpoints = band["/BandInfo/NumberOfKpoints"][0]
        data = band["/UnfoldingBandInfo/Spin1/UnfoldingBand"]
        weight = band["/UnfoldingBandInfo/Spin1/Weight"]
    elif band_dir.endswith(".json"):
        with open(band_dir, "r") as f:
            band = json.load(f)
        number_of_band = band["BandInfo"]["NumberOfBand"]
        number_of_kpoints = band["BandInfo"]["NumberOfKpoints"]
        data = band["UnfoldingBandInfo"]["Spin1"]["UnfoldingBand"]
        weight = band["UnfoldingBandInfo"]["Spin1"]["Weight"]
    else:
        print("file - " + band_dir + " :  Unsupported format!")
        return

    celtot = np.array(data).reshape((number_of_kpoints, number_of_band)).T
    proj_wt = np.array(weight).reshape((number_of_kpoints, number_of_band)).T

    return getEwtData(number_of_kpoints, number_of_band, celtot, proj_wt, ef, de, dele)


def _read_aimd_converge_data(h5file: str, index: str = None):
    """从h5file指定的路径读取index指定的数据，返回绘图用的xs和ys两个数组

    Parameters
    ----------
    h5file : str
        hdf5文件路径
    index : str, optional
        编号, by default None

    Returns
    -------
    xs : np.ndarray
        x轴数据
    ys : np.ndarray
        y轴数据
    """
    hf = h5py.File(h5file)  # 加载h5文件
    Nstep = len(np.array(hf.get("/Structures"))) - 2  # 步数（可能存在未完成的）
    ys = np.empty(Nstep)  # 准备一个空数组

    # 开始读取
    if index == "5":
        for i in range(1, Nstep + 1):
            ys[i - 1] = np.linalg.det(hf.get("/Structures/Step-%d/Lattice" % i))
    else:
        map = {
            "1": "IonsKineticEnergy",
            "2": "TotalEnergy0",
            "3": "PressureKinetic",
            "4": "Temperature",
        }
        for i in range(1, Nstep + 1):
            # 如果计算中断，则没有PressureKinetic这个键
            try:
                ys[i - 1] = np.array(hf.get("/AimdInfo/Step-%d/%s" % (i, map[index])))
            except:
                ys[i - 1] = 0
                ys = np.delete(ys, -1)
                print(f"-> 计算中断于第{Nstep}步，未读取到该步的压力数据！")

    Nstep = len(ys)  # 步数更新为实际完成的步数

    # 返回xs，ys两个数组
    return np.linspace(1, Nstep, Nstep), np.array(ys)


def plot_aimd(
    h5file: str = "aimd.h5",
    show: bool = False,
    figName: str = "aimd.png",
    flags_str: str = None,
):
    """根据用户指定的h5文件画图

    Parameters
    ----------
    h5file : str
        h5文件位置. 默认 'aimd.h5'.
    show : bool
        是否展示交互界面. 默认 False.
    figName : str
        保存的图片名. 默认 'aimd.h5'.
    flags_str : str
        子图编号. 默认全部绘制.

    Returns
    ----------
    figName : str
        保存图片，默认aimd.png

    Examples
    ----------
    >>> from dspawpy.plot import plot_aimd
    >>> plot_aimd(h5file='aimd.h5', show=True)
    """
    print(f"{flags_str=}")
    # 处理用户读取，按顺序去重
    temp = set()
    if flags_str == "" or flags_str == None:
        flags = ["1", "2", "3", "4", "5"]
    else:
        flags = [x for x in flags_str if x not in temp and (temp.add(x) or True)]
        flags.remove(" ")  # remove wierd empty string

    for flag in flags:
        assert flag in ["1", "2", "3", "4", "5"], "读取错误！"

    # 开始画组合图
    N_figs = len(flags)
    fig, axes = plt.subplots(N_figs, 1, sharex=True, figsize=(6, 2 * N_figs))
    if N_figs == 1:  # 'AxesSubplot' object is not subscriptable
        axes = [axes]  # 避免上述类型错误
    fig.suptitle("DSPAW AIMD")
    for i, flag in enumerate(flags):
        print("正在处理子图" + flag)
        # 读取数据
        xs, ys = _read_aimd_converge_data(h5file, flag)
        axes[i].plot(xs, ys)  # 绘制坐标点
        # 子图的y轴标签
        if flag == "1":
            axes[i].set_ylabel("Kinetic Energy (eV)")
        elif flag == "2":
            axes[i].set_ylabel("Energy (eV)")
        elif flag == "3":
            axes[i].set_ylabel("Pressure Kinetic (kbar)")
        elif flag == "4":
            axes[i].set_ylabel("Temperature (K)")
        else:
            axes[i].set_ylabel("Volume (Angstrom^3)")

    fig.tight_layout()
    plt.savefig(figName)
    if show:
        plt.show()

    print(f"--> 图片已保存为 {os.path.abspath(figName)}")
