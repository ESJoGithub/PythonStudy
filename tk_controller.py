class Controller:
  global sub_windows
  global sub_window
  sub_windows = {}
  sub_window = None

  def __init__():
    pass

  def show_subwin(_count):
    subwin_name = "window_" + _count
    sub_window = sub_windows[subwin_name]
    sub_window.tkraise()

  def get_subwin(self, subwin, count):
    subwin_name = "window_" + str(count)
    sub_windows[subwin_name] = subwin
    sub_window = subwin