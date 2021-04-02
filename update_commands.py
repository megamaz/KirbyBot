import requests, json, logging


class HTTPException(Exception):
    pass


data = json.load(open("./data.json"))
logging.info("Loaded data.json")

url = f"https://discord.com/api/v8/applications/{data['appID']}/commands"

headers = {
    "Authorization":f"Bot {data['token']}"
}

# get all commands
commands = json.load(open("./commands.json"))
logging.info("Loaded client side commands")

commandsServer = requests.get(url, headers=headers)
logging.info("Requested server side commands")

if commandsServer.status_code != 200:
    message = f"Could not complete request: {commandsServer.status_code} {commandsServer.reason} (check latest.log for more details)"
    logging.critical(f"{message}\nfull content: {commandsServer.text}")
    raise HTTPException(message)
    
logging.info("Success loading server side commands")

logging.info("Rebasing")

serverCommandNames = [x['name'] for x in commandsServer.json()]
clientCommandNames = [x['name'] for x in commands]

commandsToRemove = [y for y in commandsServer.json() if y['name'] not in clientCommandNames]
newCommands = [x for x in commands if x.get('id') is None]

logging.debug(f'remove {commandsToRemove}')
logging.debug(f'add {newCommands}')

for new in range(len(newCommands)):
    logging.info(f"Adding new command {newCommands[new]['name']}...")
    
    postReq = requests.post(url, json=newCommands[new], headers=headers)

    if not str(postReq.status_code).startswith("2"):
        message = f"Could not complete request: {postReq.status_code} {postReq.reason} (check latest.log for more details)"
        logging.critical(f'{message}\nfull content:{postReq.text}')
        raise HTTPException(message)
    
    logging.info("Success")
    newCommands[new]['id'] = postReq.json()['id']

if len(newCommands) != 0:
    allNewCommands = newCommands
    json.dump(allNewCommands, open("commands.json", 'w'))


for old in commandsToRemove:
    logging.info(f"Removing command {old['name']}...")
    delReq = requests.delete(f'{url}/{old["id"]}', headers=headers)

    if not str(delReq.status_code).startswith("2"):
        message = f"Could not complete request: {delReq.status_code} {delReq.reason} (check latest.log for more details)"
        logging.critical(f'{message}\nfull content:{postReq.text}')
        raise HTTPException(message)
    
    logging.info("Success")
    

logging.info(f"Commands successfully updated. Removed {len(commandsToRemove)} commands and added {len(newCommands)} commands")