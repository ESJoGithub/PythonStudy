class Controller:
  global sub_windows
  global sub_window
  sub_windows = {}

  def __init__():
    pass

  def show_subwin(_count):
    subwin_name = "window_" + _count
    subwin = sub_windows[subwin_name]
    subwin.frame.tkraise()

  def get_subwin(self, subwin=object, count=0):
    subwin_name = "window_" + str(count)
    sub_windows[subwin_name] = subwin