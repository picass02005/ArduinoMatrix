import time

from Modules import animation
from Modules.arduino import Arduino
from Modules.scrollCalculator import calcul_scroll_rtl
from Modules.text_to_matrix import Font

arduino = Arduino()
arduino.start()

time.sleep(2)

font = Font()

extended_matrix = font.text_to_matrix("TEST")
frames = calcul_scroll_rtl(extended_matrix, True, True)

anim = animation.Animation(arduino)
anim.setup(frames, 0.05)
anim.set_run_once(True)

anim.daemon = False
anim.start()
