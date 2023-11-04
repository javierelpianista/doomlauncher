import sys
import os
import glob
import chardet

from PyQt5 import uic

from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QFont, QFontMetrics, QTextCursor
from PyQt5.QtWidgets import (
        QMainWindow,
        QApplication,
        QDialog,
        QFileDialog,
        )

from .profile import Profile
from .profilemanager import ProfileManager

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources
import pkg_resources

pkg = importlib_resources.files("doomlauncher")

form_class = uic.loadUiType(pkg / "main.ui")[0]
edit_profile_class = uic.loadUiType(pkg / "edit_profile.ui")[0]

class GUIProfileManager(QMainWindow, form_class):

    def __init__(self, app, parent=None):
        # Initialize the ProfileManager by reading the file
        self.mgr = ProfileManager.load()

        # Initialize the graphical interface
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Populate the QListWidget with the current profiles
        self.update_list_of_profiles()
        self.listProfiles.setCurrentRow(0)

        # Set a monospace font for the WAD description
        font = QFont('whatever')
        font.setStyleHint(QFont.Monospace)
        self.textDescription.setFont(font)

        # Set the minimum width for the WAD description
        metric = QFontMetrics(font)
        font_width = metric.averageCharWidth()
        self.textDescription.setMinimumWidth(font_width*60)

        self.skill_levels = [
                "I'm too young to die",
                "Hey, not too rough",
                "Hurt me plenty",
                "Ultra violence",
                "Nightmare"
                ]


    def update_list_of_profiles(self):
        self.listProfiles.clear()
        for profile in self.mgr:
            self.listProfiles.addItem(profile)

    # -------------------------------------------------------------------------
    # Functions linked to buttons

    # Run current profile
    def run_current_profile(self):
        profile_name = self.listProfiles.currentItem().text()

        skill = self.comboSkill.currentText()
        level = self.spinLevel.cleanText()

        if skill in self.skill_levels:
            self.mgr[profile_name]['skill'] = str(self.skill_levels.index(skill)+1)

        if level != '0': 
            self.mgr[profile_name]['warp'] = str(level)

        command = self.mgr.run_command(profile_name)

        p = QProcess()
        p.start(command[0], [*command[1:]])
        p.waitForFinished(-1)

    # Open dialog to create a new profile
    def new_profile(self):
        new_dialog = GUIEditProfileDialog(self)

        if new_dialog.exec():
            curr_profile = new_dialog.profile
            name = curr_profile['name']

            if name in self.mgr:
                print('profile already created')

            else:
                self.mgr[name] = curr_profile
                self.update_list_of_profiles()

    # Open dialog to edit existing profile
    def edit_profile(self):
        name = self.listProfiles.currentItem().text()
        profile = self.mgr[name]

        new_dialog = GUIEditProfileDialog(self, profile)

        if new_dialog.exec():
            pass

    # Quit program
    def quit_program(self):
        self.mgr.save()
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Other slots

    def update_description(self):
        '''
        Check if there is a .txt file in the same directory as the .wad file
        for each wad.
        If so it puts the description in the corresponding text box.

        Also, check if the warp and skill are set, if so set them in their
        corresponding boxes.
        '''

        import chardet

        curr_item = self.listProfiles.currentItem()
        if curr_item is None:
            return

        curr_profile = self.listProfiles.currentItem().text()


        files = self.mgr[curr_profile]['files']
        for file in files:
            dir = os.path.dirname(file)
            basename = os.path.splitext(os.path.basename(file))[0]
            filelist = os.listdir(dir)

            match = None
            text_found = False
            for filename in filelist:
                if filename.lower() == basename.lower() + '.txt':
                    match = filename

            if match is not None:
                fullpath = os.path.join(dir, match)

                data = open(fullpath, 'rb').read()
                enc = chardet.detect(data)['encoding']

                text = open(fullpath, 'r', encoding=enc).read()
                text_found = True
            else:
                text = "No description available."

            self.textDescription.clear()
            self.textDescription.insertPlainText(text)
            self.textDescription.moveCursor(QTextCursor.Start)

            if text_found: break

        if self.mgr[curr_profile]['skill'] is not None:
            self.comboSkill.setCurrentIndex(
                    int(self.mgr[curr_profile]['skill'])
                    )

        if self.mgr[curr_profile]['warp'] is not None:
            self.spinLevel.setValue(int(self.mgr[curr_profile]['warp']))

def main():
    app = QApplication(sys.argv)
    window = GUIProfileManager(app)
    window.show()
    app.exec_()

    #mgr = ProfileManager.load()
    #mgr.run_profile(profile_name)


class GUIEditProfileDialog(QDialog, edit_profile_class):

    def __init__(self, parent, profile=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        if profile is None:
            self.profile = Profile(
                    {
                    'name' : '', 
                    'iwad' : '',
                    'port' : 'prboom-plus',
                    'files' : []
                    }
                    )
        else:
            self.profile = profile
            self.update()

    def update(self):
        self.textEditName.setText(self.profile['name'])
        self.textEditIWAD.setText(self.profile['iwad'])

        self.listFiles.clear()
        for file in self.profile['files']:
            self.listFiles.addItem(file)

    def change_name(self):
        self.profile['name'] = self.textEditName.toPlainText()

    def change_iwad(self):
        self.profile['iwad'] = self.textEditIWAD.toPlainText()

    def add_file(self):
        filename = QFileDialog.getOpenFileName(
                self, "Add file(s)", "", "WAD files (*.wad);; PK3 files (*.pk3);; All files (*)")[0]

        if not filename in self.profile['files']:
            self.profile['files'].append(filename)

        self.update()

    def move_file_up(self):
        '''
        Move the currently selected file up in the list.
        '''
        if self.listFiles.count() > 1:
            curr_index = self.listFiles.currentRow()
            if curr_index in (0, -1): return
            self.profile['files'].insert(
                    curr_index-1, self.profile['files'].pop(curr_index))
            self.update()
            self.listFiles.setCurrentRow(curr_index-1)

    def move_file_down(self):
        '''
        Move the currently selected file down in the list.
        '''
        count = self.listFiles.count() 
        if count > 1:
            curr_index = self.listFiles.currentRow()
            if curr_index in (-1, count-1): return
            self.profile['files'].insert(
                    curr_index+1, self.profile['files'].pop(curr_index))
            self.update()
            self.listFiles.setCurrentRow(curr_index+1)


    def remove_file(self):
        if self.listFiles.count() > 0:
            filename = self.listFiles.currentItem().text()
            if filename is not None:
                self.profile['files'].remove(filename)

        self.update()
