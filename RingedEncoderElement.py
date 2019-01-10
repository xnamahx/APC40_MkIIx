# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_APC/RingedEncoderElement.py
# Compiled at: 2018-04-23 20:27:04
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.EncoderElement import TouchEncoderElement as EncoderElement
from _Framework.ButtonElement import ButtonElement

from .APCMessenger import APCMessenger

RING_OFF_VALUE = 0
RING_SIN_VALUE = 1
RING_VOL_VALUE = 2
RING_PAN_VALUE = 3

class RingedEncoderElement(EncoderElement, APCMessenger):
    u"""
    Class representing a continuous control on the controller enclosed with an LED ring
    """

    def __init__(self, msg_type, channel, identifier, map_mode, *a, **k):
        self._prev_value = -1
        super(RingedEncoderElement, self).__init__(msg_type, channel, identifier, map_mode, *a, **k)
        self._ring_mode_button = None
        self.set_needs_takeover(False)
        return

    def set_ring_mode_button(self, button):
        assert button == None or isinstance(button, ButtonElement)
        if self._ring_mode_button != None:
            self._ring_mode_button.send_value(RING_OFF_VALUE, force=True)
        self._ring_mode_button = button
        self._update_ring_mode()
        return

    def connect_to(self, parameter):
        if parameter != self._parameter_to_map_to and not self.is_mapped_manually():
            self._ring_mode_button.send_value(RING_OFF_VALUE, force=True)
        super(RingedEncoderElement, self).connect_to(parameter)

    def release_parameter(self):
        super(RingedEncoderElement, self).release_parameter()
        self._update_ring_mode()

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        super(RingedEncoderElement, self).install_connections(install_translation_callback, install_mapping_callback, install_forwarding_callback)
        if not self._is_mapped and self.value_listener_count() == 0:
            self._is_being_forwarded = install_forwarding_callback(self)
        self._update_ring_mode()

    def is_mapped_manually(self):
        return not self._is_mapped and not self._is_being_forwarded

    def _update_ring_mode(self):
        """ Don't update if being used as pseudo-relative """
        if self.normalized_value_listener_count():
          return
        else:
            if self._ring_mode_button != None:
                if self.is_mapped_manually():
                    self._ring_mode_button.send_value(RING_SIN_VALUE, force=True)
                elif self._parameter_to_map_to != None:
                    param = self._parameter_to_map_to
                    p_range = param.max - param.min
                    value = (param.value - param.min) / p_range * 127
                    self.send_value(int(value), force=True)
                    if self._parameter_to_map_to.min == -1 * self._parameter_to_map_to.max:
                        self._ring_mode_button.send_value(RING_PAN_VALUE, force=True)
                    elif self._parameter_to_map_to.is_quantized:
                        self._ring_mode_button.send_value(RING_SIN_VALUE, force=True)
                    else:
                        self._ring_mode_button.send_value(RING_VOL_VALUE, force=True)
                else:
                    self._ring_mode_button.send_value(RING_OFF_VALUE, force=True)
        return



    def is_pressed(self):
        """ We're only pretending to be a touch encoder to keep Push happy"""
        return False

    def normalize_value(self, value):
        """ This is not actually a relative value, but we'll fake it """
        delta = 0
        if value == 127 or value > self._prev_value:
          delta = 0.01
        elif value == 0 or value < self._prev_value:
          delta = -0.01
        self._prev_value = value
        return delta

    def add_touch_value_listener(self, *a, **k):
        if self.value_listener_count() == 0:
            super(RingedEncoderElement, self).request_listen_nested_control_elements()
        super(RingedEncoderElement, self).add_touch_value_listener(*a, **k)

    def remove_touch_value_listener(self, *a, **k):
        pass
        #super(RingedEncoderElement, self).remove_touch_value_listener(*a, **k)
        #if self.value_listener_count() == 0:
        #    self.unrequest_listen_nested_control_elements()

    def on_nested_control_element_value(self, value, control):
        print('srarasa')

        #self.notify_touch_value(value)