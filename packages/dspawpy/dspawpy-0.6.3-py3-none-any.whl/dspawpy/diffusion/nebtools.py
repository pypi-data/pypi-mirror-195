import os
import h5py
import json
import numpy as np
np.set_printoptions(suppress=True)  # 不使用科学计数法
from dspawpy.io.utils import get_pos_ele_lat, get_ele_from_h5

def set_pbc(spo: np.ndarray or list):
    """根据周期性边界条件将分数坐标分量移入 [-0.5, 0.5) 区间

    Parameters
    ----------
    spo (np.ndarray or list): 分数坐标列表

    Returns
    -------
    np.ndarray:
        符合周期性边界条件的分数坐标列表
    """
    # 周期性边界条件
    pbc_spo = np.array(spo) - np.floor(spo + 0.5)
    
    return pbc_spo


def get_distance(spo1: np.ndarray, spo2: np.ndarray, lat1: np.ndarray, lat2: np.ndarray):
    """根据两个结构的分数坐标和晶胞计算距离

    Parameters
    ----------
    spo1 : np.ndarray
        分数坐标1
    spo2 : np.ndarray
        分数坐标2
    lat1 : np.ndarray
        晶胞1
    lat2 : np.ndarray
        晶胞2

    Returns
    -------
    float
        距离
    """
    diff_spo = spo1 - spo2  # 分数坐标差
    avglatv = 0.5*(lat1 + lat2)  # 平均晶格矢量
    pbc_diff_spo = set_pbc(diff_spo)  # 笛卡尔坐标差
    # 分数坐标点乘平均晶胞，转回笛卡尔坐标
    pbc_diff_pos = np.dot(pbc_diff_spo, avglatv)  # 笛卡尔坐标差
    distance = np.sqrt(np.sum(pbc_diff_pos**2))

    return distance


def get_neb_subfolders(directory: str = "."):
    """获取NEB子文件夹名称列表
    将directory路径下的子文件夹名称列表按照数字大小排序
    仅保留形如00，01数字类型的NEB子文件夹路径

    Parameters
    ----------
    subfolders : list
        子文件夹名称列表

    Returns
    -------
    list
        排序后的子文件夹名称列表
    """
    raw_subfolders = next(os.walk(directory))[1]
    subfolders = []
    for subfolder in raw_subfolders:
        try:
            assert 0 <= int(subfolder) < 100
            subfolders.append(subfolder)
        except:
            pass
    subfolders.sort()  # 从小到大排序
    return subfolders

def plot_neb_converge(neb_dir:str, image_key:str="01", show:bool=True, image_name:str=None):
    """Read neb.h5 or neb.json and plot the convergence of NEB

    Args:
        neb_dir: directory of the NEB calculation
        image_key: image key 01, 02, 03, ...
        show: show the plot or not
        image_name: image name, e.g. "neb_conv.png"

    Returns:
        subplot left ax,right ax
    """
    if os.path.exists(f"{neb_dir}/neb.h5"):
        import h5py
        neb_total = h5py.File(f"{neb_dir}/neb.h5")
        try: # new output (>=2022B)
            maxforce = np.array(neb_total.get(
                "/LoopInfo/" + image_key + "/MaxForce"))
        except: # old output
            maxforce = np.array(neb_total.get(
                "/Iteration/" + image_key + "/MaxForce"))
        
        try: # new output (>=2022B)
            total_energy = np.array(
                neb_total.get("/LoopInfo/" + image_key + "/TotalEnergy"))
        except: # old output
            total_energy = np.array(
                neb_total.get("/Iteration/" + image_key + "/TotalEnergy"))

    elif os.path.exists(f"{neb_dir}/neb.json"):
        import json
        with open(f"{neb_dir}/neb.json", 'r') as fin:
            neb_total = json.load(fin)
        try:
            neb = neb_total["LoopInfo"][image_key]
        except:
            neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

        maxforce = np.array(maxforce)
        total_energy = np.array(total_energy)

    else:
        print(f"请检查{neb_dir}/neb.h5或{neb_dir}/neb.json是否都存在！")

    x = np.arange(len(maxforce))

    force = maxforce
    energy = total_energy

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, force, label="Max Force", c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force (eV/Å)")

    ax2 = ax1.twinx()
    ax2.plot(x, energy, label="Energy", c="r")
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy (eV)")
    ax2.ticklabel_format(useOffset=False)  # y轴坐标显示绝对值而不是相对值

    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    if image_name:
        plt.tight_layout()
        plt.savefig(image_name)
    if show:
        plt.show()

    return ax1, ax2


