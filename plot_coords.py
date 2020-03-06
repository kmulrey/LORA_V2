import numpy as np
import matplotlib.pyplot as plt

coord_file=open('coords.txt','r')

info=np.genfromtxt(coord_file,usecols=(0,1,2,3))
print(info)










