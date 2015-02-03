# GoToAnchor
# Create anchors and references for easily move everywhere!
# Hosted at https://github.com/eecolella/GoToAnchor

import sublime, sublime_plugin
import urllib, urllib.parse, time, re, webbrowser, os 

SETTINGS = 'go_to_anchor.sublime-settings'

def SelectDescInLine(view, idAnchor=None):
 
    match = view.find(idAnchor, 0, sublime.LITERAL | sublime.IGNORECASE)
    flag = True


    if True:
        print("\nDEBUG START SelectDescInLine")
        print('DEBUG SelectDescInLine: idAnchor: %s' % idAnchor)
        print('DEBUG SelectDescInLine: view.file_name(): %s' % view.file_name())
        print('DEBUG SelectDescInLine: view.id(): %s' % view.id())
        print('DEBUG SelectDescInLine: view.size(): %s' % view.size())
        print('DEBUG SelectDescInLine: match1: %s' % match)

    if not idAnchor:
        match = view.sel()[0] 


    if True:
        print('DEBUG SelectDescInLine: match2: %s' % match)
        print('DEBUG SelectDescInLine: match.begin(): %s' % match.begin())

    # calc string region
    line = view.lines(sublime.Region(match.begin(), match.begin()))[0]
    beginLine = line.begin()
    lineStr = view.substr(line)
    if True:
        print('DEBUG SelectDescInLine: beginLine: %s' % beginLine)
        print('DEBUG SelectDescInLine: line: %s' % line)
        print('DEBUG SelectDescInLine: lineStr: %s' % lineStr)

    try:
        string = re.search("(?<=ANCH0R:)(.*)(?=ID:)", lineStr).group(1).strip()
    except:
        flag = False

    if flag:
        descBegin = lineStr.find(string)
        descLenght = len(string)
        regionDesc = sublime.Region(beginLine + descBegin, beginLine + descBegin + descLenght)
        if False:
            print('DEBUG SelectDescInLine: descBegin: %s' % descBegin)
            print('DEBUG SelectDescInLine: descLenght: %s' % descLenght)
            print('DEBUG SelectDescInLine: descFromLine: "%s"' % lineStr[descBegin:descBegin+descLenght])
            print("DEBUG END SelectDescInLine\n")

        # select string
        view.sel().clear()
        view.sel().add(regionDesc) 
        view.show_at_center(regionDesc)
        return False
    else:
        return True

def SelectStringInLine(view, string):


    if not view.is_loading():   
        # calc string region
        line = view.lines(sublime.Region(view.sel()[0].begin(), view.sel()[0].begin()))[0]
        beginLine = line.begin()
        lineStr = view.substr(line)
        descBegin = lineStr.find(string)
        descLenght = len(string)
        regionDesc = sublime.Region(beginLine + descBegin, beginLine + descBegin + descLenght)

        if False:
            print("\nDEBUG START SelectStringInLine")
            print('DEBUG SelectStringInLine: beginLine: %s' % beginLine)
            print('DEBUG SelectStringInLine: line: %s' % line)
            print('DEBUG SelectStringInLine: lineStr: %s' % lineStr)
            print('DEBUG SelectStringInLine: descBegin: %s' % descBegin)
            print('DEBUG SelectStringInLine: descLenght: %s' % descLenght)
            print('DEBUG SelectStringInLine: descFromLine: "%s"' % lineStr[descBegin:descBegin+descLenght])
            print("DEBUG END SelectStringInLine\n")

        # select string
        view.sel().clear()
        view.sel().add(regionDesc) 
        view.show_at_center(regionDesc)     
    else:
        sublime.set_timeout(lambda: SelectStringInLine(view, string), 10)

