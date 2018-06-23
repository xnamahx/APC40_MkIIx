from pushbase import special_session_component

class CustomClipSlotCopyHandler(special_session_component.ClipSlotCopyHandler):

    def is_copying(self):
        return self._is_copying