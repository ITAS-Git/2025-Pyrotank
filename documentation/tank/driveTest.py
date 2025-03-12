from gpiozero import Motor
import time

# Initialize motors for forward movement only (using a dummy pin for backward)
left_motor = Motor(forward=17, backward=27)  # Dummy pin 27
right_motor = Motor(forward=22, backward=23) # Dummy pin 23

# Ensure motors are stopped initially
left_motor.stop()
right_motor.stop()

try:
    print("🚀 Motor test: Moving forward for 5 seconds...")

    # Move both motors forward
    left_motor.forward()
    right_motor.forward()
    time.sleep(5)

    # Stop the motors
    print("⏹️  Stopping motors...")
    left_motor.stop()
    right_motor.stop()

except KeyboardInterrupt:
    print("🛑 Interrupted! Stopping motors...")
    left_motor.stop()
    right_motor.stop()
