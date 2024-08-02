# This file contains the screen mirror function that is used to apply update the RGB on the keyboard.

import pyautogui

from cuesdk import CorsairLedColor
from corsair_rgb.config import KEYBOARD_WIDTH, KEYBOARD_HEIGHT

# Clear all LEDs on the keyboard, as the previous programmed sequence is not removed
def clear_all_leds(led_positions, device_id, sdk):
    led_colors = [CorsairLedColor(id=led.id, r=0, g=0, b=0, a=255) for led in led_positions]
    sdk.set_led_colors(device_id, led_colors)

# Get the pixel color at the specified screen coordinates, based on the pyautogui screenshot
def get_screen_pixel(x, y, screen):
    return screen.getpixel((x, y))

# Map the screen to the keyboard by updating the LED colors based on the screen pixel colors
def map_screen_to_keyboard(led_mapping, device_id, sdk):
    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()
    key_width = screen_width // KEYBOARD_WIDTH
    key_height = screen_height // KEYBOARD_HEIGHT

    # Take a screenshot of the screen
    screen = pyautogui.screenshot()
    led_colors = []

    # Iterate over each key on the keyboard and get the corresponding pixel color from the screen.
    # This grid approach has been taken to:
    # 1. Reduce the number of calls to the SDK, which can be slow.
    # 2. Remove the need for calculating the nearest key, which was proven to be very slow.
    # Downside of the method is that it assumes a grid layout for the keyboard, which is not 100% accurate for keyboards.
    # It also requires manual configuration of the keyboard layout, rather than a scalable calculated solution.
    for y in range(KEYBOARD_HEIGHT):
        for x in range(KEYBOARD_WIDTH):
            if (x, y) in led_mapping:
                pixel_color = get_screen_pixel(x * key_width, y * key_height, screen)
                led_colors.append(CorsairLedColor(id=led_mapping[(x, y)], r=pixel_color[0], g=pixel_color[1], b=pixel_color[2], a=255))

    # Set the LED colors on the keyboard
    if led_colors:
        sdk.set_led_colors(device_id, led_colors)
