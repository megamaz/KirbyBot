import json, requests, os, getpass
from cmd import Cmd

with open('data.json', 'r') as getData:
    data = json.load(getData)

with open('commands.json', 'r') as getCommands:
    slashes = json.load(getCommands)

url = f"https://discord.com/api/v8/applications/{data['appID']}/commands"

headers = {
    "Authorization":f"Bot {data['token']}"
}


class CustomSlashed(Cmd):

    def do_exit(self, inp):
        '''Exits the CMD'''
        return True
    
    def do_clear(self, inp):
        '''Clears the screen'''
        os.system('cls')

    def do_get(self, inp):
        '''Gets info about commands'''
        r = requests.get(url=url, headers=headers)

        if not str(r.status_code).startswith("2"):
            print(f"Could not complete request: {r.status_code} {r.reason}")
            return
        b = json.loads(r.text)
        if inp == "all":
            for x in b:
                print(f'ID:{x["id"]} name:{x["name"]}')
            # print(r.text)
        else:            
            for x in b:
                if x["id"] == inp or x["name"] == inp:
                    # d = json.loads(x)
                    print(json.dumps(x, indent=2))
                    return False
            
            print("could not find the ID/name of the command.")
    
    def do_remove(self, inp):
        '''Removes a command on the Server side'''
        if inp == "":
            print("No ID specified")
            return False
        
        r = requests.delete(url=url + f'/{inp}', headers=headers)
        if r.text != " ":
            print(f"""---RESPONSE---
{r}""")
        else:
            print(f"""---RESPONSE---
{r}
{json.dumps(json.loads(r.text), indent=2)}""")
    
    def do_update(self, inp):
        '''Updates a command'''

        if inp == "":
            print("Specify the command to update.")
            return
        serverSideCommands = requests.get(url, headers=headers).json()

        newVer = None
        for y in slashes:
            if y["name"] == inp:
                newVer = y
        
        if newVer is None:
            print("Could not find command.")
            return
        for x in serverSideCommands:
            if x["name"] == inp:
                pat = requests.patch(url + f"/{x['id']}", headers=headers, json=newVer)
                if not str(pat.status_code).startswith("2"):
                    print(f"Could not complete request. {pat.status_code} {pat.reason}")
                else:
                    print(f"---RESPONSE---\n{pat}\n{json.dumps(json.loads(pat.text), indent=2)}")
                

    def do_add(self, inp):
        '''Uploads a command.'''
        for x in slashes:
            # print(x)
            if x["name"] == inp:
                r = requests.post(url=url, headers=headers, json=x)
                print(f"""---RESPONSE---\n{r}\n{json.dumps(json.loads(r.text), indent=2)}""")
                break
    def do_cmd(self, inp):
        '''Runs a command in the windows CMD'''
        if inp == "":
            print("Missing arguments")
            return
        
        os.system(inp)
        
    def do_change(self, inp):
        '''Change the URL.'''
        global url
        if not inp.startswith("https://discord.com/api/v8/applications/"):
            print("invalid URL.")
        else:
            url = inp


if __name__ == "__main__":
    if data["token"] == "":
        token = getpass.getpass("Insert token: ")
        data["token"] = token
        data["headers"]["Authorization"] = f"Bot {token}"
        with open('data.json', 'w') as dumpData:
            json.dump(data, dumpData)
    os.system('cls')
    CustomSlashed().cmdloop()
    