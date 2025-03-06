from inputs import get_gamepad
import time

def test_controller():
    print("🔍 Waiting for Switch Pro Controller input...")
    print("➡️  Press any button or move a joystick. (Press X to exit)")

    try:
        while True:
            events = get_gamepad()
            for event in events:
                print(f"Event: {event.ev_type}, Code: {event.code}, State: {event.state}")

                # Exit the script if the X button is pressed (BTN_NORTH for Switch Pro Controller)
                if event.code == "BTN_NORTH" and event.state == 1:
                    print("🚪 Exiting controller test.")
                    return

            time.sleep(0.01)  # Prevent CPU overload

    except KeyboardInterrupt:
        print("🚪 Exiting via keyboard interrupt.")

if __name__ == "__main__":
    test_controller()
