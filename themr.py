import sublime, sublime_plugin
import os, zipfile

class Themr():
	def load_themes(self):
		themes = []

		for root, dirs, files in os.walk(sublime.packages_path()):
			for filename in (filename for filename in files if filename.endswith('.sublime-theme')):
					name = filename.replace('.sublime-theme', '')
					themes.append([name, filename])

		for root, dirs, files in os.walk(sublime.installed_packages_path()):
			for filename in (filename for filename in files if filename.startswith('Theme - ') and filename.endswith('.sublime-package')):
					package = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), filename))
					for f in (f for f in package.namelist() if f.endswith('.sublime-theme')):
						name = f.replace('.sublime-theme', '')
						themes.append([name, f])

		return themes

	def set_theme(self, s):
		self.settings().set('theme', s)
		sublime.save_settings('Preferences.sublime-settings')

	def get_theme(self):
		return self.settings().get('theme')

	def cycle_theme(self, d):
		themes = self.load_themes()
		the_theme = self.get_theme()
		the_index = [theme[1] for theme in themes].index(the_theme)
		num_of_themes = len(themes)

		if d == 1:
			index = the_index + 1 if the_index < num_of_themes - 1 else 0

		if d == -1:
			index = the_index - 1 if the_index > 0 else num_of_themes - 1

		self.set_theme(themes[index][1])
		sublime.status_message('Themr: ' + themes[index][1])

	def settings(self):
		return sublime.load_settings('Preferences.sublime-settings')

Themr = Themr()

class ThemrListThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		themes = Themr.load_themes()

		def on_done(index):
			if index != -1:
				Themr.set_theme(themes[index][1])

		self.window.show_quick_panel(themes, on_done)

class ThemrNextThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.cycle_theme(1)

class ThemrPrevThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.cycle_theme(-1)
