from _Framework.ButtonElement import ButtonElement
from .ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.Skin import Skin, SkinColorMissingError
from .Colors import Rgb

class ColorButtonElement(ConfigurableButtonElement):
  """ Same as Push's but doesn't change channels """
  _skin_name = None

  class Colors:
    class DefaultButton:
      On = Rgb.GREEN
      Off = Rgb.BLACK
      Disabled = Rgb.BLACK
      Alert = Rgb.RED
  default_skin = Skin(Colors)
  default_states = {True: 'DefaultButton.On',
   False: 'DefaultButton.Off'}

  def __init__(self, is_momentary, msg_type, channel, identifier, skin = None, is_rgb = False, default_states = None, *a, **k):
    super(ConfigurableButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin=(skin or self.default_skin), *a, **k)
    if default_states is not None:
      self.default_states = default_states
    self.states = dict(self.default_states)
    self.is_rgb = is_rgb
    self._force_next_value = False
