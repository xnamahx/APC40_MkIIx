#Embedded file name: /Users/versonator/Jenkins/live/Binary/Core_Release_64_static/midi-remote-scripts/_APC/SkinDefault.py
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color
from .Colors import Basic, Rgb, Pulse, Blink, BiLed


GREEN = Color(1)
GREEN_BLINK = Color(2)
RED = Color(3)
RED_BLINK = Color(4)
AMBER = Color(5)

class Defaults:
  class DefaultButton:
    On = Color(127)
    Off = Color(0)


class BiLedColors:
    class DefaultButton:
      On = Color(127)
      Off = Color(0)
    class Session:
        ClipStopped = AMBER
        ClipStarted = GREEN
        ClipRecording = RED
        ClipTriggeredPlay = GREEN_BLINK
        ClipTriggeredRecord = RED_BLINK
        ClipEmpty = Color(0)
        Scene = Color(0)
        SceneTriggered = GREEN_BLINK
        NoScene = Color(0)
        StopClip = Color(0)
        StopClipTriggered = GREEN_BLINK
        RecordButton = Color(0)

    class Zooming:
        Selected = AMBER
        Stopped = RED
        Playing = GREEN
        Empty = Color(0)


class RgbColors:
    class DrumGroup:
      PadSelected = Rgb.OCEAN
      PadSelectedNotSoloed = Rgb.OCEAN
      PadFilled = Rgb.YELLOW
      PadEmpty = Rgb.YELLOW.shade(2)
      PadMuted = Rgb.AMBER.shade(1)
      PadMutedSelected = Rgb.OCEAN.shade(1)
      PadSoloed = Rgb.BLUE
      PadSoloedSelected = Rgb.OCEAN.highlight()
      PadInvisible = Rgb.BLACK
      PadAction = Rgb.RED
    class LoopSelector:
      Playhead = Rgb.GREEN
      PlayheadRecord = Rgb.RED
      SelectedPage = Rgb.BLACK#Rgb.MAGENTA         # lew
      InsideLoopStartBar = Rgb.OCEAN
      InsideLoop = Rgb.CYAN
      OutsideLoop = Rgb.WHITE
    class DefaultButton:
      On = Color(127)
      Off = Color(0)
    class NoteEditor:
      class Step:
        Empty = Rgb.WHITE
        Low = Rgb.SKY.highlight()
        Medium = Rgb.SKY
        High = Rgb.OCEAN
        Full = Rgb.BLUE
        Muted = Rgb.AMBER.shade(2)
      class StepEditing:
        Low = Rgb.YELLOW.highlight()
        High = Rgb.YELLOW
        Full = Rgb.AMBER
        Muted = Rgb.WHITE
      StepSelected = Rgb.WHITE
      StepEmpty = Rgb.BLACK
      StepEmptyBase = Rgb.OCEAN.shade(2)
      StepEmptyScale = Rgb.DARK_GREY
      StepDisabled = Rgb.RED.shade(2)
      Playhead = Rgb.GREEN
      PlayheadRecord = Rgb.RED
      QuantizationSelected = Rgb.GREEN
      QuantizationUnselected = Rgb.YELLOW
      NoteBase = Rgb.OCEAN.shade(2)
      NoteScale = Rgb.DARK_GREY
      NoteNotScale = Rgb.BLACK
      NoteInvalid = Rgb.RED.shade(2)
    class Melodic:
      Playhead = Rgb.GREEN.shade(1)
      PlayheadRecord = Rgb.RED.shade(1)
    class Session:
      Scene = Rgb.GREEN
      SceneTriggered = Blink(Rgb.GREEN, Rgb.BLACK, 24)
      NoScene = Rgb.BLACK
      ClipStopped = Rgb.AMBER
      ClipStarted = Pulse(Rgb.GREEN.shade(1), Rgb.GREEN, 48)
      ClipRecording = Pulse(Rgb.BLACK, Rgb.RED, 48)
      ClipTriggeredPlay = Blink(Rgb.GREEN, Rgb.BLACK, 24)
      ClipTriggeredRecord = Blink(Rgb.RED, Rgb.BLACK, 24)
      ClipEmpty = Rgb.BLACK
      RecordButton = Rgb.BLACK
    class Zooming:
      Selected = Rgb.AMBER
      Stopped = Rgb.RED
      Playing = Rgb.GREEN
      Empty = Rgb.BLACK


class StopButtons:
    class Session:
        StopClip = Color(1)
        StopClipTriggered = Color(2)


class CrossfadeButtons:
    class Mixer:
        class Crossfade:
            Off = Color(0)
            A = Color(1)
            B = Color(2)

