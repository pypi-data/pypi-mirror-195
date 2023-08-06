# -*- coding: utf-8 -*-

"""
 @Time    : 2022/11/16 15:01
 @Author  : Tianxiang Wang
 @Contact : wangtianxiang@hzwtech.com
 @License : Copyright(C), Hongzhiwei Technology (Shanghai) Co., LTD.
 @File    : rmsd.py
 @Desc    :
"""
from pymatgen.core.structure import Structure
import numpy as np
from typing import List
from dspawpy.io.utils import get_ele_from_h5, get_coordinateType_from_h5
import h5py

class RMSD:
    def __init__(self, structures: List[Structure]):
        self.structures = structures

        self.n_frames = len(self.structures)
        self.n_particles = len(self.structures[0])
        self.lattice = self.structures[0].lattice

        self._position_array = np.zeros(
            (self.n_frames, self.n_particles, 3))

        for i, s in enumerate(self.structures):
            self._position_array[i, :, :] = s.frac_coords

    def run(self, base_index=0):
        result = np.zeros(self.n_frames)
        rd = np.zeros((self.n_frames, self.n_particles, 3))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - \
                self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - \
                np.sign(disp[np.abs(disp) > 0.5])
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)

        for i in range(self.n_frames):
            sqdist = np.square(rd[i] - rd[base_index]).sum(axis=-1)
            result[i] = sqdist.mean()

        return np.sqrt(result)


def get_Structures(aimdh5: str = 'aimd.h5'):
    """get pymatgen structures from aimd.h5 file
    """
    data = h5py.File(aimdh5)

    Nstep = np.array(data.get('/Structures/FinalStep'))[0]
    coordinateType = get_coordinateType_from_h5(aimdh5)[0]
    is_direct = coordinateType == "Direct"
    ele = get_ele_from_h5(aimdh5)

    structures = []
    for i in range(Nstep):
        lat = np.array(data.get('/Structures/Step-%d/Lattice' % (i+1)))
        pos = np.array(data.get('/Structures/Step-%d/Position' % (i+1)))
        structure = Structure(
            lat, ele, pos, coords_are_cartesian=(not is_direct))
        structures.append(structure)

    return structures


def build_structure_list(filepath, ele1, ele2):
    if filepath.endswith('.json'):
        from monty.serialization import loadfn
        # Parse the DiffusionAnalyzer object from json file directly
        obj = loadfn(filepath)
        structure_list = []
        for i, s in enumerate(obj.get_drift_corrected_structures()):
            structure_list.append(s)
            if i == 9:
                break
    elif filepath.endswith('.h5'):
        # create Structure structure_list from aimd.h5
        structure_list = get_Structures(filepath)
    else:
        raise ValueError("File format not supported")

    return structure_list


if __name__ == "__main__":
    sl = build_structure_list('aimd.h5', 'H', 'O')
    result = RMSD(structures=sl).run()
    print(f'RMSD: {result}')
