# Connect arduno to pc and run this to display score for tank
# COM PORT WILL NEED TO BE ADJUSTED FOR ARDUNO
import tkinter as tk
import serial

# Set up serial communication
arduino = serial.Serial('COM4', 9600)  # Adjust COM port as needed

# Create the tkinter root window
root = tk.Tk()

# Declare firstLoop as global
firstLoop = True

# Set window to full screen
root.attributes("-fullscreen", True)
root.configure(bg="black")  # Set background color to black for better visibility

# Create a label widget to display Arduino output
label = tk.Label(root, font=("Helvetica", 32), fg="white", bg="black", width=50, height=20)
label.pack(expand=True)

# Function to read from serial and update the label
def update_label():
    global firstLoop  # Declare firstLoop as global to modify its value
    
    try:
        if arduino.in_waiting > 0:
            # Read a line of data from Arduino (assuming it ends with a newline)
            data = arduino.readline().decode('utf-8').strip()
            
            # Check if the data is the score string
            if data.startswith("S"):
                # Only display the score
                label.config(text=data)
            elif firstLoop:
                # Set initial score to 0 for first loop
                label.config(text='Score: 0')
                firstLoop = False  # Set firstLoop to False after the first display
    except serial.SerialException:
        pass

    # Call the function again after 100ms
    root.after(50, update_label)

# Start the update loop
update_label()

# Run the tkinter event loop
root.mainloop()
