# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC40_MkII/APC40_MkII.py
# Compiled at: 2018-04-23 20:27:04
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from contextlib import contextmanager
import sys

from _Framework.SubjectSlot import subject_slot
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ImmediateBehaviour, MultiEntryMode, DelayMode, ModesComponent, CancellableBehaviour, AlternativeBehaviour, ReenterBehaviour, DynamicBehaviourMixin, ExcludingBehaviourMixin, EnablingModesComponent, LazyComponentMode

from _Framework.Resource import PrioritizedResource
from _Framework.SessionRecordingComponent import SessionRecordingComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ClipCreator import ClipCreator
from _Framework.Util import const, nop, recursive_map
from _Framework.Dependency import inject
from _Framework.BackgroundComponent import BackgroundComponent, ModifierBackgroundComponent

from _APC.APC import APC
from _APC.DeviceComponent import DeviceComponent
from _APC.DeviceBankButtonElement import DeviceBankButtonElement
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent
from _APC.SessionComponent import SessionComponent
from _APC.ControlElementUtils import make_encoder, make_slider, make_pedal_button #, make_ring_encoder
from _APC.SkinDefault import make_rgb_skin, make_default_skin, make_stop_button_skin, make_crossfade_button_skin

from .MelodicComponent import MelodicComponent
from _PushLegacy.DrumGroupComponent import DrumGroupComponent
from _PushLegacy.StepSeqComponent import DrumGroupFinderComponent

from . import Colors, consts
from .BankToggleComponent import BankToggleComponent
from .MixerComponent import MixerComponent
from .QuantizationComponent import QuantizationComponent
from .TransportComponent import TransportComponent
from .CustomSessionComponent import CustomSessionComponent
from .SkinDefault import make_default_skin as make_custom_skin
from .ButtonSliderElement import ButtonSliderElement
from .AutoArmComponent import AutoArmComponent

from .NoteRepeatComponent import NoteRepeatComponent
from .StepSeqComponent import StepSeqComponent
from .GridResolution import GridResolution
from .PlayheadElement import PlayheadElement
from .ControlElementUtils import make_button, make_ring_encoder
from . import ControlElementUtils
from . import SkinDefault
from . import SessionComponent
from .MatrixMaps import FEEDBACK_CHANNELS
from .CustomModesComponent import CustomReenterBehaviour
from .NoteSettings import NoteEditorSettingsComponent

sys.modules['_APC.ControlElementUtils'] = ControlElementUtils
sys.modules['_APC.SkinDefault'] = SkinDefault
sys.modules['_APC.SessionComponent'] = SessionComponent

NUM_TRACKS = 8
NUM_SCENES = 5

import pydevd


