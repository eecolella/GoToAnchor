# GoToAnchor a Sublime Text 3 Plugin

## Description

Create anchors and references for easily move everywhere!

Inspirated on [Open Url] (https://github.com/noahcoad/open-url/blob/master/README.md) and [Search In Project] (https://github.com/leonid-shevtsov/SearchInProject_SublimeText)

## Introduction

* A anchor is like:
```js
// ANCHOR:some optional description ID:1394328786.442311
```

* A reference is like:
```js
// GOTOANCHOR:some optional description URL:'Absolute:\Path@1394328786.442311'
```

* Every anchor can point to file, folder or url
* N references can point to 1 anchor

## How to use

[![Alt text for your video](https://raw.github.com/eecolella/GoToAnchor/master/YouTubeImage.jpg)](http://www.youtube.com/watch?v=ikw48Jm7Q5g)

## Commands

###Go To Anchor
ctrl/super+u or find "GOTOANCHOR: Go To Anchor" from list of ST commands (ctrl/super+shift+p) (if you are not in valid url will be run automatically "Go to the closest previous reference")
###Search Anchor in Project
ctrl/super+shift+alt+u or find "GOTOANCHOR: Search Anchor" from list of ST commands (ctrl/super+shift+p)
###Go to the closest previous reference
ctrl/super+shift+u or find "GOTOANCHOR: Find Prev Reference" from list of ST commands (ctrl/super+shift+p) (if there isn&#39;t a previous reference re-start to find from the end of the file)
###Go to the closest previous anchor
ctrl/super+alt+u or find "GOTOANCHOR: Find Prev Anchor" from list of ST commands (ctrl/super+shift+p) (if there isn&#39;t a previous anchor re-start to find from the end of the file)



###Create a anchor
ctrl/super+alt+z then ctrl/super+a or find "GOTOANCHOR: Create Anchor" from list of ST commands (ctrl/super+shift+p)
###Create a reference to the last anchor
ctrl/super+alt+z then ctrl/super+shift+a or find "GOTOANCHOR: Create Reference Last Anchor" from list of ST commands (ctrl/super+shift+p)
###Create a empty reference
ctrl/super+alt+z then ctrl/super+alt+a or find "Create Empty Reference" from list of ST commands (ctrl/super+shift+p)
###Re-create a reference to the anchor under the cursor
ctrl/super+alt+z then ctrl/super+shift+alt+a or find "GOTOANCHOR: Re-create Reference From Current Anchor" from list of ST commands (ctrl/super+shift+p)


## PS
Inherited from [Open Url] (https://github.com/noahcoad/open-url/blob/master/README.md) (with some cut) you can open any URL, folder or file (the files will open by default except the extensions defined in go_to_anchor.sublime-settings)
