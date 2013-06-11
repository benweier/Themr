import sublime, sublime_plugin
import os, zipfile
from random import random

class Themr():
	preferences = 'Preferences.sublime-settings'

	def load_themes(self):
		themes = []

		for root, dirs, files in os.walk(sublime.packages_path()):
			for filename in (filename for filename in files if filename.endswith('.sublime-theme')):
				name = filename.replace('.sublime-theme', '')
				themes.append(['Theme: ' + name, filename])

		for root, dirs, files in os.walk(sublime.installed_packages_path()):
			for package in (package for package in files if package.endswith('.sublime-package')):
				zf = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), package))
				for filename in (filename for filename in zf.namelist() if filename.endswith('.sublime-theme')):
					name = os.path.basename(filename).replace('.sublime-theme', '')
					themes.append(["Theme: " + name, filename])

		default_theme = os.path.join(os.getcwd(), 'Packages', 'Theme - Default.sublime-package')
		if os.path.exists(default_theme):
			themes.append(["Theme: Default", "Default.sublime-theme"])

		themes.sort()
		return themes

	def cycle_theme(self, direction):
		themes = self.load_themes()
		the_theme = self.load('theme', 'Default.sublime-theme')
		index = 0
		the_index = [theme[1] for theme in themes].index(the_theme)
		num_of_themes = len(themes)

		if direction == 'next':
			index = the_index + 1 if the_index < num_of_themes - 1 else 0

		if direction == 'prev':
			index = the_index - 1 if the_index > 0 else num_of_themes - 1

		if direction == 'rand':
			index = int(random() * len(themes))

		self.save('theme', themes[index][1])
		sublime.status_message(themes[index][0])

	def save(self, setting, value):
		sublime.load_settings(self.preferences).set(setting, value)
		sublime.save_settings(self.preferences)

	def load(self, setting, default):
		return sublime.load_settings(self.preferences).get(setting, default)

Themr = Themr()

class ThemrListThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		themes = Themr.load_themes()
		the_theme = Themr.load('theme', 'Default.sublime-theme')
		try:
			the_index = [theme[1] for theme in themes].index(the_theme)
		except (ValueError):
			the_index = 0

		def on_done(index):
			if index != -1:
				Themr.save('theme', themes[index][1])

		try:
			self.window.show_quick_panel(themes, on_done, 0, the_index)
		except:
			self.window.show_quick_panel(themes, on_done)

class ThemrNextThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.cycle_theme('next')

class ThemrPreviousThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.cycle_theme('prev')

class ThemrRandomThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.cycle_theme('rand')
