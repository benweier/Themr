import sublime, sublime_plugin
import os, zipfile, re
from random import random

PREFERENCES = 'Preferences.sublime-settings'
FAVORITES = 'ThemrFavorites.sublime-settings'
DEFAULT_THEME = 'Default.sublime-theme'

is_ST2 = int(sublime.version()) < 3000

class Themr(object):
	_instance = None

	@classmethod
	def instance(cls):
		if not cls._instance:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.preferences = sublime.load_settings(PREFERENCES)
		self.favorites = sublime.load_settings(FAVORITES)
		self.theme = self.preferences.get('theme', DEFAULT_THEME)

		def check_theme():
			""" Check the theme can be set and revert to the previous or default theme if invalid """

			the_theme = self.get_theme()
			themes = self.find_themes()

			if the_theme in themes:
				self.theme = the_theme
			else:
				if self.theme in themes:
					self.set_theme(self.theme)
					sublime.status_message('Theme not found. Reverting to ' + self.theme)
				else:
					self.set_theme(DEFAULT_THEME)
					sublime.status_message('Theme not found. Reverting to ' + DEFAULT_THEME)

		if self.preferences.get('themr_watch_settings', True):
			self.preferences.add_on_change('themr', check_theme)
			check_theme() # run once at startup to validate theme setting

	def find_themes(self):
		""" Return a set of all .sublime-theme files in the Sublime Text package folders """

		themes = set()

		try: # use find_resources() first for ST3
			for theme_resource in sublime.find_resources('*.sublime-theme'):
				filename = os.path.basename(theme_resource)
				themes.add(filename)

		except: # fallback to walk() for ST2
			for root, dirs, files in os.walk(sublime.packages_path()):
				for filename in (filename for filename in files if filename.endswith('.sublime-theme')):
					themes.add(filename)

			for root, dirs, files in os.walk(sublime.installed_packages_path()):
				for package in (package for package in files if package.endswith('.sublime-package')):
					zf = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), package))
					for filename in (filename for filename in zf.namelist() if filename.endswith('.sublime-theme')):
						themes.add(filename)

		return themes

	def load_themes(self):
		""" Return a list of all .sublime-theme files with favorites flagged """

		all_themes = self.find_themes()
		favorite_themes = self.get_favorites()
		themes = []

		for theme in all_themes:
			favorited = theme in favorite_themes
			pretty_name = 'Theme: ' + theme.replace('.sublime-theme', '')
			if favorited: pretty_name += u'   \u2605' # Put a pretty star icon next to favorited themes. :)
			themes.append([pretty_name, theme, favorited])

		themes.sort()
		return themes

	def list_themes(self, window, theme_list):
		""" Display a quick panel with the contents of the theme_list """

		themes = [[theme[0], theme[1]] for theme in theme_list]
		the_theme = self.get_theme()
		try:
			the_index = [theme[1] for theme in themes].index(the_theme)
		except (ValueError):
			the_index = 0

		def on_done(index):
			""" Set the selected theme """

			if index != -1:
				self.set_theme(themes[index][1])
				sublime.status_message(themes[index][0])

		try:
			window.show_quick_panel(themes, on_done, 0, the_index)
		except:
			window.show_quick_panel(themes, on_done)

	def cycle_themes(self, themes, direction):
		""" Adjust the selected theme in the given direction """

		the_theme = Themr.instance().get_theme()
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

		Themr.instance().set_theme(themes[index][1])
		sublime.status_message(themes[index][0])

	def set_theme(self, theme):
		""" Save the theme value """

		self.preferences.set('theme', theme)
		sublime.save_settings(PREFERENCES)

	def get_theme(self):
		""" Return the current theme value """

		return self.preferences.get('theme', DEFAULT_THEME)

	def set_favorites(self, themes):
		""" Save the favorites theme list """

		self.favorites.set('themr_favorites', themes)
		sublime.save_settings(FAVORITES)

	def get_favorites(self):
		""" Return the current favorites list """

		return self.favorites.get('themr_favorites')

	# Look for "settings" keys within the theme file
	def load_theme_settings(self):
		""" Parse the .sublime-theme file for any settings keys """

		the_theme = Themr.instance().get_theme()
		pattern = re.compile(r'"settings":\s*\[(?:[, ]*"!?(\w+)")*\]')
		theme_settings = set()

		# Load the actual theme resource files
		resources = [sublime.load_resource(theme) for theme in sublime.find_resources(the_theme)]
		for resource in resources:
			for key in re.findall(pattern, resource):
				theme_settings.add(key)

		# Return a list of tuples with setting key and values
		return [(key, self.preferences.get(key, False)) for key in theme_settings]

	# Called when Sublime API is ready [ST3]
def plugin_loaded():
	Themr.instance()

def plugin_unloaded():
	Themr.instance().preferences.clear_on_change('themr')

class ThemrListThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.instance().list_themes(self.window, Themr.instance().load_themes())

class ThemrListFavoriteThemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		Themr.instance().list_themes(self.window, [theme for theme in Themr.instance().load_themes() if theme[2]])

	def is_enabled(self):
		return len(Themr.instance().get_favorites()) > 0

class ThemrCycleThemesCommand(sublime_plugin.WindowCommand):
	def run(self, direction):
		Themr.instance().cycle_themes(Themr.instance().load_themes(), direction)

class ThemrCycleFavoriteThemesCommand(sublime_plugin.WindowCommand):
	def run(self, direction):
		Themr.instance().cycle_themes([theme for theme in Themr.instance().load_themes() if theme[2]], direction)

	def is_enabled(self):
		return len(Themr.instance().get_favorites()) > 1

class ThemrFavoriteCurrentThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme = Themr.instance().get_theme()
		favorites = Themr.instance().get_favorites()
		favorites.append(the_theme)
		Themr.instance().set_favorites(favorites)
		sublime.status_message(the_theme + ' added to favorites')

	def is_enabled(self):
		return Themr.instance().get_theme() not in Themr.instance().get_favorites()

class ThemrUnfavoriteCurrentThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme = Themr.instance().get_theme()
		favorites = Themr.instance().get_favorites()
		favorites.remove(the_theme)
		Themr.instance().set_favorites(favorites)
		sublime.status_message(the_theme + ' removed from favorites')

	def is_enabled(self):
		return Themr.instance().get_theme() in Themr.instance().get_favorites()

# Toggle one of the boolean settings used to customize current theme
class ThemrToggleSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme_settings = Themr.instance().load_theme_settings()
		the_theme_settings.sort()
		theme_setting_list = []

		for setting in the_theme_settings:
			if setting[1]:
				theme_setting_list.append('Disable ' + setting[0] + u'   [\u2713]')
			else:
				theme_setting_list.append('Enable ' + setting[0] + u'   [\u2717]')

		# Toggles the setting key/val at the index specified
		def on_done(index):
			Themr.instance().preferences.set(the_theme_settings[index][0], not the_theme_settings[index][1])
			sublime.save_settings(PREFERENCES)

			if the_theme_settings[index][1]:
				sublime.status_message('Themr: Disabled ' + the_theme_settings[index][0])
			else:
				sublime.status_message('Themr: Enabled ' + the_theme_settings[index][0])

		self.window.show_quick_panel(theme_setting_list, on_done)

	def is_enabled(self):
		return int(sublime.version()) >= 3000

class ThemrNextThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'next'})
class ThemrPreviousThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'prev'})
class ThemrRandomThemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.run_command('themr_cycle_themes', {'direction': 'rand'})

if is_ST2: plugin_loaded()

unload_handler = plugin_unloaded if is_ST2 else lambda: None
