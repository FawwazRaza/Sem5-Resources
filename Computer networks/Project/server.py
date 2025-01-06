import socket

def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the server address and port
    server_address = ('127.0.0.1', 2000)
    sock.bind(server_address)

    print("Socket created and bound")
    print("Listening for messages...\n")

    while True:
        try:
            # Receive the message from the client (name and roll)
            client_message, client_address = sock.recvfrom(2000)
            print(f"Received message from IP: {client_address[0]} and Port No: {client_address[1]}")
            print(f"Client Message: {client_message.decode()}")

            # Split the client message into name and roll number
            client_message = client_message.decode().lower().split('|')
            name = client_message[0].strip()
            roll = client_message[1].strip()

            # Check if the student exists in the file (like 'file.txt')
            data_to_write_Arr = []

            with open('file.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    data_to_write_Arr.append(line.strip().lower())

            # Check if the student is already registered
            found = False
            for line in data_to_write_Arr:
                split_name_and_roll = line.split('|')
                if len(split_name_and_roll) >= 2:
                    file_name = split_name_and_roll[0].strip()
                    file_roll = split_name_and_roll[1].strip()
                    if name == file_name and roll == file_roll:
                        print("Name: ", file_name)
                        print("Roll: ", file_roll)
                        found = True
                        break

            if found:
                # Check if the student is already in registered.txt
                with open('registered.txt', 'r') as file:
                    registered_data = file.readlines()

                already_registered = False
                for line in registered_data:
                    registered_name, registered_roll = line.strip().split('|')
                    if registered_name == name and registered_roll == roll:
                        already_registered = True
                        break

                if already_registered:
                    response = "You have already registered"
                    sock.sendto(response.encode(), client_address)
                else:
                    # Append the student to registered.txt
                    with open('registered.txt', 'a') as file:
                        file.write(f"{name}|{roll}\n")

                    # Send the courses available (like courses.txt)
                    with open('courses.txt', 'r') as file:
                        courses_data = file.read()
                    sock.sendto(courses_data.encode(), client_address)

                    # Receive the number of courses registered from the client
                    client_courses, client_address = sock.recvfrom(2000)
                    client_courses_list = client_courses.decode().split(',')
                    print(f"Courses registered: {client_courses_list}")

                    response = f"You registered {len(client_courses_list)} courses"
                    sock.sendto(response.encode(), client_address)

            else:
                print("Data not found")
                response = "Data not found"
                sock.sendto(response.encode(), client_address)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Closing the socket
    sock.close()

if __name__ == "__main__":
    main()
