# GoToAnchor a Sublime Text 3 Plugin

## Description
Create anchors in your project for easily move in it.
Strongly based on [Open Url] (https://github.com/noahcoad/open-url/blob/master/README.md)

## How to use


* Create a anchor: ctrl/super+alt+z then ctrl/super+a or find "GOTOANCHOR: Create Anchor" from list of ST commands (ctrl/super+shift+p)
* Create a reference to the last anchor: ctrl/super+alt+z then ctrl/super+shift+a or find "GOTOANCHOR: Create Reference Last Anchor" from list of ST commands (ctrl/super+shift+p)
* Create a empty reference: ctrl/super+alt+z then ctrl/super+alt+a or find "Create Empty Reference" from list of ST commands (ctrl/super+shift+p)
* Re-create a reference to the anchor under the cursor: ctrl/super+alt+z then ctrl/super+shift+alt+a or find "GOTOANCHOR: Re-crate Reference From Current Anchor" from list of ST commands (ctrl/super+shift+p)

* Go to the closest previous reference: ctrl/super+alt+u or find "GOTOANCHOR: Find Prev Reference" from list of ST commands (ctrl/super+shift+p)
* Open: ctrl/super+u or find "GOTOANCHOR: Open Url" from list of ST commands (ctrl/super+shift+p) (if you are not in valid url will be run automatically "Go to the closest previous reference")

Inherited from [Open Url] (https://github.com/noahcoad/open-url/blob/master/README.md) (with some cut) you can open any URL, folder or file (the files will open by default except the extensions defined in go_to_anchor.sublime-settings)
