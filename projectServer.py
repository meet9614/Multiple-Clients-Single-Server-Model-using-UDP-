import socket
import threading

def xor_cipher(text, key=3):
    return "".join(chr(ord(char) ^ key) for char in text)
# Server configuration
server_ip = "127.0.0.1"
server_port = 12345
clients = {}
numbers = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print("UDP Server is up and waiting for client data...")

def handle_client():
    global numbers
    while True:
        data, addr = server_socket.recvfrom(1024)
        num = int(data.decode())

        if addr not in clients:
            clients[addr] = num
            numbers.append(num)

        # Process once we receive 3 different clients
        if len(clients) == 3:
            total = sum(numbers)
            
            encrypted_total = xor_cipher(str(total))
            decrypted_total = xor_cipher(encrypted_total)

            print(f"Encrypted Sum: {encrypted_total}, Decrypted Sum: {decrypted_total}")

            # Broadcast to all clients
            for client in clients.keys():
                server_socket.sendto(decrypted_total.encode(), client)

            # Reset for next round
            clients.clear()
            numbers.clear()
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass  # Keep server running
