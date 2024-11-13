import serial

def run_client():
    # Initialize the serial connection on COM3
    ser = serial.Serial('COM12', 9600, timeout=1)
    print("Client is running on COM12...")

    try:
        # Send a message to the server
        message = "Hello, Virtual Server!"
        ser.write(f"{message}\n".encode())
        print(f"Sent: {message}")

        # Read the response from the server
        response = ser.readline().decode().strip()
        print(f"Received from server: {response}")

    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        ser.close()

if __name__ == "__main__":
    run_client()
