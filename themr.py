import sublime, sublime_plugin

def get_theme(t):
	s = sublime
	t = s.load_settings("Global.sublime-settings").get("theme", t)
	s.status_message(t)

def set_theme(t):
	s = sublime
	s.load_settings("Global.sublime-settings").set("theme", t)
	s.save_settings("Global.sublime-settings")

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def run(self, t):
		set_theme(t)
