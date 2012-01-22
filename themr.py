import sublime, sublime_plugin

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		# TODO get list of theme files to build menu structure
		# TODO use command pallete to run a theme menu rebuild
		self.settings = sublime.load_settings("Global.sublime-settings")
		sublime.status_message("Themr: " + self.get_theme())

	def run(self, t):
		if self.get_theme() != t:
			self.set_theme(t)

	def list_themes(self):
		# packages = os.listdir(sublime.packages_path())
		return

	def get_theme(self):
		return self.settings.get("theme", "Default.sublime-theme")

	def set_theme(self, t):
		self.settings.set("theme", t)
		sublime.save_settings("Global.sublime-settings")
		if self.get_theme() == t:
			# TODO update checkbox on selected theme in menu
			sublime.status_message("Themr: " + t)
		else:
			sublime.status_message("Error saving theme. The read/write operation may have failed.")
