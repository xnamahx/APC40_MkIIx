from _Framework.ButtonElement import ButtonElement as ButtonElementBase, DummyUndoStepHandler
from _Framework.Skin import SkinColorMissingError
from _Framework.Skin import Skin
from .CustomSkinDefault import make_rgb_skin

class ButtonElement(ButtonElementBase):
  """ Extended ButtonElement that exposes the correct API for
  Various Push-specific tools """
  _skin_name = None

  def __init__(self, is_momentary, msg_type, channel, identifier, skin=Skin(), undo_step_handler=DummyUndoStepHandler(),
               *a, **k):
    super(ButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
    self._skin = make_rgb_skin()

  def set_on_off_values(self, on_value, off_value):
    """ We don't actually care, but the script does want to set these.
    If the button doesn't support 'em, no change is necessary """
    pass

  def set_light(self, value):
    self._set_skin_light(value)