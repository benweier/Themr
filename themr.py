import sublime, sublime_plugin
import os, zipfile
from random import random

class Themr():
	def load_themes(self):
		all_themes = []

		try: # use find_resources() first for ST3
			for theme_resource in sublime.find_resources('*.sublime-theme'):
				filename = os.path.basename(theme_resource)
				all_themes.append(filename)

		except: # fallback to walk() for ST2
			for root, dirs, files in os.walk(sublime.packages_path()):
				for filename in (filename for filename in files if filename.endswith('.sublime-theme')):
					all_themes.append(filename)

			for root, dirs, files in os.walk(sublime.installed_packages_path()):
				for package in (package for package in files if package.endswith('.sublime-package')):
					zf = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), package))
					for filename in (filename for filename in zf.namelist() if filename.endswith('.sublime-theme')):
						all_themes.append(filename)

		favorite_themes = self.get_favorites()
		themes = []

		for theme in all_themes:
			favorited = theme in favorite_themes
			pretty_name = 'Theme: ' + theme.replace('.sublime-theme', '')
			if favorited: pretty_name += u' \N{BLACK STAR}' # Put a pretty star icon next to favorited themes. :)
			themes.append([pretty_name, theme, favorited])

		themes.sort()
		return themes

	def list_themes(self, window, theme_list):
		themes = [[theme[0], theme[1]] for theme in theme_list]
		the_theme = self.get_theme()
		try:
			the_index = [theme[1] for theme in themes].index(the_theme)
		except (ValueError):
			the_index = 0

		def on_done(index):
			if index != -1:
				self.set_theme(themes[index][1])
				sublime.status_message(themes[index][0])

		try:
			window.show_quick_panel(themes, on_done, 0, the_index)
		except:
			window.show_quick_panel(themes, on_done)

	def cycle_themes(self, themes, direction):
		the_theme = Themr.get_theme()
		index = 0
		num_of_themes = len(themes)
		try:
			the_index = [theme[1] for theme in themes].index(the_theme)
		except (ValueError):
			the_index = 0

		if direction == 'next':
			index = the_index + 1 if the_index < num_of_themes - 1 else 0

		if direction == 'prev':
			index = the_index - 1 if the_index > 0 else num_of_themes - 1

		if direction == 'rand':
			index = int(random() * len(themes))

		Themr.set_theme(themes[index][1])
		sublime.status_message(themes[index][0])

	def set_theme(self, theme):
		sublime.load_settings('Preferences.sublime-settings').set('theme', theme)
		sublime.save_settings('Preferences.sublime-settings')

	def get_theme(self):
		return sublime.load_settings('Preferences.sublime-settings').get('theme')

	def set_favorites(self, themes):
		sublime.load_settings('ThemrFavorites.sublime-settings').set('themr_favorites', themes)
		sublime.save_settings('ThemrFavorites.sublime-settings')

	def get_favorites(self):
		return sublime.load_settings('ThemrFavorites.sublime-settings').get('themr_favorites')

Themr = Themr()

	# Called when Sublime API is ready [ST3]
def plugin_loaded():
	print('themr ready')

	the_theme = Themr.get_theme()
	if sublime.find_resources(the_theme):
		Themr.theme = the_theme
	else:
		Themr.set_theme('Default.sublime-theme')
		sublime.status_message('Theme not found. Reverting to Default.sublime-theme')

class ThemrListThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.list_themes(self.window, Themr.load_themes())

class ThemrListFavoriteThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.list_themes(self.window, [theme for theme in Themr.load_themes() if theme[2]])

	def is_enabled(self):
		return len(Themr.get_favorites()) > 0

class ThemrCycleThemesCommand(sublime_plugin.WindowCommand):
	def run(self, direction):
		Themr.cycle_themes(Themr.load_themes(), direction)

class ThemrCycleFavoriteThemesCommand(sublime_plugin.WindowCommand):
	def run(self, direction):
		Themr.cycle_themes([theme for theme in Themr.load_themes() if theme[2]], direction)

	def is_enabled(self):
		return len(Themr.get_favorites()) > 1

class ThemrFavoriteCurrentThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme = Themr.get_theme()
		favorites = Themr.get_favorites()
		favorites.append(the_theme)
		Themr.set_favorites(favorites)
		sublime.status_message(the_theme + ' added to favorites')

	def is_enabled(self):
		return Themr.get_theme() not in Themr.get_favorites()

class ThemrUnfavoriteCurrentThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme = Themr.get_theme()
		favorites = Themr.get_favorites()
		favorites.remove(the_theme)
		Themr.set_favorites(favorites)
		sublime.status_message(the_theme + ' removed from favorites')

	def is_enabled(self):
		return Themr.get_theme() in Themr.get_favorites()

class ThemrNextThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'next'})
class ThemrPreviousThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'prev'})
class ThemrRandomThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'rand'})
