import gc
import json
import time
from threading import Thread
from typing import Union

import serial
from serial import Serial

from Modules.logs import Logs


class Arduino(Thread):
    """
    Thread used to manage arduino's bluetooth connection

    Detect if not connected
    """

    def __init__(self) -> None:
        Thread.__init__(self)
        self.daemon = True

        with open("config.json", "r") as f:
            config = json.loads(f.read())

        self.port = config['port']
        self.baud_rate = config['baud_rate']
        self.timeout = config['timeout']
        self.check_time = config['check_time']
        self.connection_timeout = config['connection_timeout']

        self.serial = Serial(baudrate=self.baud_rate, timeout=self.timeout)
        self.serial.setPort(self.port)
        self.is_connected = False
        self.autoconnect = True

        self.awaiting_response = False

    def run(self) -> None:
        """
        Thread used to verify connection
        :return: None
        """

        while True:
            try:
                if self.autoconnect and not self.is_connected:
                    if self.connect():
                        time.sleep(self.connection_timeout)

                if self.is_connected:
                    self.__send_packet("P        ", 3)

                time.sleep(self.check_time)

            except Exception as err:
                Logs.error(f"{type(err)}: {err}")

    def connect(self) -> bool:
        """
        Connect the arduino over serial
        :return: A bool indicating if connection was successfully established
        """

        try:
            self.serial.open()
            self.is_connected = True
            Logs.info("Connected")
            return True

        except serial.serialutil.SerialException:
            return False

    def disconnect(self) -> None:
        """
        Disconnect the serial
        :return: None
        """

        self.is_connected = False
        Logs.info("Disconnected")
        self.serial.close()

    def __send_packet(
            self,
            packet: Union[str, bytes],
            recv_len: int,
            recv_decode: bool = True
    ) -> Union[str, bytes, None]:

        """
        Send a packet to the arduino
        :param packet: The packet to send
        :param recv_len: The received packet length
        :return: None if sending failed, else the received packet
        """

        if type(packet) == str:
            packet = packet.encode()

        while self.awaiting_response:
            time.sleep(0.1)

        self.awaiting_response = True

        try:
            Logs.info(f"Sending packet: {packet}")
            self.serial.write(packet)
            recv = self.serial.read(recv_len)

            Logs.info(f"Receiving packet: " + str(recv.replace(b'\r\n', b'\\r\\n')))

            if recv_decode:
                recv = recv.decode()

            self.awaiting_response = False
            gc.collect()

            return recv

        except serial.serialutil.SerialException:
            self.disconnect()

        except TypeError:
            self.is_connected = False

        self.awaiting_response = False
        gc.collect()

    def send_matrix_bytes(self, raw_bytes: bytes) -> bool:
        """
        :param raw_bytes: Raw bytes or bytearray representing leds to light
        :return: Success status
        """

        recv = self.__send_packet(b"S" + raw_bytes, 1)

        r_data = int(raw_bytes.hex(), 16)

        checksum = "UNKNOWN"
        checksum_local = checksum

        try:
            if (checksum := ord(recv)) == (checksum_local := r_data.bit_count()):
                Logs.info(f"Successfully lighted {checksum} leds")

                return True

        except TypeError:
            pass

        Logs.error(f"An error occurred while setting {checksum_local} leds lighted: lighted {checksum} leds instead")

        return False

    def get_matrix_bytes(self) -> bytes:
        """
        :return: Bytearray containing currently lighted leds
        """

        return self.__send_packet(b"G        ", 8, recv_decode=False)
