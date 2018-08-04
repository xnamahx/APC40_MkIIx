import sys
from itertools import chain, imap, ifilter
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from .NoteEditorComponent import NoteEditorComponent, most_significant_note
from .APCMessenger import APCMessenger

def color_for_note(note):
  velocity = note[3]
  muted = note[4]
  if not muted:
    if velocity == 127:
      return 'Full'
    elif velocity >= 94:
      return 'High'
    elif velocity >= 62:
      return 'Medium'
    elif velocity >= 31:
      return "Low"
    else:
      return 'Empty'
  else:
    return 'Muted'

class APCNoteEditorComponent(NoteEditorComponent, APCMessenger):
  """ Customized to have a ButtonSlider for adjustable velocity 
  And add colors to note velocity display
  """

  _velocity = 100

  def _add_note_in_step(self, step, modify_existing = True):
    """
    Add note in given step if there are none in there, otherwise
    select the step for potential deletion or modification

    Overriden to use self.velocity
    """
    if self._sequencer_clip != None:
      x, y = step
      time = self._get_step_start_time(x, y)
      notes = self._time_step(time).filter_notes(self._clip_notes)
      if notes:
        if modify_existing:
          most_significant_velocity = most_significant_note(notes)[3]
          if self._mute_button and self._mute_button.is_pressed() or most_significant_velocity != 127 and self.full_velocity:
            self._trigger_modification(step, immediate=True)
      else:
        pitch = self._note_index
        mute = self._mute_button and self._mute_button.is_pressed()
        velocity = 127 if self.full_velocity else self._velocity
        note = (pitch,
         time,
         self._get_step_length(),
         velocity,
         mute)
        self._sequencer_clip.set_notes((note,))
        self._sequencer_clip.deselect_all_notes()
        self._trigger_modification(step, done=True)
        return True
    return False


  def _update_editor_matrix(self):
    """
    update offline array of button LED values, based on note
    velocity and mute states
    """
    step_colors = ['NoteEditor.StepDisabled'] * self._get_step_count()
    width = self._width
    coords_to_index = lambda (x, y): x + y * width
    editing_indices = set(map(coords_to_index, self._modified_steps))
    selected_indices = set(map(coords_to_index, self._pressed_steps))
    last_editing_notes = []
    for time_step, index in self._visible_steps():
      notes = time_step.filter_notes(self._clip_notes)
      if len(notes) > 0:
        last_editing_notes = []
        if index in selected_indices:
          color = 'NoteEditor.StepSelected'
        elif index in editing_indices:
          note_color = color_for_note(most_significant_note(notes))
          color = 'NoteEditor.StepEditing.' + note_color
          last_editing_notes = notes
        else:
          note_color = color_for_note(most_significant_note(notes))
          color = 'NoteEditor.Step.' + note_color
      elif any(imap(time_step.overlaps_note, last_editing_notes)):
        color = 'NoteEditor.StepEditing.' + note_color
      elif index in editing_indices or index in selected_indices:
        color = 'NoteEditor.StepSelected'
        last_editing_notes = []
      else:
        color = self.background_color
        last_editing_notes = []
      step_colors[index] = color

    self._step_colors = step_colors
    self._update_editor_matrix_leds()

  def _visible_steps(self):
    """ Patched to support four-wide """
    first_time = self.page_length * self._page_index
    steps_per_page = self._get_step_count()
    step_length = self._get_step_length()
    indices = range(steps_per_page)
    if self._is_triplet_quantization():
      indices = filter(lambda k: k % 4 != 3, indices)
    return [ (self._time_step(first_time + k * step_length), index) for k, index in enumerate(indices) ]

  def on_selected_track_changed(self):
    if self.song().view.selected_track.has_midi_input:
      self.set_enabled(True)
      self.update()
    else:
      self.set_enabled(False)

  def set_velocity_slider(self, button_slider):
    if not hasattr(self, '_velocity'):
      self._velocity = 100
    self._velocity_slider = button_slider
    self._on_velocity_changed.subject = button_slider
    self._update_velocity_slider()

  def _update_velocity_slider(self):
    if hasattr(self, "_velocity_slider") and self._velocity_slider:
      self._velocity_slider.send_value(self._velocity, force_send = True)
  
  @subject_slot("value")
  def _on_velocity_changed(self, value):
    self._velocity = value
    self._update_velocity_slider()

  def update(self):
    super(NoteEditorComponent, self).update()
    self._update_velocity_slider()
