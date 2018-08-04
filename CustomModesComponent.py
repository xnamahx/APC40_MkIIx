from _Framework.ModesComponent import LatchingBehaviour

class CustomReenterBehaviour(LatchingBehaviour):
    u"""
    Like latching, but calls a callback when the mode is-reentered.
    """

    def __init__(self, on_reenter=None, on_enter=None, *a, **k):
        super(CustomReenterBehaviour, self).__init__(*a, **k)
        if on_reenter is not None:
            self.on_reenter = on_reenter
        if on_enter is not None:
            self.on_enter = on_enter
        return

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(CustomReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self.on_reenter()
        else:
            self.on_enter()

    def on_reenter(self):
        pass

    def on_enter(self):
        pass