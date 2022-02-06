import json
import requests
import time
import urllib
import os
import subprocess

def _url():
    return 'http://<IP-ADDRESS>/zabbix/api_jsonrpc.php'

sessiondata = '''
{ 
    "jsonrpc": "2.0", 
    "method":"user.login", 
    "params": { 
        "user": "<USERNAME>", 
        "password": "<PASSWORD>"
        }, 
    "auth": null, 
    "id":0 
}
'''

#def EPOCH(i):
#    date_time = i
#    pattern = '%d.%m.%Y %H:%M:%S'
#    epoch = int(time.mktime(time.strptime(date_time, pattern)))
#    print('sada : '+str(epoch))
#    return (subprocess.call('date --date=i +%s', shell=True))

sessiondata = json.loads(sessiondata)

tokenHeaders = { 'Content-Type': 'application/json' }
tokenResponse = requests.post(_url(), data=json.dumps(sessiondata), headers=tokenHeaders)
tokenJson = tokenResponse.json()
token = tokenJson['result']

################## EPOCH CODE ##########################
userInput=input('Enter DATE(YYYY-MM-DD) from which you want SMS details : ')
pattern = '%Y-%m-%d'
epoch = int(time.mktime(time.strptime(userInput,pattern)))

userdata = '''
{
    "jsonrpc": "2.0", 
    "method": "alert.get",
    "params": { 
        "output": "extend",
        "time_from": "'''+str(epoch)+'''"
        },
    "auth": "'''+token+'''",
    "id":0
}
'''

#print(userdata)
#userdata = json.loads(userdata)

userHeaders = { 'Content-Type': 'application/json' }
#userResponse = requests.post(_url(), data=json.dumps(userdata, indent=2), headers=userHeaders)
userResponse = requests.post(_url(), data=userdata, headers=userHeaders)
userResponse = userResponse.json()
#print(userResponse['jsonrpc'])


SB = VM = 0

for i in userResponse['result']:
    #print(i['sendto'])
    if i['sendto'] == '<USER1_MOBILE_NUMBER>':
        SB = SB + 1
print()
print('SB :\t' + str(SB))
print()

for i in userResponse['result']:
    if i['sendto'] == '<USER2_MOBILE_NUMBER>':
        VM = VM +1
print('VM :\t\t' + str(VM))
print()

print('-----------------------------')

total = int(SB) + int(VM)
print('Total SMS Sent \t\t' + str(total))
print()
