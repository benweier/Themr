import sublime, sublime_plugin
import os

class ChangeThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self, os):
		# TODO get list of theme files to build menu structure
		# TODO EventListener for new .sublime-theme files to rebuild menu?
		self.settings = sublime.load_settings("Global.sublime-settings")
		sublime.status_message("Themr: " + self.get_theme())
		self.list_themes()

	def run(self, t):
		self.set_theme(t)

	def list_themes(self):
		self.packages = os.listdir(sublime.packages_path())
		sublime.error_message(self.packages)

	def get_theme(self):
		return self.settings.get("theme", "Default.sublime-theme")

	def set_theme(self, t):
		if self.get_theme() == t:
			sublime.status_message("Themr: no change")
			# TODO set_setting to update checkbox on menu item
			# run_command("set_setting", {"setting": "theme", "value": t})
		else:
			self.settings.set("theme", t)
			sublime.save_settings("Global.sublime-settings")
			if self.get_theme() == t:
				sublime.status_message("Themr: " + t + " saved.")
			else:
				sublime.error_message("Error saving theme. The read/write operation may have failed.")