def from_structures(directory:str):
    """从structure00.as，structure01.as，...，中读取结构信息，
    写入neb_movie_init，以便用DeviceStudio打开观察

    Parameters
    ----------
    directory : str
        NEB计算路径，默认当前路径

    Returns
    -------
    用于json文件的各个数组
    """
    output = 'neb_movie_init.json'
    step = 0

    subfolders = get_neb_subfolders(directory)
    # print(subfolders)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional
    maxForces = np.zeros(shape=nimage-2)  # optional
    tangents = np.zeros(shape=nimage-2)  # optional
    MaxForces = np.zeros(shape=(nimage-2, step+1))  # optional
    TotalEnergies = np.zeros(shape=(nimage-2, step+1))  # optional

    Poses = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    

    for i, folder in enumerate(subfolders):
        structure_path = os.path.join(
            directory, folder, f'structure{folder}.as')
        pos, ele, lat = get_pos_ele_lat(structure_path)
        Poses.append(pos)
        Elems.append(ele)
        Latvs.append(lat)
    
    Natom = len(Elems[0])
    
    # reshape data
    Poses = np.array(Poses).reshape((nimage,Natom,3))
    Elems = np.array(Elems).reshape((nimage,Natom))
    Latvs = np.array(Latvs).reshape((nimage,9))
    Fixs = np.zeros(shape=(Natom, 3))  # optional

    return output, subfolders, step, MaxForces, TotalEnergies, Poses, Latvs, Elems, Fixs, reactionCoordinates, totalEnergies, maxForces, tangents

