import sublime, sublime_plugin
import os
import json

themr = os.getcwd()

class SwitchThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		# TODO get list of theme files to build menu structure
		# TODO use command pallete to run a theme menu rebuild
		self.settings = sublime.load_settings('Global.sublime-settings')
		sublime.status_message('Themr: ' + self.get_theme())
		
		self.themes = self.list_themes()
		self.build_theme_data()

	def run(self, t):
		if self.get_theme() != t:
			self.set_theme(t)

	def list_themes(self):
		themes = []
		packages = os.listdir(sublime.packages_path())

		for package in (package for package in packages if package.startswith('Theme -')):
			theme = os.listdir(sublime.packages_path() + '\\' + package)

			for filename in (filenames for filenames in theme if filenames.endswith('.sublime-theme')):
				themes.append(filename)

		return themes

	def build_theme_data(self):
		data = []

		for theme in self.themes:
			data.append({'caption': 'Themr: ' + os.path.splitext(theme)[0], 'command': 'switch_theme', 'args': { 't': theme }})
			commands = json.dumps(data, indent = 4)

		f = open(themr + "\\" + "Default.sublime-commands", 'w')
		f.write(commands + "\n")
		f.close

	def get_theme(self):
		return self.settings.get('theme', 'Default.sublime-theme')

	def set_theme(self, t):
		self.settings.set('theme', t)
		sublime.save_settings('Global.sublime-settings')
		if self.get_theme() == t:
			sublime.status_message('Themr: ' + t)
		else:
			sublime.status_message('Error saving theme. The read/write operation may have failed.')
