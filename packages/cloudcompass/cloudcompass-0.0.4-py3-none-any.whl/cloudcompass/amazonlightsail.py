import requests, json

root = requests.get('http://10.35.234.245:5000/resource/1')

# Get list of all services available in amazon lightsail
def services_list():
    return {root['products'][i]['productFamily'] for i in root['products']}

# Get count of services available in amazon lightsail
def services_count():
    print(len({root['products'][i]['productFamily'] for i in root['products']}))

# Get list of all attributes available for a service
def service_attributes():
    return(root['products']['BD6CCGKBZGJQSHXD']['attributes'].keys())
   

    

    