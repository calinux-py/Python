Wi-Fi Password Cracker - PowerShell Script

This repository contains a PowerShell script that allows you to crack Wi-Fi passwords using the pywifi library. The script was written by CaliNux.
Prerequisites

Before running the script, make sure you have the following installed:

    Python
    pywifi library

Usage

    Ensure you have a file named pass.txt containing a list of possible Wi-Fi passwords, with each password on a separate line.
    Run the script using the Python interpreter.
    The script will scan for available Wi-Fi networks and display their SSID and MAC addresses.
    Enter the SSID of the network you want to crack when prompted. If you want to crack all networks, enter 'CRACKALL'.
    The script will attempt to crack the Wi-Fi password for the selected network or all networks.
    If successful, the password will be displayed, and the results will be saved in cracked-passwords.txt.