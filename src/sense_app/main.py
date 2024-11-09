"""Main entry point"""

import time
import os
from asyncio import Event, run_coroutine_threadsafe, new_event_loop
from threading import Thread

from sense_hat import SenseHat  # pylint: disable=import-error
from common import get_sensor_data, pattern_gen, set_pixels  # pylint: disable=import-error


# pylint: disable=global-statement
ASYNC_EVENT = None
CURRENT_LOOP = None
RUNNING_THREAD = None


def temps():
    """Entry point for displaying a nice coloured graphic on the sense screen,
    depending on the temperature values fetched from a remote temp sensor
    (specified in common/config.json).
    """
    temp_boundaries = {
        "DEATH": [38, 99],
        "RED": [30, 38],  # we should never get above here...
        "ORANGE": [26, 30],
        "GREEN": [19, 26],
        "BLUE": [5, 19]
    }

    pattern_generator = pattern_gen.ConstrainedRandPatternGen()

    temp_sensor = None
    while True: # We never stop this train
        # Moved the hat object into here so we regularly re-create it.
        # Hoping this will help the stability of long running instances of the sense hat flashy
        # flashy.
        hat = SenseHat()
        screen_colour = "DEATH"  # Assume death

        try:
            if not temp_sensor:
                temp_sensor = get_sensor_data.get_sensor()
                print(f"temp sensor: {temp_sensor}")

            sensor_temp = get_sensor_data.get_sensor_temp(temp_sensor)
            for _key, _val in temp_boundaries.items():
                if _val[0] <= int(sensor_temp) < _val[1]:
                    screen_colour = _key
                    break
            else:
                print(
                    f"Temp value: {sensor_temp} is not in any boundary: {temp_boundaries.keys()}. "
                    "Setting to death!"
                )

        except get_sensor_data.SensorConnectionFailure:
            print(f"Failed to connect to sensor: {temp_sensor} (with retires).")

        try:
            for _ in range(60):
                hat.set_pixels(
                    pattern_generator.gen_single_colour(getattr(pattern_generator, screen_colour))
                )
                time.sleep(1)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Making this a broad except as I have noticed the screen hanging on a pattern.
            print(f"Execption thrown setting pixels: {repr(exc)}.")


def creeper_face():
    """Sets a creeper face on the display"""
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "common", "example_patterns", "creeper.json"
    )
    set_pixels.SetPatternFromJsonFile(file_path).set()


def gen_random_pattern():
    """Sets a random pattern on the display"""
    pattern_generator = pattern_gen.ConstrainedRandPatternGen()
    set_pixels.SetPattern(pattern_generator.gen()).set()


def clear_display():
    """Clears the display"""
    set_pixels.RawSenseHat().clear()


def enable_low_light():
    """Sets the display to low light mode"""
    set_pixels.RawSenseHat().enable_low_light()


def disable_low_light():
    """Sets the display back to normal lighting"""
    set_pixels.RawSenseHat().disable_low_light()


def stop_rotation():
    """Stops rotating the display"""
    global ASYNC_EVENT
    global CURRENT_LOOP
    global RUNNING_THREAD
    if isinstance(ASYNC_EVENT, Event):
        ASYNC_EVENT.set()
        print("Waiting 5 seconds for clean up")
        time.sleep(5)
    ASYNC_EVENT = None
    if CURRENT_LOOP and RUNNING_THREAD:
        CURRENT_LOOP.call_soon_threadsafe(CURRENT_LOOP.stop)
        RUNNING_THREAD.join()
        CURRENT_LOOP = None
        RUNNING_THREAD = None


def rotate_display():
    """Rotates the display"""
    stop_rotation()  # Just in case we already have something rotating the display
    global ASYNC_EVENT
    global CURRENT_LOOP
    global RUNNING_THREAD
    ASYNC_EVENT = Event()
    display = set_pixels.RawSenseHat()
    CURRENT_LOOP = new_event_loop()
    RUNNING_THREAD = Thread(target=CURRENT_LOOP.run_forever)
    RUNNING_THREAD.start()
    run_coroutine_threadsafe(display.rotater(ASYNC_EVENT), CURRENT_LOOP)
