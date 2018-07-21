from __future__ import with_statement
import Live
from _Framework.Control import RadioButtonControl, control_list
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from contextlib import contextmanager
from _Framework.ButtonElement import ButtonElement
from ableton.v2.control_surface.control import ButtonControl, EncoderControl, ToggleButtonControl


#from _NKFW.VisualMetroComponent import VisualMetroComponent
#from _Framework.ModeSelectorComponent import ModeSelectorComponent
PSC_NUM_STRIPS = 8






class LooperComponent(ControlSurfaceComponent):
  """ Allows DJ-style looping of the currently selected clip """
  loop_buttons = control_list(RadioButtonControl)
  capture_midi_button = ButtonControl()
  
  
  
  def __init__(self, *a, **k):
    super(LooperComponent, self).__init__(*a, **k)
    
 
    
     
    
 #   self.control_surface = control_surface
    self._loop_length = 16
    self._loop_start = 0
    
    self._shift_button = None
    self._shift_pressed = False
   # self._session = session
  #  self._width = 8#self._session.width()
 #   enable_skinning and self._enable_skinning()
    

 
  
  
  
  
  
  def set_shift_button(self, button):
      assert ((button == None) or (isinstance(button, ButtonElement) and button.is_momentary()))
      if (self._shift_button != button):
        if (self._shift_button != None):
          self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = button
        if (self._shift_button != None):
          self._shift_button.add_value_listener(self._shift_value)
        self.update()  
 

  
  def _enable_skinning(self):
   #   self.set_stopped_value('Zooming.Stopped')
    #  self.set_selected_value('Zooming.Selected')
      self.set_looping_value('clip.looping')           # testing testing
   #   self.set_empty_value('Zooming.Empty')  
  
  
  def _shift_value(self, value):
      assert (self._shift_button != None)
      assert (value in range(128))
      self._shift_pressed = (value != 0)
      self.update()    
    
  
  def set_looping_value(self, value):
      self._playing_value = value  
  
  # PROPERTIES
  @property
  def clip(self):
    clip = self.song().view.detail_clip
    return clip if clip and clip.is_audio_clip else None
  
  @property
  def start(self):
    return self.clip.loop_start
  @property
  def end(self):
    return self.clip.loop_end
  @property
  def length(self):
    return self.clip.length
  @property
  def rounded_playing_position(self):
    """ rounded to the nearest beat """
    return round(self.clip.playing_position)

  # SETTERS
  
  
 
  

  

  def set_loop_buttons(self, start_button):
          if self._shift_pressed: 
            assert ((start_button == None) or isinstance(start_button, ButtonElement))
            assert ((toggle_button == None) or isinstance(toggle_button, ButtonElement))
            if (self._start_button != None):
                self._start_button.remove_value_listener(self._start_value)
            self._start_button = start_button
            if (self._start_button != None):
                self._start_button.add_value_listener(self._start_value)     
           
            if (self._toggle_button != None):
                self._toggle_button.remove_value_listener(self._toggle_value)
            self._toggle_button = toggle_button
            if (self._toggle_button != None):
                self._toggle_button.add_value_listener(self._toggle_value)         
       
       
 
       
       
       
       
       
        #  self.update()
     
#      assert ((buttons == None) or (isinstance(buttons, tuple))) #and (len(buttons) == self._width))) #height)))
#      if (self._loop_buttons != buttons):
#          if (self._loop_buttons  != None):
#            for button in self._loop_buttons :
#              button.remove_value_listener(self._loop_button_value)
#          self._loop_buttons = buttons
#          if (self._loop_buttons  != None):
#            for button in self._loop_buttons :
#              assert isinstance(button, ButtonElement)
#              button.add_value_listener(self._loop_button_value, identify_sender=True)      
  
  
  
  
  
  def set_toggle_button(self, button):
    self._toggle_button = button
    self._on_clip_looping_value.subject = button

  
  def set_capture_button(self, button):
 #   self._capture_button = button
    self._on_capture.subject = button  
  
  
  
  
  def set_start_button(self, button):
    self._set_start.subject = button

  def set_halve_button(self, button):
    self._on_halve.subject = button 

  def set_double_button(self, button):
    self._on_double.subject = button 

  def set_left1_button(self, button):         #lewp
    self._on_left.subject = button

  def set_right1_button(self, button):        #lewp
    self._on_right.subject = button

  def set_nudge_left_button(self, button):
    self._nudge_left.subject = button

  def set_nudge_right_button(self, button):
    self._nudge_right.subject = button

  # EVENTS
  @subject_slot('value')
  def _on_clip_looping_value(self, value):
    if self.clip and value > 0:
      self.clip.looping = not self.clip.looping

  @subject_slot('value')
  def _set_start(self, value):
    if self.clip and value > 0:
      with self.hold_loop():
        self.set_loop(self.rounded_playing_position, 
            self.rounded_playing_position + 16)
      self.clip.looping = True

  @subject_slot('value')
  def _on_left(self, value): 
    """ Move left by loop length """ 
    if self.clip and value > 0:
      with self.hold_loop():
        self.move(-self.length)

  @subject_slot('value')
  def _on_right(self, value): 
    """ Move right by loop length """ 
    if self.clip and value > 0:
      with self.hold_loop():
        self.move(self.length)

  @subject_slot('value')
  def _on_halve(self, value): 
    if self.clip and value > 0:
      with self.hold_loop():
        self.set_loop(self.start, self.start + (self.length / 2))

  @subject_slot('value')
  def _on_double(self, value):
    if self.clip and value > 0:
      with self.hold_loop():
        self.set_loop(self.start, self.start + (self.length * 2))

  @subject_slot('value')
  def _nudge_left(self, value):
    """ Nudge left a bar """
    if self.clip and value > 0:
      with self.hold_loop():
        self.move(-4)

  @subject_slot('value')
  def _nudge_right(self, value):
    """ Nudge right a bar """
    if self.clip and value > 0:
      with self.hold_loop():
        self.move(4)
  

  
  @capture_midi_button.pressed
  def _on_capture(self, button):
    try:
      self.song.capture_midi()
#      self.set_trigger_recording_on_release(not any((self._record_button.is_pressed, self.arrangement_record_button.is_pressed)))
    except RuntimeError:
      pass  
  
  
  
  
  
  
  def move(self, amount):
    """ Move start and end points by amount. Can be negative """
    self.set_loop(self.start + amount, self.end + amount)

  def set_loop(self, start, end):
    """ 
    Set start and end points to fixed values 
    Will calculate correct order to make changes, e.g.
    If new start value >= current end value
    """
    if start >= self.end: 
      self.clip.loop_end = end
      self.clip.loop_start = start
    else:
      self.clip.loop_start = start
      self.clip.loop_end = end

  @contextmanager
  def hold_loop(self, loop = True):
    """ 
    Some properties are only available when looping or not looping
    So we hold loop on/off to access these properties
    """
    was_looping = self.clip.looping # Remember whether we were looping
    self.clip.looping = loop
    yield
    self.clip.looping = was_looping
