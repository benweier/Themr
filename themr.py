import sublime, sublime_plugin
import os

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		# TODO get list of theme files to build menu structure
		# TODO add command pallete options to select a theme
		self.list_themes()
		# TODO EventListener for new .sublime-theme files to dynamically rebuild menu?
		self.settings = sublime.load_settings("Global.sublime-settings")
		sublime.status_message("Themr: " + self.get_theme())

	def run(self, t):
		self.set_theme(t)

	def list_themes(self):
		# packages = os.listdir(sublime.packages_path())
		return

	def get_theme(self):
		return self.settings.get("theme", "Default.sublime-theme")

	def set_theme(self, t):
		# TODO set_setting to update checkbox on selected theme
		# run_command("set_setting", {"setting": "theme", "value": t})
		self.settings.set("theme", t)
		sublime.save_settings("Global.sublime-settings")
		if self.get_theme() == t:
			sublime.status_message("Themr: " + t)
		else:
			sublime.status_message("Error saving theme. The read/write operation may have failed.")
