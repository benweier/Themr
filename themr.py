import sublime, sublime_plugin
import os
import json

themr = os.getcwd()

if sublime.arch() == 'windows':
	sep = '\\'
else:
	sep = '/'

def theme_data():
	packages = os.listdir(sublime.packages_path())
	themes = []
	data = []

	for package in (package for package in packages if package.startswith('Theme -')):
		dirs = os.listdir(sublime.packages_path() + sep + package)

		for filename in (filenames for filenames in dirs if filenames.endswith('.sublime-theme')):
			themes.append(filename)

	sublime.status_message('Themr: ' + str(len(themes)) + ' themes found.')

	for theme in themes:
		data.append({'caption': 'Themr: ' + os.path.splitext(theme)[0], 'command': 'switch_theme', 'args': { 't': theme }})

	data.append({'caption': 'Themr: Scan Themes', 'command' : 'scan_themes'})
	commands = json.dumps(data, indent = 4)

	f = open(themr + sep + 'Default.sublime-commands', 'w')
	f.write(commands + '\n')
	f.close

class SwitchThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		self.settings = sublime.load_settings('Global.sublime-settings')
		theme_data()

	def run(self, t):
		if self.get_theme() != t:
			self.set_theme(t)

	def get_theme(self):
		return self.settings.get('theme', 'Default.sublime-theme')

	def set_theme(self, t):
		self.settings.set('theme', t)
		sublime.save_settings('Global.sublime-settings')

		if self.get_theme() == t:
			sublime.status_message('Themr: ' + t)
		else:
			sublime.status_message('Error saving theme. The read/write operation may have failed.')

class ScanThemesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		theme_data()
