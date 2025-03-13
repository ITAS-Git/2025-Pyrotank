import pygame
import time
from gpiozero import Motor, Servo, LED

# Initialize motors for tank steering (relay-based)
left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=10, backward=23)

# Initialize LED for Laser
Led = LED(4)  # GPIO 4

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
DEADZONE = 0.1  
ACTIVATION_THRESHOLD = 0.5  # Joystick must be moved at least halfway

# Smoothing factor (higher value = smoother but slower response)
SMOOTHING_FACTOR = 0.8
previous_servo_value = 0  

try:
    print("➡️ Use the left stick for tank steering (relay control).")
    print("➡️ Use the right stick to move the servo.")
    print("➡️ Press the A button to toggle the LED.")

    while True:
        pygame.event.pump()  # Update the event queue

        # 🚨 LED Control (A Button)
        if joystick.get_button(1):  # A button on the Switch Pro Controller
            Led.on()  # Turn LED on
        else:
            Led.off()  # Turn LED off

        # 🎮 Tank Steering (Left Joystick)
        move = -joystick.get_axis(1)  # Forward/Backward (Invert Y-axis)
        turn = joystick.get_axis(0)   # Left/Right Steering

        # Apply deadzone
        if abs(move) < DEADZONE:
            move = 0
        if abs(turn) < DEADZONE:
            turn = 0

        # Motor control logic (fully ON or OFF)
        if move >= ACTIVATION_THRESHOLD:
            left_motor.forward()
            right_motor.forward()
        elif move <= -ACTIVATION_THRESHOLD:
            left_motor.backward()
            right_motor.backward()
        elif turn >= ACTIVATION_THRESHOLD:
            left_motor.forward()
            right_motor.backward()
        elif turn <= -ACTIVATION_THRESHOLD:
            left_motor.backward()
            right_motor.forward()
        else:
            left_motor.stop()
            right_motor.stop()

        # 🎯 Servo Control (Right Joystick X-Axis)
        horizontal_axis = joystick.get_axis(2)  # Right stick X-axis

        # Apply deadzone filtering
        if abs(horizontal_axis) < DEADZONE:
            horizontal_axis = 0
            servo.value = None  # Stop servo completely to avoid jitter
        else:
            # Smooth out fluctuations
            smoothed_value = (SMOOTHING_FACTOR * horizontal_axis) + (1 - SMOOTHING_FACTOR) * previous_servo_value
            previous_servo_value = smoothed_value

            # Scale joystick input to servo range (-1 to 1)
            servo_position = max(-1, min(1, smoothed_value))

            # Set servo position
            servo.value = servo_position  

        time.sleep(0.1)  # Sleep to prevent high CPU usage

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors and servo.")
    left_motor.stop()
    right_motor.stop()
    servo.value = None  # Stop the servo
