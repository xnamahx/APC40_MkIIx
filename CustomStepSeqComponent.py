from itertools import imap, chain, starmap, izip, ifilter
from _Framework.Util import first
from _Framework.ClipCreator import ClipCreator
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Layer import Layer
from _Framework.SlideComponent import SlideComponent
from .StepSeqComponent import StepSeqComponent
from .StepSeqComponent import DrumGroupFinderComponent
#from _PushLegacy.StepSeqComponent import DrumGroupFinderComponent
#from pushbase.step_seq_component import StepSeqComponent
from .SkinDefault import make_default_skin
#from .CustomSkinDefault import make_default_skin
#from _Framework.SlideComponent import Slideable, SlideComponent


from NoteSettings import NoteEditorSettingsComponent 
from .APCDrumGroupComponent import APCDrumGroupComponent
from APCMessenger import APCMessenger
from MatrixMaps import PAD_FEEDBACK_CHANNEL
from APCNoteEditorComponent import APCNoteEditorComponent


#from _PushLegacy.LoopSelectorComponent import LoopSelectorComponent

#from functools import partial
#from _Framework import Task
#from _Framework import Defaults
from _Framework.Control import ButtonControl

class StepSeqComponent(StepSeqComponent, APCMessenger):
  """ Step sequencer for APC40 MkII """

  next_page_button = ButtonControl()                               # lew 
 

  def __init__(self, *a, **k):
    super(StepSeqComponent, self).__init__(
        clip_creator = ClipCreator(),
        note_editor_settings = self._note_editor_setting(),
        is_enabled = False,
        skin = make_default_skin(),
        *a, **k)

#    self._grid_resolution = grid_resolution      # added 10/17
#    self._slider = self.register_component(SlideComponent(self))

    self._drum_group.__class__ = APCDrumGroupComponent
    self._note_editor.__class__ = APCNoteEditorComponent
    self._setup_drum_group_finder()
    self._configure_playhead()
   
   
   #lew onwards for next page button
   
#    self._is_following = False
#    self._follow_task = self._tasks.add(Task.sequence(Task.wait(Defaults.MOMENTARY_DELAY), Task.run(partial(self._set_is_following, True))))
#    self._follow_task.kill()
  
  
  
  
#  def _get_is_following(self):
#      return self._can_follow and self._is_following  
  
  
#  def _set_is_following(self, value):
#      self._is_following = value
#      self.notify_is_following(value)
  
#  is_following = property(_get_is_following, _set_is_following)  
  
 
 
 
  # back to orig
 
  def _note_editor_setting(self):
    return NoteEditorSettingsComponent(self.control_surface._grid_resolution,
        Layer(initial_encoders = self.control_surface._mixer_encoders),
        Layer(encoders = self.control_surface._mixer_encoders))

  def set_velocity_slider(self, button_slider):
    self._note_editor.set_velocity_slider(button_slider)

  def _configure_playhead(self):
    self._playhead_component._notes=tuple(chain(*starmap(range, (
         (28, 32),
         (20, 24),
         (12, 16),
         (4, 8)))))
    self._playhead_component._triplet_notes=tuple(chain(*starmap(range, (
         (28, 31),
         (20, 23),
         (12, 15),
         (4, 7)))))

  def _setup_drum_group_finder(self):
    self._drum_group_finder = DrumGroupFinderComponent()
    self._on_drum_group_changed.subject = self._drum_group_finder
    self._drum_group_finder.update()


  
  @subject_slot('drum_group')
  def _on_drum_group_changed(self):
    self.set_device(self._drum_group_finder)
  
  
  
  def on_selected_track_changed(self):
    self.set_device(self._drum_group_finder)

  def set_button_matrix(self, matrix):
    """ This method, as with most set_* methods, is called every time
    This component is enabled """
    self._note_editor_matrix = matrix
    if matrix:
      for button, _ in ifilter(first, matrix.iterbuttons()):
        button.set_channel(PAD_FEEDBACK_CHANNEL)

    self._update_note_editor_matrix()
    self._note_editor.set_enabled(True)
    self._big_loop_selector.set_loop_selector_matrix(self._note_editor_matrix)
    self._note_editor.set_button_matrix(self._note_editor_matrix)

  def set_loop_selector_matrix(self, matrix):
    self._loop_selector.set_loop_selector_matrix(matrix)
    if matrix:
      for button, _ in ifilter(first, matrix.iterbuttons()):
        button.set_channel(PAD_FEEDBACK_CHANNEL)


  """lew adding note matrix   15/10/17 will see"""

#  def set_note_matrix(self, matrix):
 #   self._note_selector.set_matrix()
#    if matrix:
#      for button, _ in ifilter(first, matrix.iterbuttons()):
 #       button.set_channel(PAD_FEEDBACK_CHANNEL)

  def set_octave_down_button(self, button):
    pass
    #self._note_selector.set_octave_down_button(button)
    #self._slider.set_scroll_page_down_button(button)


  def set_octave_up_button(self, button):
    pass
    #self._note_selector.set_octave_up_button(button)
    #self._slider.set_scroll_page_up_button(button)


  def set_scale_down_button(self, button):
      pass
  #  self._note_selector._slider.set_octave_down_button(button)


  def set_scale_up_button(self, button):
      pass
  #  self._note_selector.set_scale_up_button(button)


  #def set_octave_down_button(self, button):
  #  pass
   #     self._slider.set_scroll_page_down_button(button)

  #def set_octave_up_button(self, button):
  #  pass
   #     self._slider.set_scroll_page_down_button(button)



 #lew
  
#  def _get_size(self):
#    return max(len(self._loop_selector_matrix or []), len(self._short_loop_selector_matrix or []), 1) 
  
#  def _selected_pages_range(self):
#    size = self._get_size()
#    page_length = self._page_length_in_beats
#    seq_page_length = max(self._paginator.page_length / page_length, 1)
#    seq_page_start = int(self._paginator.page_index * self._paginator.page_length / page_length)
#    seq_page_end = int(min(seq_page_start + seq_page_length, self.page_offset + size))
#    return (seq_page_start, seq_page_end) 
 
 
 
 
 
 
 
 
 
 
#  @property
#  def _can_follow(self):
#      return True 
 
 
 
 
 
#  @next_page_button.pressed
#  def next_page_button(self, button):
#    if self.is_following:
#        self.is_following = False
#    else:
#        _, end = self._selected_pages_range()
#        self._jump_to_page(end)
#        self._follow_task.restart()
      
#  @next_page_button.released
#  def next_page_button(self, button):
#      self._follow_task.kill()  
  
  
  
  
#  def set_next_page_button(self, button):
#      self.next_page_button.set_control_element(button)


