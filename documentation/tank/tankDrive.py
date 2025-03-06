from inputs import get_gamepad
import time
from gpiozero import Motor

# Initialize motors
left_motor = Motor(forward=17, backward=18)
right_motor = Motor(forward=22, backward=23)

# Motor control functions
def forward():
    left_motor.forward()
    right_motor.forward()

def backward():
    left_motor.backward()
    right_motor.backward()

def turn_left():
    left_motor.backward()
    right_motor.forward()

def turn_right():
    left_motor.forward()
    right_motor.backward()

def stop():
    left_motor.stop()
    right_motor.stop()

# Map Switch Pro Controller buttons
BUTTON_A = "BTN_SOUTH"  # Forward
BUTTON_B = "BTN_EAST"   # Backward
BUTTON_X = "BTN_NORTH"  # Exit
BUTTON_Y = "BTN_WEST"   # Left turn

# Main loop to read controller input
def control_tank():
    print("Waiting for Switch Pro Controller input...")

    try:
        while True:
            events = get_gamepad()

            for event in events:
                # Check button presses
                if event.ev_type == "Key":
                    if event.code == BUTTON_A and event.state == 1:
                        print("Forward")
                        forward()
                    elif event.code == BUTTON_B and event.state == 1:
                        print("Backward")
                        backward()
                    elif event.code == BUTTON_Y and event.state == 1:
                        print("Left")
                        turn_left()
                    elif event.state == 0:  # Stop on button release
                        print("Stop")
                        stop()

                    # Exit on X button press
                    if event.code == BUTTON_X and event.state == 1:
                        print("Exiting...")
                        stop()
                        return

    except KeyboardInterrupt:
        print("Stopping...")
        stop()

if __name__ == "__main__":
    control_tank()