def from_h5(directory:str, step:int):
    """从NEB路径下的h5文件读取指定step数的结构和能量信息，
    写入json文件，以便用DeviceStudio打开观察

    Parameters
    ----------
    directory : str
        NEB路径，默认当前路径
    step : int
        step数，默认-1，读取最后一个构型

    Returns
    -------
    用于json文件的各个数组
    """
    # ^ 前期设置
    neb_h5 = os.path.join(directory,'01/neb01.h5')
    data = h5py.File(neb_h5)
    total_steps = np.array(data.get('/NebSize'))[0]
    print(f'从{os.path.abspath(neb_h5)}中读取到的总离子步数为：{total_steps}')

    if step == -1 or step > total_steps-1:
        output = 'neb_movie_last.json'
        step = total_steps-1
        print('正在尝试根据最后一个离子步信息生成neb_movie_last.json...\n')
    else:
        output = 'neb_movie_{}.json'.format(step)
        print(f'正在尝试根据第{step}个离子步信息生成{output}...\n')

    # ^ 读取前，准备好json文件所需数组框架
    subfolders = get_neb_subfolders(directory)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional
    maxForces = np.zeros(shape=nimage-2)  # optional
    tangents = np.zeros(shape=nimage-2)  # optional
    MaxForces = np.zeros(shape=(nimage-2, step+1))  # optional
    TotalEnergies = np.zeros(shape=(nimage-2, step+1))  # optional
    Poses = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    Fixs = []  # Natom x 3, set

    for folder in subfolders:
        '''如果是首尾两个构型，最多只有scf.h5文件，没有neb.h5文件
        用户如果算NEB的时候，不计算首尾构型的自洽，
         或者在别处算完了但是没有复制到首尾文件夹中并命名为scf.h5，
          便不能使用第一个功能
        '''
        if folder == subfolders[0] or folder == subfolders[-1]:
            h5_path = os.path.join(directory, folder, 'scf.h5')
        else:
            h5_path = os.path.join(directory, folder, f'neb{folder}.h5')
        assert os.path.exists(h5_path), f'请确认{h5_path}是否存在！'

    # ^ 开始分功能读取数据
    for i, folder in enumerate(subfolders):
        if folder == subfolders[0] or folder == subfolders[-1]:
            h5_path = os.path.join(directory, folder, 'scf.h5')
            data = h5py.File(h5_path)
            # 不影响可视化，直接定为0
            if folder == subfolders[0]:
                reactionCoordinates[i] = 0

        else:
            h5_path = os.path.join(directory, folder, f'neb{folder}.h5')
            data = h5py.File(h5_path)
            # reading...
            reactionCoordinates[i-1] = np.array(
                data.get('/Distance/Previous'))[-1]
            maxForces[i-1] = np.array(data.get('/MaxForce'))[-1]
            tangents[i-1] = np.array(data.get('/Tangent'))[-1]
            if folder == subfolders[-2]:
                reactionCoordinates[i +
                                    1] = np.array(data.get('/Distance/Next'))[-1]
            # read MaxForces and TotalEnergies
            nionStep = np.array(data.get('/MaxForce')).shape[0]
            assert step <= nionStep, f'总共只完成了{nionStep}个离子步!'
            for j in range(step):
                MaxForces[i-1, j+1] = np.array(data.get('/MaxForce'))[j]
                TotalEnergies[i-1, j +
                                1] = np.array(data.get('/TotalEnergy'))[j]

        totalEnergies[i] = np.array(data.get('/Energy/TotalEnergy0'))
        pos = np.array(data.get('/AtomInfo/Position'))
        Poses.append(pos)

        elems = get_ele_from_h5(hpath=h5_path)
        Elems.append(elems)

        lat = np.array(data.get('/AtomInfo/Lattice'))
        Latvs.append(lat)

    tdata = h5py.File(os.path.join(directory, 'neb.h5'))
    fix_array = np.array(tdata.get('/UnrelaxStructure/Image00/Fix'))
    for fix in fix_array:
        if fix == 0.0:
            F = False
        elif fix == 1.0:
            F = True
        else:
            raise ValueError('Fix值只能为0或1')
        Fixs.append(F)

    Natom = len(Elems[0])

    # 累加reactionCoordinates中的元素
    for i in range(1, len(reactionCoordinates)):
        reactionCoordinates[i] += reactionCoordinates[i-1]

    # reshape data
    Poses = np.array(Poses).reshape((nimage,Natom,3))
    Elems = np.array(Elems).reshape((nimage,Natom))
    Latvs = np.array(Latvs).reshape((nimage,9))
    Fixs = np.array(Fixs).reshape((Natom,3))

    return output, subfolders, step, MaxForces, TotalEnergies, Poses, Latvs, Elems, Fixs, reactionCoordinates, totalEnergies, maxForces, tangents


