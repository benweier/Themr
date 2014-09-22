import sublime, sublime_plugin
import os, zipfile, re
from random import random

class Themr():
	def load_themes(self):
		all_themes = set()

		try: # use find_resources() first for ST3
			for theme_resource in sublime.find_resources('*.sublime-theme'):
				filename = os.path.basename(theme_resource)
				all_themes.add(filename)

		except: # fallback to walk() for ST2
			for root, dirs, files in os.walk(sublime.packages_path()):
				for filename in (filename for filename in files if filename.endswith('.sublime-theme')):
					all_themes.add(filename)

			for root, dirs, files in os.walk(sublime.installed_packages_path()):
				for package in (package for package in files if package.endswith('.sublime-package')):
					zf = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), package))
					for filename in (filename for filename in zf.namelist() if filename.endswith('.sublime-theme')):
						all_themes.add(filename)

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
		return sublime.load_settings('Preferences.sublime-settings').get('theme', 'Default.sublime-theme')

	def set_favorites(self, themes):
		sublime.load_settings('ThemrFavorites.sublime-settings').set('themr_favorites', themes)
		sublime.save_settings('ThemrFavorites.sublime-settings')

	def get_favorites(self):
		return sublime.load_settings('ThemrFavorites.sublime-settings').get('themr_favorites')

	# Look for "settings" keys within the theme file
	def load_theme_settings(self):
		the_theme = Themr.get_theme()
		pattern = re.compile(r'"settings":\s*\[(?:[, ]*"!?(\w+)")*\]')
		theme_settings = set()

		# Load the actual theme resource files
		resources = [sublime.load_resource(theme) for theme in sublime.find_resources(the_theme)]
		for resource in resources:
			for key in re.findall(pattern, resource):
				theme_settings.add(key)

		# Return a list of tuples with setting key and values
		return [(key, sublime.load_settings('Preferences.sublime-settings').get(key, False)) for key in theme_settings]

Themr = Themr()

	# Called when Sublime API is ready [ST3]
def plugin_loaded():
	print('themr ready')

	def on_theme_change():
		the_theme = Themr.get_theme()
		if sublime.find_resources(the_theme):
			Themr.theme = the_theme
		else:
			Themr.set_theme(Themr.theme)
			sublime.status_message('Theme not found. Reverting to ' + Themr.theme)

	def on_ignored_packages_change():
		the_theme = Themr.get_theme()
		if sublime.find_resources(the_theme):
			Themr.theme = the_theme
		else:
			Themr.set_theme('Default.sublime-theme')
			sublime.status_message('Theme disabled. Reverting to Default.sublime-theme')

	preferences = sublime.load_settings('Preferences.sublime-settings')

	preferences.add_on_change('theme', on_theme_change)
	preferences.add_on_change('ignored_packages', on_ignored_packages_change)

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

# Toggle one of the boolean settings used to customize current theme
class ThemrToggleSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		the_theme_settings = Themr.load_theme_settings()
		the_theme_settings.sort()
		theme_setting_list = []

		for setting in the_theme_settings:
			if setting[1]:
				theme_setting_list.append('Disable ' + setting[0] + u'   [\u2713]')
			else:
				theme_setting_list.append('Enable ' + setting[0] + u'   [\u2717]')

		# Toggles the setting key/val at the index specified
		def on_done(index):
			sublime.load_settings('Preferences.sublime-settings').set(the_theme_settings[index][0], not the_theme_settings[index][1])
			sublime.save_settings('Preferences.sublime-settings')

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
