import requests
from time import sleep
# LOGIN_TOKEN = 'be590b7a4c26e54091d6d83ee6b85e157b058000'
# AUTH = {
#         'Authorization': 'Token {}'.format(LOGIN_TOKEN)
#     }

url = 'http://localhost:8000/value/1'

PARAMS = {
    'integer':90,
}
try:
    for i in range(0,90,1):
        new_response = requests.post(url,
                                    json={
                                        'integer':i,
                                        })
        print("Sending...")
        #sleep(0.8)
        
    # print(new_response.json()['integer'])

except Exception as e:
    print("ERROR",e)