class Colors:

    class Option:
        Selected = BiLed.AMBER
        Unselected = BiLed.YELLOW_HALF
        On = BiLed.YELLOW
        Off = BiLed.OFF
        Unused = BiLed.OFF

    class List:
        ScrollerOn = BiLed.AMBER
        ScrollerOff = BiLed.AMBER_HALF

    class DefaultButton:
        On = Basic.FULL
        Off = Basic.HALF
        Disabled = Basic.OFF
        Alert = Basic.FULL_BLINK_SLOW

    class DefaultMatrix:
        On = Rgb.WHITE
        Off = Rgb.BLACK

    class Scales:
        Selected = BiLed.YELLOW
        Unselected = BiLed.GREEN_HALF
        FixedOn = BiLed.AMBER
        FixedOff = BiLed.YELLOW_HALF
        Diatonic = BiLed.AMBER
        Chromatic = BiLed.YELLOW_HALF

    class Instrument:
        NoteBase = Rgb.OCEAN
        NoteScale = Rgb.WHITE
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.BLACK
        Feedback = Rgb.GREEN
        FeedbackRecord = Rgb.RED.shade(1)
        NoteAction = Rgb.RED

    class Recording:
        On = Basic.FULL
        Off = Basic.HALF
        Transition = Basic.FULL_BLINK_FAST

    class Session:
        Scene = BiLed.GREEN
        SceneTriggered = BiLed.GREEN_BLINK_FAST
        NoScene = BiLed.OFF
        ClipStopped = Rgb.AMBER
        ClipStarted = Pulse(Rgb.GREEN.shade(1), Rgb.GREEN, 48)
        ClipRecording = Pulse(Rgb.BLACK, Rgb.RED, 48)
        ClipTriggeredPlay = Blink(Rgb.GREEN, Rgb.BLACK, 24)
        ClipTriggeredRecord = Blink(Rgb.RED, Rgb.BLACK, 24)
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED.shade(2)
        StopClip = Rgb.RED
        StopClipTriggered = Blink(Rgb.RED, Rgb.BLACK, 24)
        StoppedClip = Rgb.DARK_GREY

    class Zooming:
        Selected = Rgb.AMBER
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class TrackState:
        Common = Rgb.BLACK
        Stopped = Rgb.RED
        Disabled = Basic.OFF

    class DrumGroup:
        PadSelected = Rgb.OCEAN
        PadSelectedNotSoloed = Rgb.OCEAN
        PadFilled = Rgb.YELLOW
        PadEmpty = Rgb.YELLOW.shade(2)
        PadMuted = Rgb.AMBER.shade(1)
        PadMutedSelected = Rgb.OCEAN.shade(1)
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.OCEAN.highlight()
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.RED

    class LoopSelector:
        Playhead = Rgb.GREEN       # looper playhead
        PlayheadRecord = Rgb.RED#
        SelectedPage = Rgb.YELLOW.highlight()
        InsideLoopStartBar = Rgb.WHITE
        InsideLoop = Rgb.WHITE
        OutsideLoop = Rgb.WHITE   #Rgb.BLACK

    class NoteEditor:

        class Step:
            Low = Rgb.SKY.highlight()
            High = Rgb.OCEAN
            Full = Rgb.BLUE
            Muted = Rgb.AMBER.shade(2)

        class StepEditing:
            Low = Rgb.YELLOW.highlight()
            High = Rgb.YELLOW
            Full = Rgb.AMBER
            Muted = Rgb.WHITE

        StepSelected = Rgb.WHITE
        StepEmpty = Rgb.BLACK
        StepEmptyBase = Rgb.OCEAN.shade(2)
        StepEmptyScale = Rgb.DARK_GREY
        StepDisabled = Rgb.RED.shade(2)
        Playhead = Rgb.GREEN
        PlayheadRecord = Rgb.RED
        QuantizationSelected = BiLed.GREEN
        QuantizationUnselected = BiLed.YELLOW
        NoteBase = Rgb.OCEAN.shade(2)
        NoteScale = Rgb.DARK_GREY
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.RED.shade(2)

    class Melodic:
        Playhead = Rgb.GREEN.shade(1)
        PlayheadRecord = Rgb.RED.shade(1)

    class NoteRepeat:
        RateSelected = BiLed.RED
        RateUnselected = BiLed.YELLOW

    class Mixer:
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.DARK_GREY
        MuteOn = Rgb.DARK_GREY
        MuteOff = BiLed.YELLOW
        ArmSelected = BiLed.RED
        ArmUnselected = BiLed.RED_HALF

    class Browser:
        Load = BiLed.GREEN
        LoadNext = BiLed.YELLOW
        LoadNotPossible = BiLed.OFF
        Loading = BiLed.OFF

    class MessageBox:
        Cancel = BiLed.GREEN


def make_default_skin():
    return Skin(Defaults)

def make_custom_skin():
    return Skin(Colors)

def make_biled_skin():
    return Skin(BiLedColors)

def make_rgb_skin():
    return Skin(RgbColors)

def make_stop_button_skin():
    return Skin(StopButtons)

def make_crossfade_button_skin():
    return Skin(CrossfadeButtons)

