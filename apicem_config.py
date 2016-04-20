# Configure APIC-EM IP, username, password, also create a function to obtain a service ticket
import requests   # We use Python external "requests" module to do HTTP GET query
import json       # External JSON encoder and decode module
import sys        # For system-specific functions
import re	  # Regex funcitonality
import codecs	  # for testing to see what encoding the JSON results are in

# Please note that you may want install this external module in your working environment
# We just copy source code in here for the convenient
from tabulate import tabulate

# It's used to get rid of certificate warning messages when using Python 3.
# For more information please refer to: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings() # Disable warning message

# Step 1
# Change apic-em IP to the one you are using
apicem_ip = "sandboxapic.cisco.com:9443"

# Step 2
# Eneter user name and password to get a service ticket
# If you assign username, password and version here you don't need to pass parameter when calling
username = "admin"
password = "C!sc0123"
version = "v1"

def get_X_auth_token(ip=apicem_ip,uname = username,pword = password):
    """
    This function returns a new service ticket.
    Passing ip, username and password when use as standalone function
    or overwrite the configuration above.
    """
    global version

    # JSON input for the post ticket API request
    r_json = {
    "username": uname,
    "password": pword
    }
    # url for the post ticket API request
    post_url = "https://"+ip+"/api/"+version+"/ticket"
    # All APIC-EM REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, data = json.dumps(r_json), headers=headers,verify=False)
        # remove '#' if need to print out response
        # print (r.text)

        # return service ticket
        return r.json()["response"]["serviceTicket"]
    except:
        # Something wrong, cannot get service ticket
        print ("Status: %s"%r.status_code)
        print ("Response: %s"%r.text)
        sys.exit ()




def tab_json_1_deep_new(dump,parent,child):
    #this function prints out your specified json data in an easy to read table
    #parent is usually 'response', and child is a list in ['item1', 'item2', 'etc'] form.
    #Things I learned, the data matrix json created from the raw json dump is in a different format (strings)
    #than the response_json[parent], which is a matrix
    child_list = []
    child_list = child
    json_raw = []
    response_json = dump
    json_raw = response_json[parent]
    if json != [] :
        json_list = []
        for item in json_raw :
            i = 0
            temp_list = []
            while i < len(child_list) :
                temp_list.append(item[child_list[i]])
                i += 1
            json_list.append(temp_list)
        #This ensures there are no null characters (None), i.e., empty data
        #THis was done for python3 because the sort function can't deal with it
        #notice I didnt need to use the child_list variable here, because this is not dealing with json data
        #it is dealing with my new matrix list i created above.  You can think of the data you are trying
        #to change as json_list[x][y] = ""
        for item in json_list :
            i=0
            while i < len(item) :
                if item[i] is None :
                    item[i] = ""
                i += 1
        #print (json_list)

        #just sorts out the first child data alphabetically.  THis can be modified later to be more clever
        # e.g., selecting what variable you want to sort on, etc
        json_list.sort()
        #print (json.dumps(response_json,indent=4))  #This prints out the raw json for testing
        print (tabulate(json_list, headers=child,tablefmt="rst"))
        return json_list
        #print (json_list[12][0])
    else :
        print ("Couldn't find data to print")

#End def



def get_json(url,headers) :
    try:
        resp= requests.get(url,headers=headers,verify = False) # The response (result) from "GET /network-device" request
        status = resp.status_code
        print("Status: ",status)
        response_json = resp.json() # Get the json-encoded content from response
        return response_json
    except:
        print ("Something wrong, cannot get network device information")
        sys.exit()
    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()




def build_url_table(url_list):
    i = 1
    url_table = []
    for item in url_list :
        url_table.append([str(i), item])
        i += 1
        #print (item)
    return url_table




def print_url_table(url_table) :
    for item in url_table:
        print (item)

def print_api_json(response_json):
    print ("Raw JSON for testing:\n",json.dumps(response_json,indent = 4))


def build_pretty_table(response_json):
    user_input = ""
    child = []
    parent = "response"
    print ("\n\n\n=======================================================\nSelect your table columns - (Copy-Paste) - one variable at a time. \nWhen you are done, enter \'0\'\n=======================================================")
    while user_input != "0" :
        user_input = input('=> Select column: ')
        if user_input != "0" :
            child.append(user_input)
    tab_json_1_deep_new(response_json,parent,child)


def print_table_options(response_json):
    json_list = json.dumps(response_json) # Converts to string: regex can only be searched in string form
    json_list_regex_temp = re.findall('\"\w+\":',json_list) # "\w+":   - Finds alphanumeric word inside "": the \" is to escape the quote and search for it literally
    json_list_regex0 = json.dumps(json_list_regex_temp) # Converts to string: regex can only be searched in string form
    json_list_regex = re.findall('\w+',json_list_regex0) # \w+  - Finds words (gets rid of the quotes and colon:)
    json_list_pruned = remove_duplicates(json_list_regex)
    json_list_pruned.sort()
    print ("\n\n")
    for item in json_list_pruned :
        if "response" not in item :
            print (item)
    print ("\n Recommended to include hostname/portname as well as id\n\n ")

def get_variable_info(var) :
    #This is useful for figuring out what type of variable (List,tuple,Dict,string) that the json responses are in
    #For instance, tabulate only works with dicts, and regex searches only work with strings.
    print (len(var))
    #print (codecs.decode(var, 'utf-8'))
    print (type(var))

def remove_duplicates(seq):
    #Found on Stack Exchange - fastest way to remove duplicate results from a list
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
