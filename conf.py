import sublime

class ConfigLoader(object):

  def load(self):
    return sublime.load_settings("SublimeJira.sublime-settings")


settings = ConfigLoader().load
