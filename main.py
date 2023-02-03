import socket
import threading
import time
import requests
import datetime

def create_packet():
    # Create the packet to query the server
    packet = bytearray()
    packet.extend(b'\xFE\x01')
    return packet

# Create the packet
packet = create_packet()

def check_server(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, port))
        s.send(packet)
        data = s.recv(1024)
        s.close()

        if len(data) > 0:
            print(f"Server found at {ip}:{port}")
            message = f"Server found at {ip}:{port} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            requests.post("https://discord.com/api/webhooks/1071013978530119690/Ra33VyHupRQ5aanV_WXczFcWTR1Vx_SSmuV3TPUY2V5Z3LWUCci0QQbXELgqCAFsR9kg",
                          json={"content": "```" + message + "```"})
    except socket.error:
        print(f"Could not connect to {ip}:{port}")

def main():
    start_ip = input("Enter the starting IP address (e.g. 1.1.1.1): ")
    start_ip = start_ip.strip().split(".")
    start_ip = [int(x) for x in start_ip]
    start_ip = (start_ip[0], start_ip[1], start_ip[2], start_ip[3])

    end_ip = input("Enter the ending IP address (e.g. 255.255.255.255): ")
    end_ip = end_ip.strip().split(".")
    end_ip = [int(x) for x in end_ip]
    end_ip = (end_ip[0], end_ip[1], end_ip[2], end_ip[3])

    port = int(input("Enter the port to scan (e.g. 25565): "))

    threads = []
    for i in range(start_ip[0], end_ip[0]+1):
        for j in range(start_ip[1], end_ip[1]+1):
            for k in range(start_ip[2], end_ip[2]+1):
                for l in range(start_ip[3], end_ip[3]+1):
                    ip = f"{i}.{j}.{k}.{l}"
                    t = threading.Thread(target=check_server, args=(ip, port))
                    threads.append(t)
                    t.start()
                    time.sleep(0.1)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()



#178.63.19.87