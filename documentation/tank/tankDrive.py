import pygame
import time
from gpiozero import Motor, Servo

# Initialize motors for forward movement
left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=10, backward=23)

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

# Check if a joystick is detected
if pygame.joystick.get_count() == 0:
    print("❌ No joystick detected.")
    exit()

# Assuming the first joystick (index 0) is the Switch Pro Controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")

# Set up gpiozero for servo control (using GPIO 18)
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025) # GPIO 18 for the servo

try:
    print("➡️ Press the A button to move forward.")
    print("➡️ Use the left analog stick to control the servo.")

    while True:
        pygame.event.pump()  # Update the event queue

        # Check for the A button (BTN_A) press
        if joystick.get_button(0):  # A button corresponds to button 0 on the Switch Pro Controller
            print("🚀 A button pressed: Moving forward!")
            left_motor.forward()  # Move left motor forward
            right_motor.forward()  # Move right motor forward
        else:
            print("⏹️  A button not pressed: Stopping motors.")
            left_motor.stop()  # Stop left motor
            right_motor.stop()  # Stop right motor

        # Read the horizontal axis (axis 0) of the left analog stick
        # This axis typically ranges from -1.0 (left) to 1.0 (right)
        horizontal_axis = joystick.get_axis(0)
        print(horizontal_axis)
        
        # Map horizontal axis range (-1.0 to 1.0) to servo range (-1 to 1)
        # Scale the joystick input to increase rotation range
        scaled_position = horizontal_axis * 1.5  # Increase range
        servo_position = max(-1, min(1, scaled_position))  # Clamp between -1 and 1

        servo.value = servo_position

        # Update the servo position
        servo.value = servo_position  # Set the servo position based on joystick input

        time.sleep(0.1)  # Sleep to prevent high CPU usage

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors and servo.")
    left_motor.stop()
    right_motor.stop()
    servo.value = None  # Stop the servo (neutral position)