def from_json(directory:str, step:int):
    """从NEB路径下的json文件读取指定step数的结构和能量信息，
    写入json文件，以便用DeviceStudio打开观察

    Parameters
    ----------
    directory : str
        NEB路径，默认当前路径
    step : int
        step数，默认-1，读取最后一个构型

    Returns
    -------
    用于json文件的各个数组
    """
    
    # ^ 前期设置
    neb_js = os.path.join(directory, '01/neb01.json')
    with open(neb_js, 'r') as f:
        data = json.load(f)
    total_steps = len(data)
    print(f'从{os.path.abspath(neb_js)}中读取到的总离子步数为：{total_steps}')
    
    if step == -1 or step > total_steps-1:
        print('正在尝试根据最后一个离子步信息生成neb_movie_last.json...\n')
        step = total_steps-1
        output = 'neb_movie_last.json'
    else:
        output = f'neb_movie_{step}.json'
        print(f'正在尝试根据第{step}个离子步信息生成{output}...\n')

    # ^ 读取前，准备好json文件所需数组框架
    subfolders = get_neb_subfolders(directory)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional
    maxForces = np.zeros(shape=nimage-2)  # optional
    tangents = np.zeros(shape=nimage-2)  # optional
    MaxForces = np.zeros(shape=(nimage-2, step+1))  # optional
    TotalEnergies = np.zeros(shape=(nimage-2, step+1))  # optional
    Poses = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    Fixs = []   # Natom x 3, set

    for folder in subfolders:
        '''如果是首尾两个构型，最多只有system.json文件，没有neb*.json文件
        用户如果算NEB的时候，不计算首尾构型的自洽，
         或者在别处算完了但是没有复制到首尾文件夹中并命名为system.json，
          便不能使用第一个功能
        '''
        if folder == subfolders[0] or folder == subfolders[-1]:
            js_path = os.path.join(directory, folder, 'system.json')
        else:
            js_path = os.path.join(directory, folder, f'neb{folder}.json')
        assert os.path.exists(js_path), f'请确认{js_path}是否存在！'

    # ^ 开始分功能读取数据
    for i, folder in enumerate(subfolders):
        if i != 0 and i != nimage-1:
            js_path = os.path.join(directory, folder, f'neb{folder}.json')
            with open(js_path, 'r') as f:
                ndata = json.load(f)
            # 读取与前一个构型相比的反应坐标
            reactionCoordinates[i-1] = ndata[step]['ReactionCoordinate'][-2]
            tangents[i-1] = ndata[step]['Tangent']
            if folder == subfolders[-2]: # 末态前一个构型的计算结果中读取反应坐标
                reactionCoordinates[i +
                                    1] = ndata[step]['ReactionCoordinate'][-1]
            for j in range(step):
                MaxForces[i-1, j+1] = ndata[j]['MaxForce']
                TotalEnergies[i-1, j +
                                1] = ndata[j]['TotalEnergy']
        elif i == 0:
            reactionCoordinates[i] = 0

        js_path = os.path.join(directory, folder, 'system.json')
        with open(js_path, 'r') as f:
            sdata = json.load(f)
            
        Natom = len(sdata['AtomInfo']['Atoms'])
        elems = []
        for i in range(Natom):
            ele = sdata['AtomInfo']['Atoms'][i]['Element']
            elems.append(ele)
            pos = sdata['AtomInfo']['Atoms'][i]['Position']
            Poses.append(pos)
        Elems.append(elems)

        lat = sdata['AtomInfo']['Lattice']
        Latvs.append(lat)

    Natom = len(Elems[0])

    tneb_js = os.path.join(directory, 'neb.json')
    with open(tneb_js, 'r') as f:
        tdata = json.load(f)
    for atom in range(Natom):
        fix_array = tdata['UnrelaxStructure'][1]['Atoms'][atom]['Fix'] # (1,3)
        for fix in fix_array:
            if fix == 0.0:
                F = False
            elif fix == 1.0:
                F = True
            else:
                raise ValueError('Fix值只能为0或1')
            Fixs.append(F)
                    
    # 累加reactionCoordinates中的元素
    for i in range(1, len(reactionCoordinates)):
        reactionCoordinates[i] += reactionCoordinates[i-1]

    # reshape data
    Poses = np.array(Poses).reshape((nimage,Natom,3))
    Elems = np.array(Elems).reshape((nimage,Natom))
    Latvs = np.array(Latvs).reshape((nimage,9))
    Fixs = np.array(Fixs).reshape((Natom,3))

    return output, subfolders, step, MaxForces, TotalEnergies, Poses, Latvs, Elems, Fixs, reactionCoordinates, totalEnergies, maxForces, tangents


def _dump_neb_movie_json(raw):
    """根据之前收集到的各数据列表，dump json文件到output"""
    output, subfolders, step, MaxForces, TotalEnergies, Poses, Latvs, Elems, Fixs, reactionCoordinates, totalEnergies, maxForces, tangents = raw

    IterDict = {}
    for s, sf in enumerate(subfolders):
        if sf == subfolders[0] or sf == subfolders[-1]:
            continue
        else:
            Eflist = []
            for l in range(step+1):
                ef = {'MaxForce': MaxForces[s-1, l].tolist(),
                      'TotalEnergy': TotalEnergies[s-1, l].tolist()}
                Eflist.append(ef)
                iterDict = {sf: Eflist}  # construct sub-dict
                IterDict.update(iterDict)  # append sub-dict

    RSList = []
    '''
    从外到内依次遍历 构型、原子（子字典）
    原子的键值对为：'Atoms': 原子信息列表
    原子信息列表是一个由字典组成的列表，每个字典对应一个原子的信息
    '''
    for s, sf in enumerate(subfolders):
        pos = Poses[s]
        lat = Latvs[s]
        elem = Elems[s]
        atoms = []
        for i in range(len(elem)):
            atom = {'Element': elem[i],
                    'Fix': Fixs[i].tolist(),
                    'Mag': [],  # empty
                    'Position': pos[i].tolist(),
                    'Pot': ""}  # empty
            atoms.append(atom)
        rs = {'Atoms': atoms,
              'CoordinateType': 'Cartesian',
              'Lattice': lat.tolist()}
        RSList.append(rs)

    URSList = []  # DS似乎并不读取这部分信息，空置即可

    data = {'Distance': {'ReactionCoordinate': reactionCoordinates.tolist()},
            'Energy': {'TotalEnergy': totalEnergies.tolist()},
            'Force': {'MaxForce': maxForces.tolist(),
                      'Tangent': tangents.tolist()},
            'Iteration': IterDict,
            'RelaxedStructure': RSList,
            'UnrelaxedStructure': URSList}

    # ^ 将字典写入json文件
    with open(output, 'w') as f:
        json.dump(data, f, indent=4)

