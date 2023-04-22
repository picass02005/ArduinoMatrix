import time

from Modules.arduino import Arduino
from Modules.converters import int_to_bytes


class BinaryClock:
    def __init__(self) -> None:
        self.arduino = Arduino()
        self.arduino.start()

        time.sleep(2)

    def run(self) -> None:
        """
        :return: None
        """

        while True:
            self.arduino.send_matrix_bytes(int_to_bytes(int(time.time())))

            time.sleep(1)
