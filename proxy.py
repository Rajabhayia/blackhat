import sys
import socket
import threading

def hexdump(src, length=16):
    result = []
    if isinstance(src, str):
        src = src.encode()

    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join([f"{x:02X}" for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append(f"{i:04X}   {hexa:<{length * 3}}   {text}")
    
    print('\n'.join(result))

def receive_from(connection):
    buffer = b""
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
        print(f"[*] Listening on {local_host}:{local_port}")
        server.listen(5)
    except Exception as e:
        print(f"[!!] Failed to listen on {local_host}:{local_port}: {e}")
        sys.exit(0)
    
    while True:
        client_socket, addr = server.accept()
        print(f"[==>] Received incoming connection from {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # If receive_first is True, fetch data from remote server first
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print("[<==] Initial data from remote server:")
            hexdump(remote_buffer)
            client_socket.send(remote_buffer)

    while True:
        try:
            # Receive data from client and forward it to remote server
            local_buffer = receive_from(client_socket)
            if local_buffer:
                print(f"[==>] Received {len(local_buffer)} bytes from localhost.")
                hexdump(local_buffer)
                remote_socket.send(local_buffer)
                print("[==>] Sent to remote server.")

            # Receive data from remote server and forward it to client
            remote_buffer = receive_from(remote_socket)
            if remote_buffer:
                print(f"[<==] Received {len(remote_buffer)} bytes from remote server.")
                hexdump(remote_buffer)
                client_socket.send(remote_buffer)
                print("[<==] Sent to localhost.")
            
            # Check if connections should terminate
            if not local_buffer and not remote_buffer:
                print("[*] No more data. Closing connections.")
                client_socket.close()
                remote_socket.close()
                break

        except Exception as e:
            print(f"[!!] Error in proxy_handler: {e}")
            client_socket.close()
            remote_socket.close()
            break

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 21 test.rebex.net 21 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() in ['true', '1', 'yes']

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()
