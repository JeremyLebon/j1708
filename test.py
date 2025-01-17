import serial
import time

# Configure the serial port
ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=0.01  # Short timeout for reading characters
)

def calculate_checksum(message):
    """Calculate J1708 checksum."""
    return (256 - sum(message[:-1]) % 256) & 0xFF

def process_message(message):
    """Process and validate the message."""
    if len(message) < 2:  # Minimum size: 1 byte MID + 1 byte checksum
        print("Incomplete message. Discarding.")
        return

    received_checksum = message[-1]
    calculated_checksum = calculate_checksum(message)

    if received_checksum == calculated_checksum:
        print(f"Valid Message: {message}")
    else:
        print(f"Invalid Message (Checksum Error): {message}")

# Main loop to read and process J1708 messages
buffer = []
last_byte_time = time.time()

while True:
    byte = ser.read(1)  # Read one byte at a time
    if byte:
        current_time = time.time()
        elapsed_time = current_time - last_byte_time

        if elapsed_time > 0.00166667:  # Gap > 2 character times (≈2.08 ms)
            if buffer:
                process_message(buffer)  # Process the complete message
                buffer = []  # Clear the buffer for the next message

        buffer.append(ord(byte))  # Add the byte to the buffer
        last_byte_time = current_time
