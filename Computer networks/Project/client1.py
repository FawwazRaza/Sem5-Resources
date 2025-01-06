import socket

def send_message(message, host='127.0.0.1', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'), (host, port))
    response, _ = sock.recvfrom(1024)
    print(f"Server response: {response.decode('utf-8')}")
    sock.close()

if __name__ == "__main__":
    while True:
        message = input("Enter your message (YY-AAAA-CI or YY-AAAA-CO), or 'quit' to exit: ")
        if message.lower() == 'quit':
            break
        send_message(message)