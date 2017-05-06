#!/usr/bin/env python3

#generic
import csv,shutil,os,sys,time,tempfile,re,glob
import numpy as np
from utils import *

# caffe model
#import caffe
#import cPickle

# processing
import subprocess
import ctypes
import logging 

#networking
from client_functions import *

#+++++++++++++++++++++++++++ Network Variables +++++++++++++++++++++++++++++++++++++++++++++++++
network = {}
network["host_ipaddress"] = "192.168.1.2"
network["host_port"] = "8000"
network["username"] = "lpirc"
network["password"] = "pass"
network["csv_filename"] = "this.csv"
network["image_directory"] = "imgs"
network["temp_directory"] = "tmp"

##SET UP CLIENT


if __name__ == "__main__":

    #++++++++++ clean up old files ++++++++++++++
    for mfile in glob.glob("/dev/shm/images*"): ## dependent on filename prefix in utils.py
        os.remove(mfile)

    #++++++++++ Start of the script +++++++++++++


    # arr = np.array([1,2,3,4])
    # print(arr)
    # filename = numpy_to_memory(arr)
    # del arr
    # try:
    #     print(arr)
    # except:
    #     print("arr doesn't exist")
    # arr = numpy_from_memory(filename)
    # print(arr)

    ##CAFFE MODEL
    # cfg.GPU_ID = 0
    # t_prototxt = "/home/ubuntu/Documents/py-faster-rcnn/models/pascal_voc/ZF/faster_rcnn_end2end/test.prototxt"
    # caffemodel = "/home/ubuntu/Documents/py-faster-rcnn/weights/pascal_voc/ZF_faster_rcnn_final.caffemodel"
    # net = caffe.Net(t_prototxt, caffemodel, caffe.TEST)
    # net.name = os.path.splitext(os.path.basename(caffemodel))[0]

    ## LOGIN AND GET TOKEN
    network = parse_cmd_line(network)

    [token, status] = get_token(network)   # Login to server and obtain token
    if status==0:
        print("Incorrect Username and Password. Bye!")
        sys.exit()
    print("LOGGED IN")

    ## START SUBPROCESS
    arg_string = "--token {0:s} ".format(token.decode("utf-8"))
    for name,value in network.items():
        arg_string += '--{0:s} {1:s} '.format(name,str(value))
        #print(arg_string)
    p = subprocess.Popen(['python3 get_zip.py ' + arg_string], shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE)
    count = 0
    while p.poll() is None:
        count = count*100 + 1
        if count > 300:
            sys.exit(0)
        print(bytes(str(count),"utf-8"))
        #filenames,_ = p.communicate(bytes(str(count),"utf-8"))
        filenames = p.stdout.readline()
        print(filenames)
        filenames = filenames.decode("utf-8")
        #print(filenames.split("\n")[0])
        if len(filenames) > 0 and "images" in filenames: ## dependent on filename prefix in utils.py
            for filename in filenames.split("\n")[1:]:
                filename = filename
                match = re.search(r"images",filename)
                if len(filename) > 0 and match is not None:
                    img = numpy_from_memory(filename)

                    #print(img.shape,"IN")
                else:
                    print(filename)
