<#
.SYNOPSIS
    Runs the Melissa Global IP Cloud API Python 3 sample.

.DESCRIPTION
    This script runs GlobalIPPython3.py with python3, passing along the license
    and (if supplied) the IP address.

    Overall flow:
      1. Resolve the license (parameter, prompt, or MD_LICENSE environment variable).
      2. Run GlobalIPPython3.py: with the IP if one was supplied, otherwise with
         only the license (the Python program prompts for the IP).

.PARAMETER ip
    IP address to look up.

.PARAMETER license
    License string. Resolved in this order:
      1. This parameter.
      2. An interactive prompt, if the parameter was not supplied.
      3. The MD_LICENSE environment variable, if the prompt was left blank.
    Note that the environment variable is the last resort, not the first: running
    without -license always prompts, even when MD_LICENSE is set.

.PARAMETER quiet
    Accepted for parity with other sample scripts; not currently used to suppress output.

.EXAMPLE
    .\GlobalIPPython3.ps1 -license "your-license"

.EXAMPLE
    .\GlobalIPPython3.ps1 -ip "12.203.219.6" -license "your-license"
#>

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
# No IP supplied -> run with only the license (the program prompts); otherwise pass the IP through.
if ([string]::IsNullOrEmpty($ip)) {
  python3 GlobalIPPython3.py --license $license
}
else {
  python3 GlobalIPPython3.py --license $license --ip $ip
}
