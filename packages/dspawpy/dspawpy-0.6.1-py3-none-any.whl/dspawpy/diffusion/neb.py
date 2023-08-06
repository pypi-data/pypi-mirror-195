# -*- coding: utf-8 -*-
import json
import os
from typing import List

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from pymatgen.core import Structure
from dspawpy.io.read import load_h5
from dspawpy.io.structure import to_file
from dspawpy.diffusion.pathfinder import IDPPSolver


class NEB:
    """

    Args:
        initial_structure:
        final_structure:
        nimages: number of images,contain initial and final structure
    """

    def __init__(self, initial_structure, final_structure, nimages):
        """

        Args:
            initial_structure:
            final_structure:
            nimages: number of images,contain initial and final structure
        """

        self.nimages = nimages
        self.iddp = IDPPSolver.from_endpoints(
            endpoints=[initial_structure, final_structure], nimages=self.nimages - 2)

    def linear_interpolate(self):
        return self.iddp.structures

    def idpp_interpolate(
        self,
        maxiter=1000,
        tol=1e-5,
        gtol=1e-3,
        step_size=0.05,
        max_disp=0.05,
        spring_const=5.0,
    ):
        """

        Args:
            maxiter:
            tol:
            gtol:
            step_size:
            max_disp:
            spring_const:

        Returns:

        """
        return self.iddp.run(maxiter, tol, gtol, step_size, max_disp, spring_const)


def write_neb_structures(structures: List[Structure], coords_are_cartesian=True, fmt: str = "json", path: str = ".", prefix="structure"):
    """

    Args:
        structures: list of structures
        coords_are_cartesian:
        fmt: support "json","as","poscar","hzw"
        path: output path
        prefix: structure prefix name if fmt != "poscar"

    """
    N = len(str(len(structures)))
    if N <= 2:
        N = 2
    for i, structure in enumerate(structures):
        path_name = str(i).zfill(N)
        os.makedirs(os.path.join(path, path_name), exist_ok=True)
        if fmt == "poscar":
            structure.to(fmt="poscar", filename=os.path.join(
                path, path_name, "POSCAR"))
        else:
            filename = os.path.join(
                path, path_name, "%s%s.%s" % (prefix, path_name, fmt))
            to_file(structure, filename,
                    coords_are_cartesian=coords_are_cartesian, fmt=fmt)


def plot_neb_barrier(neb_dir: str, ri: float = None, rf: float = None, ei: float = None, ef: float = None):
    if neb_dir.endswith(".h5"):
        neb = load_h5(neb_dir)
        reaction_coordinate = neb["/Distance/ReactionCoordinate"]
        energy = neb["/Energy/TotalEnergy"]
    elif neb_dir.endswith(".json"):
        with open(neb_dir, 'r') as fin:
            neb = json.load(fin)

        reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
        energy = neb["Energy"]["TotalEnergy"]
    else:
        print("file - " + neb_dir + " :  Unsupported format!")
        return

    x = []
    for c in reaction_coordinate:
        if len(x) > 0:
            x.append(x[-1] + c)
        else:
            x.append(c)

    y = [x-energy[0] for x in energy]

    if ri is not None:  # add initial reaction coordinate
        x.insert(0, ri)
    if rf is not None:  # add final reaction coordinate
        x.append(rf)

    if ei is not None:  # add initial energy
        y.insert(0, ei)
    if ef is not None:  # add final energy
        y.append(ef)

    inter_f = interp1d(x, y, kind="cubic")
    xnew = np.linspace(x[0], x[-1], 100)
    ynew = inter_f(xnew)

    plt.plot(xnew, ynew, c="b")
    plt.scatter(x, y, c="r")
    plt.xlabel("Reaction Coordinate")
    plt.ylabel("Energy")
    # plt.show()


def plot_neb_converge(neb_dir: str, image_key="01"):
    """

    Args:
        neb_dir: neb.h5 directory
        image_key: image key 01,02,03...

    Returns:
            subplot left ax,right ax
    """
    if os.path.exists(f"{neb_dir}/neb.h5"):
        neb_total = load_h5(f"{neb_dir}/neb.h5")
        maxforce = np.array(neb_total["/Iteration/" + image_key + "/MaxForce"])
        total_energy = np.array(
            neb_total["/Iteration/" + image_key + "/TotalEnergy"])

    elif os.path.exists(f"{neb_dir}/neb.json"):
        with open(f"{neb_dir}/neb.json", 'r') as fin:
            neb_total = json.load(fin)
        neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

        maxforce = np.array(maxforce)
        total_energy = np.array(total_energy)

    else:
        print(f"{neb_dir}路径中找不到neb.h5或者neb.json文件")

    x = np.arange(len(maxforce))

    force = maxforce
    energy = total_energy

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, force, label="Max Force", c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force")

    ax2 = ax1.twinx()
    ax2.plot(x, energy, label="Energy", c="r")
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy")
    ax2.ticklabel_format(useOffset=False)  # y轴坐标显示绝对值而不是相对值

    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    plt.tight_layout()

    return ax1, ax2
