usage_text = """
Usage:
------
main.py [OPTION]...

Options:
         -w, --ip
                IP address of the server in format <xxx.xxx.xxx.xxx>
                Default: 128.46.75.108

         -p, --port
                Port number of the server.
                Default: 80

         --user
                Username
                The user must send a mail to lpirc@ecn.purdue.edu to request 
        for a username and password.

         --pass
                Password for the username
                The user must send a mail to lpirc@ecn.purdue.edu to request 
        for a username and password.
        
         --im_dir
        Directory with respect to the client.py 
                where received images are stored
        Default: ../images

     --temp_dir
        Directory with respect to the client.py
        where temporary data is stored
        Default: ../temp

         --in
        Name of the csv file to take the input with respect to source directory
        Default: golden_output.csv
        (This is for testing purpose only. It should not be in the real client.)

         -h, --help
                Displays all the available option

"""
