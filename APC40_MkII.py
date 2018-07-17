from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from contextlib import contextmanager
import sys

from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ComboElement import ComboElement, DoublePressElement, MultiElement
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.Layer import Layer
from _Framework.ModesComponent import ModesComponent, ImmediateBehaviour, DelayMode, AddLayerMode, ReenterBehaviour
from _Framework.Resource import PrioritizedResource
from _Framework.SessionRecordingComponent import SessionRecordingComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ClipCreator import ClipCreator
from _Framework.Util import const, nop, recursive_map
from _Framework.Dependency import inject

from _PushLegacy.PlayheadElement import PlayheadElement
from _PushLegacy.GridResolution import GridResolution
from _PushLegacy.MelodicComponent import MelodicComponent
#from _PushLegacy.AutoArmComponent import AutoArmComponent

from _APC.APC import APC
from _APC.DeviceComponent import DeviceComponent
from _APC.DeviceBankButtonElement import DeviceBankButtonElement
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent
from _APC.ControlElementUtils import make_button, make_encoder, make_slider, make_ring_encoder, make_pedal_button
from _APC.SkinDefault import make_rgb_skin, make_default_skin, make_stop_button_skin, make_crossfade_button_skin
from . import Colors
from .BankToggleComponent import BankToggleComponent
from .MixerComponent import MixerComponent
from .QuantizationComponent import QuantizationComponent
from .TransportComponent import TransportComponent
from .custom_auto_arm_component import AutoArmComponent

from APCSequencer_LEWa.SelectComponent import SelectComponent
from APCSequencer_LEWa.ButtonSliderElement import ButtonSliderElement
from APCSequencer_LEWa.LooperComponent import LooperComponent

#from APCSequencer_LEWa.StepSeqComponent import StepSeqComponent

from APCSequencer_LEWa.ControlElementUtils import make_button as make_custom_button

# Monkeypatch things
import APCSequencer_LEWa.ControlElementUtils
import APCSequencer_LEWa.SkinDefault
import APCSequencer_LEWa.SessionComponent
#from APCSequencer_LEWa.SessionComponent import SessionComponent

from .CustomSessionComponent import CustomSessionComponent as SessionComponent

from APCSequencer_LEWa.SkinDefault import make_rgb_skin, make_default_skin, make_stop_button_skin, make_crossfade_button_skin
from APCSequencer_LEWa.StepSeqComponent import StepSeqComponent

sys.modules['_APC.ControlElementUtils'] = APCSequencer_LEWa.ControlElementUtils
sys.modules['_APC.SkinDefault'] = APCSequencer_LEWa.SkinDefault
sys.modules['_APC.SessionComponent'] = SessionComponent

import pydevd

NUM_TRACKS = 8
NUM_SCENES = 5

