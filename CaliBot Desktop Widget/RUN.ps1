$scriptPaths = @("C:\Programming\#PythonScripts\CaliBot\calibot.py"); foreach ($scriptPath in $scriptPaths) { Start-Process -FilePath $scriptPath -WindowStyle Hidden }
