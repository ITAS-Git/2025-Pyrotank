import pygame
import time
from gpiozero import Motor, Servo, LED

time.sleep(15)

# Initialize motors for tank steering (relay-based)
left_motor = Motor(forward=17, backward=27)
right_motor = Motor(forward=10, backward=23)

left_motor.stop()

# Initialize LED for Laser
led = LED(4)  # GPIO 4

# Initialize pygame and joystick

controller = False
    

pygame.init()
while not controller:    
    
    pygame.joystick.init()
    print("Searching for controller")
    
    if pygame.joystick.get_count() > 0:
        controller = True
        print("Controller Found")
    else:
        pygame.joystick.quit()
        time.sleep(1)

# Assuming the first joystick (index 0) is the Switch Pro Controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")

# Set up gpiozero for servo control (using GPIO 18)
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)  # GPIO 18 for the servo

# Reset servo to the straight (neutral) position
servo.value = 0  
time.sleep(0.5)  # Allow some time for the servo to move before taking input

try:
    print("➡️ Use the **D-pad** for tank steering.")
    print("➡️ Use the **right stick** to move the servo.")
    print("➡️ Press **A button** to toggle the LED.")

    while True:
        pygame.event.pump()  # Update the event queue

        # 🚨 LED Control (A Button)
        if joystick.get_button(1):  # A button on the Switch Pro Controller
            print("Button A pressed")
            led.on()  # Turn LED on
        else:
            led.off()  # Turn LED off

        # 🎮 **D-pad Motor Control (Safe)**
        dpad_up = joystick.get_hat(0)[1] == 1
        dpad_down = joystick.get_hat(0)[1] == -1
        dpad_left = joystick.get_hat(0)[0] == 1
        dpad_right = joystick.get_hat(0)[0] == -1

        # Ensure no conflicting motor commands
        if dpad_up and not dpad_down and not dpad_left and not dpad_right:
            print("D-pad Up = Moving Forward")
            left_motor.forward()
            right_motor.forward()
        elif dpad_down and not dpad_up and not dpad_left and not dpad_right:
            print("D-pad Down = Moving Backward")
            left_motor.backward()
            right_motor.backward()
        elif dpad_left and not dpad_right and not dpad_down and not dpad_up:
            print("D-pad Left = Turning Left")
            left_motor.forward()
            right_motor.backward()
        elif dpad_right and not dpad_left and not dpad_down and not dpad_up:
            print("D-pad Right = Turning Right")
            left_motor.backward()
            right_motor.forward()
        else:
            left_motor.stop()
            right_motor.stop()

        # 🎯 Servo Control (Right Joystick X-Axis)
        horizontal_axis = joystick.get_axis(2)  # Right stick X-axis

        # Apply deadzone filtering
        if abs(horizontal_axis) < 0.1:
            horizontal_axis = 0
            servo.value = None  # Stop servo completely to avoid jitter
        else:
            # Scale joystick input to servo range (-1 to 1)
            servo_position = max(-1, min(1, horizontal_axis))

            # Set servo position
            print(f"Right Joystick = {servo_position}")
            servo.value = -servo_position  

        time.sleep(0.1)  # Sleep to prevent high CPU usage

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors and servo.")
    left_motor.stop()
    right_motor.stop()
    servo.value = None  # Stop the servo
