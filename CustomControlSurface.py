from functools import partial
import traceback, Live

from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE, MIDI_PB_TYPE, MIDI_NOTE_TYPE, MIDI_SYSEX_TYPE, MIDI_PB_STATUS

class CustomControlSurface(ControlSurface):
    pass
    '''def _install_forwarding(self, midi_map_handle, control):
        assert self._in_build_midi_map
        assert control != None
        assert isinstance(control, InputControlElement)
        success = False
        if control.message_type() is MIDI_NOTE_TYPE:
            success = Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier())
        else:
            if control.message_type() is MIDI_CC_TYPE:
                success = Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier())
            else:
                if control.message_type() is MIDI_PB_TYPE:
                    success = Live.MidiMap.forward_midi_pitchbend(self._c_instance.handle(), midi_map_handle, control.message_channel())
                else:
                    assert control.message_type() == MIDI_SYSEX_TYPE
                    success = True
        if success:
            forwarding_keys = control.identifier_bytes()
            for key in forwarding_keys:
                if control.message_type() != MIDI_SYSEX_TYPE:
                    registry = self._forwarding_registry if 1 else self._forwarding_long_identifier_registry
                    if key in registry.keys():
                        assert key not in registry.keys(), 'Registry key %s registered twice. Check Midi messages!' % str(key)
                    registry[key] = control

        return success'''

class CustomOptimizedControlSurface(CustomControlSurface):
    pass