class APC40_MkII(APC, OptimizedControlSurface):

    def __init__(self, *a, **k):
        super(APC40_MkII, self).__init__(*a, **k)
        self._color_skin = make_rgb_skin()
        self._default_skin = make_default_skin()
        self._stop_button_skin = make_stop_button_skin()
        self._crossfade_button_skin = make_crossfade_button_skin()
        pydevd.settrace('localhost', port=4223, stdoutToServer=True, stderrToServer=True)
        with self.component_guard():
            self._clip_creator = ClipCreator()
            self._create_controls()

            self._create_bank_toggle()
            self._create_session()
            self._create_mixer()
            self._create_transport()
            self._create_device()
            self._create_view_control()

            self._create_sequencer()
            self._create_instrument()
            self._create_session_mode()
            self._init_auto_arm()

            self._create_quantization_selection()
            self._create_recording()
            self._session.set_mixer(self._mixer)
        self.set_highlighting_session_component(self._session)
        self.set_device_component(self._device)

    def _with_shift(self, button):
        return ComboElement(button, modifiers=[self._shift_button])

    def _create_controls(self):
        make_on_off_button = partial(make_button, skin=self._default_skin)

        # Make these prioritized resources, which share between Layers() equally
        # Rather than building a stack

        def make_color_button(*a, **k):
            button = make_button(skin=self._color_skin, *a, **k)
            button.is_rgb = True
            button.num_delayed_messages = 2
            return button

        def make_matrix_button(track, scene):
            return make_color_button(0, 32 + track - NUM_TRACKS * scene, name='%d_Clip_%d_Button' % (track, scene))

        def make_stop_button(track):
            return make_custom_button(track, 52, name='%d_Stop_Button' % track, skin=self._stop_button_skin)

        self._metronome_button = make_button(0, 90, name='Delete_Button')
        self._shift_button = make_button(0, 98, name='Shift_Button', resource_type=PrioritizedResource)
        self._bank_button = make_on_off_button(0, 103, name='Bank_Button')
        self._left_button = make_button(0, 97, name='Bank_Select_Left_Button')
        self._right_button = make_button(0, 96, name='Bank_Select_Right_Button')
        self._up_button = make_button(0, 94, name='Bank_Select_Up_Button')
        self._down_button = make_button(0, 95, name='Bank_Select_Down_Button')
        self._stop_buttons = ButtonMatrixElement(rows=[[ make_stop_button(track) for track in xrange(NUM_TRACKS) ]])
        self._stop_all_button = make_button(0, 81, name='Stop_All_Clips_Button')
        self._scene_launch_buttons_raw = [ make_color_button(0, scene + 82, name='Scene_%d_Launch_Button' % scene) for scene in xrange(NUM_SCENES)
                                         ]
        self._scene_launch_buttons = ButtonMatrixElement(rows=[
         self._scene_launch_buttons_raw])
        self._matrix_rows_raw = [ [ make_matrix_button(track, scene) for track in xrange(NUM_TRACKS) ] for scene in xrange(NUM_SCENES)
                                ]
        self._session_matrix = ButtonMatrixElement(rows=self._matrix_rows_raw)
        self._pan_button = make_on_off_button(0, 87, name='Pan_Button', resource_type=PrioritizedResource)
        self._sends_button = make_on_off_button(0, 88, name='Sends_Button', resource_type=PrioritizedResource)
        self._user_button = make_on_off_button(0, 89, name='User_Button')

        self._mixer_encoders = ButtonMatrixElement(rows=[
         [ make_ring_encoder(48 + track, 56 + track, name='Track_Control_%d' % track) for track in xrange(NUM_TRACKS)
         ]])
        self._volume_controls = ButtonMatrixElement(rows=[
         [ make_slider(track, 7, name='%d_Volume_Control' % track) for track in xrange(NUM_TRACKS)
         ]])
        self._master_volume_control = make_slider(0, 14, name='Master_Volume_Control')
        self._prehear_control = make_encoder(0, 47, name='Prehear_Volume_Control')
        self._crossfader_control = make_slider(0, 15, name='Crossfader')
        self._raw_select_buttons = [ make_on_off_button(channel, 51, name='%d_Select_Button' % channel) for channel in xrange(NUM_TRACKS)
                                   ]
        self._arm_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 48, name='%d_Arm_Button' % channel) for channel in xrange(NUM_TRACKS)
         ]])
        self._solo_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 49, name='%d_Solo_Button' % channel) for channel in xrange(NUM_TRACKS)
         ]])
        self._mute_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 50, name='%d_Mute_Button' % channel) for channel in xrange(NUM_TRACKS)
         ]])
        self._crossfade_buttons = ButtonMatrixElement(rows=[
         [ make_button(channel, 66, name='%d_Crossfade_Button' % channel, skin=self._crossfade_button_skin) for channel in xrange(NUM_TRACKS)
         ]])
        self._select_buttons = ButtonMatrixElement(rows=[
         self._raw_select_buttons])
        self._master_select_button = make_on_off_button(channel=0, identifier=80, name='Master_Select_Button')
        self._send_select_buttons = ButtonMatrixElement(rows=[
         [ ComboElement(button, modifiers=[self._sends_button]) for button in self._raw_select_buttons
         ]])
        self._quantization_buttons = ButtonMatrixElement(rows=[
         [ ComboElement(button, modifiers=[self._shift_button]) for button in self._raw_select_buttons
         ]])

        self._play_button = make_on_off_button(0, 91, name='Play_Button')
        self._record_button = make_on_off_button(0, 93, name='Record_Button')
        self._session_record_button = make_on_off_button(0, 102, name='Session_Record_Button')
        self._nudge_down_button = make_button(0, 100, name='Nudge_Down_Button')
        self._nudge_up_button = make_button(0, 101, name='Nudge_Up_Button')
        self._tap_tempo_button = make_button(0, 99, name='Tap_Tempo_Button')
        self._tempo_control = make_encoder(0, 13, name='Tempo_Control')
        self._device_controls = ButtonMatrixElement(rows=[
         [ make_ring_encoder(16 + index, 24 + index, name='Device_Control_%d' % index) for index in xrange(8)
         ]])
        self._device_control_buttons_raw = [ make_on_off_button(0, 58 + index) for index in xrange(8)
                                           ]
        self._device_bank_buttons = ButtonMatrixElement(rows=[
         [ DeviceBankButtonElement(button, modifiers=[self._shift_button]) for button in self._device_control_buttons_raw
         ]])
        self._device_prev_bank_button = self._device_control_buttons_raw[2]
        self._device_prev_bank_button.name = 'Device_Prev_Bank_Button'
        self._device_next_bank_button = self._device_control_buttons_raw[3]
        self._device_next_bank_button.name = 'Device_Next_Bank_Button'
        self._device_on_off_button = self._device_control_buttons_raw[4]
        self._device_on_off_button.name = 'Device_On_Off_Button'
        self._device_lock_button = self._device_control_buttons_raw[5]
        self._device_lock_button.name = 'Device_Lock_Button'
        self._prev_device_button = self._device_control_buttons_raw[0]
        self._prev_device_button.name = 'Prev_Device_Button'
        self._next_device_button = self._device_control_buttons_raw[1]
        self._next_device_button.name = 'Next_Device_Button'
        self._clip_device_button = self._device_control_buttons_raw[6]
        self._clip_device_button.name = 'Clip_Device_Button'
        self._detail_view_button = self._device_control_buttons_raw[7]
        self._detail_view_button.name = 'Detail_View_Button'
        self._foot_pedal_button = DoublePressElement(make_pedal_button(64, name='Foot_Pedal'))
        self._shifted_matrix = ButtonMatrixElement(rows=recursive_map(self._with_shift, self._matrix_rows_raw))
        self._shifted_scene_buttons = ButtonMatrixElement(rows=[
         [ self._with_shift(button) for button in self._scene_launch_buttons_raw
         ]])

        self._grid_resolution = GridResolution()
        self._velocity_slider = ButtonSliderElement(tuple(self._scene_launch_buttons_raw[::-1]))
        double_press_rows = recursive_map(DoublePressElement, self._matrix_rows_raw)
        self._double_press_matrix = ButtonMatrixElement(name='Double_Press_Matrix', rows=double_press_rows)
        self._double_press_event_matrix = ButtonMatrixElement(name='Double_Press_Event_Matrix',
                                                              rows=recursive_map(lambda x: x.double_press,
                                                                                 double_press_rows))
        self._playhead = PlayheadElement(self._c_instance.playhead)

    def _create_bank_toggle(self):
        self._bank_toggle = BankToggleComponent(is_enabled=False, layer=Layer(bank_toggle_button=self._bank_button))

    def _create_session(self):

        def when_bank_on(button):
            return self._bank_toggle.create_toggle_element(on_control=button)

        def when_bank_off(button):
            return self._bank_toggle.create_toggle_element(off_control=button)

        self._session = SessionComponent(NUM_TRACKS, NUM_SCENES, auto_name=True, is_enabled=False, enable_skinning=True, layer=Layer( track_bank_left_button=when_bank_off(self._left_button), track_bank_right_button=when_bank_off(self._right_button), scene_bank_up_button=when_bank_off(self._up_button), scene_bank_down_button=when_bank_off(self._down_button), page_left_button=when_bank_on(self._left_button), page_right_button=when_bank_on(self._right_button), page_up_button=when_bank_on(self._up_button), page_down_button=when_bank_on(self._down_button), stop_track_clip_buttons=self._stop_buttons, stop_all_clips_button=self._stop_all_button, scene_launch_buttons=self._scene_launch_buttons, clip_launch_buttons=self._session_matrix))
        self._session.set_delete_button(self._metronome_button)
        self._session.set_copy_button(self._nudge_down_button)
        self._session.set_paste_button(self._nudge_up_button)

        self._session.add_clip_button_function()

        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self._session.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)
        self._session_zoom = SessionZoomingComponent(self._session, name='Session_Overview', enable_skinning=True, is_enabled=False, layer=Layer(button_matrix=self._shifted_matrix, nav_left_button=self._with_shift(self._left_button), nav_right_button=self._with_shift(self._right_button), nav_up_button=self._with_shift(self._up_button), nav_down_button=self._with_shift(self._down_button), scene_bank_buttons=self._shifted_scene_buttons))

    def _create_mixer(self):
        self._mixer = MixerComponent(NUM_TRACKS, auto_name=True, is_enabled=False, invert_mute_feedback=True, layer=Layer(volume_controls=self._volume_controls, arm_buttons=self._arm_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, shift_button=self._shift_button, track_select_buttons=self._select_buttons, prehear_volume_control=self._prehear_control, crossfader_control=self._crossfader_control, crossfade_buttons=self._crossfade_buttons))
        self._mixer.master_strip().layer = Layer(volume_control=self._master_volume_control, select_button=self._master_select_button)
        self._encoder_mode = ModesComponent(name='Encoder_Mode', is_enabled=False)
        self._encoder_mode.default_behaviour = ImmediateBehaviour()
        self._encoder_mode.add_mode('pan', [
         AddLayerMode(self._mixer, Layer(pan_controls=self._mixer_encoders))])
        self._encoder_mode.add_mode('sends', [
         AddLayerMode(self._mixer, Layer(send_controls=self._mixer_encoders)),
         DelayMode(AddLayerMode(self._mixer, Layer(send_select_buttons=self._send_select_buttons)))])
        self._encoder_mode.add_mode('user', [
         AddLayerMode(self._mixer, Layer(user_controls=self._mixer_encoders))])
        self._encoder_mode.layer = Layer(pan_button=self._pan_button, sends_button=self._sends_button)#, user_button=self._user_button)
        self._encoder_mode.selected_mode = 'pan'

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport', is_enabled=False, layer=Layer(shift_button=self._shift_button, play_button=self._play_button, stop_button=ComboElement(self._play_button, modifiers=[
         self._shift_button]), record_button=self._record_button, metronome_button=self._with_shift(self._tap_tempo_button), tap_tempo_button=self._tap_tempo_button, nudge_down_button=self._with_shift(self._nudge_down_button), nudge_up_button=self._with_shift(self._nudge_up_button), tempo_encoder=self._tempo_control), play_toggle_model_transform=lambda v: v)

    def _create_device(self):
        self._device = DeviceComponent(name='Device', is_enabled=False, layer=Layer(parameter_controls=self._device_controls, bank_buttons=self._device_bank_buttons, bank_prev_button=self._device_prev_bank_button, bank_next_button=self._device_next_bank_button, on_off_button=self._device_on_off_button, lock_button=self._device_lock_button), device_selection_follows_track_selection=True)

    def _create_view_control(self):
        self._view_control = DetailViewCntrlComponent(name='View_Control', is_enabled=False, layer=Layer(device_nav_left_button=self._prev_device_button, device_nav_right_button=self._next_device_button, device_clip_toggle_button=self._clip_device_button, detail_toggle_button=self._detail_view_button))
        self._view_control.device_clip_toggle_button.pressed_color = 'DefaultButton.On'

    def _create_quantization_selection(self):
        self._quantization_selection = QuantizationComponent(name='Quantization_Selection', is_enabled=False, layer=Layer(quantization_buttons=self._quantization_buttons))

    def _create_recording(self):
        record_button = MultiElement(self._session_record_button, self._foot_pedal_button.single_press)
        self._session_recording = SessionRecordingComponent(ClipCreator(), self._view_control, name='Session_Recording', is_enabled=False, layer=Layer(new_button=self._foot_pedal_button.double_press, record_button=record_button, _uses_foot_pedal=self._foot_pedal_button))

    def get_matrix_button(self, column, row):
        return self._matrix_rows_raw[row][column]

    def _product_model_id_byte(self):
        return 41




    def _create_session_mode(self):
        """ Switch between Session and StepSequencer modes """
        self._session_mode = ModesComponent(name='Session_Mode', is_enabled=False)
        self._session_mode.default_behaviour = ImmediateBehaviour()
        self._session_mode.add_mode('session', self._session_mode_layers())
        self._session_mode.add_mode('session_2', self._session_mode_layers())
        self._session_mode.add_mode('sequencer', (self._sequencer, self._sequencer_layer()))
        self._session_mode.add_mode('instrument', (self._instrument, self._instrument_layer()))

        self._session_mode.layer = Layer(
            session_button=self._pan_button,
            session_2_button=self._sends_button,
            instrument_button=self._with_shift(self._user_button),
            sequencer_button=self._user_button)

        self._session_mode.selected_mode = "session"

        # added for looping capability
        self._looper = LooperComponent(self)
        self._looper.name = 'looper_Component'

    def _create_sequencer(self):
        self._sequencer = StepSeqComponent(grid_resolution=self._grid_resolution)

    def _create_instrument(self):
        self._instrument = MelodicComponent(grid_resolution=self._grid_resolution)

    def _session_mode_layers(self):
        return [self._session, self._session_zoom]

    def _sequencer_layer(self):
        return Layer(
            playhead=self._playhead,
            button_matrix=self._double_press_matrix.submatrix[4:8, 1:5],
            #button_matrix=self._session_matrix.submatrix[:8, :4],
            drum_matrix=self._session_matrix.submatrix[:4, 1:5],
            loop_selector_matrix=self._double_press_matrix.submatrix[:4, :1],
            short_loop_selector_matrix=self._double_press_event_matrix.submatrix[:4, :1],

            #touch_strip=self._touch_strip_control,
            #detail_touch_strip=self._with_shift(self._touch_strip_control),
            #quantization_buttons=self._side_buttons,
            #solo_button=self._global_solo_button,
            select_button=self._user_button,
            delete_button=self._stop_all_button,
            shift_button=self._shift_button,
            drum_bank_up_button=self._right_button,
            drum_bank_down_button=self._left_button,
            octave_up_button=self._up_button,
            octave_down_button=self._down_button
            #quantize_button=self._quantize_button,
            #mute_button=self._global_mute_button,
            #drum_bank_detail_up_button=self._with_shift(self._octave_up_button),
            #drum_bank_detail_down_button=self._with_shift(self._octave_down_button)
        )

        '''
        return Layer(
            velocity_slider=self._velocity_slider,
            drum_matrix=self._session_matrix.submatrix[:4, 1:5],
            # [4, 1:5],  mess with this for possible future 32 pad drum rack :

            #  lewie add 15/10/17  07:06
            # note_matrix = self._session_matrix.submatrix[:8, 1:5],
            button_matrix=self._double_press_matrix.submatrix[4:8, 1:5],  # [4:8, 1:5],

            # next_page_button = self._bank_button,

            select_button=self._user_button,
            delete_button=self._stop_all_button,
            playhead=self._playhead,
            quantization_buttons=self._stop_buttons,
            shift_button=self._shift_button,
            loop_selector_matrix=self._double_press_matrix.submatrix[:4, :1],
            # changed from [:8, :1] so as to enable bottem row of rack   . second value clip length rows
            short_loop_selector_matrix=self._double_press_event_matrix.submatrix[:4, :1],
            # changed from [:8, :1] no change noticed as of yet
            drum_bank_up_button=self._right_button,
            drum_bank_down_button=self._left_button
            #octave_up_button=self._right_button,
            #octave_down_button=self._left_button
        )'''

    def _instrument_layer(self):
        return Layer(playhead=self._playhead,  # mute_button=self._global_mute_button,
                     quantization_buttons=self._stop_buttons,
                     note_editor_matrices=ButtonMatrixElement(
                         [[self._session_matrix.submatrix[:, 6 - row] for row in xrange(7)]]))
                         #[[self._session_matrix.submatrix[:, 7 - row] for row in xrange(7)]]))

    def _init_auto_arm(self):
        self._auto_arm = AutoArmComponent(is_enabled=True)

        # added so as to have looping with pan_button held
        self._select_modes = SelectComponent(self, tuple(self._raw_select_buttons), self._metronome_button,
                                             self._nudge_down_button, self._nudge_up_button, self._tap_tempo_button,
                                             self._transport, self._looper, self._session, self._session_matrix,
                                             self._session_record_button)
        self._select_modes.name = 'Select_Modes'
        self._select_modes.set_mode_toggle(self._pan_button)

    def make_injector(self):
        """ Adds some additional stuff to the injector, used in BaseMessenger """
        return inject(
            control_surface=const(self))

    # EVENT HANDLING FUNCTIONS
    def reset_controlled_track(self):
        self.set_controlled_track(self.song().view.selected_track)

    def update(self):
        self.reset_controlled_track()
        super(APC40_MkII, self).update()

    def _on_selected_track_changed(self):
        self.reset_controlled_track()
        if self._auto_arm.needs_restore_auto_arm:
            self.schedule_message(1, self._auto_arm.restore_auto_arm)
        super(APC40_MkII, self)._on_selected_track_changed()

    @contextmanager
    def component_guard(self):
        """ Customized to inject additional things """
        with super(APC40_MkII, self).component_guard():
            with self.make_injector().everywhere():
                yield

    def make_injector(self):
        """ Adds some additional stuff to the injector, used in BaseMessenger """
        return inject(
            control_surface=const(self),
            log_message=const(self.log_message))
