import sublime, sublime_plugin
import os

class SwitchThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		# TODO get list of theme files to build menu structure
		# TODO use command pallete to run a theme menu rebuild
		self.settings = sublime.load_settings('Global.sublime-settings')
		sublime.status_message('Themr: ' + self.get_theme())
		self.themes = self.list_themes()

	def run(self, t):
		if self.get_theme() != t:
			self.set_theme(t)

	def list_themes(self):
		themes = []
		packages = os.listdir(sublime.packages_path())

		for package in (package for package in packages if package.startswith('Theme -')):
			theme = os.listdir(sublime.packages_path() + "\\" + package)

			for filename in (filenames for filenames in theme if filenames.endswith('.sublime-theme')):
				themes.append(filename)

		return themes

	def get_theme(self):
		return self.settings.get('theme', 'Default.sublime-theme')

	def set_theme(self, t):
		self.settings.set('theme', t)
		sublime.save_settings('Global.sublime-settings')
		if self.get_theme() == t:
			sublime.status_message('Themr: ' + t)
		else:
			sublime.status_message('Error saving theme. The read/write operation may have failed.')
