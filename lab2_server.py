import serial

def run_server():
    # Initialize the serial connection on COM4
    ser = serial.Serial('COM11', 9600, timeout=1)  # Adjust timeout as needed
    print("Server is running on COM11...")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the message from the client
                message = ser.readline().decode().strip()
                print(f"Received: {message}")

                # Modify the message (e.g., convert to uppercase)
                modified_message = message.upper()
                modified_message += "Abrosimov"

                # Send the modified message back to the client
                ser.write(f"{modified_message}\n".encode())
                print(f"Sent: {modified_message}")
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        ser.close()

if __name__ == "__main__":
    run_server()