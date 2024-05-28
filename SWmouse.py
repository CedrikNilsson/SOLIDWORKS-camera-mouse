import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize joystick pins
x_axis = AnalogIn(board.A1)  # Joystick x-axis
y_axis = AnalogIn(board.A2)  # Joystick y-axis
z_axis = AnalogIn(board.A3)  # Zoom control

# Initialize buttons
button_pan = DigitalInOut(board.GP14)
button_pan.direction = Direction.INPUT
button_pan.pull = Pull.UP

button_s = DigitalInOut(board.GP15)
button_s.direction = Direction.INPUT
button_s.pull = Pull.UP

button_f = DigitalInOut(board.GP16)
button_f.direction = Direction.INPUT
button_f.pull = Pull.UP

# Initialize the mouse and keyboard
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# Function to map joystick input to a range
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Press middle mouse button at the start
mouse.press(Mouse.MIDDLE_BUTTON)

while True:
    x = x_axis.value  # Read x-axis value
    y = y_axis.value  # Read y-axis value
    z = z_axis.value  # Read zoom control value

    # Move mouse if x or y axis changes
    x_movement = map_value(x, 0, 65535, -20, 20)  # Adjust sensitivity as needed
    y_movement = map_value(y, 0, 65535, -20, 20)
    mouse.move(x=x_movement, y=y_movement)

    # Press and hold Control key if pan button is pressed
    if not button_pan.value:
        keyboard.press(Keycode.CONTROL)
    else:
        keyboard.release(Keycode.CONTROL)

    # Press S if S button is pressed
    if not button_s.value:
        keyboard.press(Keycode.S)
        time.sleep(0.1)  # Adjust as needed
        keyboard.release(Keycode.S)

    # Press F if F button is pressed
    if not button_f.value:
        keyboard.press(Keycode.F)
        time.sleep(0.1)  # Adjust as needed
        keyboard.release(Keycode.F)

    # Release middle mouse button if absolute value of mouse movement is less or equal to 30
    if abs(x_movement) <= 1 and abs(y_movement) <= 1:
        mouse.release(Mouse.MIDDLE_BUTTON)
        middle_button_pressed = False
    else:
        mouse.press(Mouse.MIDDLE_BUTTON)

    # Map zoom control to mouse scroll
    if z < 30000:
        mouse.move(wheel=1)  # Scroll up
    elif z > 35000:
        mouse.move(wheel=-1)  # Scroll down

    # Short delay to avoid flooding the computer with inputs
    time.sleep(0.05)