class APC40_MkII(APC, OptimizedControlSurface):

    def __init__(self, *a, **k):

        pydevd.settrace('localhost', port=4223, stdoutToServer=True, stderrToServer=True)

        super(APC40_MkII, self).__init__(*a, **k)
        self._color_skin = make_rgb_skin()
        self._default_skin = make_default_skin()
        self._stop_button_skin = make_stop_button_skin()
        self._crossfade_button_skin = make_crossfade_button_skin()
        self._double_press_context = DoublePressContext()

        with self.component_guard():
            self._create_controls()
            self._create_bank_toggle()
            self._create_mixer()
            self._create_transport()
            self._create_view_control()
            self._create_quantization_selection()
            self._create_recording()

            self._skin = make_custom_skin()

            self._clip_creator = ClipCreator()

            self._init_background()
            self._init_instrument()
            self._init_step_sequencer()
            self._init_drum_component()
            self._init_note_repeat()
            self._create_session()
            self._session.set_mixer(self._mixer)

            self._init_matrix_modes()
            self._create_device()
            self._on_selected_track_changed()

            self.set_feedback_channels(FEEDBACK_CHANNELS)

        self.set_highlighting_session_component(self._session)
        self.set_device_component(self._device)

    def _with_shift(self, button):
        return ComboElement(button, modifiers=[self._shift_button])

    def _create_controls(self):
        make_on_off_button = partial(make_button, skin=self._default_skin)

        def make_color_button(*a, **k):
            button = make_button(skin=self._color_skin, *a, **k)
            button.is_rgb = True
            button.num_delayed_messages = 2
            return button

        def make_matrix_button(track, scene):
            return make_color_button(0, 32 + track - NUM_TRACKS * scene, name='%d_Clip_%d_Button' % (track, scene))

        def make_stop_button(track):
            return make_button(track, 52, name='%d_Stop_Button' % track, skin=self._stop_button_skin)

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
        self._user_button = make_on_off_button(0, 89, name='User_Button', resource_type=PrioritizedResource)
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
        self._metronome_button = make_on_off_button(0, 90, name='Metronome_Button')
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

        self._session = CustomSessionComponent(NUM_TRACKS, NUM_SCENES, auto_name=True, is_enabled=False,
                                               enable_skinning=True,
                                               layer=Layer(track_bank_left_button=when_bank_off(self._left_button),
                                                           track_bank_right_button=when_bank_off(self._right_button),
                                                           scene_bank_up_button=when_bank_off(self._up_button),
                                                           scene_bank_down_button=when_bank_off(self._down_button),
                                                           page_left_button=when_bank_on(self._left_button),
                                                           page_right_button=when_bank_on(self._right_button),
                                                           page_up_button=when_bank_on(self._up_button),
                                                           page_down_button=when_bank_on(self._down_button),
                                                           stop_track_clip_buttons=self._stop_buttons,
                                                           stop_all_clips_button=self._stop_all_button,
                                                           scene_launch_buttons=self._scene_launch_buttons,
                                                           clip_launch_buttons=self._session_matrix))

        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self._session.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)
        self._session_zoom = SessionZoomingComponent(self._session, name='Session_Overview', enable_skinning=True, is_enabled=False, layer=Layer(button_matrix=self._shifted_matrix, nav_left_button=self._with_shift(self._left_button), nav_right_button=self._with_shift(self._right_button), nav_up_button=self._with_shift(self._up_button), nav_down_button=self._with_shift(self._down_button), scene_bank_buttons=self._shifted_scene_buttons))
        self._session.set_delete_button(self._nudge_down_button)
        self._session.set_copy_button(self._nudge_up_button)

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
        self._encoder_mode.layer = Layer(pan_button=self._pan_button, sends_button=self._sends_button, user_button=self._user_button)
        self._encoder_mode.selected_mode = 'pan'

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport', is_enabled=False, layer=Layer(shift_button=self._shift_button, play_button=self._play_button, stop_button=ComboElement(self._play_button, modifiers=[
         self._shift_button]), record_button=self._record_button, metronome_button=self._with_shift(self._tap_tempo_button), tap_tempo_button=self._tap_tempo_button, nudge_down_button=self._with_shift(self._nudge_down_button), nudge_up_button=self._with_shift(self._nudge_up_button), tempo_encoder=self._tempo_control), play_toggle_model_transform=lambda v: v)

    def _create_device(self):
        self._device = DeviceComponent(name=u'Device', is_enabled=False,
                                       layer=Layer(parameter_controls=self._device_controls,
                                                   bank_buttons=self._device_bank_buttons,
                                                   bank_prev_button=self._device_prev_bank_button,
                                                   bank_next_button=self._device_next_bank_button,
                                                   on_off_button=self._device_on_off_button,
                                                   lock_button=self._device_lock_button),
                                       device_selection_follows_track_selection=True)

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

    def _init_background(self):
        self._background = BackgroundComponent(is_root=True)
        self._background.set_enabled(False)
        self._background.layer = Layer(velocity_slider=self._velocity_slider, stop_buttons=self._stop_buttons)  # , display_line2=self._display_line2, display_line3=self._display_line3, display_line4=self._display_line4, top_buttons=self._select_buttons, bottom_buttons=self._track_state_buttons, scales_button=self._scale_presets_button, octave_up=self._octave_up_button, octave_down=self._octave_down_button, side_buttons=self._side_buttons, repeat_button=self._repeat_button, accent_button=self._accent_button, double_button=self._double_button, in_button=self._in_button, out_button=self._out_button, param_controls=self._global_param_controls, param_touch=self._global_param_touch_buttons, tempo_control_tap=self._tempo_control_tap, master_control_tap=self._master_volume_control_tap, touch_strip=self._touch_strip_control, touch_strip_tap=self._touch_strip_tap, nav_up_button=self._nav_up_button, nav_down_button=self._nav_down_button, nav_left_button=self._nav_left_button, nav_right_button=self._nav_right_button, aftertouch=self._aftertouch_control, pad_parameters=self._pad_parameter_control, _notification=self._notification.use_single_line(2), priority=consts.BACKGROUND_PRIORITY)

        self._matrix_background = BackgroundComponent()
        self._matrix_background.set_enabled(False)
        self._matrix_background.layer = Layer(matrix=self._session_matrix)

    #  self._mod_background = ModifierBackgroundComponent(is_root=True)
    #  self._mod_background.layer = Layer(shift_button=self._shift_button, velocity_slider = self._velocity_slider, stop_buttons = self._stop_buttons)

    def _init_step_sequencer(self):
        self._step_sequencer = StepSeqComponent(grid_resolution=self._grid_resolution)
        self._step_sequencer.layer = self._create_step_sequencer_layer()

    def _create_step_sequencer_layer(self):
        return Layer(
            velocity_slider=self._velocity_slider,
            drum_matrix=self._session_matrix.submatrix[:4, 0:5],
            # [4, 1:5],  mess with this for possible future 32 pad drum rack :

            button_matrix=self._double_press_matrix.submatrix[4:8, 0:4],  # [4:8, 1:5],

            #  next_page_button = self._bank_button,

            #select_button=self._user_button,
            delete_button=self._stop_all_button,
            playhead=self._playhead,
            quantization_buttons=self._stop_buttons,
            shift_button=self._shift_button,
            loop_selector_matrix=self._double_press_matrix.submatrix[4:8, 4],
            # changed from [:8, :1] so as to enable bottem row of rack   . second value clip length rows
            short_loop_selector_matrix=self._double_press_event_matrix.submatrix[4:8, 4],
            # changed from [:8, :1] no change noticed as of yet
            drum_bank_up_button=self._up_button,
            drum_bank_down_button=self._down_button)

    #       capture_button = self._tap_tempo_button)

    def _init_drum_component(self):
        self._drum_component = DrumGroupComponent(name='Drum_Group', is_enabled=False)
        self._drum_component.layer = Layer(
            drum_matrix=self._session_matrix,
            #    page_strip=self._touch_strip_control,
            #    scroll_strip=self._with_shift(self._touch_strip_control),
            #    solo_button=self._global_solo_button,
            #select_button=self._metronome_button,
            #    delete_button=self._delete_button,
            scroll_page_up_button=self._up_button,
            scroll_page_down_button=self._down_button,
            #    quantize_button=self._quantize_button,
            #    mute_button=self._global_mute_button,
            scroll_up_button=self._with_shift(self._up_button),
            scroll_down_button=self._with_shift(self._down_button))

    #    self._drum_component.select_drum_pad = self._selector.on_select_drum_pad
    #    self._drum_component.quantize_pitch = self._quantize.quantize_pitch

    def _init_instrument(self):
        instrument_basic_layer = Layer(
            # octave_strip=self._with_shift(self._touch_strip_control),
            #   capture_button = self._tap_tempo_button,
            #scales_toggle_button=self._metronome_button,
            octave_up_button=self._up_button,
            octave_down_button=self._down_button,
            scale_up_button=self._with_shift(self._up_button),
            scale_down_button=self._with_shift(self._down_button))

        self._instrument = MelodicComponent(skin=self._skin, is_enabled=False,
                                            clip_creator=self._clip_creator, name='Melodic_Component',
                                            grid_resolution=self._grid_resolution,
                                            note_editor_settings=self._add_note_editor_setting(),
                                            layer=self._create_instrument_layer(),
                                            instrument_play_layer=Layer(
                                                octave_up_button=self._up_button,
                                                octave_down_button=self._down_button,
                                                scale_up_button=self._with_shift(self._up_button),
                                                scale_down_button=self._with_shift(self._down_button),
                                                matrix=self._session_matrix
                                            ),
                                            # touch_strip=self._touch_strip_control, touch_strip_indication=self._with_firmware_version(1, 16, ComboElement(self._touch_strip_control, modifiers=[self._select_button])),
                                            # touch_strip_toggle=self._with_firmware_version(1, 16, ComboElement(self._touch_strip_tap, modifiers=[self._select_button])),
                                            # aftertouch_control=self._aftertouch_control, delete_button=self._delete_button),
                                            instrument_sequence_layer=instrument_basic_layer  # + Layer(note_strip=self._touch_strip_control)
                                            )
        self._on_note_editor_layout_changed.subject = self._instrument

    def _create_instrument_layer(self):
        return Layer(
            playhead=self._playhead,
            velocity_slider=self._velocity_slider,
            # mute_button=self._global_mute_button,
            quantization_buttons=self._stop_buttons,
            loop_selector_matrix=self._double_press_matrix.submatrix[0:8, 0],  # [:, 0]
            short_loop_selector_matrix=self._double_press_event_matrix.submatrix[0:8, 0],  # [:, 0]
            #note_editor_matrices=ButtonMatrixElement(
            #    [[self._session_matrix.submatrix[:, 4 - row] for row in xrange(7)]]))
            note_editor_matrices=ButtonMatrixElement([[ self._session_matrix.submatrix[:8, 4 - row] for row in xrange(4)]]))

    def enter_note_mode_layout(self):
        self._matrix_modes.selected_mode = 'user'
        self._select_note_mode()

        if self._user_modes.selected_mode == 'instrument':
            self._instrument._set_selected_mode(self._instrument.selected_mode)
        elif self._user_modes.selected_mode == 'drums':
            self._drum_modes._set_selected_mode(self._drum_modes.selected_mode)

        self.reset_controlled_track()

    def exit_note_mode_layout(self):
        self.reset_controlled_track()

    def switch_note_mode_layout(self):
        self._matrix_modes.selected_mode = 'user'
        self._select_note_mode()

        if self._user_modes.selected_mode == 'instrument':
            getattr(self._instrument, 'cycle_mode', nop)()
        elif self._user_modes.selected_mode == 'drums':
            getattr(self._drum_modes, 'cycle_mode', nop)()

        self.reset_controlled_track()

    def _init_matrix_modes(self):
        """ Switch between Session and StepSequencer modes """

        """here we go trying to switch.... lew  05:53   21/10/17"""

        self._auto_arm = AutoArmComponent(name='Auto_Arm')

        self._drum_group_finder = DrumGroupFinderComponent()
        self._on_drum_group_changed.subject = self._drum_group_finder

        self._drum_modes = ModesComponent(name='Drum_Modes', is_enabled=False)
        self._drum_modes.add_mode('sequencer', self._step_sequencer)
        self._drum_modes.add_mode('64pads', self._drum_component)  # added 15:18 subday 22/10/17     can maybe look into this. causes issues when trying to scroll.(drumcomp1)

        self._drum_modes.selected_mode = '64pads'

        self._user_modes = ModesComponent(name='User_Modes', is_enabled=False)
        self._user_modes.add_mode('drums', [self._drum_modes])
        self._user_modes.add_mode('instrument', [self._note_repeat_enabler, self._instrument])
        self._user_modes.selected_mode = 'drums'

        self._matrix_modes = ModesComponent(name='Matrix_Modes', is_root=True)
        self._matrix_modes.add_mode('session', self._session_mode_layers())
        self._matrix_modes.add_mode('sends', self._session_mode_layers())
        self._matrix_modes.add_mode('user', [self._user_modes], behaviour=CustomReenterBehaviour(on_reenter=self.switch_note_mode_layout, on_enter=self.enter_note_mode_layout))
        self._matrix_modes.add_mode('disable', [self._matrix_background, self._background])

        #self._matrix_modes.add_mode('user', [self._drum_group_finder, self._view_control, self._user_modes],
        #                           behaviour=self._auto_arm.auto_arm_restore_behaviour(ReenterBehaviour,
        #                                                                               on_reenter=self.switch_note_mode_layout))

        self._matrix_modes.layer = Layer(session_button=self._pan_button, sends_button=self._sends_button, user_button=self._user_button, disable_button=self._metronome_button)

        self._on_matrix_mode_changed.subject = self._matrix_modes
        self._matrix_modes.selected_mode = 'session'

        #self._disable_mode = ModesComponent(name='Disable_Mode', is_enabled=False)
        #self._disable_mode.add_mode('disable', [self._matrix_background, self._background])


    def _session_mode_layers(self):
        return [self._session, self._view_control, self._session_zoom]#, self._mixer

    def _init_note_repeat(self):
        self._note_repeat = NoteRepeatComponent(name='Note_Repeat')
        self._note_repeat.set_enabled(False)
        self._note_repeat.set_note_repeat(self._c_instance.note_repeat)
        self._note_repeat.layer = Layer(
            # aftertouch_control=self._aftertouch_control,
            select_buttons=self._stop_buttons,
            # pad_parameters=self._pad_parameter_control
        )
        self._note_repeat.layer.priority = consts.DIALOG_PRIORITY
        self._note_repeat_enabler = EnablingModesComponent(name='Note_Repeat_Enabler', component=self._note_repeat,
                                                           toggle_value='DefaultButton.Alert',
                                                           disabled_value='DefaultButton.On')
        self._note_repeat_enabler.set_enabled(False)
        self._note_repeat_enabler.layer = Layer(toggle_button=self._bank_button)

    def _select_note_mode(self):
        """
        Selects which note mode to use depending on the kind of
        current selected track and its device chain...
        """
        track = self.song().view.selected_track
        drum_device = self._drum_group_finder.drum_group
        self._step_sequencer.set_drum_group_device(drum_device)
        self._drum_component.set_drum_group_device(drum_device)
        if track == None or track.is_foldable or track in self.song().return_tracks or track == self.song().master_track or track.is_frozen:
            self._user_modes.selected_mode = 'disabled'
        elif track and track.has_audio_input:
            self._user_modes.selected_mode = 'disabled'
            #self._note_modes.selected_mode = 'looper'
        elif drum_device:
            self._user_modes.selected_mode = 'drums'
        else:
            self._user_modes.selected_mode = 'instrument'
        #self.reset_controlled_track()

    @subject_slot('drum_group')
    def _on_drum_group_changed(self):
        if self._matrix_modes.selected_mode != 'session':
            self._select_note_mode()

    @subject_slot('selected_mode')
    def _on_matrix_mode_changed(self, mode):
        if self._matrix_modes.selected_mode != mode and mode != 'session':
            self._select_note_mode()
        #if self._matrix_modes.selected_mode != mode and mode == 'session':
        #    self._create_session()

            #self._disable_mode.selected_mode = 'disable'
            #self._session.set_enabled(True)
        self._update_auto_arm(selected_mode=mode)
        self.reset_controlled_track()

    def _update_auto_arm(self, selected_mode=None):
        self._auto_arm.set_enabled(selected_mode or self._matrix_modes.selected_mode == 'user')

    @subject_slot('selected_mode')
    def _on_note_editor_layout_changed(self, mode):
        pass
        #self.reset_controlled_track(mode)

    def reset_controlled_track(self, mode=None):
        if mode == None:
            mode = self._instrument.selected_mode
        if self._instrument and self._instrument.is_enabled() and mode == 'sequence':
            self.release_controlled_track()
        else:
            self.set_controlled_track(self.song().view.selected_track)


    def _add_note_editor_setting(self):
        return NoteEditorSettingsComponent(self._grid_resolution,
                                           Layer(initial_encoders=self._mixer_encoders),
                                           Layer(encoders=self._mixer_encoders))

    @contextmanager
    def component_guard(self):
        """ Customized to inject additional things """
        with super(APC40_MkII, self).component_guard():
            with self.make_injector().everywhere():
                yield

    def make_injector(self):
        """ Adds some additional stuff to the injector, used in BaseMessenger """
        return inject(
            double_press_context=const(self._double_press_context),
            control_surface=const(self),

            log_message=const(self.log_message))
