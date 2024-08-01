from cuesdk import CueSdk, CorsairDeviceFilter, CorsairDeviceType, CorsairError, CorsairLedColor, CorsairLedId_Keyboard
import pyautogui
import time

MAX_RETRIES = 5

# Define the keyboard layout (e.g., 6 rows and 21 columns for a K95 RGB Platinum)
KEYBOARD_WIDTH = 21
KEYBOARD_HEIGHT = 6

# Initialize the iCUE SDK
sdk = CueSdk()

# Define the callback function for state changes
def on_state_changed(event):
    print(event.state)

def main():
    retries = 0
    while retries < MAX_RETRIES:
        sdk.connect(on_state_changed)
        print("Waiting for connection to Corsair iCUE software...")
        time.sleep(1)  # Pause for 1 second before retrying
        session_details, _ = sdk.get_session_details()
        if session_details.client_version.major != 0:
            print("Connected to Corsair iCUE software.")
            break
        retries += 1
    else:
        raise RuntimeError("Unable to connect to Corsair iCUE software after {} attempts.".format(MAX_RETRIES))

    # Create a device filter to retrieve all devices
    device_filter = CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_All)

    # Retrieve information about all connected devices
    devices, err = sdk.get_devices(device_filter)

    if err != CorsairError.CE_Success:
        raise RuntimeError("Error retrieving devices: {}".format(err))

    # Check if any devices are found
    if not devices:
        raise RuntimeError("No devices found.")

    # Assume we are using the first device
    device_id = devices[0].device_id

    # Get LED positions for the selected device
    led_positions, err = sdk.get_led_positions(device_id)
    if not led_positions:
        raise RuntimeError("Failed to get LED positions: {}".format(err))
    
    max_cx = max(led.cx for led in led_positions)
    max_cy = max(led.cy for led in led_positions)
    
    # Clear all LEDs before starting the main loop
    clear_all_leds(led_positions, device_id)

    # Pre-calculate the mapping between keys and LED IDs
    led_mapping = precompute_led_mapping()

    try:
        while True:
            map_screen_to_keyboard(led_mapping, device_id)
            time.sleep(0.1)  # Small delay to control the update frequency
    except KeyboardInterrupt:
        print("Stopping iCUE test...")

def clear_all_leds(led_positions, device_id):
    led_colors = [CorsairLedColor(id=led.id, r=0, g=0, b=0, a=255) for led in led_positions]
    sdk.set_led_colors(device_id, led_colors)

def get_screen_pixel(x, y, screen):
    # Get the color of the pixel at (x, y) from the captured screen
    return screen.getpixel((x, y))

