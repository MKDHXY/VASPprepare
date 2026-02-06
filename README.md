这个项目主要是让VASP使用者可以更方便的从DFT转到ZPE，更方便的处理提交的POSCAR. 这是从DFT转换到ZPE计算的三件套，当你用scp从超算download下所有文件夹后，这个可以快速的将CONTCAR替换到你的POSCAR，并且快速分析要T T T的原子，并且F F F住你的slab。后期也会继续添加更多实用的Python脚本。

       一、 DFT-->ZPE kit 使用步骤 Step
        
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
        
        
        3.按顺序运行 1.py 2.py 3.py，等前一个运行完全再运行下一个。

        二、 一些快捷使用HPC超算的VASP的语句大全

                            grep "TOTE" Tem300K/Surface/OUTCAR
                            
                            grep "TOTE" Tem300K/Center/OUTCAR
                            
                            grep --text "TOTEN" OUTCAR
                            
                            for d in */; do
                              printf "%-45s " "$d"
                              grep "free  energy   TOTEN" "$d/OUTCAR" | tail -n 1
                            done
                            
                            
                            for d in */; do
                              printf "%-45s " "$d"
                              grep "Hz" "$d/OUTCAR" | tail -n 30
                            done
                            
                            for d in */; do
                              if [ -f "$d/submit.sh" ]; then
                                (cd "$d" && qsub submit.sh)
                                sleep 1
                              fi
                            done
                            
                            
                            
                            
                            
                            qstat | awk 'NR>2 {print $1}' | while read jid; do
                              name=$(qstat -f "$jid" | awk -F' = ' '/Job_Name/{print $2; exit}')
                              workdir=$(qstat -f "$jid" \
                                | awk 'BEGIN{ORS=""}{print}END{print "\n"}' \
                                | sed -n 's/.*PBS_O_WORKDIR=\([^,]*\).*/\1/p')
                              printf "%-22s %-20s %s\n" "$jid" "$name" "$workdir"
                            done
<img width="602" height="806" alt="image" src="https://github.com/user-attachments/assets/a68ab5a5-c72e-4e5c-ab2b-8d89b487090a" />
