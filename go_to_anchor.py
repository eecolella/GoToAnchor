# GoToAnchor
# Create anchors and references for easily move everywhere!
# Hosted at https://github.com/eecolella/GoToAnchor

import sublime, sublime_plugin
import urllib, urllib.parse, time, re, webbrowser
import os.path, os, sys, inspect

### Start of fixing import paths
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if script is called in different ways on Windows
 # __file__ fails if someone does os.chdir() before
 # sys.argv[0] also fails because it doesn't not always contains the path
### End of fixing import paths

import searchengines

SETTINGS = 'go_to_anchor.sublime-settings'
GoToLastAnchor = ''
basedir = os.getcwd()

class GoToAnchorCommand(sublime_plugin.TextCommand):
	debug = False

	# method: go_to_url
	# method: find_prev_something
	def run(self, edit, method="open_url", something="GOTOANCHOR"):

		if self.debug:
			print("\n\nDEBUG START ### go_to_anchor." + method + " ###")
			print("DEBUG: method: ", method)
			print("DEBUG: something: ", something)

		if method == "go_to_url":
			self.go_to_url(edit)
		elif method == "find_prev_something":
			self.find_prev_something(something)

	def go_to_url(self, edit):
		view = self.view		

		# select text under cursor
		url = self.selection()
			

		# strip quotes if quoted
		if (url.startswith("\"") & url.endswith("\"")) | (url.startswith("\'") & url.endswith("\'")):
			url = url[1:-1]

		# if is in a GOTOANCHOR line re-select the url
		if url == 'GOTOANCHOR': 
			line = view.lines(sublime.Region(view.sel()[0].begin(), view.sel()[0].begin()))[0]
			lineStr = view.substr(line)
			url = lineStr.split('\'')[1]

		# try to find a Anchor Id and if so split url and id
		idAnchor = ''
		iSharp = url.find('@')
		if iSharp >= 0:
			idAnchor = url[iSharp+1:len(url)]
			url = url[0:iSharp]

		# find the relative path to the current file
		try:
			relative_path = os.path.normpath(os.path.join(os.path.dirname(view.file_name()), url))
		except TypeError:
			relative_path = None

		# if this is a directory, show it (absolute or relative)
		# if it is a path to a file, open the file in sublime (absolute or relative)
		# if it is a URL, open in browser
		# otherwise find prev GOTOANCHOR		
		view.run_command('side_bar_open');

		# debug info
		if self.debug and True:
			print("DEBUG: url: ", url)
			print("DEBUG: idAnchor: ", idAnchor)
			print("DEBUG: relative_path: ", relative_path)

		if url:

			if os.path.isdir(url):
				os.startfile(url)

			elif relative_path and os.path.isdir(relative_path):
				os.startfile(relative_path)

			elif os.path.exists(url):
				self.open_file(url, idAnchor)

			elif os.path.exists(os.path.expandvars(url)):
				self.open_file(os.path.expandvars(url), idAnchor)

			elif relative_path and os.path.exists(relative_path):
				self.open_file(relative_path, idAnchor)

			else:
				if "://" in url:
					webbrowser.open_new_tab(url)				
				elif re.search(r"\w[^\s]*\.(?:" + sublime.load_settings(SETTINGS).get('reg_exp_domains') + ")[^\s]*\Z", url):
					if not "://" in url:
						url = "http://" + url
					webbrowser.open_new_tab(url)
				else:
					self.find_prev_something()
		
		else:
			self.find_prev_something()

	# pulls the current selection or url under the cursor
	def selection(self):
		view = self.view

		s = view.sel()[0]

		# expand selection to possible URL
		start = s.a
		end = s.b

		# if nothing is selected, expand selection to nearest terminators
		if (start == end):
			view_size = view.size()
			terminator = list('\t\"\'><, []()')

			# move the selection back to the start of the url
			while (start > 0
					and not view.substr(start - 1) in terminator
					and view.classify(start) & sublime.CLASS_LINE_START == 0):
				start -= 1

			# move end of selection forward to the end of the url
			while (end < view_size
					and not view.substr(end) in terminator
					and view.classify(end) & sublime.CLASS_LINE_END == 0):
				end += 1

		# grab the URL
		return view.substr(sublime.Region(start, end)).strip()

	def open_file(self, file, idAnchor):

		if re.search(r"\w[^\s]*\.(?:" + sublime.load_settings(SETTINGS).get('reg_exp_file_to_tun') + ")[^\s]*\Z", file):

			#run file
			os.system("\"" + file + "\"")

		else:
			if file == self.view.file_name():
				self.find_anchor_same_file(idAnchor)

			else:
				view_opened_file = self.view.window().open_file(file)
				sublime.set_timeout(lambda: self.find_anchor(view_opened_file, idAnchor), 10)

	def find_anchor(self, view_opened_file, idAnchor):

		# fix for find in the same file with the anchor after the reference
		idAnchor = "ID:" + idAnchor

		if not view_opened_file.is_loading():
			match = view_opened_file.find(idAnchor, 0, sublime.LITERAL | sublime.IGNORECASE)

			# calc new cursor position
			point = view_opened_file.lines(match)[0].end() + 1
			newMach = sublime.Region(point, point)

			# move cursor in position mach
			view_opened_file.sel().clear()
			view_opened_file.sel().add(newMach)
			view_opened_file.show_at_center(newMach) 

			sublime.set_timeout(lambda: view_opened_file.show_at_center(newMach), 10)
		else:
			sublime.set_timeout(lambda: self.find_anchor(view_opened_file, idAnchor), 10)

	def find_anchor_same_file(self, idAnchor):

		# fix for find in the same file with the anchor after the reference
		idAnchor = "ID:" + idAnchor

		view = self.view
	
		match = view.find(idAnchor, 0, sublime.LITERAL | sublime.IGNORECASE)

		# calc new cursor position
		point = view.lines(match)[0].end() + 1
		newMach = sublime.Region(point, point)

		# move cursor in position mach
		view.sel().clear()
		view.sel().add(newMach)
		view.show_at_center(newMach) 

	def find_prev_something(self, something='GOTOANCHOR'):
		

		if self.debug:
			print("DEBUG: something: ", something)
			
		view = self.view
		maches = view.find_all(something)
		current = view.sel()[0]
		mach = current
		flag = True

		if self.debug:
			print("DEBUG: maches: ", maches)

		for index in range(len(maches)):
			if ( maches[index].begin() < current.begin() ):
				mach = maches[index]
				flag = False

		if flag and len(maches) > 0:
			mach = maches[len(maches) - 1]
			

		if self.debug:
			print("DEBUG: mach: ", mach)
			
		# move cursor in position mach
		view.sel().clear()
		view.sel().add(mach)
		view.show_at_center(mach) 

