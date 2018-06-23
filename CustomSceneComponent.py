from _Framework.SceneComponent import SceneComponent
from .CustomClipSlotComponent import CustomClipSlotComponent as ClipSlotComponent

class CustomSceneComponent(SceneComponent):

  clip_slot_component_type = ClipSlotComponent
  _delete_button = None

  def _create_clip_slot(self):
    return self.clip_slot_component_type()

