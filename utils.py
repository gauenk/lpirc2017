import os,sys,tempfile
import numpy as np

def numpy_to_memory(obj):
    llp = tempfile.mkstemp(prefix='images',dir='/dev/shm',text=False)
    np.save(llp[1], obj)
    os.close(llp[0])
    return llp[1]

def numpy_from_memory(filename):
    arr =  np.load(filename+".npy")
    os.remove(filename)
    os.remove(filename+".npy")
    return arr
