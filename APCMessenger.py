from _Framework.Dependency import dependency

class APCMessenger(object):
  log_message = dependency(log_message=None)
  control_surface = dependency(control_surface=None)
