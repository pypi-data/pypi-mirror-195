# -*- coding: utf-8 -*-
import json
import h5py
import numpy as np
from typing import Dict, List
from dspawpy.io.read import load_h5


def write_atoms(fileobj, hdf5):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = np.asarray(hdf5["/AtomInfo/Lattice"]).reshape(-1,1)    # 将列表lattice下的多个列表整合

    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[0], lattice[1], lattice[2]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[3], lattice[4], lattice[5]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[6], lattice[7], lattice[8]))

    elements = hdf5["/AtomInfo/Elements"]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%5d" % (elements_number[e]))
    fileobj.write("\n")
    if hdf5["/AtomInfo/CoordinateType"][0] == "Direct":
        fileobj.write("Direct\n")
    else:
        fileobj.write("Cartesian\n")
    for i, p in enumerate(hdf5["/AtomInfo/Position"]):
        fileobj.write("%10.6f" % p)
        if (i + 1) % 3 == 0:
            fileobj.write("\n")
    fileobj.write("\n")

def write_VESTA_format(hdf5:Dict, datakeys:str, filename):
    with open(filename, 'w') as file:
        write_atoms(file, hdf5)
        for key in datakeys:
            d = np.asarray(hdf5[key]).reshape(-1,1)     # 将列表hdf5[key]下的多个列表整合
            file.write("%5d %5d %5d\n" % tuple(hdf5["/AtomInfo/Grid"]))
            i = 0
            while i < len(d):
                for j in range(10):
                    file.write("%10.5f " % d[i])
                    i += 1
                    if i >= len(d):
                        break
                file.write("\n")

            file.write("\n")

def write_atoms_json(fileobj, atom_info):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = atom_info["Lattice"]

    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[0], lattice[1], lattice[2]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[3], lattice[4], lattice[5]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[6], lattice[7], lattice[8]))

    elements = [atom["Element"] for atom in atom_info["Atoms"]]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%5d" % (elements_number[e]))
    fileobj.write("\n")
    if atom_info["CoordinateType"] == "Direct":
        fileobj.write("Direct\n")
    else:
        fileobj.write("Cartesian\n")
    for atom in atom_info["Atoms"]:
        fileobj.write("%10.6f %10.6f %10.6f\n" % tuple(atom["Position"]))
    fileobj.write("\n")

def write_VESTA_format_json(atom_info: Dict, data: List, filename):
    with open(filename, 'w') as file:
        write_atoms_json(file, atom_info)
        for d in data:
            file.write("%5d %5d %5d\n" % tuple(atom_info["Grid"]))
            i = 0
            while i < len(d):
                for j in range(10):
                    file.write("%10.5f " % d[i])
                    i += 1
                    if i >= len(d):
                        break
                file.write("\n")

            file.write("\n")

def write_VESTA(in_filename:str, data_type, out_filename="DS-PAW.vesta"):
    """

    Args:
        in_filename:
        data_type:   "rho" / "Rho" / "RHO"
                    "potential" / "Potential" / "POTENTIAL"
                    "elf" / "Elf" / "ELF"
                    "pcharge" / "Pcharge" / "PCHARGE"
                    "boundcharge" / "BoundCharge" / "BOUNDCHARGE"
        out_filename:

    Returns:

    """
    if in_filename.endswith(".h5"):
        data = load_h5(in_filename)
        if data_type == "rho" or data_type == "Rho" or data_type == "RHO":
            write_VESTA_format(data, ["/Rho/TotalCharge"], out_filename)

        elif data_type == "potential" or data_type == "Potential" or data_type == "POTENTIAL":
            write_VESTA_format(data, ["/Potential/TotalElectrostaticPotential", "/Potential/TotalLocalPotential"], out_filename)

        elif data_type == "elf" or data_type == "Elf" or data_type == "ELF":
            write_VESTA_format(data, ["/ELF/TotalELF"], out_filename)

        elif data_type == "pcharge" or data_type == "Pcharge" or data_type == "PCHARGE":
            write_VESTA_format(data, ["/Pcharge/1/TotalCharge"], out_filename)

        elif data_type == "boundcharge" or data_type == "BoundCharge" or data_type == "BOUNDCHARGE":
            write_VESTA_format(data, ["/Rho"], out_filename)

        else:
            print(" -rho/potential/elf/pcharge- ONLY")
            return

    elif in_filename.endswith(".json"):
        with open(in_filename, 'r') as fin:
            data = json.load(fin)

        if data_type == "rho" or data_type == "Rho" or data_type == "RHO":
            write_VESTA_format_json(data["AtomInfo"], [data["Rho"]["TotalCharge"]], out_filename)

        elif data_type == "potential" or data_type == "Potential" or data_type == "POTENTIAL":
            write_VESTA_format_json(data["AtomInfo"], [data["Potential"]["TotalElectrostaticPotential"], data["Potential"]["TotalLocalPotential"]], out_filename)

        elif data_type == "elf" or data_type == "Elf" or data_type == "ELF":
            write_VESTA_format_json(data["AtomInfo"], [data["ELF"]["TotalELF"]], out_filename)

        elif data_type == "pcharge" or data_type == "Pcharge" or data_type == "PCHARGE":
            write_VESTA_format_json(data["AtomInfo"], [data["Pcharge"][0]["TotalCharge"]], out_filename)

        elif data_type == "boundcharge" or data_type == "BoundCharge" or data_type == "BOUNDCHARGE":
            write_VESTA_format_json(data["AtomInfo"], [data["Rho"]], out_filename)

        else:
            print(" -rho/potential/elf/pcharge- ONLY")
            return

    else:
        print("file - " + in_filename + " :  Unsupported format!")
        return


