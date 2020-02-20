#! /bin/bash
#SBATCH --time=3:00:00


use root

python process_V2.py -f 20200109_2217
python process_V2.py -f 20200110_0017
python process_V2.py -f 20200111_0017
python process_V2.py -f 20200112_0017
python process_V2.py -f 20200113_0017
python process_V2.py -f 20200113_2228
python process_V2.py -f 20200114_0028
python process_V2.py -f 20200115_0028
python process_V2.py -f 20200115_0922
python process_V2.py -f 20200115_1436
python process_V2.py -f 20200116_0036
python process_V2.py -f 20200119_2211
python process_V2.py -f 20200120_0011