def write_movie_json(preview:bool, directory:str='./', step:int=0):
    """预览或者根据计算结果写入neb_movie*.json文件
    
    ----------
    输入
        preview (bool): 是否预览模式
        directory (str, optional): 计算结果所在目录. Defaults to './'.
        step (int, optional): 计算步数. Defaults to 0.
    
    ----------
    运行结果
        保存为neb_movie*.json文件
    """
    
    if preview: # preview mode, write neb_movie_init.json from structure.as
        print('--> 预览模式\n正在尝试根据初插结构保存neb_movie_init.json...')
        try:
            raw = from_structures(directory)
        except FileNotFoundError:
            print('未找到初始插值结构！')
        except:
            print('初始插值结构读取失败！')
    else:
        print('--> 非预览模式')
        if step == 0: # try preview mode to save time
            try:
                raw = from_structures(directory)
            except:
                print('未找到初始插值结构，将从计算结果中读取！')

        try: # read from h5 file
            print('优先尝试从h5文件读取结果...')
            raw = from_h5(directory, step)
        except FileNotFoundError: 
            try: # read from json file
                print('h5文件不存在，尝试从json文件读取结果...')
                raw = from_json(directory, step)
            except FileNotFoundError:
                print('h5和json文件都不存在！')
            except json.decoder.JSONDecodeError:
                print('json文件格式错误！')
        except:
            print('h5文件内容读取失败！')

    _dump_neb_movie_json(raw)


