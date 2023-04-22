import time

from Modules.animation import Animation
from Modules.arduino import Arduino
from Modules.scrollCalculator import calcul_scroll_rtl
from Modules.text_to_matrix import Font


class DigitalClock:
    def __init__(self, format_: str = "%H:%M:%S", delay: float = 0.15) -> None:
        """
        :param format_: Date time format (look time.strftime format for more information)
        :param delay: Delay that will be passed into Modules.animation.Animation class
        """

        self.__format = format_
        self.__delay = delay

        self.arduino = Arduino()
        self.arduino.start()

        time.sleep(2)

    def run(self) -> None:
        """
        :return: None
        """

        font = Font()
        animation = Animation(self.arduino)
        animation.setup(
            frames=[bytes(8) for _ in range(8)],
            delay=self.__delay
        )

        animation.start()

        while True:
            animation.set_frames(calcul_scroll_rtl(font.text_to_matrix(time.strftime(self.__format)), True, True))

            time.sleep(1)
