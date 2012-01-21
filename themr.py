import sublime, sublime_plugin

def get_theme(g):
	return sublime.load_settings(g).get("theme")

def set_theme(t, g):
	s = sublime
	s.load_settings(g).set("theme", t)
	s.save_settings(g)
	if get_theme(g) == t:
		s.status_message("Themr saved: " + t)
		s.window.run_command("set_setting", {"setting": "theme", "value": t})
	else:
		s.error_message("Error saving theme. The read/write operation may have failed.")

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		g = "Global.sublime-settings"
		sublime.status_message("Themr: " + get_theme(g))

	def run(self, t):
		g = "Global.sublime-settings"
		set_theme(t, g)
