import Live
from _Framework.ClipSlotComponent import *

class CustomClipSlotComponent(ClipSlotComponent):

  _copy_button = None
  _clip_slot_copy_handler = None

  @subject_slot('value')
  def _launch_button_value(self, value):
    if self.is_enabled():
      if self._select_button and self._select_button.is_pressed() and value:
        self._do_select_clip(self._clip_slot)
      elif self._clip_slot != None:
        if self._duplicate_button and self._duplicate_button.is_pressed():
          if value:
            self._do_duplicate_clip()
        elif self._copy_button and self._copy_button.is_pressed():
          if value:
            if not self._is_copying():
              self._do_start_copy_clip()
            else:
              self._do_finish_copy_clip()
        elif self._delete_button and self._delete_button.is_pressed():
          if value:
            self._do_delete_clip()
        else:
          self._do_launch_clip(value)
    return

  def _is_copying(self):
    return self._clip_slot_copy_handler.is_copying()

  def _do_start_copy_clip(self):
    if self._clip_slot and self._clip_slot.has_clip:
      try:
        self._clip_slot_copy_handler._start_copying(self._clip_slot)
      except Live.Base.LimitationError:
        pass
      except RuntimeError:
        pass

  def _do_finish_copy_clip(self):
    if self._clip_slot:
      try:
        self._clip_slot_copy_handler._finish_copying(self._clip_slot)
      except Live.Base.LimitationError:
        pass
      except RuntimeError:
        pass



  def set_delete_button(self, button):
    self._delete_button = button

  def set_paste_button(self, button):
    self._paste_button = button

  def set_copy_button(self, button, clip_slot_copy_handler):
    self._copy_button = button
    self._clip_slot_copy_handler = clip_slot_copy_handler