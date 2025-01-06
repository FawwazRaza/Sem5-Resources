import socket

def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 2000)

    try:
        # Get input from the user
        client_message = input("Enter name only: ")
        client_roll = input("Enter roll number only: ")
        client_message = client_message + "|" + client_roll
        print(client_message)

        # Send the message to the server
        sock.sendto(client_message.encode(), server_address)

        # Receive the response from the server
        server_message, _ = sock.recvfrom(2000)
        print(f"Server Message: {server_message.decode()}")

        # Send the courses list
        client_courses = input("Enter course numbers separated by commas: ")
        courses = client_courses.split(',')
        print(courses)

        # Send the list of courses to the server
        sock.sendto(','.join(courses).encode(), server_address)

        # Receive the final response from the server
        server_message, _ = sock.recvfrom(2000)
        print(f"Server Message: {server_message.decode()}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    main()