class GoToAnchorCommand(sublime_plugin.TextCommand):
    debug = True

    # method: go_to_url
    # method: find_prev_something
    def run(self, edit, method="open_url", something="REFER3NCE"):

        if self.debug:
            print("\n\nDEBUG START go_to_anchor")
            print("DEBUG go_to_anchor: parameter method: ", method)
            print("DEBUG go_to_anchor: parameter something: ", something)

        if method == "go_to_url":
            self.go_to_url(edit)
        elif method == "find_prev_something":
            self.find_prev_something(something)

    def go_to_url(self, edit):

        if self.debug:
            print("\nDEBUG START go_to_anchor.go_to_url")

        view = self.view       

        line = view.lines(sublime.Region(view.sel()[0].begin(), view.sel()[0].begin()))[0]
        lineStr = view.substr(line)
        if self.debug and True:
            print("DEBUG go_to_anchor.go_to_url: line under the cursor: %s" % lineStr)

        if lineStr.find('REFER3NCE') >= 0:
            url = re.search("(?<=URL:')(.*)(?=')", lineStr).group(1)
            if self.debug and True:
                print("DEBUG go_to_anchor.go_to_url: url plus (maybe) idAnchor: %s" % url)
        else:
            # select text under cursor
            url = self.selection()
            # strip quotes if quoted
            if (url.startswith("\"") & url.endswith("\"")) | (url.startswith("\'") & url.endswith("\'")):
                url = url[1:-1]

        # try to find a Anchor Id and if so split url and id
        idAnchor = ''
        indexAt = url.find('@')
        if indexAt >= 0:
            idAnchor = url[indexAt+1:len(url)]
            url = url[0:indexAt]
        
        folder = os.path.normpath(view.window().folders()[0])
        # if the url is relative calc the absolute path
        absolute_path = os.path.join(folder, url)     

        if self.debug and True:
            print("DEBUG go_to_anchor.go_to_url: url without: ", url)
            print("DEBUG go_to_anchor.go_to_url: idAnchor: ", idAnchor)
            print("DEBUG go_to_anchor.go_to_url: absolute_path: ", absolute_path)

        if url:
            if absolute_path == view.file_name():
                # if the anchor is in the reference's file
                self.find_anchor(view, idAnchor)

            elif os.path.isdir(url):
                # if url is a directory open it in the os explorer
                os.startfile(url)

            elif os.path.isdir(absolute_path):
                # if absolute_path is a directory open it in the os explorer
                os.startfile(absolute_path)

            elif os.path.exists(url):
                # if url is file open/run it
                self.open_file(url, idAnchor)

            elif os.path.exists(os.path.expandvars(url)):
                # if url is file open/run it (with path expansion)
                self.open_file(os.path.expandvars(url), idAnchor)

            elif os.path.exists(absolute_path):
                # if absolute_path is file open/run it
                self.open_file(absolute_path, idAnchor)

            else:
                if "://" in url:
                    webbrowser.open_new_tab(url)                
                elif re.search(r"\w[^\s]*\.(?:" + sublime.load_settings(SETTINGS).get('reg_exp_domains') + ")[^\s]*\Z", url):
                    if not "://" in url:
                        url = "http://" + url
                    webbrowser.open_new_tab(url)
                else:
                    if not self.find_prev_something():
                        self.find_prev_something('ANCH0R')   
        
        else:
            if not self.find_prev_something():
                self.find_prev_something('ANCH0R')    

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
            
            view_opened_file = self.view.window().open_file(file, sublime.ENCODED_POSITION)

            # if not view_opened_file.is_loading():
            #     match1 = view_opened_file.find(idAnchor, 0)
            #     print("match1: ", match1)
            self.find_anchor(view_opened_file, idAnchor)

    def find_anchor(self, view_opened_file, idAnchor):


        if not view_opened_file.is_loading():
            if self.debug:
                print("\nDEBUG START go_to_anchor.find_anchor")
                print("DEBUG go_to_anchor.find_anchor: parameter idAnchor: ", idAnchor)

            SelectDescInLine(view_opened_file, "ID:" + idAnchor)
            sublime.set_timeout(lambda: SelectDescInLine(view_opened_file, idAnchor), 20)
            sublime.set_timeout(lambda: SelectDescInLine(view_opened_file, idAnchor), 40)
            sublime.set_timeout(lambda: SelectDescInLine(view_opened_file, idAnchor), 100)
        else:
            sublime.set_timeout(lambda: self.find_anchor(view_opened_file, idAnchor), 20)

    def find_prev_something(self, something='REFER3NCE'):
        
        if self.debug:
            print("\nDEBUG START go_to_anchor.find_prev_something")
            print("DEBUG go_to_anchor.find_prev_something: parameter something: ", something)
            
        view = self.view
        maches = view.find_all(something)
        if len(maches) > 0:
            current = view.sel()[0]
            mach = current
            flag = True

            if self.debug and True:
                print("DEBUG go_to_anchor.find_prev_something: maches: ", maches)

            for index in range(len(maches)):
                if ( maches[index].begin() < current.begin() ):
                    mach = maches[index]
                    flag = False

            if flag and len(maches) > 0:
                mach = maches[len(maches) - 1]
                

            if self.debug:
                print("DEBUG go_to_anchor.find_prev_something: mach: ", mach)
                
            # move cursor in position mach
            view.sel().clear()
            view.sel().add(mach)
            view.show_at_center(mach) 

            sublime.status_message('#GTA# Previous %s finded.' % something)

            return True
        else:
            return False

