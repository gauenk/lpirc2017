def usage():
    import usage_text
    print(usage_text.usage_text)

    
def parse_cmd_line(network_dict):
    import getopt,sys, time

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hw:p:", ["help", "ip=", "port=", "user=", "pass=", "in=", "im_dir=","temp_dir="])
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)
    for switch, val in opts:

        if switch in ("-h", "--help"):
            usage()
            sys.exit()
        elif switch in ("-w", "--ip"):
            network_dict["host_ipaddress"] = val
        elif switch in ("-p", "--port"):
            network_dict["host_port"] = val
        elif switch == "--user":
            network_dict["username"] = val
        elif switch == "--pass":
            network_dict["password"] = val
        elif switch in ("-i","--in"):
            network_dict["csv_filename"] = val
        elif switch == "--im_dir":
            network_dict["image_directory"] = val
        elif switch == "--temp_dir":
            network_dict["temp_directory"] = val
        else:
            assert False, "unhandled option"

    print("\nhost = "+network_dict["host_ipaddress"]+":"+network_dict["host_port"]+"\nUsername = "+network_dict["username"]+"\nPassword = "+network_dict["password"]+"")
    return network_dict


#++++++++++++++++++++++++++++ get_token: Can be used by the participant directly ++++++++++++++++++++
# 
# Functionality : 
# Sends request to the server to log in with username and password and returns the token and status. 
# Token needs to be used in all the communication with the server in the session.
# If the username and password are invalid or the session has expired, status returned is 0.
# If the token is is valid, status returned is 1.
# 
# This must be the first message to the server.
#
# Usage: [token, status] = get_token(username, password)
# 
# Inputs: 
#         1. username
#         2. password
#
# Outputs:
#         1. token
#     2. status
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_token (network_dict):

    from io import StringIO as StringIO
    from io import BytesIO as BytesIO
    import pycurl
    import urllib
    from urllib.parse import urlencode as urlencode

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, network_dict["host_ipaddress"]+':'+network_dict["host_port"]+'/login')
    post_data = {'username':network_dict["username"],'password':network_dict["password"]}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS,postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    if status == 200:
        return [buffer.getvalue(),1]
    else:
        print("Unauthorised Access\n")
        return [buffer.getvalue(),0]