def precompute_led_mapping():
    key_to_led_id = {
    (0, 0): CorsairLedId_Keyboard.CLK_Escape,
    (1, 0): CorsairLedId_Keyboard.CLK_F1,
    (2, 0): CorsairLedId_Keyboard.CLK_F2,
    (3, 0): CorsairLedId_Keyboard.CLK_F3,
    (4, 0): CorsairLedId_Keyboard.CLK_F4,
    (5, 0): CorsairLedId_Keyboard.CLK_F5,
    (6, 0): CorsairLedId_Keyboard.CLK_F6,
    (7, 0): CorsairLedId_Keyboard.CLK_F7,
    (8, 0): CorsairLedId_Keyboard.CLK_F8,
    (9, 0): CorsairLedId_Keyboard.CLK_F9,
    (10, 0): CorsairLedId_Keyboard.CLK_F10,
    (11, 0): CorsairLedId_Keyboard.CLK_F11,
    (12, 0): CorsairLedId_Keyboard.CLK_F12,
    (13, 0): CorsairLedId_Keyboard.CLK_PrintScreen,
    (14, 0): CorsairLedId_Keyboard.CLK_ScrollLock,
    (15, 0): CorsairLedId_Keyboard.CLK_PauseBreak,
    # For now these are set to Invalid, which doesn't exist on my keyboard as there are no keys in this position
    (16, 0): CorsairLedId_Keyboard.CLK_Invalid,
    (17, 0): CorsairLedId_Keyboard.CLK_Invalid,
    (18, 0): CorsairLedId_Keyboard.CLK_Invalid,
    (19, 0): CorsairLedId_Keyboard.CLK_Invalid,
    (20, 0): CorsairLedId_Keyboard.CLK_Invalid,

    (0, 1): CorsairLedId_Keyboard.CLK_GraveAccentAndTilde,
    (1, 1): CorsairLedId_Keyboard.CLK_1,
    (2, 1): CorsairLedId_Keyboard.CLK_2,
    (3, 1): CorsairLedId_Keyboard.CLK_3,
    (4, 1): CorsairLedId_Keyboard.CLK_4,
    (5, 1): CorsairLedId_Keyboard.CLK_5,
    (6, 1): CorsairLedId_Keyboard.CLK_6,
    (7, 1): CorsairLedId_Keyboard.CLK_7,
    (8, 1): CorsairLedId_Keyboard.CLK_8,
    (9, 1): CorsairLedId_Keyboard.CLK_9,
    (10, 1): CorsairLedId_Keyboard.CLK_0,
    (11, 1): CorsairLedId_Keyboard.CLK_MinusAndUnderscore,
    (12, 1): CorsairLedId_Keyboard.CLK_EqualsAndPlus,
    (13, 1): CorsairLedId_Keyboard.CLK_Backspace,
    (14, 1): CorsairLedId_Keyboard.CLK_Insert,
    (15, 1): CorsairLedId_Keyboard.CLK_Home,
    (16, 1): CorsairLedId_Keyboard.CLK_PageUp,
    (17, 1): CorsairLedId_Keyboard.CLK_NumLock,
    (18, 1): CorsairLedId_Keyboard.CLK_KeypadSlash,
    (19, 1): CorsairLedId_Keyboard.CLK_KeypadAsterisk,
    (20, 1): CorsairLedId_Keyboard.CLK_KeypadMinus,

    (0, 2): CorsairLedId_Keyboard.CLK_Tab,
    (1, 2): CorsairLedId_Keyboard.CLK_Q,
    (2, 2): CorsairLedId_Keyboard.CLK_W,
    (3, 2): CorsairLedId_Keyboard.CLK_E,
    (4, 2): CorsairLedId_Keyboard.CLK_R,
    (5, 2): CorsairLedId_Keyboard.CLK_T,
    (6, 2): CorsairLedId_Keyboard.CLK_Y,
    (7, 2): CorsairLedId_Keyboard.CLK_U,
    (8, 2): CorsairLedId_Keyboard.CLK_I,
    (9, 2): CorsairLedId_Keyboard.CLK_O,
    (10, 2): CorsairLedId_Keyboard.CLK_P,
    (11, 2): CorsairLedId_Keyboard.CLK_BracketLeft,
    (12, 2): CorsairLedId_Keyboard.CLK_BracketRight,
    (13, 2): CorsairLedId_Keyboard.CLK_Enter,
    (14, 2): CorsairLedId_Keyboard.CLK_Delete,
    (15, 2): CorsairLedId_Keyboard.CLK_End,
    (16, 2): CorsairLedId_Keyboard.CLK_PageDown,
    (17, 2): CorsairLedId_Keyboard.CLK_Keypad7,
    (18, 2): CorsairLedId_Keyboard.CLK_Keypad8,
    (19, 2): CorsairLedId_Keyboard.CLK_Keypad9,
    (20, 2): CorsairLedId_Keyboard.CLK_KeypadPlus,

    (0, 3): CorsairLedId_Keyboard.CLK_CapsLock,
    (1, 3): CorsairLedId_Keyboard.CLK_A,
    (2, 3): CorsairLedId_Keyboard.CLK_S,
    (3, 3): CorsairLedId_Keyboard.CLK_D,
    (4, 3): CorsairLedId_Keyboard.CLK_F,
    (5, 3): CorsairLedId_Keyboard.CLK_G,
    (6, 3): CorsairLedId_Keyboard.CLK_H,
    (7, 3): CorsairLedId_Keyboard.CLK_J,
    (8, 3): CorsairLedId_Keyboard.CLK_K,
    (9, 3): CorsairLedId_Keyboard.CLK_L,
    (10, 3): CorsairLedId_Keyboard.CLK_SemicolonAndColon,
    (11, 3): CorsairLedId_Keyboard.CLK_ApostropheAndDoubleQuote,
    (12, 3): CorsairLedId_Keyboard.CLK_NonUsTilde, #Not sure about this one
    (13, 3): CorsairLedId_Keyboard.CLK_Invalid,
    (14, 3): CorsairLedId_Keyboard.CLK_Invalid,
    (15, 3): CorsairLedId_Keyboard.CLK_Invalid,
    (16, 3): CorsairLedId_Keyboard.CLK_Invalid,
    (17, 3): CorsairLedId_Keyboard.CLK_Keypad4,
    (18, 3): CorsairLedId_Keyboard.CLK_Keypad5,
    (19, 3): CorsairLedId_Keyboard.CLK_Keypad6,
    (20, 3): CorsairLedId_Keyboard.CLK_Invalid,

    (0, 4): CorsairLedId_Keyboard.CLK_LeftShift,
    (1, 4): CorsairLedId_Keyboard.CLK_NonUsBackslash,
    (2, 4): CorsairLedId_Keyboard.CLK_Z,
    (3, 4): CorsairLedId_Keyboard.CLK_X,
    (4, 4): CorsairLedId_Keyboard.CLK_C,
    (5, 4): CorsairLedId_Keyboard.CLK_V,
    (6, 4): CorsairLedId_Keyboard.CLK_B,
    (7, 4): CorsairLedId_Keyboard.CLK_N,
    (8, 4): CorsairLedId_Keyboard.CLK_M,
    (9, 4): CorsairLedId_Keyboard.CLK_CommaAndLessThan,
    (10, 4): CorsairLedId_Keyboard.CLK_PeriodAndBiggerThan,
    (11, 4): CorsairLedId_Keyboard.CLK_SlashAndQuestionMark,
    (12, 4): CorsairLedId_Keyboard.CLK_RightShift,
    (13, 4): CorsairLedId_Keyboard.CLK_Invalid,
    (14, 4): CorsairLedId_Keyboard.CLK_Invalid,
    (15, 4): CorsairLedId_Keyboard.CLK_UpArrow,
    (16, 4): CorsairLedId_Keyboard.CLK_Invalid,
    (17, 4): CorsairLedId_Keyboard.CLK_Keypad1,
    (18, 4): CorsairLedId_Keyboard.CLK_Keypad2,
    (19, 4): CorsairLedId_Keyboard.CLK_Keypad3,
    (20, 4): CorsairLedId_Keyboard.CLK_KeypadEnter,

    (0, 5): CorsairLedId_Keyboard.CLK_LeftCtrl,
    (1, 5): CorsairLedId_Keyboard.CLK_LeftGui,
    (2, 5): CorsairLedId_Keyboard.CLK_LeftAlt,
    (3, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (4, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (5, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (6, 5): CorsairLedId_Keyboard.CLK_Space,
    (7, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (8, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (9, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (10, 5): CorsairLedId_Keyboard.CLK_RightAlt,
    (11, 5): CorsairLedId_Keyboard.CLK_RightGui,
    (12, 5): CorsairLedId_Keyboard.CLK_Application,
    (13, 5): CorsairLedId_Keyboard.CLK_RightCtrl,
    (14, 5): CorsairLedId_Keyboard.CLK_LeftArrow,
    (15, 5): CorsairLedId_Keyboard.CLK_DownArrow,
    (16, 5): CorsairLedId_Keyboard.CLK_RightArrow,
    (17, 5): CorsairLedId_Keyboard.CLK_Keypad0,
    (18, 5): CorsairLedId_Keyboard.CLK_Invalid,
    (19, 5): CorsairLedId_Keyboard.CLK_KeypadPeriodAndDelete,
    (20, 5): CorsairLedId_Keyboard.CLK_Invalid,
    }

    return key_to_led_id

def map_screen_to_keyboard(led_mapping, device_id):
    screen_width, screen_height = pyautogui.size()
    key_width = screen_width // KEYBOARD_WIDTH
    key_height = screen_height // KEYBOARD_HEIGHT

    # Capture the screen once per iteration
    screen = pyautogui.screenshot()

    led_colors = []

    for y in range(KEYBOARD_HEIGHT):
        for x in range(KEYBOARD_WIDTH):
            if (x, y) in led_mapping:
                pixel_color = get_screen_pixel(x * key_width, y * key_height, screen)
                led_colors.append(CorsairLedColor(id=led_mapping[(x, y)], r=pixel_color[0], g=pixel_color[1], b=pixel_color[2], a=255))

    if led_colors:
        sdk.set_led_colors(device_id, led_colors)

if __name__ == "__main__":
    main()
