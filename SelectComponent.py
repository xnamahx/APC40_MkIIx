import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent 


class SelectComponent(ModeSelectorComponent):
    """ SelectorComponent that assigns buttons to functions based on the shift button """
    
    
    def __init__(self, raw_select_buttons, mode_callback, tap_tempo_button, transport, looper, session, session_matrix, session_record_button):
        
 
        ModeSelectorComponent.__init__(self)
        self._toggle_pressed = False  
        self._invert_assignment = False
 
        self._session = session
        self._mode_callback = mode_callback
        self._select_buttons = raw_select_buttons
        
        self._session_record_button = session_record_button
        self._session_matrix = session_matrix

        self._metronome_button = None
        self._nudge_down_button = None
        self._nudge_up_button = None
       
        #self._metronome_button = metronome_button
        #self._nudge_down_button = nudge_down_button
        #self._nudge_up_button = nudge_up_button
        self._tap_tempo_button = tap_tempo_button
        self._transport = transport
        
        self._looper = looper
    
    
    def disconnect(self):
        ModeSelectorComponent.disconnect(self)        
   
        self._session = None 
        self._select_buttons = None
  
        self._metronome_button = None
       
        
        self._session_record_button = None
        self._nudge_down_button = None
        self._nudge_up_button = None
        self._tap_tempo_button = None
        self._transport = None
        
        
        
        self._looper = None
    
    
    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)     
        
        
        
    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()
        
    def number_of_modes(self):
        return 2
        
    def update(self):
        if self.is_enabled():
            if self._mode_index == 0: #shift/modifier released #int(self._invert_assignment):    
                
                    
                self._session.set_clip_launch_buttons(self._session_matrix)
                
                
                for scene_index in range(5):
                    scene = self._session.scene(scene_index)                                              # clip launch
                    scene.name = 'Scene_' + str(scene_index)
                    button_row = []
               #     scene.set_launch_button(self._scene_launch_buttons[scene_index])                
                    for track_index in range(8):                
                        button = self._session_matrix.get_button(track_index, scene_index)
       #                 button.use_default_message()
                        clip_slot = scene.clip_slot(track_index)
                        clip_slot.set_launch_button(button)
                        clip_slot.set_select_button(None)
                        clip_slot.set_delete_button(None)
                        clip_slot.set_duplicate_button(None)
              #          button.set_enabled(True)                        
                
                
                
                
                
                
                
                self._transport.set_metronome_button(self._metronome_button) 
                self._transport.set_tap_tempo_button(self._tap_tempo_button) 
                self._transport.set_nudge_down_button(self._nudge_down_button)
                self._transport.set_nudge_up_button(self._nudge_up_button)
                
                
                
                self._looper.set_toggle_button(None)           # shiftable looper
                self._looper.set_start_button(None)      
                self._looper.set_halve_button(None)
                self._looper.set_double_button (None)             
                self._looper.set_capture_button (None) 
           
            
            
            
            else: #if shift/modifier pressed
                
    #            self._session.set_clip_launch_buttons(None)
                
                
                for scene_index in range(5):
                    scene = self._session.scene(scene_index)                                             #(clip select)
                    scene.name = 'Scene_' + str(scene_index)
                    button_row = []
              #      scene.set_launch_button(None)                         
                    for track_index in range(8):                
                        button = self._session_matrix.get_button(track_index, scene_index)
             #           button.use_default_message()
                        clip_slot = scene.clip_slot(track_index)
                        clip_slot.set_select_button(button)
                        clip_slot.set_delete_button(None)
                        clip_slot.set_duplicate_button(None)
              #          button.set_enabled(True)                           
               
               
               
               
               
               
               
               
                self._transport.set_metronome_button(None)
                self._transport.set_tap_tempo_button(None) 
                self._transport.set_nudge_down_button(None) 
                self._transport.set_nudge_up_button(None)    
                
                
                self._looper.set_toggle_button(self._metronome_button)     # turn looper on when shift pressed
                self._looper.set_start_button(self._tap_tempo_button)
                self._looper.set_halve_button(self._nudge_down_button)
                self._looper.set_double_button(self._nudge_up_button)                
                self._looper.set_capture_button(self._session_record_button) 
    
    
    
    def _toggle_value(self, value):
        assert self._mode_toggle != None
        assert value in range(128)
        self._toggle_pressed = value > 0
        self._recalculate_mode()
        if value < 1 and self._mode_index > 1: #refresh on Shift button release, and if previous mode was Note Mode
            self._parent.schedule_message(2, self._partial_refresh, value)
    
    def _recalculate_mode(self):
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())    