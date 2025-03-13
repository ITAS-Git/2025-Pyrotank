import pygame
import time
from gpiozero import Motor, Servo, LED

# Initialize motors for forward movement
left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=10, backward=23)

# Initialize LED for Laser
led = LED(4) # GPIO 4

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
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)  # GPIO 18 for the servo

# Reset servo to the straight (neutral) position
servo.value = 0  
time.sleep(0.5)  # Allow some time for the servo to move before taking input

# Deadzone threshold to prevent jitter
DEADZONE = 0.01

# Smoothing factor (higher value = smoother but slower response)
SMOOTHING_FACTOR = 0.8

previous_servo_value = 0  # Store previous value for smoothing

try:
    print("➡️ Press the A button to move forward.")
    print("➡️ Use the left analog stick to control the servo.")

    while True:
        pygame.event.pump()  # Update the event queue
        
        # Check for the B button (BTN_B) press
        if joystick.get_button(0):
            print("B button pressed: Shooting laser")
            Led.on() # Turn the LED on
        else:
            print("B button not pressed: laser off")
            Led.off() # Turn the LED off
        
        # Check for the A button (BTN_A) press
        if joystick.get_button(1):  # A button corresponds to button 0 on the Switch Pro Controller
            print("🚀 A button pressed: Moving forward!")
            left_motor.forward()  # Move left motor forward
            right_motor.forward()  # Move right motor forward
        else:
            left_motor.stop()
            right_motor.stop()

        # Read the horizontal axis (axis 0) of the left analog stick
        horizontal_axis = joystick.get_axis(0)

        # Apply deadzone filtering
        if abs(horizontal_axis) < DEADZONE:
            horizontal_axis = 0  # Ignore small movements
            servo.value = None  # Stop servo completely to avoid jitter
        else:
            # Smooth out fluctuations (Moving Average Filter)
            smoothed_value = (SMOOTHING_FACTOR * horizontal_axis) + (1 - SMOOTHING_FACTOR) * previous_servo_value
            previous_servo_value = smoothed_value  # Update for next loop

            print(f"Joystick Axis (Raw): {horizontal_axis}, Smoothed: {smoothed_value}")

            # Scale the joystick input to increase rotation range
            scaled_position = smoothed_value * 1  # Increase range
            servo_position = max(-1, min(1, scaled_position))  # Clamp between -1 and 1

            # Set servo value (Reversed direction removed)
            servo.value = -servo_position  

        time.sleep(0.1)  # Sleep to prevent high CPU usage

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors and servo.")
    left_motor.stop()
    right_motor.stop()
    servo.value = None  # Stop the servo (neutral position)
