import subprocess
import ipaddress
import threading
import socket
import os
from datetime import date

def get_default_gateway():
    result = subprocess.run('powershell.exe Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -ExpandProperty NextHop',
                            capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()

def map_subnet(ip_range, output_file):
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
        hosts = [socket.getfqdn(str(host)) for host in network.hosts()]
        with open(output_file, 'a', newline='') as file:
            file.write(f"Subnet: {network.network_address}/{network.prefixlen}\nHosts:\n")
            file.writelines(f"{host} - {name}\n" for host, name in zip(network.hosts(), hosts) if name)
    except ValueError as e:
        with open(output_file, 'a', newline='') as file:
            file.write(f"Error mapping subnet for {ip_range}: {e}\n")

def main():
    gateway = get_default_gateway()
    if gateway:
        hostname = socket.gethostname()
        today = date.today().strftime("%Y-%m-%d")
        output_file = os.path.join(os.environ.get('TEMP'), f"DeviceGrabLoot_{hostname}_{today}.txt")  # Updated line
        threads = [threading.Thread(target=map_subnet, args=(f"{gateway.rsplit('.', 1)[0]}.{i}", output_file))
                   for i in range(1, 256)]
        [t.start() for t in threads]
        [t.join() for t in threads]

if __name__ == '__main__':
    main()