def restart(direrctory: str, inputin: str, output: str):
    """将旧NEB任务归档压缩，并在原路径下准备续算

    Parameters
    ----------
    direrctory : str
        旧NEB任务所在路径，默认当前路径
    inputin : str
        输入参数文件名，默认input.in
    output : str
        备份文件夹路径

    Raises
    ------
    FileNotFoundError
        如果原NEB路径下没有结构文件，抛出异常
    """
    if output == '':
        raise ValueError('备份文件夹路径不能为空！')
    elif os.path.isdir(output):
        raise ValueError('备份文件夹已存在！')

    if direrctory == '':
        directory = os.getcwd()
    if inputin == '':
        inputin = 'input.in'

    # 读取子文件夹名称列表，仅保留形如00，01数字文件夹路径
    subfolders = get_neb_subfolders(directory)
    # 创建备份文件夹并进入
    os.makedirs(f'{directory}/{output}')
    os.chdir(f'{directory}/{output}')
    # 将-0改成-9可提供极限压缩比
    os.environ["XZ_OPT"] = '-T0 -0'
    for subfolder in subfolders:
        # 备份
        os.system(f'mv {directory}/{subfolder} ./')
        # 准备续算用的结构文件
        os.mkdir(f'{directory}/{subfolder}')
        latestStructureFile = os.path.join(
            directory, output, subfolder, 'latestStructure%s.as' % subfolder)
        structureFile = os.path.join(
            directory, output, subfolder, 'structure%s.as' % subfolder)
        bk_latestStructure = f'{directory}/latestStructure{subfolder}.as'
        bk_structure = f'{directory}/structure{subfolder}.as'

        if os.path.exists(latestStructureFile):
            os.system(  # 复制到子文件夹
                f'cp {latestStructureFile} {directory}/{subfolder}/structure{subfolder}.as')
            # 备份latestStructureFile到主目录
            os.system(f'cp {latestStructureFile} {bk_latestStructure}')
        elif os.path.exists(structureFile):
            print(f'未找到{latestStructureFile}，复用{structureFile}续算')
            os.system(  # 复制到子文件夹
                f'cp {structureFile} {directory}/{subfolder}/structure{subfolder}.as')
        else:
            raise FileNotFoundError(
                f'{latestStructureFile}和{structureFile}都不存在！')
        # 备份structureFile到主目录
        if os.path.exists(structureFile):
            os.system(f'cp {structureFile} {bk_structure}')

        # 压缩和移动文件
        # 若存在latestStructure00.as和structure00.as，则压缩00文件夹并把主结构移入00文件夹
        if os.path.exists(bk_latestStructure) and os.path.exists(bk_structure):
            os.system(
                f"tar -Jcf {subfolder}.tar.xz -C {subfolder} . --remove-files && mkdir {subfolder} && mv {subfolder}.tar.xz {directory}/latestStructure{subfolder}.as {directory}/structure{subfolder}.as {subfolder}/ &")
        # 若仅存在latestStructure00.as，则压缩00文件夹并把主结构移入00文件夹
        elif os.path.exists(bk_latestStructure):
            os.system(
                f"tar -Jcf {subfolder}.tar.xz {subfolder} . --remove-files && mkdir {subfolder} && mv {subfolder}.tar.xz {directory}/latestStructure{subfolder}.as {subfolder}/ &")
        # 若仅存在structure00.as，则压缩00文件夹并把主结构移入00文件夹
        elif os.path.exists(bk_structure):
            os.system(
                f"tar -Jcf {subfolder}.tar.xz -C {subfolder} . --remove-files && mkdir {subfolder} && mv {subfolder}.tar.xz {directory}/structure{subfolder}.as {subfolder}/ &")
        else:  # 如果都不存在，说明备份失败
            raise FileNotFoundError(
                f'{bk_latestStructure}和{bk_structure}都不存在！')

    # 备份neb.h5,neb.json和DS-PAW.log
    if os.path.exists(f'{directory}/neb.json'):
        os.system(
            f'mv {directory}/neb.h5 {directory}/neb.json {directory}/DS-PAW.log ./')
        os.system(f'tar -Jcf neb.tar.xz neb.h5 neb.json --remove-files &')
    else:
        os.system(
            f'mv {directory}/neb.h5 {directory}/DS-PAW.log ./')
        os.system(f'tar -Jcf neb.tar.xz neb.h5 --remove-files &')