GoToLastAnchor = ''

def SaveGoToLastAnchor(view, idAnchor):

    global GoToLastAnchor

    folder = view.window().folders()
    absolute = view.file_name()
    relative = None

    if len(folder) == 1:
        folder = folder[0]
        relative = absolute[len(folder) + 1:]

    if False:
        print("\nDEBUG START SaveGoToLastAnchor")
        print("DEBUG SaveGoToLastAnchor: folder: %s" % folder)
        print("DEBUG SaveGoToLastAnchor: absolute: %s" % absolute)
        print("DEBUG SaveGoToLastAnchor: path: %s" % relative)
        print("DEBUG END SaveGoToLastAnchor\n")

    # save text in global variable
    if relative:
        GoToLastAnchor = [idAnchor, absolute, relative]
    else:
        GoToLastAnchor = [idAnchor, absolute]

class GenerateAnchorCommand(sublime_plugin.TextCommand):
    debug = True
    edit = None
    # method: create_anchor
    # method: create_gotoanchor_last
    # method: create_gotoanchor_empty
    # method: re_create_gotoanchor
    def run(self, edit, method="create_anchor", option=False):

        self.edit = edit

        if self.debug:
            print("\n\nDEBUG START generate_anchor")
            print("DEBUG generate_anchor: parameter method: ", method)

        if method == "create_anchor":
            self.create_anchor(edit)
        elif method == "create_gotoanchor_last":
            self.create_gotoanchor_last(edit)
        elif method == "create_gotoanchor_empty":
            self.create_gotoanchor_empty(edit)
        elif method == "re_create_gotoanchor":
            self.re_create_gotoanchor(edit)        
        elif method == "create_gotoanchor_last_option_chose":
            self.create_gotoanchor_last_option_chose(edit, option)

    def create_anchor(self, edit):
        view = self.view

        if self.debug:
            print("\nDEBUG START generate_anchor.create_anchor")

        # create id by current date
        idAnchor = "%s" % time.time()

        # create comment
        view.run_command('toggle_comment', { "block": False });
        
        # insert text
        desc = "optional-recommended description"
        view.insert(edit, view.sel()[0].begin(), "#GTA# ANCH0R:%s ID:%s" % (desc, idAnchor) )
         
        SelectStringInLine(view, desc)

        SaveGoToLastAnchor(view, idAnchor)

        sublime.status_message('#GTA# Reference to this anchor saved in "Create a reference to the last anchor"')

    def create_gotoanchor_last(self, edit):

        if len(GoToLastAnchor) == 2:
            self.create_gotoanchor_last_option_chose(edit, 1)
        else:
            sublime.active_window().show_quick_panel(["Relative Path", "Absolute Path"], self.create_gotoanchor_last_option_chose_fake)

    def create_gotoanchor_last_option_chose_fake(self, option):
        self.view.run_command('generate_anchor', {"method": "create_gotoanchor_last_option_chose", "option" : option});

    def create_gotoanchor_last_option_chose(self, edit, option):
        view = self.view

        if self.debug:
            print("\nDEBUG START generate_anchor.create_gotoanchor_last_option_chose")
            print("DEBUG generate_anchor.create_gotoanchor_last_option_chose: parameter option: %s" % option)

        idAnchor = GoToLastAnchor[0]
        path = GoToLastAnchor[2] if not option else GoToLastAnchor[1] 

        desc = "optional-recommended description" 
        string = "#GTA# REFER3NCE:%s URL:'%s@%s'" % (desc, path, idAnchor)

        view.run_command('toggle_comment', { "block": False });
        view.insert(self.edit, view.sel()[0].begin(), string)

        SelectStringInLine(view, desc)

        sublime.status_message('#GTA# Reference to %s@%s created' % (path, idAnchor) )

    def create_gotoanchor_empty(self, edit):
        view = self.view

        # create comment
        view.run_command('toggle_comment', { "block": False });

        # insert REFER3NCE text with empty url
        desc = "optional-recommended description"
        view.insert(edit, view.sel()[0].begin(), "#GTA# REFER3NCE: URL:'%s'" % desc)
         
        SelectStringInLine(view, desc)


        sublime.status_message('#GTA# Created empty reference.')

    def re_create_gotoanchor(self, edit):


        if self.debug:
            print("\nDEBUG START generate_anchor.re_create_gotoanchor")

        view = self.view
        lineStr = view.substr(view.lines(sublime.Region(view.sel()[0].begin(), view.sel()[0].begin()))[0])

        if lineStr.find('ANCH0R') >= 0:

            idAnchor = re.search("(?<=ID:)([.,0-9]*)", lineStr).group(1)

            if self.debug:
                print("DEBUG generate_anchor.re_create_gotoanchor: idAnchor: %s" % idAnchor)
                print("DEBUG generate_anchor.re_create_gotoanchor: lineStr: %s" % lineStr)

            SaveGoToLastAnchor(view, idAnchor)
            sublime.status_message('#GTA# Reference to this anchor saved in "Create a reference to the last anchor"')

        else:
            sublime.status_message('#GTA# You aren\'t in a line with a ANCH0R')

