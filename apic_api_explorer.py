from apicem_config import * # APIC-EM IP is assigned in apicem_config.pyy
# Get ticket - function is in apicem_config.py
ticket = get_X_auth_token()
headers = {"X-Auth-Token": ticket}

id = ""
start = ""
stop = ""
user_input = ""


"""
This script shouldn't be changed until you complete the Cisco Learning Lab tutorials, which formed the
basis of this script.

As APIs change or get added upon, you can change/add to the url_lists defined below.

Functions used that I created (all defined in apicem_config.py):
    build_url_table ()
        Takes the list of options and associates them with a number in a matrix.  This so you can easily just add
        to the url_lists defined below, and they will be given a dynamic number in the list

    print_url_table()
        takes the table created in 'build_url_table()' function and prints it out

    get_json()
        just a simplified method to get the response from the API and place it in a variable for use
        Includes some error handling if something goes wrong

    remove_duplicates()
        takes the result of a regex findall function and removes duplicates

    build_pretty_table()
        This is an automated way to use the tabulate function defined in tabulate.py.  It will
        take user input (Copy Paste) from the different JSON API variables, and then build a table
        with the columns that you select.

        It calls another function I created called tab_json_1_deep_new().  Which is just an easier way
        to build tables based upon the default tabulate() function defined in tabulte.py

    print_api_json()
        just prints raw JSON


Functions defined by someone else or standard librarys:
    json.dumps()
        just takes the raw JSON response and places it into a string.  Usseful for printing raw JSON
        as well as regex searches.  It is used in my print_api_json function

    re.findall()
        regex fuction that finds all instances of any regex search parameter you enter.  Must be a string value
        which is why I convert the JSON to string using the json.dumps() function
"""


while user_input != "0" :
    print ("\n\n\nThis program allows you to view the response for each API GET call.\n0 exits the program")
    user_input = input('\n  1  -  Main GET calls\n  2  -  COUNT\n  3  -  RANGE\n=> Make a selection: ')
    try :
        if user_input == "1":
            url_list = [
                "https://"+apicem_ip+"/api/"+version+"/network-device",
                "https://"+apicem_ip+"/api/"+version+"/host",
                "https://"+apicem_ip+"/api/"+version+"/device-credential",
                "https://"+apicem_ip+"/api/"+version+"/qos/traffic-class",
                "https://"+apicem_ip+"/api/"+version+"/qos/status"

                ]
            url_table = build_url_table(url_list)
            url_selected = url_table
            print_url_table(url_selected)
            user_input1 = input('=> Please enter the number of API URL you would like to see: ')
            for item in url_selected :
                if user_input1 in item :
                    url = item[1]
                    response_json = get_json(url,headers)
                    print ("URL selected = ", url)
            user_input2 = input('=> Want to see an organized table or raw json results?\n  1  -  Organized table\n  2  -  Raw JSON\n => ')
            if user_input2 == "1" :
                print_table_options(response_json)
                build_pretty_table(response_json)
            elif user_input2 == "2" :
                print_api_json(response_json)
            id = input('=> If you want to drill down by ID, Copy-Paste the ID below, or 0 to exit\n => ')
            if id != "0" :
                url_list_id = [
                    "https://"+apicem_ip+"/api/"+version+"/interface/network-device/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/network-device/"+id+"/config",
                    "https://"+apicem_ip+"/api/"+version+"/host/user-id/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/host/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/discovery/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/application/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/category/"+id,
                    "https://"+apicem_ip+"/api/"+version+"/policy/"+id
                    ]
                url_table_id = build_url_table(url_list_id)
                url_selected = url_table_id
                print_url_table(url_selected)
                user_input1 = input('=> Please enter the number of API URL you would like to see: ')
                for item in url_selected :
                    if user_input1 in item :
                        url = item[1]
                        response_json = get_json(url,headers)
                        print ("URL selected = ", url)
                user_input2 = input('=> Want to see an organized table or raw json results?\n  1  -  Organized table\n  2  -  Raw JSON\n => ')
                if user_input2 == "1" :
                    print_table_options(response_json)
                    build_pretty_table(response_json)
                elif user_input2 == "2" :
                    print_api_json(response_json)
        elif user_input == "2":
            url_list_count = [
                "https://"+apicem_ip+"/api/"+version+"/reachability-info/count",
                "https://"+apicem_ip+"/api/"+version+"/host/count",
                "https://"+apicem_ip+"/api/"+version+"/discovery/count",
                "https://"+apicem_ip+"/api/"+version+"/application/count",
                "https://"+apicem_ip+"/api/"+version+"/category/count",
                "https://"+apicem_ip+"/api/"+version+"/policy/count",
                "https://"+apicem_ip+"/api/"+version+"/qos/traffic-class/count"
                ]
            url_table_count = build_url_table(url_list_count)
            url_selected = url_table_count
            print_url_table(url_selected)
            user_input1 = input('=> Please enter the number of API URL you would like to see: ')
            for item in url_selected :
                if user_input1 in item :
                    url = item[1]
                    print ("URL selected = ", url)
                    response_json = get_json(url,headers)
                    print_api_json(response_json)
        elif user_input == "3":
            start = input('=> Start range: ')
            stop = input('=> Stop range: ')
            url_list_range = [
                "https://"+apicem_ip+"/api/"+version+"/reachability-info/"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/host"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/discovery/"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/application/"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/category/count/"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/policy/count/"+start+"/"+stop,
                "https://"+apicem_ip+"/api/"+version+"/qos/traffic-class/"+start+"/"+stop
                ]
            url_table_range = build_url_table(url_list_range)
            url_selected = url_table_range
            print_url_table(url_selected)
            user_input1 = input('=> Please enter the number of API URL you would like to see: ')
            for item in url_selected :
                if user_input1 in item :
                    url = item[1]
                    print ("URL selected = ", url)
                    response_json = get_json(url,headers)
                    print_api_json(response_json)
        elif user_input == "0" :
            exit
    except :
        print ("Something went wrong, try again")
