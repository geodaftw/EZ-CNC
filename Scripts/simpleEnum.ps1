<#
.SYNOPSIS
Simple Windows Enumeration Script
.DESCRIPTION
Quick Enumeration test to make sure we can gather info on a system remotely. Taken from JAWS-ENUM
.EXAMPLE
PS > 
.EXAMPLE
PS > 
.LINK

#>
Param(
    [String]$OutputFilename = "ScriptOutput.txt"
)

function SIMPLE-ENUM {
    write-output "`nRunning Simple Enumeration Script"
    $output = "" 
    $win_version = (Get-WmiObject -class Win32_OperatingSystem)
    $output = $output +  "Windows Version: " + (($win_version.caption -join $win_version.version) + "`r`n")
    $output = $output +  "Architecture: " + (($env:processor_architecture) + "`r`n")
    $output = $output +  "Hostname: " + (($env:ComputerName) + "`r`n")
    $output = $output +  "Current User: " + (($env:username) + "`r`n")
    $output = $output +  "Current Time\Date: " + (get-date)
    $output = $output +  "`r`n"
    $output = $output +  "`r`n"
    write-output "	- Gathering User Information"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Users`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $adsi = [ADSI]"WinNT://$env:COMPUTERNAME"
    $adsi.Children | where {$_.SchemaClassName -eq 'user'} | Foreach-Object {
        $groups = $_.Groups() | Foreach-Object {$_.GetType().InvokeMember("Name", 'GetProperty', $null, $_, $null)}
        $output = $output +  "----------`r`n"
        $output = $output +  "Username: " + $_.Name +  "`r`n"
        $output = $output +  "Groups:   "  + $groups +  "`r`n"
    }
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Network Information`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output + (ipconfig | out-string)
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Arp`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output + (arp -a | out-string) 
    $output = $output +  "`r`n"
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " NetStat`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output + (netstat -ano | out-string)
    $output = $output +  "`r`n"
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Hosts File Content`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  "`r`n"
    $output = $output + ((get-content $env:windir\System32\drivers\etc\hosts | out-string) + "`r`n")
    $output = $output +  "`r`n"
    write-output "	- Gathering Processes, Services and Scheduled Tasks"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Processes`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  ((Get-WmiObject win32_process | Select-Object Name,ProcessID,@{n='Owner';e={$_.GetOwner().User}},CommandLine | sort name | format-table -wrap -autosize | out-string) + "`r`n")
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Scheduled Tasks`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  "Current System Time: " + (get-date)
    $output = $output + (schtasks /query /FO CSV /v | convertfrom-csv | where { $_.TaskName -ne "TaskName" } | select "TaskName","Run As User", "Task to Run"  | fl | out-string)
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Services`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output + (get-service | Select Name,DisplayName,Status | sort status | Format-Table -Property * -AutoSize | Out-String -Width 4096)
    $output = $output +  "`r`n"
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  " Stored Credentials`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output + (cmdkey /list | out-string)
    $output = $output +  "`r`n"
    $output = $output +  "-----------------------------------------------------------`r`n"
    $output = $output +  "`r`n"
    
    # Write to File no matter what
    $output | Out-File -FilePath $OutputFileName -encoding utf8
        
}

if ($OutputFilename.length -gt 0)
    {
        Try 
            { 
                [io.file]::OpenWrite($OutputFilename).close()  
                SIMPLE-ENUM
            }
        Catch 
            { 
                Write-Warning "`nUnable to write to output file $OutputFilename, Check path and permissions" 
            }
    } 
else 
    {
    SIMPLE-ENUM
    }
