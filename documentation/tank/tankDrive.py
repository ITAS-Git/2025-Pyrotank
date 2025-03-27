import pygame
import time
from gpiozero import Motor, Servo, LED, PWMLED
import RPi.GPIO as GPIO

# GPIO PIN CONFIGURATION
IR_LED_PIN = 22  # GPIO pin for IR LED (change if needed)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_LED_PIN, GPIO.OUT)

# Initialize motors for tank steering (relay-based)
left_motor = Motor(forward=17, backward=27)

# Initialize LED for Laser
led = LED(4)  # GPIO 4
led_state = False  # Track LED state
a_button_last_state = False  # Track last button state

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

# IR TRANSMISSION FUNCTION
def send_ir_signal(message="1234"):
    pwm = GPIO.PWM(IR_LED_PIN, 38000)  # 38 kHz frequency
    pwm.start(0)  # Start with 0% duty cycle (off)

    for char in message:
        number = int(char)  # Convert to integer
        print(f"🔢 Sending: {number}")

        # Send pulses based on number (basic encoding, modify if needed)
        for _ in range(number + 1):  # Send 'number' pulses
            pwm.ChangeDutyCycle(50)  # Turn IR LED ON (50% duty cycle)
            time.sleep(0.0006)  # Short pulse
            pwm.ChangeDutyCycle(0)  # Turn IR LED OFF
            time.sleep(0.0006)  # Short pause

        time.sleep(0.002)  # Small delay between numbers

    pwm.stop()  # Stop PWM after sending
    print("✅ IR Transmission Complete.")

# Main loop for joystick control
try:
    print("➡️ Use the **D-pad** for tank steering.")
    print("➡️ Use the **right stick** to move the servo.")
    print("➡️ Press **A button** to toggle the LED and send an IR message.")

    while True:
        pygame.event.pump()  # Update the event queue

        # 🚨 LED Toggle & IR Transmission (A Button)
        a_button_pressed = joystick.get_button(1)  # A button on the Switch Pro Controller
        
        if a_button_pressed and not a_button_last_state:  # Detect press event (not holding)
            led_state = not led_state  # Toggle LED state
            if led_state:
                print("🔴 LED ON")
                led.on()
                send_ir_signal("1234")  # Send a string of numbers via IR
            else:
                print("⚫ LED OFF")
                led.off()
        
        a_button_last_state = a_button_pressed  # Update last button state

        # 🎮 **D-pad Motor Control (Safe)**
        dpad_up = joystick.get_hat(0)[1] == 1
        dpad_down = joystick.get_hat(0)[1] == -1
        dpad_left = joystick.get_hat(0)[0] == -1
        dpad_right = joystick.get_hat(0)[0] == 1

        # Ensure no conflicting motor commands
        if dpad_up and not dpad_down:
            print("D-pad Up = Moving Forward")
            left_motor.forward()
        elif dpad_down and not dpad_up:
            print("D-pad Down = Moving Backward")
            left_motor.backward()
        elif dpad_left and not dpad_right:
            print("D-pad Left = Turning Left")
            left_motor.forward()
        elif dpad_right and not dpad_left:
            print("D-pad Right = Turning Right")
            left_motor.backward()
        else:
            left_motor.stop()

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
            servo.value = servo_position  

        time.sleep(0.1)  # Sleep to prevent high CPU usage

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors and servo.")
    left_motor.stop()
    servo.value = None  # Stop the servo
    GPIO.cleanup()  # Clean up GPIO resources
