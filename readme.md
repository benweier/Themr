## About
Themr allows you to quickly change your UI theme using the command palette or keyboard shortcuts. With Themr, you get commands to easily cycle forward, backward and randomly through your available themes.

## Features
* Full compatibility with Sublime Text 2 and 3.
* Allows themes to be favorited for even faster access.
* Automatically loads all available `.sublime-theme` files, including those found inside `.sublime-package` files. No need to restart Sublime Text or initiate a reload!
* Registers a callback when the `theme` setting is changed to protect against saving an invalid filename (e.g. when manually editing the `Preferences.sublime-settings` file).
* Configure all customizable theme settings without checking the theme readme or manually scanning the theme file with a real-time preview via quick panel.

## Author's Note
When changing to or from some themes, Sublime Text may need be restarted to fully clear the old theme settings and apply the new theme settings. Switching themes within the same family (e.g. Soda Light <-> Soda Dark) usually doesn't cause any issues.

## Installation
Install Themr through [Package Control](https://sublime.wbond.net/) or download and extract it into your Sublime Text `Packages` folder.

## Contributors
Toggle Theme Settings by [Eibbor](https://github.com/eibbors)

## Usage

**Themr: List themes** displays all the available themes in alphabetical order.

* Default binding: <kbd>Ctrl+F5</kbd> (Windows/Linux) <kbd>Cmd+F5</kbd> (OSX)

**Themr: Next theme** switches immediately to the alphabetically next theme.

* Default binding: <kbd>Ctrl+F7</kbd> (Windows/Linux) <kbd>Cmd+F7</kbd> (OSX)

**Themr: Previous theme** switches immediately to the alphabetically previous theme.

* Default binding: <kbd>Ctrl+F8</kbd> (Windows/Linux) <kbd>Cmd+F8</kbd> (OSX)

**Themr: Random theme** switches immediately to a random theme that you have installed.

* Default binding: <kbd>Ctrl+F10</kbd> (Windows/Linux) <kbd>Cmd+F10</kbd> (OSX)

### Favorites

**Themr: Add current theme to favorites** and **Themr: Remove current theme from favorites** add and remove the currently selected theme to your favorites list.

* You can also edit your favorites list manually through **Preferences > Package Settings > Themr**.

**Themr: List favorite themes** displays your favorite themes in alphabetical order.

* Default binding: <kbd>Ctrl+Shift+F5</kbd> (Windows/Linux) <kbd>Cmd+Shift+F5</kbd> (OSX)

**Themr: Next favorite theme** switches immediately to the alphabetically next theme in your favorites.

* Default binding: <kbd>Ctrl+Shift+F7</kbd> (Windows/Linux) <kbd>Cmd+Shift+F7</kbd> (OSX)

**Themr: Previous favorite theme** switches immediately to the alphabetically previous theme in your favorites.

* Default binding: <kbd>Ctrl+Shift+F8</kbd> (Windows/Linux) <kbd>Cmd+Shift+F8</kbd> (OSX)

**Themr: Random favorite theme** switches immediately to a random theme in your favorites.

* Default binding: <kbd>Ctrl+Shift+F10</kbd> (Windows/Linux) <kbd>Cmd+Shift+F10</kbd> (OSX)

### Other

**Themr: Toggle Theme Settings** displays a list of settings supported by your current theme to preview changes in real time
