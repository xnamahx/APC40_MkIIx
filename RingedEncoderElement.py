from _APC.RingedEncoderElement import RingedEncoderElement
from _Framework.EncoderElement import TouchEncoderElementBase
from .APCMessenger import APCMessenger

class RingedEncoderElement(RingedEncoderElement, TouchEncoderElementBase, APCMessenger):
  """ Modified to provide pseudo-relative encoder behaviour """
  def __init__(self, *a, **k):
    self._prev_value = -1
    super(RingedEncoderElement, self).__init__(*a, **k)

  def is_pressed(self):
    """ We're only pretending to be a touch encoder to keep Push happy"""
    return False

  def _update_ring_mode(self):
    """ Don't update if being used as pseudo-relative """
    if self.normalized_value_listener_count():
      return
    else:
      super(RingedEncoderElement, self)._update_ring_mode()

  def normalize_value(self, value):
    """ This is not actually a relative value, but we'll fake it """
    delta = 0 
    if value == 127 or value > self._prev_value:
      delta = 0.01 
    elif value == 0 or value < self._prev_value:
      delta = -0.01 
    self._prev_value = value
    return delta
