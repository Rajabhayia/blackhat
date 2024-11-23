import socket

target_host = "127.0.0.1"
target_port = 80

# Create a socket object (UDP socket)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the target host and port
server.bind((target_host, target_port))

print(f"Listening on {target_host}:{target_port}...")

# Listen for incoming UDP packets
while True:
    data, addr = server.recvfrom(4096)  # Buffer size of 4096 bytes
    print(f"Received data: {data.decode()} from {addr}")
