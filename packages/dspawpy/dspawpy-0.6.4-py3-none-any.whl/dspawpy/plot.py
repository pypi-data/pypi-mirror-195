# -*- coding: utf-8 -*-

import math, json
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import h5py
from numpy import pi
from scipy.interpolate import interp1d
from dspawpy.io.read import load_h5

import os
from dspawpy.diffusion.nebtools import get_neb_subfolders

def get_subfolders_quantum_totals(directory:str):
    """返回铁电极化计算任务的子目录、量子数、极化总量

    Parameters
    ----------
    directory : str
        铁电极化计算任务主目录
    
    Returns
    -------
    subfolders : list
        子目录列表
    quantum : np.ndarray
        量子数，xyz三个方向, shape=(1, 3)
    totals : np.ndarray
        极化总量，xyz三个方向, shape=(len(subfolders), 3)
    """
    subfolders = get_neb_subfolders(directory)

    if os.path.exists(f'{subfolders[0]}/polarization.json'):
        print('reading from polarization.json file')
        import json
        # quantum number if constant across the whole calculation,
        # so, read only once
        with open(f'{subfolders[0]}/polarization.json', 'r') as f:
            quantum = json.load(f)['PolarizationInfo']['Quantum']
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            with open('%s/polarization.json' % fd, 'r') as f:
                data = json.load(f)
            total = data['PolarizationInfo']['Total']
            print('Total: ', total)
            totals[i] = float(total)

    elif os.path.exists(f'{subfolders[0]}/scf.h5'):
        print('reading from scf.h5 file')
        import h5py
        # quantum number if constant across the whole calculation,
        # so, read only once
        quantum = np.array(h5py.File('./%s/scf.h5' %
                        subfolders[0]).get('/PolarizationInfo/Quantum'))
        # the Total number is not constant
        totals = np.empty(shape=(len(subfolders), 3))
        for i, fd in enumerate(subfolders):
            data = h5py.File('./%s/scf.h5' % fd)
            total = np.array(data.get('/PolarizationInfo/Total'))
            print('Total: ', total)
            totals[i] = total
    else:
        raise ValueError('no polarization.json or scf.h5 file found')

    return subfolders, quantum, totals


