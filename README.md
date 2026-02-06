这个项目主要是让VASP使用者可以更方便的从DFT转到ZPE，更方便的处理提交的POSCAR. 这是从DFT转换到ZPE计算的三件套，当你用scp从超算download下所有文件夹后，这个可以快速的将CONTCAR替换到你的POSCAR，并且快速分析要T T T的原子，并且F F F住你的slab。后期也会继续添加更多实用的Python脚本。

使用步骤 Step

1.修改INCAR到你需要的参数，注意IDPOL是方向一定要修改到你真空层的方向！

2.然后将你这四个文件放到同一个目录，你的POSCAR INCAR这些处于这个目录下的子文件夹中，
----------
    |----- 1.py 2.py 3.py INCAR
    |
    |—————— slab_CO2
    |    |
    |    | —————— POSCAR INCAR POTCAR CONTCAR POTCAR submit.sh
    |—————— slab_CO
         |
         | —————— POSCAR INCAR POTCAR CONTCAR POTCAR submit.sh