def write_delta_rho_vesta(AB, A, B, output):
    '''Write delta rho vesta file
    
    DeviceStudio has not been able to visualize large file yet,
        call VESTA to visualize large data instead
    '''
    if AB.endswith('.h5'):
        dataAB = load_h5(AB)
        rhoAB = np.array(dataAB['/Rho/TotalCharge'])
        nGrids = dataAB['/AtomInfo/Grid']
        atom_symbol = dataAB['/AtomInfo/Elements']
        atom_pos = dataAB['/AtomInfo/Position']
        latticeConstantMatrix = dataAB['/AtomInfo/Lattice']
        atom_pos = np.array(atom_pos).reshape(-1,3)

    elif AB.endswith('.json'):
        atom_symbol = []
        atom_pos = []
        with open(AB,'r') as f1:
            dataAB = json.load(f1)
            rhoAB = np.array(dataAB['Rho']['TotalCharge'])
            nGrids = dataAB['AtomInfo']['Grid']

        for i in range(len(dataAB['AtomInfo']['Atoms'])):
            atom_symbol.append(dataAB['AtomInfo']['Atoms'][i]['Element'])
            atom_pos.append(dataAB['AtomInfo']['Atoms'][i]['Position'])
            atom_pos = np.array(atom_pos)

        latticeConstantMatrix = dataAB['AtomInfo']['Lattice']

    else:
        raise ValueError(f'file format must be either h5 or json: {AB}')
    
    if A.endswith('.h5'):
        dataA = load_h5(A)
        rhoA = np.array(dataA['/Rho/TotalCharge'])
    elif A.endswith('.json'):
        with open(A,'r') as f2:
            dataA = json.load(f2)
            rhoA = np.array(dataA['Rho']['TotalCharge'])
    else:
        raise ValueError(f'file format must be either h5 or json: {A}')
    
    if B.endswith('.h5'):
        dataB = load_h5(B)
        rhoB = np.array(dataB['/Rho/TotalCharge'])
    elif B.endswith('.json'):
        with open(B,'r') as f3:
            dataB = json.load(f3)
            rhoB = np.array(dataB['Rho']['TotalCharge'])
    else:
        raise ValueError(f'file format must be either h5 or json: {B}')

    rho = rhoAB - rhoA - rhoB
    rho = np.array(rho).reshape(nGrids[0], nGrids[1], nGrids[2])

    element = list(set(atom_symbol))
    element = sorted(set(atom_symbol),key=atom_symbol.index)
    element_num = np.zeros(len(element))
    for i in range(len(element)):
        element_num[i] = atom_symbol.count(element[i])

    latticeConstantMatrix = np.array(latticeConstantMatrix)
    latticeConstantMatrix = latticeConstantMatrix.reshape(3, 3)

    with open(output, 'w') as out:
        out.write('DS-PAW_rho\n')
        out.write('    1.000000\n')
        for i in range(3):
            for j in range(3):
                out.write('    '+str(latticeConstantMatrix[i, j])+'    ')
            out.write('\n')
        for i in range(len(element)):
            out.write('    '+element[i]+'    ')
        out.write('\n')

        for i in range(len(element_num)):
            out.write('    '+str(int(element_num[i]))+'    ')
        out.write('\n')
        out.write('Direct\n')
        for i in range(len(atom_pos)):
            for j in range(3):
                out.write('    '+str(atom_pos[i, j])+'    ')
            out.write('\n')
        out.write('\n')

        for i in range(3):
            out.write('  '+str(nGrids[i])+'  ')
        out.write('\n')

        ind = 0
        for i in range(nGrids[0]):
            for j in range(nGrids[1]):
                for k in range(nGrids[2]):
                    out.write('  '+str(rho[i, j, k])+'  ')
                    ind = ind +1
                    if ind % 5 == 0:
                        out.write('\n')

    print(f'Write {output} file successfully!')
