from itertools import imap, ifilter
from _Framework.Util import find_if, first

from _Framework.Control import control_matrix    # added


from _Framework.SubjectSlot import subject_slot, subject_slot_group  # added 10/17

from .PadControl import PadControl    # added


from .DrumGroupComponent import DrumGroupComponent
from .MatrixMaps import DRUM_FEEDBACK_CHANNEL
from .APCMessenger import APCMessenger


"""all this reference to Push/ DrumGroupComponent.py"""


# no errors so far 17/10/17     

class APCDrumGroupComponent(DrumGroupComponent, APCMessenger):
  """ Customized to use its own feedback channel """

  """
  Class representing a drum group pads in a matrix.
  """  
  
  matrix = control_matrix(PadControl)  # switched 10/17
  
#  drum_matrix = control_matrix(PadControl)      # added
  
  
  #switched 10/17
  def __init__(self, *a, **k):
      super(DrumGroupComponent, self).__init__(touch_slideable=self, translation_channel=DRUM_FEEDBACK_CHANNEL, dragging_enabled=True, *a, **k)

  position_count = 32
  page_length = 4
  page_offset = 1 
 
  def set_drum_group_device(self, drum_group_device):
    super(DrumGroupComponent, self).set_drum_group_device(drum_group_device)
    self._on_chains_changed.subject = self._drum_group_device
    self.notify_contents() 
 
 # untill here 10/17
 
 
 
 # def set_drum_matrix(self, matrix): 
 #   "Added from cylabs APsequencer_master/APCDrumGroupComponent "    # added to stop log error
 #   self.drum_matrix.set_control_element(matrix)
 #   for button in self.drum_matrix:
 #     button.channel = PAD_FEEDBACK_CHANNEL  
  
  
  #added temp to sort select button 
  
  
#  @drum_matrix.pressed
#  def drum_matrix(self, pad):
#      self._on_matrix_pressed(pad)

#  @drum_matrix.released
#  def drum_matrix(self, pad):
#      self._on_matrix_released(pad)  
  
  
  @matrix.pressed                                # switched 10/17
  def matrix(self, pad):
      self._on_matrix_pressed(pad)
      
  @matrix.released
  def matrix(self, pad):
      self._on_matrix_released(pad)  
  
  
  
  
  
  
  
  def set_select_button(self, button):
    self.select_button.set_control_element(button)  
  
  def set_delete_button(self, button):
    self.delete_button.set_control_element(button)  
  
  
 

  @subject_slot('chains')         # added 10/17
  def _on_chains_changed(self):
      self._update_led_feedback()
      self.notify_contents() 
 
 
  # not sure if needed   10/17
  
  def delete_pitch(self, drum_pad):
      clip = self.song().view.detail_clip
      if clip:
          loop_length = clip.loop_end - clip.loop_start
          clip.remove_notes(clip.loop_start, drum_pad.note, loop_length, 1)
      #    self.show_notification(MessageBoxText.DELETE_NOTES % drum_pad.name)   # im assuming push display for this line  10/17
 
 
 
 

  
  def _update_control_from_script(self):
    super(DrumGroupComponent, self)._update_control_from_script()
    profile = 'default' if self._takeover_drums or self._selected_pads else 'drums'
    for button in self.drum_matrix:
      button.sensitivity_profile = profile  
  
  #deleted temp ... with out this not deleted it does not detect drum rack by the looks of it and light up the correct 16 pads
  
  
 # def _update_control_from_script(self):
 #   """ Patched to use our own feedback channel """
 #   takeover_drums = self._takeover_drums or self._selected_pads
 #   profile = 'default' if takeover_drums else 'drums'
 #   if self._drum_matrix:
 #     for button, _ in ifilter(first, self._drum_matrix.iterbuttons()):
 #       button.set_channel(PAD_FEEDBACK_CHANNEL)
 #       button.set_enabled(takeover_drums)
 #       button.sensitivity_profile = profile



# del 10/17

#  def on_selected_track_changed(self):
#    if self.song().view.selected_track.has_midi_input:
#      self.set_enabled(True)
#    else:
#      self.set_enabled(False)
#    self.update()

#  def _update_drum_pad_leds(self):
#    if (not self.is_enabled()) and self._drum_matrix:
#      for button, (col, row) in ifilter(first, self._drum_matrix.iterbuttons()):
#        button.set_light('DrumGroup.PadInvisible')
#    else:
#      super(APCDrumGroupComponent, self)._update_drum_pad_leds()
