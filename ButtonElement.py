from _Framework.ButtonElement import ButtonElement
from _Framework.Skin import SkinColorMissingError

class ButtonElement(ButtonElement):
  """ Extended ButtonElement that exposes the correct API for
  Various Push-specific tools """
  _skin_name = None

  def set_on_off_values(self, on_value, off_value):
    """ We don't actually care, but the script does want to set these.
    If the button doesn't support 'em, no change is necessary """
    pass

  def set_light(self, value):
    self._set_skin_light(value)

