import socket
import threading
import time
import requests
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from mcclient import SLPClient

def create_packet():
    # Create the packet to query the server
    packet = bytearray()
    packet.extend(b'\xFE\x01')
    return packet

# Create the packet
packet = create_packet()

def check_server(ip, port):
    try:
        client = SLPClient(ip, port)
        res = client.get_status()

        players = ""
        for player in res.res.get('players', {}).get('list', []):
            players += f"\n - {player['name']}"

        message = DiscordEmbed(title="__New Minecraft Server Found! (*Click Me!*)__",
                               url=f"https://mcsrvstat.us/server/{ip}:{port}",
                               description=f"Server Ip: `{ip}:{port}`\n Players Online: `{res.res['players']['online']}`{players}\n Max Players: `{res.res['players']['max']}`\n Version: `{res.res['version']}`\n\n*Bot Made By __xxx__*",
                               color=242424)
        hook = DiscordWebhook(url="https://discord.com/api/webhooks/1071013978530119690/Ra33VyHupRQ5aanV_WXczFcWTR1Vx_SSmuV3TPUY2V5Z3LWUCci0QQbXELgqCAFsR9kg",
                              username="The Fifth Eye")
        hook.add_embed(message)
        hook.execute()
    except socket.error:
        print(f"Checked The Ip: {ip}:{port}")

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
