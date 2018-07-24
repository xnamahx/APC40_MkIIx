from _Framework.ButtonSliderElement import ButtonSliderElement
from .Colors import Rgb

class ButtonSliderElement(ButtonSliderElement):
  """ Fixes the broken scaling code on the _Framework example
  caused by odd numbers of buttons 
  
  Also adds force_send
  """

  def send_value(self, value, force_send = False):
    if force_send or value != self._last_sent_value:
      num_buttons = len(self._buttons)
      index_to_light = 0
      index_to_light = int(round((num_buttons - 1) * float(value) / 127)) if value > 0 else 0
      for index in xrange(num_buttons):
        if index <= index_to_light:
          self._buttons[index].set_light(self._button_color(index))
        else:
          self._buttons[index].turn_off()

      self._last_sent_value = value

  def _button_color(self, index):
    return "NoteEditor.Step." + [
      "Empty",
      "Low",
      "Medium",
      "High",
      "Full"
    ][index]
