import socket

target_host = "127.0.0.1"
target_port = 80

# Create a socket object (UDP socket)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data to the target host and port
client.sendto(b"AAABBBCCC", (target_host, target_port))

# Close the socket
client.close()