# Name:    GlobalIPCloudAPI
# Purpose: Execute the GlobalIPCloudAPI program

######################### Parameters ##########################
param(
    $ip = '',  
    $license = '', 
    [switch]$quiet = $false
    )

########################## Main ############################
Write-Host "`n=================== Melissa Global IP Cloud API ======================`n"

# Get license (either from parameters or user input)
if ([string]::IsNullOrEmpty($license) ) {
  $license = Read-Host "Please enter your license string"
}

# Check for License from Environment Variables 
if ([string]::IsNullOrEmpty($license) ) {
  $license = $env:MD_LICENSE
}

if ([string]::IsNullOrEmpty($license)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}

# Run project
if ([string]::IsNullOrEmpty($ip)) {
  python3 GlobalIPPython3.py --license $license 
}
else {
  python3 GlobalIPPython3.py --license $license --ip $ip
}