# import sublime
# import sublime_plugin
import os.path
#import os
import sys
import inspect

### Start of fixing import paths
# Added by jcoc611 based on the Emmet package.
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
sys.path += [BASE_PATH] + [os.path.join(BASE_PATH, 'searchengines')]
### End of fixing import paths

import searchengines

basedir = os.getcwd()


class SearchAnchorCommand(sublime_plugin.WindowCommand):

    # Start new code GoToAnchor
    debug = True
    lock_to_close = []
    last_close = None
    shadowResults = []
    # End new code GoToAnchor

    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''
        pass

    def run(self):

        # Start new code GoToAnchor
        if self.debug:
            print("\n\nDEBUG START search_anchor")
        # End new code GoToAnchor

        self.settings = sublime.load_settings('GoToAnchor.sublime-settings')
        self.engine_name = self.settings.get("go_to_anchor_engine")
        pushd = os.getcwd()
        os.chdir(basedir)
        __import__("searchengines.%s" % self.engine_name)
        self.engine = searchengines.__dict__[self.engine_name].engine_class(self.settings)
        os.chdir(pushd)

        # Old code Search in Project
        # view = self.window.active_view()
        # selection_text = view.substr(view.sel()[0])
        # self.window.show_input_panel(
        #     "GoToAnchor:",
        #     selection_text or self.last_search_string,
        #     self.perform_search, None, None)
                
        # Start new code GoToAnchor
        self.perform_search('ANCH0R')
        # End new code GoToAnchor

    def perform_search(self, text):


        if self.debug:
            print("\nDEBUG START search_anchor.perform_search")

        self.last_search_string = text


        folders = self.search_folders()

        self.common_path = self.find_common_path(folders)
        if self.debug and True:
            print('DEBUG search_anchor.perform_search: self.common_path: %s' % self.common_path)
            print('DEBUG search_anchor.perform_search: folders: %s' % folders)
        self.results = self.engine.run(text, folders)

        # Old code Search in Project
        # if self.results:
        #     self.results = [[result[0].replace(self.common_path.replace('\"', ''), ''), result[1]] for result in self.results]
        #     self.window.show_quick_panel(self.results, self.goto_result)
        # else:
        #     self.results = []
        #     self.window.show_quick_panel(["No results"], None)

        # Start new code GoToAnchor
        if folders != False:
            if self.results:

                self.results = [[result[0].replace(self.common_path.replace('\"', ''), ''), result[1]] for result in self.results]
                self.results.remove(self.results[0])

                for index in range(len(self.results)):

                    temp = self.results[index][0]
                    self.shadowResults.append([self.results[index][0], self.results[index][1]])


                    if self.debug and True:
                        print('DEBUG search_anchor.perform_search: self.shadowResults[index]: %s' % self.shadowResults[index])

                    self.results[index][0] = re.search("(?<=ANCH0R:)(.*)(?=ID:)", self.results[index][1]).group(1).strip()
                    self.results[index][1] = temp

                    if self.debug and False:
                        print('DEBUG search_anchor.perform_search: self.shadowResults[index]: %s' % self.shadowResults[index])



                if self.debug and False:
                    print('DEBUG search_anchor.perform_search: self.shadowResults: %s' % self.shadowResults)
                    print('DEBUG search_anchor.perform_search: self.results %s' % self.results)

                self.lock_to_close = [v.id() for v in self.window.views()]
                self.last_close = self.window.active_view()
                if self.debug and True:
                    print('DEBUG search_anchor.perform_search: slef.lock_to_close: %s' % self.lock_to_close)

                self.window.show_quick_panel(self.results, None, 0, -1, self.on_select)

            else:
                self.results = []
                self.shadowResults = []
                self.window.show_quick_panel(["No results"], None)
        # End new code GoToAnchor

    def search_folders(self):
        window_folders = self.window.folders()
        for index, item in enumerate(window_folders):
                window_folders[index] = "\"" + window_folders[index] + "\""

        # Old code Search in Project
        # file_dirname = ["\"" + os.path.dirname(self.window.active_view().file_name()) + "\""]
        # return window_folders or file_dirname

        # Start new code GoToAnchor
        try:
            file_dirname = ["\"" + os.path.dirname(self.window.active_view().file_name()) + "\""]
        except:
            file_dirname = None

        if (not window_folders) and (not file_dirname):    
            self.window.show_quick_panel(["Something went wrong!","Try to repeat this search with some file opened"], None)                       
            return False
        else:
            return window_folders or file_dirname
        # End new code GoToAnchor

    # Old code Search in Project
    # def goto_result(self, file_no):
    #     if file_no != -1:
    #         file_name = self.common_path.replace('\"', '') + self.results[file_no][0]
    #         view = self.window.open_file(file_name, sublime.ENCODED_POSITION)
    #         regions = view.find_all(self.last_search_string)
    #         view.add_regions("go_to_anchor", regions, "entity.name.filename.find-in-files", "circle", sublime.DRAW_OUTLINED)                         

    # Start new code GoToAnchor
    def on_select(self, file_no=None):
        global GoToLastAnchor

        if self.debug:
            print("\nDEBUG START search_anchor.on_select")
            print("DEBUG search_anchor.on_select: file_no:", file_no)

        if file_no != -1:
            # go to anchor
            file_name = self.common_path.replace('\"', '') + self.results[file_no][1]
            view = self.window.open_file(file_name, sublime.ENCODED_POSITION)

            string = self.results[file_no][0]
            SelectStringInLine(view, string)         
            
            if self.debug:
                print('DEBUG search_anchor.on_select: self.shadowResults[file_no]: %s' % self.shadowResults[file_no])

            idAnchor = re.search("(?<=ID:)(.*)",  self.shadowResults[file_no][1]).group(1).strip()

            SaveGoToLastAnchor(view, idAnchor) 
            
            sublime.status_message('#GTA# Reference to "%s" saved in "GTA: Paste Reference To Last Anchor"' % self.results[file_no][0])
            
            if self.debug:
                print('DEBUG search_anchor.on_select: GoToLastAnchor: %s' % GoToLastAnchor)
                print('DEBUG search_anchor.on_select: self.last_close.id() in self.lock_to_close: %s' % self.last_close.id() in self.lock_to_close)


            # if the match is in another file
            if view.file_name() != self.last_close.file_name() and not self.last_close.id() in self.lock_to_close and len(self.window.views()) > 1:

                if self.debug:
                    print('DEBUG search_anchor.on_select: I\'m closing the last')                

                # close the last
                self.window.focus_view(self.last_close)
                self.window.run_command("close")
                # re-focus in the current
                self.window.focus_view(view)

            # store the new view
            self.last_close = view
    # End new code GoToAnchor 

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

# class EventDump(sublime_plugin.EventListener):  
  
#     def on_load(self, view):  
#         sublime.status_message("loaded1")
#         print('loaded1')
  
#     def on_load_async(self, view):  
#         sublime.status_message("loaded2")
#         print('loaded2')
  
#     def on_activated(self, view):  
#         sublime.status_message("loaded2")
#         print('on_activated')
  
#     def on_activated_async(self, view):  
#         sublime.status_message("loaded2")
#         print('on_activated_async')

          
