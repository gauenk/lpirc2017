#general 
import os,sys,zipfile,shutil
import numpy as np
from PIL import Image

#networking
import pycurl
from urllib.parse import urlencode as urlencode

#file io
from io import StringIO as StringIO
from io import BytesIO as BytesIO

#subprocessing
import subprocess
from utils import *

def parse_cmd_line():
    network_dict = {}
    import getopt,sys, time
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw:p:", ["help", "host_ipaddress=", "host_port=", "username=", "password=", "image_directory=","temp_directory=","token=","csv_filename="])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)
    for switch, val in opts:
        if switch in ("-h", "--help"):
            usage()
            sys.exit()
        elif switch in ("-w", "--host_ipaddress"):
            network_dict["host_ipaddress"] = val
        elif switch in ("-p", "--host_port"):
            network_dict["host_port"] = val
        elif switch == "--username":
            network_dict["username"] = val
        elif switch == "--password":
            network_dict["password"] = val
        elif switch in ("-csv","--csv_filename"):
            network_dict["csv_filename"] = val
        elif switch == "--image_directory":
            network_dict["image_directory"] = val
        elif switch == "--temp_directory":
            network_dict["temp_directory"] = val
        elif switch == "--token":
            network_dict["token"] = val
        else:
            assert False, "unhandled option"

    # print("\nhost = "+network_dict["host_ipaddress"]+":"+network_dict["host_port"]+"\nUsername = "+network_dict["username"]+"\nPassword = "+network_dict["password"]+"")
    return network_dict

def network_buffer(network,count):
    c = pycurl.Curl()
    c.setopt(c.URL, network["host_ipaddress"]+':'+network["host_port"]+'/zipimages')
    post_data = {'token':network["token"], 'image_name':str(count)}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS,postfields)

    my_buffer = BytesIO()    

    c.setopt(c.WRITEDATA,my_buffer)
    #c.setopt(c.WRITEDATA, f)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    c.close()

    if status == 401:
        #Server replied 401, Unauthorized Access, remove the temporary file
        print("Invalid")
    elif status == 406:
        #Server replied 406, Not Acceptable, remove the temporary file
        print("Invalid")

    return my_buffer

if __name__ == "__main__":

    network = parse_cmd_line()
    prev_count,count = 0,1

    
    ## FILE IO FOR DEBUFFING

    # my_buffer = BytesIO()    
    # with open('foo.zip', 'rb') as f:
    #     shutil.copyfileobj(f,my_buffer)

    # my_buffer.seek(0)
    # with open('foo.zip', 'wb') as f:
    #     shutil.copyfileobj(my_buffer,f)

    import subprocess
    args = ""
    while(True):
        # try:
        #     print("try")
        #     args = input()
        # except:
        #     print("except")
        #     args = ""
        # if len(args) > 0:
        #     #count = int(args)
        count = 1
        if prev_count != count:
            my_buffer = network_buffer(network,count)
            my_buffer.seek(0)
            my_z = zipfile.ZipFile(my_buffer)
            for n in my_z.namelist():
                    mbuffer = BytesIO(my_z.read(n))
                    img = np.asarray(Image.open(mbuffer), dtype=np.uint8)
                    #sys.stdout.write(str(img.shape)+'\n')
                    filename = numpy_to_memory(img)
                    print(filename)
                    sys.stdout.write(filename+'\n')
                    sys.stdout.flush()
            prev_count = count
    print("alive")
