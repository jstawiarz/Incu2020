import socket
from ncclient import manager
import xmltodict
import json



def connect(addr):
    try:
        m = manager.connect(host = addr, port = '830', username = 'admin', password = 'cisco!123', hostkey_verify = False)
        return m
    except:
        print("Unable to connect " + node) 


def getVersion(addr):
    try:
        m = connect(node)
        run_xml = m.get_config(source = 'running').data_xml
        run_dict = json.loads(json.dumps(xmltodict.parse(run_xml)))
        return "Version: "+ run_dict["data"]["native"]["version"]
    except: 
        return "Unable to get this node version"


def changeHostname(addr, hostname):
    try:
        m = connect(node)
        HOSTNAME = """
               <config>
                  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                     <hostname>%s</hostname>
                  </native>
               </config>
               """

        config_str = HOSTNAME % (hostname)
        req = m.edit_config(target = 'running', config = config_str)
        return "Hostname changed succesfully"
    except:
        return "Unable to change this node hostname"



def Main():
        host = "<Ubuntu VM IP>"
        port = 5000
                
        mySocket = socket.socket()
        mySocket.bind((host, port))
                
        mySocket.listen(1)
        conn, addr = mySocket.accept()
        print ("Connection from: " + str(addr))
        while True:
                message = conn.recv(1024).decode()
                if message[0] == "show":
                    if message[1] == "version":
                        print(getVersion(addr))
                elif message[0] == "hostname":
                    hostname = message[1]
                    print(changeHostname(addr, hostname))
                conn.send(message.encode())                                        
        conn.close()
             
if __name__ == '__main__':
        Main()








