import SoftLayer

def main(dict):

    API_USERNAME = dict['user']
    API_KEY = dict['apikey']
    POWER = dict['power']
    VSI = dict['vsi']
    client = SoftLayer.create_client_from_env(username=API_USERNAME, api_key=API_KEY)

    try:
        virtualGuests = client['SoftLayer_Account'].getVirtualGuests()

    except SoftLayer.SoftLayerAPIError as e:
        print("Unable to retrieve virtual guest. "
              % (e.faultCode, e.faultString))

    vsiFound = False
    for virtualGuest in virtualGuests:
        if virtualGuest['hostname'] == VSI:
            vsiFound = True
            try:
               if POWER == 'OFF':
                    virtualMachines = client['SoftLayer_Virtual_Guest'].powerOff(id=virtualGuest['id'])
               else:
                    virtualMachines = client['SoftLayer_Virtual_Guest'].powerOn(id=virtualGuest['id'])

            except SoftLayer.SoftLayerAPIError as e:
                 vsiFound = e

    return { 'VSI' : VSI, 'Action' : POWER,  'Action_Performed' : vsiFound, 'result' : virtualMachines }