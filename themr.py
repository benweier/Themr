import sublime, sublime_plugin
import os
import json

if sublime.version() <= 2174:
	pref = 'Preferences.sublime-settings'
else:
	pref = 'Global.sublime-settings'

def theme_data():
	settings = sublime.load_settings(pref)
	packages = os.listdir(sublime.packages_path())
	ignored_packages = settings.get('ignored_packages')
	themes = []
	menu = []

	for package in (package for package in packages if package.startswith('Theme -') and package not in ignored_packages):
		theme = os.listdir(os.path.join(sublime.packages_path(), package))

		for filename in (filenames for filenames in theme if filenames.endswith('.sublime-theme')):
			themes.append(filename)

	discovered_themes = {'discovered_themes': themes}
	s = open(os.path.join(sublime.packages_path(), 'Themr', 'themr.sublime-settings'), 'w')
	s.write(json.dumps(discovered_themes, indent = 4) + '\n')
	s.close

	for theme in themes:
		menu.append({'caption': 'Themr: ' + os.path.splitext(theme)[0], 'command': 'switch_theme', 'args': { 't': theme }})

	menu.append({'caption': 'Themr: Reload themes', 'command': 'reload_themes'})
	c = open(os.path.join(sublime.packages_path(), 'Themr', 'Default.sublime-commands'), 'w')
	c.write(json.dumps(menu, indent = 4) + '\n')
	c.close

	sublime.status_message('Themr: ' + str(len(themes)) + ' theme(s) found.')

class SwitchThemeCommand(sublime_plugin.ApplicationCommand):
	def __init__(self):
		sublime.set_timeout(theme_data, 3000)

	def run(self, t):
		self.settings = sublime.load_settings(pref)
		
		if self.get_theme() != t:
			self.set_theme(t)

	def get_theme(self):
		return self.settings.get('theme', 'Default.sublime-theme')

	def set_theme(self, t):
		self.settings.set('theme', t)
		sublime.save_settings(pref)
		sublime.status_message('Themr: ' + t)

class ReloadThemesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		theme_data()

class CycleThemesCommand(sublime_plugin.ApplicationCommand):
	def run(self, d):
		settings = sublime.load_settings(pref)
		themr = sublime.load_settings('themr.sublime-settings')
		theme = settings.get('theme')
		discovered_themes = themr.get('discovered_themes')

		i = discovered_themes.index(theme)

		try:
			t = discovered_themes[i + int(d)]
		except:
			t = discovered_themes[0]

		settings.set('theme', t)
		sublime.save_settings(pref)