class GenerateAnchorCommand(sublime_plugin.TextCommand):
	debug = False
	# method: create_anchor
	# method: create_gotoanchor_last
	# method: create_gotoanchor_empty
	# method: re_create_gotoanchor
	def run(self, edit, method="create_anchor"):

		if self.debug:
			print("\n\nDEBUG START ### generate_anchor." + method + " ###")

		if method == "create_anchor":
			self.create_anchor(edit)
		elif method == "create_gotoanchor_last":
			self.create_gotoanchor_last(edit)
		elif method == "create_gotoanchor_empty":
			self.create_gotoanchor_empty(edit)
		elif method == "re_create_gotoanchor":
			self.re_create_gotoanchor(edit)

	def create_anchor(self, edit):
		global GoToLastAnchor

		view = self.view

		# create id by current date
		idAnchor = "%s" % time.time()

		# create comment
		view.run_command('toggle_comment', { "block": False });
		
		# insert text
		view.insert(edit, view.sel()[0].begin(), "ANCHOR: ID:" + idAnchor)

		# calc cursor position
		point = view.sel()[0].begin() - len(idAnchor) - 4
		newPosition = sublime.Region(point, point)

		# move cursor in position
		view.sel().clear()
		view.sel().add(newPosition)
		view.show_at_center(newPosition) 

		# save text in global variable
		GoToLastAnchor = "GOTOANCHOR: URL:'%s@%s'" % (view.file_name(), idAnchor)

	def create_gotoanchor_last(self, edit):
		view = self.view

		# create comment
		view.run_command('toggle_comment', { "block": False });
		
		# insert GOTOANCHOR text of the last anchor created
		view.insert(edit, view.sel()[0].begin(), GoToLastAnchor)


	def create_gotoanchor_empty(self, edit):
		view = self.view

		# create comment
		view.run_command('toggle_comment', { "block": False });

		# insert GOTOANCHOR text with empty url
		view.insert(edit, view.sel()[0].begin(), "GOTOANCHOR: URL:")


	def re_create_gotoanchor(self, edit):
		global GoToLastAnchor
		view = self.view

		line = view.lines(sublime.Region(view.sel()[0].begin(), view.sel()[0].begin()))[0]
		lineStr = view.substr(line)
		idAnchor = lineStr[lineStr.find("ID")+3:]

		if self.debug:
			print("DEBUG: lineStr: %s" % lineStr)
			print("DEBUG: idAnchor: %s" % idAnchor)

		# save text in global variable
		GoToLastAnchor = "GOTOANCHOR: URL:'%s@%s'" % (view.file_name(), idAnchor)

