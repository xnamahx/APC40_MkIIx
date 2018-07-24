from .NoteSettingsComponent import NoteEditorSettingsComponent
from _APC.RingedEncoderElement import RING_SIN_VALUE
from .APCMessenger import APCMessenger

class NoteEditorSettingsComponent(NoteEditorSettingsComponent, APCMessenger):
  """ Customized to highlight specific encoders for APC """

  def set_encoders(self, encoders):
    super(NoteEditorSettingsComponent, self).set_encoders(encoders)
    if encoders:
      for i, encoder in enumerate(encoders):
        encoder._ring_mode_button.send_value(RING_SIN_VALUE, force=True)
        encoder.send_value(64, force=True)
