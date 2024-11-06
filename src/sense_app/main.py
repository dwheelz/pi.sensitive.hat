"""Main entry point"""

def temps():
    """Entry point for displaying a nice coloured graphic on the sense screen,
    depending on the temperature values fetched from a remote temp sensor
    (specified in common/config.json).
    """
    # pylint: disable=import-error,import-outside-toplevel
    import time
    from sense_hat import SenseHat
    from common import get_sensor_data, pattern_gen

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
                hat.set_pixels(pattern_generator.gen(getattr(pattern_generator, screen_colour)))
                time.sleep(1)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Making this a broad except as I have noticed the screen hanging on a pattern.
            print(f"Execption thrown setting pixels: {repr(exc)}.")
