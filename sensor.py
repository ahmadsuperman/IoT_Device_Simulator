import random


class SensorSimulator():
    # Constructor for the SensorSimulator class. When an instance is created,
    # it initializes the temperature and humidity attributes with default values.
    def __init__(self):
        self._temperature = 20  # Set the initial temperature to 20 degrees.
        self._humidity = 50     # Set the initial humidity to 50%.

    # The read method simulates reading current sensor data.
    # This is simulated by generating random values within a defined range.
    def read(self):
        # Generate a random temperature value between 20 and 30 degrees.
        self._temperature = random.uniform(20, 30)
        # Generate a random humidity value between 40 and 70 percent.
        self._humidity = random.uniform(40, 70)
        # Return a dictionary containing the latest temperature and humidity readings.
        return {
            "temperature": self._temperature,
            "humidity": self._humidity
        }
