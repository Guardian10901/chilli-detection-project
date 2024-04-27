import pyfirmata
import time

# Connect to the Arduino
board = None
try:
    board = pyfirmata.Arduino('COM3')  # Update with your Arduino serial port

    # Define servo pins
    servo1_pin = 3
    servo2_pin = 6
    servo3_pin = 9
    servo4_pin = 11

    # Configure the servo pins as Servo outputs
    servo1 = board.get_pin('d:{}:s'.format(servo1_pin))
    servo2 = board.get_pin('d:{}:s'.format(servo2_pin))
    servo3 = board.get_pin('d:{}:s'.format(servo3_pin))
    servo4 = board.get_pin('d:{}:s'.format(servo4_pin))

    # Function to move a servo to a specific angle
    def move_servo(servo, angle):
        servo.write(angle)
        time.sleep(0.1)  # Wait for the servo to reach the position

    try:
        # Move servo 1 to 0 degrees
        move_servo(servo3, 90)
        # Move servo 2 to 90 degrees
        # move_servo(servo4, 90)
        # # Move servo 3 to 180 degrees
        # move_servo(servo3, 180)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

except Exception as e:
    print(f"Failed to connect to the Arduino: {str(e)}")

finally:
    if board is not None:
        board.exit()