class SearchAnchorCommand(sublime_plugin.WindowCommand):

    debug = False
    lastSelected = None

    def __init__(self, window):
        self.window = window;
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''
        pass

    def run(self):

        if self.debug:
            print("\n\nDEBUG START ### SearchInProjectCommand. ###")

        self.settings = sublime.load_settings('SearchInProject.sublime-settings')
        self.engine_name = self.settings.get("search_in_project_engine")
        pushd = os.getcwd()
        os.chdir(basedir)
        __import__("searchengines.%s" % self.engine_name)
        self.engine = searchengines.__dict__[self.engine_name].engine_class(self.settings)
        os.chdir(pushd)

        self.perform_search('ANCHOR')

    def perform_search(self, text):
        self.last_search_string = text
        folders = self.search_folders()

        self.common_path = self.find_common_path(folders)
        self.results = self.engine.run(text, folders)
        if self.results:

            if self.debug and False:
                print("\nDEBUG: self.results before fix: ", self.results)

            self.results = [[result[0].replace(self.common_path.replace('\"', ''), ''), result[1]] for result in self.results]
            self.results.remove(self.results[0])

            for index in range(len(self.results)):
                temp = self.results[index][0]
                self.results[index][0] = re.search("(?<=ANCHOR:)(.*)(?=ID:)", self.results[index][1]).group(1).strip()
                self.results[index][1] = temp

            if self.debug and False:
                print("\nDEBUG: self.results after fix: ", self.results)


            arrayTempViewOpen = []
            arrayTempPathViewOpen = []

            self.lastSelected = None
            self.window.show_quick_panel(self.results, None, 0, -1, self.on_select)
        else:
            self.results = []
            self.window.show_quick_panel(["No results"], None)                         

    def on_select(self, file_no=None):
        if file_no != -1:
            # go to anchor
            file_name = self.common_path.replace('\"', '') + self.results[file_no][1]
            view = self.window.open_file(file_name, sublime.ENCODED_POSITION)

            # store the view in first interaction
            if self.lastSelected == None:
                self.lastSelected = view

            # if the match is in another file
            elif view.file_name() != self.lastSelected.file_name():
                # close the last
                self.window.focus_view(self.lastSelected)
                self.window.run_command("close")
                # re-focus in the current
                self.window.focus_view(view)
                # store the new view
                self.lastSelected = view

    def search_folders(self):
        window_folders = self.window.folders()
        for index, item in enumerate(window_folders):
                window_folders[index] = "\"" + window_folders[index] + "\""
        file_dirname = ["\"" + os.path.dirname(self.window.active_view().file_name()) + "\""]
        return window_folders or file_dirname

    def find_common_path(self, paths):
        paths = [path.replace("\"", "") for path in paths]
        paths = [path.split("/") for path in paths]
        common_path = []
        while 0 not in [len(path) for path in paths]:
            next_segment = list(set([path.pop(0) for path in paths]))
            if len(next_segment) == 1:
                common_path += next_segment
            else:
                break
        return "\"" + "/".join(common_path) + "/\""