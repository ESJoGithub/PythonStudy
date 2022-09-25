class Controller:
  global sub_windows
  sub_windows = {}
  global current_can
  current_can = object

  def show_subwin(_count):
    subwin_name = "window_" + _count
    subwin = sub_windows[subwin_name]
    subwin.frame.tkraise()
    Controller.current_can = subwin

  def get_subwin(subwin=object, count=0):
    subwin_name = "window_" + str(count)
    sub_windows[subwin_name] = subwin