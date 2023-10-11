import re
import json

#Squeeze the server parameters out of the GET request
def parameterSort(request):
    try:
        # Get the query string part of the URL
        query_string = request.split('?')[1]

        # Split the query string into individual parameters
        parameters = query_string.split('&')

        # Create a dictionary to store the parsed query parameters
        query_params = {}

        # Iterate through each parameter and extract the key-value pair
        for param in parameters:
            key, value = param.split('=')
            # Replace '+' with space and '%2F' with slash
            value = value.replace('+', ' ').replace('%2F', '/')
            query_params[key] = value
            
            
            # Print the parsed query parameters
        for key, value in query_params.items():
            print(key, value)   
    except (IndexError, NameError, ValueError) as e:
        query_params = {}
        pass 
    
    return query_params

def extractReferer(url):
    # Find the start index of the Referer header
    referer_start_index = url.find('Referer: ')
    
    if referer_start_index != -1:
        # Extract the substring after 'Referer: ' as the Referer
        referer = url[referer_start_index + len('Referer: '):].strip()
        return referer
    else:
        return None
    
def extractRefererParams(referer):
    # Find the start index of the question mark character
    question_mark_index = referer.find('?')
    
    if question_mark_index != -1:
        # Extract the substring after the question mark
        query_string = referer[question_mark_index + 1:]
        
        # Split the query string into key-value pairs
        key_value_pairs = query_string.split('&')
        
        params_dict = {}
        for pair in key_value_pairs:
            # Split each key-value pair into key and value
            key, value = pair.split('=')
            
            # URL-decode the value
            value = value.replace('+', ' ')
            value = value.replace('%2F', '/')
            
            # Store the parameter in the dictionary
            if key in params_dict:
                # If the key already exists, convert the value to a list
                if isinstance(params_dict[key], list):
                    params_dict[key].append(value)
                else:
                    params_dict[key] = [params_dict[key], value]
            else:
                params_dict[key] = value
        
        return params_dict
    else:
        return {}

#Call saved dictionary from parameterSort function and convert to a json object and save to parameters.json
def saveVariables(new_parameters):
    if len(new_parameters) <=1:
        return
    parameters_json_object = json.dumps(new_parameters)
    print("Parameters in json object: ", parameters_json_object)
    with open("parameters.json","w") as parameters_json:
        parameters_json.write(parameters_json_object)
        
#Call saved dictionary from parameterSort function and convert to a json object and save to parameters.json
def savePreviousVariables(new_parameters):
    if len(new_parameters) <=1:
        return
    parameters_json_object = json.dumps(new_parameters)
#     print("Parameters in json object: ", parameters_json_object)
    with open("previous_parameters.json","w") as parameters_json:
        parameters_json.write(parameters_json_object)
        
#Open and print parameters.json file
def printParameters():
    parameters_print = json.load(open("parameters.json"))
    print("Parameters in JSON: ", json.dumps(parameters_print))

#load the parameters from the parameters.json file
def loadParameters():
    return (json.load(open("/parameters.json")))

#load the parameters from the previous_parameters.json file
def loadPreviousParameters():
    parameters_loaded = json.load(open("previous_parameters.json"))
    return parameters_loaded
