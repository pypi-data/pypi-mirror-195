# -*- coding: utf-8 -*-

"""
 @Time    : 2022/10/26 9:41
 @Author  : Tianxiang Wang
 @Contact : wangtianxiang@hzwtech.com
 @License : Copyright(C), Hongzhiwei Technology (Shanghai) Co., LTD.
 @File    : msd.py
 @Desc    :
 
"""

from typing import List, Union

import numpy as np
from pymatgen.core.structure import Structure


# Mean Squared Displacement.  see  https://docs.mdanalysis.org/2.0.0/documentation_pages/analysis/msd.html#
class MSD:
    def __init__(self, structures: List[Structure], select: Union[str, List[int]] = "all", msd_type='xyz'):
        self.structures = structures
        self.msd_type = msd_type

        self.n_frames = len(structures)
        if select == "all":
            self.n_particles = len(structures[0])
        else:
            self.n_particles = len(select)
        self.lattice = structures[0].lattice

        self._parse_msd_type()

        self._position_array = np.zeros(
            (self.n_frames, self.n_particles, self.dim_fac))

        if select == "all":
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[:, self._dim]
        else:
            for i, s in enumerate(self.structures):
                self._position_array[i, :,
                                     :] = s.frac_coords[select, :][:, self._dim]

    def _parse_msd_type(self):
        r""" Sets up the desired dimensionality of the MSD.

        """
        keys = {'x': [0], 'y': [1], 'z': [2], 'xy': [0, 1],
                'xz': [0, 2], 'yz': [1, 2], 'xyz': [0, 1, 2]}

        self.msd_type = self.msd_type.lower()

        try:
            self._dim = keys[self.msd_type]
        except KeyError:
            raise ValueError(
                'invalid msd_type: {} specified, please specify one of xyz, '
                'xy, xz, yz, x, y, z'.format(self.msd_type))

        self.dim_fac = len(self._dim)

    def run(self):
        result = np.zeros((self.n_frames, self.n_particles))

        rd = np.zeros((self.n_frames, self.n_particles, self.dim_fac))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - \
                self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - \
                np.sign(disp[np.abs(disp) > 0.5])
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)
        for n in range(1, self.n_frames):
            disp = rd[n:, :, :] - rd[:-n, :, :]  # [n:-n] window
            sqdist = np.square(disp).sum(axis=-1)
            result[n, :] = sqdist.mean(axis=0)

        return result.mean(axis=1)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from dspawpy.io.structure import from_dspaw_atominfos
    import os
    if os.path.exists("aimd.json"):
        # read aimd.json file
        import json
        with open("aimd.json", "r") as file:
            aimd = json.load(file)
        # get [Structure ...]
        structures = from_dspaw_atominfos(aimd["Structures"])
    elif os.path.exists("aimd.h5"):
        # read aimd.h5 file
        import h5py
        hf = h5py.File('aimd.h5')
        structures = np.array(hf.get('/Structures'))
    else:
        print("No aimd.json or aimd.h5 file found.")
        exit()

    #                    select = "all"代表计算所有原子,计算前部分原子用[原子序号...],原子序号从0开始
    #                    msd_type = "xyz"代表计算距离时x,y,z分量都参与，可选x,y,z,xy,zx,yz,xyz
    msd = MSD(structures, select=[2], msd_type="xyz")
    result = msd.run()

    # Plot
    nframes = msd.n_frames
    timestep = 1  # this needs to be the actual time between frames
    lagtimes = np.arange(nframes) * timestep  # make the lag-time axis
    fig = plt.figure()
    ax = plt.axes()
    # plot the actual MSD
    ax.plot(lagtimes, result, c="black", ls="-")
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel("Mean Squared Displacement")
    plt.show()
