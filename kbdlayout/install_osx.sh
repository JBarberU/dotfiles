#!/bin/bash

function remap_home_end {
	
	# Turn off spaces and exposé and all of that crap
	defaults write com.apple.dock mcx-expose-disabled -bool true
	killall Dock
	echo "Don't forget to disable the keyboard shortcuts for switching workspaces..."

	DIR="$HOME/Library/KeyBindings"
	mkdir -p "$DIR"
	if [ -e "$DIR"/DefaultKeyBinding.dict ]; then 
		DATE=$(date "+%Y%m%d_%H%M")
		mv "$DIR"/DefaultKeyBinding.dict{,.backup"$DATE"}
	fi

	# See the following for more key bindings :)
	# http://osxnotes.net/keybindings.html
	echo "{
	/* Remap Home / End to be correct :-) */
	\"\UF729\"  = \"moveToBeginningOfLine:\";                   /* Home         */
	\"\UF72B\"  = \"moveToEndOfLine:\";                         /* End          */
	\"$\UF729\" = \"moveToBeginningOfLineAndModifySelection:\"; /* Shift + Home */
	\"$\UF72B\" = \"moveToEndOfLineAndModifySelection:\";       /* Shift + End  */

	\"^\Uf702\" = \"moveWordBackward\";							/** Control <- */
	\"$^\Uf702\" = \"moveWordBackwardAndModifySelection\";
	\"^\Uf703\" = \"moveWordForward\";
	\"$^\Uf703\" = \"moveWordForwardAndModifySelection\";

	\"^\Uf700\" = \"moveUp\";							/** Control <- */
	\"$^\Uf700\" = \"moveUpAndModifySelection\";
	\"^\Uf701\" = \"moveDown\";
	\"$^\Uf701\" = \"moveDownAndModifySelection\";
}" > "$DIR"/DefaultKeyBinding.dict
}

function cpy_layout {
	cp -R Swedish\ -\ Svdvorak.bundle /Library/Keyboard\ Layouts
}

remap_home_end
cpy_layout
