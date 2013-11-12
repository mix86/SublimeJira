import sublime
import threading


class JiraApiCall(threading.Thread):
  def __init__(self, callback):
    self.callback = callback
    self.result = None
    threading.Thread.__init__(self)

  def run(self):
    try:
      self.payload()
      self.callback(self.result)
      return

    except Exception as e:
      err = "SublimeJira error: {}".format(e)

    sublime.error_message(err)
    self.result = False


