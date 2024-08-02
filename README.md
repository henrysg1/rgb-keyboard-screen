# Corsair RGB Keyboard Screen Mirror

This Python application applies visual effects to Corsair RGB keyboards by mapping screen pixels to keyboard LEDs. It has been written initially for a Corsair Strafe RGB keyboard (UK Layout), but it can be modified to support other Corsair RGB keyboards.

## Features

- Maps screen pixels to keyboard LEDs in real-time, using a grid layout.
- Supports customisation for different keyboard layouts.
- Utilises the Corsair iCUE SDK for controlling the RGB LEDs.

## Requirements

- Python 3.6+
- Corsair iCUE software
- Corsair RGB keyboard (initially designed for Corsair Strafe RGB)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/henrysg1/rgb-keyboard-screen.git
   cd corsair-rgb-keyboard-effects
   ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure you have the Corsair iCUE software installed and running. You may need to enable the iCUE SDK setting for this to work, if you have not already. To do this, open the application, then go to:

    ```bash
    Settings -> SDK -> iCUE SDK (Make sure the slider is enabled)
    ```

## How to Run

Assuming the keyboard is already connected, run the application using:

```bash
python corsair_rgb/main.py
```

## Configuration
### Keyboard Layout

The application has been initially configured for a Corsair Strafe RGB keyboard with a 6-row by 21-column layout. If you have a different keyboard model, you need to modify the corsair_rgb/config.py file to match your keyboard's layout.

### Example Configuration

For a different keyboard, such as the Corsair K95 RGB Platinum, update the KEYBOARD_WIDTH and KEYBOARD_HEIGHT constants and the precompute_led_mapping function to reflect the key positions and LED IDs for your specific model. For example:

```python
# config.py
KEYBOARD_WIDTH = 22
KEYBOARD_HEIGHT = 6

def precompute_led_mapping():
    key_to_led_id = {
        # Update this dictionary with the LED IDs for your keyboard
        (0, 0): CorsairLedId_Keyboard.CLK_Escape,
        # Add the remaining key mappings...
    }
    return key_to_led_id
```

### Using the Corsair iCUE SDK

This application uses the Corsair iCUE SDK to interact with the keyboard. The SDK provides functions to control the lighting of Corsair devices. For more details on the SDK, refer to the [Corsair iCUE SDK documentation](https://github.com/CorsairOfficial/cue-sdk-python/tree/master).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. It would be beneficial if users with different keyboard layouts could add their configurations, to make the tool available to a wider audience!

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/henrysg1/rgb-keyboard-screen/blob/main/LICENSE) file for details.

