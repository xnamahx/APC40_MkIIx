from pushbase.special_session_component import ClipSlotCopyHandler
from pushbase.consts import MessageBoxText

class CustomClipSlotCopyHandler(ClipSlotCopyHandler):

    def is_copying(self):
        return self._is_copying

    def _perform_copy(self, target_clip_slot):
        if not target_clip_slot.is_group_slot:
            source_is_audio = self._source_clip_slot.clip.is_audio_clip
            target_track = target_clip_slot.canonical_parent
            if source_is_audio:
                if target_track.has_audio_input:
                    self._source_clip_slot.duplicate_clip_to(target_clip_slot)
                    self._on_duplicated(self._source_clip_slot, target_clip_slot)
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_AUDIO_CLIP_TO_MIDI_TRACK)
            elif not target_track.has_audio_input:
                self._source_clip_slot.duplicate_clip_to(target_clip_slot)
                self._on_duplicated(self._source_clip_slot, target_clip_slot)
            else:
                self._show_notification(MessageBoxText.CANNOT_COPY_MIDI_CLIP_TO_AUDIO_TRACK)
        else:
            self._show_notification(MessageBoxText.CANNOT_PASTE_INTO_GROUP_SLOT)



    def _finish_copying(self):
        self._reset_copying_state()