def getef(directory: str = '.'):
    """从dire路径读取NEB计算时各构型的能量和受力

    input:
        - directory: NEB计算的路径，默认当前路径
    output:
        - subfolders: 构型文件夹名
        - resort_mfs: 构型受力的最大分量 
        - rcs: 反应坐标
        - ens: 电子总能
        - dE: 与初始构型的能量差
    """

    subfolders = get_neb_subfolders(directory)
    Nimage = len(subfolders)

    ens = []
    dEs = np.zeros(Nimage)
    rcs = [0]
    mfs = []

    # read energies
    count = 1
    for i, subfolder in enumerate(subfolders):
        if i == 0 or i == Nimage-1:
            jsf = os.path.join(directory, subfolder, f'system{subfolder}.json')
            hf = os.path.join(directory, subfolder, 'scf.h5')
            if os.path.exists(jsf):
                with open(jsf, 'r') as f:
                    data = json.load(f)
                en = data['Energy']['TotalEnergy0']
                if i == 0 or i == Nimage-1:
                    mf = np.max(np.abs(data['Force']['ForceOnAtoms']))
                    mfs.append(mf)
            elif os.path.exists(hf):
                data = h5py.File(hf)
                en = np.array(data.get('/Energy/TotalEnergy0'))
                if i == 0 or i == Nimage-1:
                    mf = np.max(
                        np.abs(np.array(data.get('/Force/ForceOnAtoms'))))
                    mfs.append(mf)
            else:
                raise FileNotFoundError(
                    '无法找到记录构型%s的能量和受力的system.json或scf.h5文件' % subfolder)
            ens.append(en)

        else:
            jsf = os.path.join(directory, subfolder, f'neb{subfolder}.json')
            hf = os.path.join(directory, subfolder, f'neb{subfolder}.h5')

            if os.path.exists(jsf):
                with open(jsf, 'r') as f:
                    data = json.load(f)
                Nion_step = len(data)
                en = data[Nion_step-1]['TotalEnergy']
                mf = data[Nion_step-1]['MaxForce']  # 最后一步的最大受力
                rc = data[Nion_step-1]['ReactionCoordinate'][0]  # 最后一步的反应坐标
                rcs.append(rc)
                if count == Nimage-2:  # before final image
                    rc = data[Nion_step-1]['ReactionCoordinate'][1]  # 最后一步的反应坐标
                    rcs.append(rc)
            elif os.path.exists(hf):
                data = h5py.File(hf)
                en = np.array(data.get('/Energy/TotalEnergy0'))
                mf = np.array(data.get('/MaxForce'))[-1]
                rc = np.array(data.get('/ReactionCoordinate'))[-2]
                rcs.append(rc)
                if count == Nimage-2:  # before final image
                    rc = np.array(data.get('/ReactionCoordinate'))[-1]
                    rcs.append(rc)
            else:
                raise FileNotFoundError('无法找到neb%s.json或hdf5文件' % subfolder)

            ens.append(en)
            mfs.append(mf)

            # get dE
            dE = ens[count] - ens[0]
            dEs[i] = dE
            count += 1
    dEs[-1] = ens[Nimage-1] - ens[0]

    # rcs 改成累加值
    for i in range(1, len(rcs)):
        rcs[i] += rcs[i-1]

    rcs = np.array(rcs)

    resort_mfs = [mfs[0]]
    final_mf = mfs[1]
    for j in range(2, len(mfs)):
        resort_mfs.append(mfs[j])
    resort_mfs.append(final_mf)

    return subfolders, resort_mfs, rcs, ens, dEs


def printef(directory):
    """打印NEB计算时各构型的能量和受力
    """
    subfolders, resort_mfs, rcs, ens, dEs = getef(directory)
    # printout summary
    print('构型\t受力(eV/Å)\t反应坐标(Å)\t此构型的能量(eV)\t与初始构型的能量差(eV)')
    for i in range(len(subfolders)):  # 注意格式化输出，对齐
        print('%s\t%8.4f\t%8.4f\t%12.4f\t%20.4f' %
              (subfolders[i], resort_mfs[i], rcs[i], ens[i], dEs[i]))

def summary(directory: str = '.'):
    """NEB任务完成总结
    依次执行以下步骤：
    1. 绘制能垒图
    2. 打印各构型受力、反应坐标、能量、与初始构型的能量差
    3. 绘制并保存结构优化过程的能量和受力收敛过程图

    Parameters
    ----------
    directory : str, 可选
        NEB路径, 默认当前路径
    ! 若inifin=false，用户必须将自洽的scf.h5或system.json放到初末态子文件夹中
    """
    # 1. 绘制能垒图
    print('--> 1. 绘制能垒图...')
    subfolders, resort_mfs, rcs, ens, dEs = getef(directory)
    from scipy.interpolate import interp1d
    import matplotlib.pyplot as plt

    inter_f = interp1d(rcs, dEs, kind="cubic")
    xnew = np.linspace(rcs[0], rcs[-1], 100)
    ynew = inter_f(xnew)
    plt.plot(xnew, ynew, c="b")
    plt.scatter(rcs, dEs, c="r")
    plt.xlabel("Reaction Coordinate")
    plt.ylabel("Energy")
    plt.savefig(f"{directory}/neb_reaction_coordinate.png")

    # 2. 打印各构型受力、反应坐标、能量、与初始构型的能量差
    print('\n--> 2. 打印NEB计算时各构型的能量和受力...')
    printef(directory)

    # 3. 绘制并保存结构优化过程的能量和受力收敛过程图到各构型文件夹中
    print('\n--> 3. 绘制收敛过程图到各构型文件夹中...')
    subfolders = get_neb_subfolders(directory)
    for subfolder in subfolders[1:len(subfolders)-1]:
        print(f"----> {subfolder}/converge.png...")
        plot_neb_converge(neb_dir=directory, image_key=subfolder, 
                          image_name=f"{directory}/{subfolder}/converge.png")
    print('\n完成!')
