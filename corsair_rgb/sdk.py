# This file contains the code to connect to the Corsair iCUE software and retrieve the device ID and LED positions for the first connected device.

import time

from cuesdk import CueSdk, CorsairDeviceFilter, CorsairDeviceType, CorsairError
from corsair_rgb.config import MAX_RETRIES

# Create an instance of the Corsair SDK
cue_sdk = CueSdk()

# Callback function to handle state changes
def on_state_changed(event):
    print(event.state)

# Connect to the Corsair iCUE software and retrieve the device ID and LED positions for the first connected device
def connect_and_get_device():
    retries = 0
    while retries < MAX_RETRIES:
        # Connect to the Corsair iCUE software
        cue_sdk.connect(on_state_changed)
        print("Waiting for connection to Corsair iCUE software...")
        time.sleep(1)  # Pause for 1 second before retrying
        # Get the session details to check if the client version is non-zero
        session_details, _ = cue_sdk.get_session_details()
        if session_details.client_version.major != 0:
            print("Connected to Corsair iCUE software.")
            break
        retries += 1
    else:
        raise RuntimeError("Unable to connect to Corsair iCUE software after {} attempts.".format(MAX_RETRIES))

    # Create a device filter to retrieve all devices
    device_filter = CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_All)

    # Retrieve information about all connected devices
    devices, err = cue_sdk.get_devices(device_filter)

    if err != CorsairError.CE_Success:
        raise RuntimeError("Error retrieving devices: {}".format(err))

    # Check if any devices are found
    if not devices:
        raise RuntimeError("No devices found.")

    # Assume we are using the first device, which may need reconsidering for multiple devices
    device_id = devices[0].device_id

    # Get LED positions for the selected device
    led_positions, err = cue_sdk.get_led_positions(device_id)
    if not led_positions:
        raise RuntimeError("Failed to get LED positions: {}".format(err))
    
    return device_id, led_positions
