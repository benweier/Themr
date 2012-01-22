import sublime, sublime_plugin

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		# TODO get list of theme files to build menu structure
		# TODO EventListener for new .sublime-theme files to rebuild menu?
		self.settings = sublime.load_settings("Global.sublime-settings")
		sublime.status_message("Themr: " + self.get_theme())

	def run(self, t):
		self.set_theme(t)

	def get_theme(self):
		# TODO better error checking, fallback to Default in case of failure?
		return self.settings.get("theme")

	def set_theme(self, t):
		# TODO check existing theme, don't save if theme is already set
		self.settings.set("theme", t)
		sublime.save_settings("Global.sublime-settings")
		if self.get_theme() == t:
			sublime.status_message("Themr saved: " + t)
			# TODO set_setting to update checkbox on menu item
			# run_command("set_setting", {"setting": "theme", "value": t})
		else:
			sublime.error_message("Error saving theme. The read/write operation may have failed.")
