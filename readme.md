# About
Themr allows you to quickly change your UI theme with keyboard shortcuts and the command palette. With Themr, you get commands to easily cycle forward, backward and randomly through your available themes.

# Features
* Full compatibility with Sublime Text 2 and 3.
* Automatically loads all available `.sublime-theme` files, including those found inside `.sublime-package` files. No need to restart Sublime Text or initiate a reload!

# Author's Note
When changing to or from some themes, Sublime Text may need be restarted to fully clear the old theme settings and apply the new theme settings.

# Installation
Install Schemr through [Package Control](http://wbond.net/sublime_packages/package_control) or download and extract it into your Packages folder.

# Usage
Select "Themr: List themes" from the command palette to display the available themes.
* Default binding: `Ctrl+Shift+F5` (Windows/Linux) `Cmd+Shift+F5` (OSX)

Skip to the next theme with the "Themr: Next theme" command.
* Default binding: `Ctrl+Shift+F7` (Windows/Linux) `Cmd+Shift+F7` (OSX)

Skip to the previous theme with the "Themr: Previous theme" command.
* Default binding: `Ctrl+Shift+F8` (Windows/Linux) `Cmd+Shift+F8` (OSX)

Select a random theme from the available themes with the "Themr: Random theme" command.
* Default binding: `Ctrl+Shift+F4` (Windows/Linux) `Cmd+Shift+F4` (OSX)

# Customisation
Themr's behaviour can be customised slightly by adding the following flag to your preferences file.
```json
"themr_allow_preview": true
```
This command will preview the selected theme while navigating through the theme list. The reason a flag is required is because of a known issue with some themes that causes the sidebar and tab settings to apply incorrectly. Use of this flag means you understand what you're getting into and that you've accepted the need to restart Sublime Text after changing theme.
