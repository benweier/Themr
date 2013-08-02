import sublime, sublime_plugin
import os, zipfile
from random import random

class Themr():
	preferences = 'Preferences.sublime-settings'

	def load_themes(self):
		themes = []

		try: # use find_resources() first for ST3
			for theme_resource in sublime.find_resources("*.sublime-theme"):
				filename = os.path.basename(theme_resource)
				name = filename.replace('.sublime-theme', '')
				themes.append(['Theme: ' + name, filename])

		except: # fallback to walk() for ST2
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

		themes.sort()
		return themes

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
		allow_preview = Themr.load('themr_allow_preview', False)
		self.user_selected = False
		try:
			the_index = [theme[1] for theme in themes].index(the_theme)
		except (ValueError):
			the_index = 0

		def on_done(index):
			if index != -1:
				Themr.save('theme', themes[index][1])
				sublime.status_message(themes[index][0])

		def on_select(index):
			if self.user_selected == True and allow_preview == True:
				Themr.save('theme', themes[index][1])
			else:
				self.user_selected = True

		try:
			self.window.show_quick_panel(themes, on_done, 0, the_index, on_select)
		except:
			self.window.show_quick_panel(themes, on_done)

class ThemrCycleThemesCommand(sublime_plugin.WindowCommand):
	def run(self, direction):
		themes = Themr.load_themes()
		the_theme = Themr.load('theme', 'Default.sublime-theme')
		index = 0
		the_index = [theme[1] for theme in themes].index(the_theme)
		num_of_themes = len(themes)

		if direction == 'next':
			index = the_index + 1 if the_index < num_of_themes - 1 else 0

		if direction == 'prev':
			index = the_index - 1 if the_index > 0 else num_of_themes - 1

		if direction == 'rand':
			index = int(random() * len(themes))

		Themr.save('theme', themes[index][1])
		sublime.status_message(themes[index][0])

class ThemrNextThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'next'})
class ThemrPreviousThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'prev'})
class ThemrRandomThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'rand'})
