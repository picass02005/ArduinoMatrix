import time
from threading import Thread
from typing import Union, List, Dict

from Modules.arduino import Arduino
from Modules.logs import Logs


class Animation(Thread):
    def __init__(self, arduino: Arduino) -> None:
        """
        :param arduino: Current arduino object
        """

        Thread.__init__(self)
        self.daemon = True

        self._arduino = arduino

        self._frames = []
        self._current_frame = 0
        self._delay = 0.05

        self._run_once = False
        self._running = True

    def run(self) -> None:
        """
        Main thread loop
        :return: None
        """

        while self._running:
            if self._frames:
                self._arduino.send_matrix_bytes(self._frames[self._current_frame])
                self._current_frame += 1

            time.sleep(self._delay)

            if self._current_frame >= len(self._frames):
                if self._run_once:
                    self.stop()

                else:
                    self._current_frame = 0

    def setup(
            self,
            frames: List[bytes],
            delay: float,
            current_frame:
            Union[None, int] = None,
            run_once: Union[None, bool] = None
    ) -> None:
        """
        :param frames: List of 8 bytes entries representing every frames
        :param delay: Delay between 2 frames
        :param current_frame: Current frame index
        :param run_once: Set to true if you want the animation to stop after one iteration
        :return: None
        """

        self.set_frames(frames)
        self.set_delay(delay)

        if current_frame:
            self.set_current_frame(current_frame)

        if run_once:
            self.set_run_once(run_once)

    def set_frames(self, frames: List[bytes]) -> None:
        """
        :param frames: List containing 8 bytes entries representing every frames
        :return: None
        """

        for i in frames:
            if len(i) != 8:
                Logs.error(f"One frame isn't 8 bytes long: {i=}")
                return

        if len(frames) == 0:
            self._arduino.send_matrix_bytes(bytes(8))

        self._frames = frames

        if self._current_frame >= len(self._frames):
            self._current_frame = 0

    def set_current_frame(self, current_frame: int) -> None:
        """
        :param current_frame: Current frame number
        :return: None
        """

        if 0 <= current_frame < len(self._frames):
            self._current_frame = 0

        else:
            self._current_frame = current_frame

    def set_delay(self, delay: float) -> None:
        """
        :param delay: New delay between 2 frames
        :return: None
        """

        self._delay = delay

    def set_run_once(self, run_once: bool) -> None:
        """
        :param run_once: Set to true if you want the animation to stop after one iteration
        :return: None
        """

        self._run_once = run_once

        if self._run_once:
            self.daemon = False

        else:
            self.daemon = True

    def get_current_status(self) -> Dict:
        """
        :return: A dict containing frames, current_frame and delay values
        """

        return {
            'frames': self._frames,
            'current_frame': self._current_frame,
            'delay': self._delay,
            'running': self._running
        }

    def stop(self) -> None:
        """
        Stop thread
        :return: None
        """

        self._running = False
        self.set_frames([])