def plot_polarization_figure(directory:str, show:bool=True, fig_name:str='pol.png'):
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
    axes
        可传递给其他函数进行进一步处理
    """
    subfolders, quantum, totals = get_subfolders_quantum_totals(directory)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, sharey=True)
    xyz = ['x', 'y', 'z']
    for j in range(3):
        axes[j].plot(subfolders, totals[:, j], '.')
        for r in range(3):
            totals_up = totals + quantum*r
            totals_down = totals - quantum*r
            axes[j].plot(subfolders, totals_up[:, j], '.')
            axes[j].plot(subfolders, totals_down[:, j], '.')
        axes[j].set_title('P%s' % xyz[j])
        axes[j].xaxis.set_ticks(subfolders) # 设置x轴刻度
        axes[j].set_xticklabels(labels=subfolders, rotation=90)
        axes[j].grid(axis='x', color='gray', linestyle=':', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(fig_name)
    if show:
        plt.show()

    return axes

def getEwtData(nk, nb, celtot, proj_wt, ef, de, dele):
    emin = np.min(celtot) - de
    emax = np.max(celtot) - de

    emin = np.floor(emin - 0.2)
    emax = max(math.ceil(emax)*1.0, 5.0)

    nps = int((emax - emin) / de)

    X = np.zeros((nps + 1, nk))
    Y = np.zeros((nps + 1, nk))

    X2 = []
    Y2 = []
    Z2 = []

    for ik in range(nk):
        for ip in range(nps+1):
            omega = ip * de + emin + ef
            X[ip][ik] = ik
            Y[ip][ik] = ip*de+emin
            ewts_value = 0
            for ib in range(nb):
                smearing =  dele / pi / ((omega - celtot[ib][ik]) ** 2 + dele ** 2)
                ewts_value += smearing * proj_wt[ib][ik]
            if ewts_value>0.01:
                X2.append(ik)
                Y2.append(ip*de+emin)
                Z2.append(ewts_value)

    Z2_half = max(Z2)/2

    for i,x in enumerate(Z2):
        if x > Z2_half:
            Z2[i] = Z2_half

    plt.scatter(X2, Y2, c = Z2, cmap="hot")
    plt.xlim(0,200)
    plt.ylim(emin - 0.5, 15)
    ax = plt.gca()
    plt.colorbar()
    ax.set_facecolor("black")

    return plt

def get_plot_potential_along_axis(data,axis=2,smooth=False,smooth_frac=0.8,**kwargs):
    all_axis = [0,1,2]
    all_axis.remove(axis)
    y = np.mean(data,tuple(all_axis))
    x = np.arange(len(y))
    if smooth:
        s = sm.nonparametric.lowess(y, x, frac=smooth_frac)
        plt.plot(s[:,0], s[:,1], label="macroscopic average",**kwargs)

    plt.plot(x,y,label="planar electrostatic",**kwargs)
    return plt

def plot_potential_along_axis(potential_dir:str):
    if potential_dir.endswith(".h5"):
        potential = load_h5(potential_dir)
        grid = potential["/AtomInfo/Grid"]
        # pot = np.asarray(potential["/Potential/TotalElectrostaticPotential"]).reshape(grid, order="F")
        # DS-PAW 数据写入h5 列优先
        # h5py 从h5读取数据 默认行优先
        # np.array(data_list) 默认行优先
        # 所以这里先以 行优先 把 “h5 行优先 读进来的数据” 转成一维， 再以 列优先 转成 grid 对应的维度
        tmp_pot = np.asarray(potential["/Potential/TotalElectrostaticPotential"]).reshape([-1, 1], order="C")
        pot = tmp_pot.reshape(grid, order="F")
    elif potential_dir.endswith(".json"):
        with open(potential_dir, 'r') as f:
            potential = json.load(f)

        grid = potential["AtomInfo"]["Grid"]
        pot = np.asarray(potential["Potential"]["TotalElectrostaticPotential"]).reshape(grid, order="F")
    else:
        print("file - " + potential_dir + " :  Unsupported format!")
        return

    return get_plot_potential_along_axis(pot, axis=2, smooth=False)

def plot_optical(optical_dir:str,key:str,index:int=0):
    """

    Args:
        optical_h5: optical.h5 filename
        key: "AbsorptionCoefficient","ExtinctionCoefficient","RefractiveIndex","Reflectance"
        index:

    Returns:

    """
    if optical_dir.endswith("h5"):
        data_all = load_h5(optical_dir)
        energy = data_all["/OpticalInfo/EnergyAxe"]
        data = data_all["/OpticalInfo/" + key]
    elif optical_dir.endswith("json"):
        with open(optical_dir, 'r') as fin:
            data_all = json.load(fin)

        energy = data_all["OpticalInfo"]["EnergyAxe"]
        data = data_all["OpticalInfo"][key]
    else:
        print("file - " + optical_dir + " :  Unsupported format!")
        return

    data = np.asarray(data).reshape(len(energy),6)[:,index]

    inter_f = interp1d(energy, data, kind="cubic")
    energy_spline = np.linspace(energy[0],energy[-1],2001)
    data_spline = inter_f(energy_spline)

    plt.plot(energy_spline,data_spline,c="b")
    plt.xlabel("Photon energy (eV)")
    plt.ylabel("%s %s"%(key,r"$\alpha (\omega )(cm^{-1})$"))

def plot_bandunfolding(band_dir:str, ef=0.0, de=0.05, dele= 0.06):
    if band_dir.endswith(".h5"):
        band = load_h5(band_dir)
        number_of_band = band["/BandInfo/NumberOfBand"][0]
        number_of_kpoints = band["/BandInfo/NumberOfKpoints"][0]
        data = band["/UnfoldingBandInfo/Spin1/UnfoldingBand"]
        weight = band["/UnfoldingBandInfo/Spin1/Weight"]
    elif band_dir.endswith(".json"):
        with open(band_dir, 'r') as f:
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


def read_aimd_converge_data(h5file, index: str = None):
    """从h5file指定的路径读取h5文件所需的数据

    ----------
    输入:
        h5file (str): h5文件位置

    ----------
    输出:
        xs (np.array): x轴数据
        ys (np.array): y轴数据
    """
    hf = h5py.File(h5file)  # 加载h5文件
    Nstep = len(np.array(hf.get('/Structures')))-2  # 步数（可能存在未完成的）
    ys = np.empty(Nstep)  # 准备一个空数组

    # 开始读取
    if index == '5':
        for i in range(1, Nstep+1):
            ys[i-1] = np.linalg.det(hf.get('/Structures/Step-%d/Lattice' % i))
    else:
        map = {'1': 'IonsKineticEnergy',
               '2': 'TotalEnergy0',
               '3': 'PressureKinetic',
               '4': 'Temperature'}
        for i in range(1, Nstep+1):
            # 如果计算中断，则没有PressureKinetic这个键
            try:
                ys[i-1] = np.array(hf.get('/AimdInfo/Step-%d/%s' %
                                   (i, map[index])))
            except:
                ys[i-1] = 0
                ys = np.delete(ys, -1)
                print(f'-> 计算中断于第{Nstep}步，未读取到该步的压力数据！')

    Nstep = len(ys)  # 步数更新为实际完成的步数

    # 返回xs，ys两个数组
    return np.linspace(1, Nstep, Nstep), np.array(ys)


def plot_aimd(h5file: str = 'aimd.h5',
              show: bool = False,
              figName: str ='aimd.png',
              flags_str: str = None):
    """根据用户指定的h5文件画图

    ----------
    输入:
        h5file (str, optional): h5文件位置. 默认 'aimd.h5'.
        show (bool, optional): 是否展示交互界面. 默认 False.
        figName (str, optional): 保存的图片名. 默认 'aimd.h5'.
        flags_str (str, optional): 子图编号. 默认全部绘制.

    ----------
    结果：
        aimd.png
    """
    print(f'{flags_str=}')
    # 处理用户输入，按顺序去重
    temp = set()
    if flags_str == '' or flags_str == None:
        flags = ['1', '2', '3', '4', '5']
    else:
        flags = [x for x in flags_str if x not in temp and (temp.add(x) or True)]
        flags.remove(' ') # remove wierd empty string
        
    for flag in flags:
        assert flag in ['1', '2', '3', '4', '5'], "输入错误！"

    # 开始画组合图
    N_figs = len(flags)
    fig, axes = plt.subplots(N_figs, 1, sharex=True, figsize=(6, 2*N_figs))
    if N_figs == 1:  # 'AxesSubplot' object is not subscriptable
        axes = [axes]  # 避免上述类型错误
    fig.suptitle('DSPAW AIMD')
    for i, flag in enumerate(flags):
        print('正在处理子图'+flag)
        # 读取数据
        xs, ys = read_aimd_converge_data(h5file, flag)
        axes[i].plot(xs, ys)  # 绘制坐标点
        # 子图的y轴标签
        if flag == '1':
            axes[i].set_ylabel('Kinetic Energy (eV)')
        elif flag == '2':
            axes[i].set_ylabel('Energy (eV)')
        elif flag == '3':
            axes[i].set_ylabel('Pressure Kinetic (kbar)')
        elif flag == '4':
            axes[i].set_ylabel('Temperature (K)')
        else:
            axes[i].set_ylabel('Volume (Angstrom^3)')

    fig.tight_layout()
    plt.savefig(figName)
    if show:
        plt.show()

    print(f'--> 图片已保存为 {os.path.abspath(figName)}')


# if __name__ == "__main__":
#     path = "./../test/band/2.22.1/band.h5"
#     p = plot_bandunfolding(path, ef=7.6923)
#     p.savefig("bandunfolding_plot.png")
#     p.show()
    