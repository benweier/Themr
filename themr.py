import sublime, sublime_plugin
import os

settings = sublime.load_settings('Preferences.sublime-settings')

class Themr():
	def load_themes(self):
		themes = []

		for root, dirs, files in os.walk(sublime.packages_path()):
			for filename in files:
				if filename.endswith('.sublime-theme'):
					name = os.path.basename(filename).replace('.sublime-theme', '')
					themes.append([name, name + '.sublime-theme'])

		return themes

	def set_theme(self, s):
		settings.set('theme', s)
		sublime.save_settings('Preferences.sublime-settings')

	def get_theme(self):
		return settings.get('theme')

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
