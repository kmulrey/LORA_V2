L#! /bin/bash
#SBATCH --time=3:00:00


use root



export RUNNR=`printf "%06d" $SLURM_ARRAY_TASK_ID`


python main.py -i $RUNNR
python runEvents.py -i $RUNNR
