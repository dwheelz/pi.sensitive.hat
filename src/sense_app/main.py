"""Main entry point"""

def temps():
    """Entry point for displaying a nice coloured graphic on the sense screen,
    depending on the temperature values fetched from a remote temp sensor
    (specified in common/config.json).
    """
    import time
    from sense_hat import SenseHat
    from common import get_sensor_data, pattern_gen

    temp_boundaries = {
        "DEATH": [35, 50],
        "RED": [30, 35],  # we should never get above here...
        "ORANGE": [26, 30],
        "GREEN": [19, 26],
        "BLUE": [5, 19]
    }

    # Get sensor and spawn pattern generator object, SenseHat object
    temp_sensor = get_sensor_data.get_sensor()
    if not temp_sensor:
        raise Exception("Unable to fetch sensor data")

    pattern_generator = pattern_gen.RandPatternGen()
    hat = SenseHat()

    while True: # We never stop this train
        screen_colour = "DEATH"  # Assume death
        try:
            sensor_temp = get_sensor_data.get_sensor_temp(temp_sensor)
            for _key, _val in temp_boundaries.items():
                if _val[0] <= int(sensor_temp) < _val[1]:
                    screen_colour = _key
                    break
            else:
                print(f"Temp value: {sensor_temp} is not in any boundary: {temp_boundaries.keys()}. Setting to death!")
        except get_sensor_data.SensorConnectionFailure:
            print(f"Failed to connect to sensor: {temp_sensor} (with retires).")

        for _ in range(60):
            hat.set_pixels(pattern_generator.gen(getattr(pattern_generator, screen_colour)))
            time.sleep(1)
