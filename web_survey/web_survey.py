#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libopensesame.exceptions import osexception
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from openexp.keyboard import keyboard

import sys 
from PyQt4 import QtNetwork
from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4.QtWebKit import QWebView

class web_survey(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Plug-in that allows you to start an online survey'

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.
		self.var.checkbox = u'yes' # yes = checked, no = unchecked
		self.var.option = u'QT: Auto exit survey (no video)'
		self.var.url_text = u'https://fppvu.eu.qualtrics.com/jfe/form/SV_07dizGnQNU3gPUV' #DELETE THIS AFTER TESTING!!!!
		self.var.exit_text = u'We thank you for your time spent'
		self.var.checkbox = u'yes' # yes = checked, no = unchecked
		
		# For in info: - "Using Chrome (no Auto exit)"

	def prepare(self):

		"""The preparation phase of the plug-in goes here."""

		# Call the parent constructor.
		item.prepare(self)
				
		# Do some checks
		if self.var.canvas_backend != u'legacy':
			raise osexception(u'The web_survey plug-in requires the legacy back-end!')
		
		if u'pygame_window_pos' in self.var:
			if self.var.pygame_window_pos != "0,0":
				raise osexception(u'Set Legacy Back-end setting "Window position" to "0,0"')
		else:
			raise osexception(u'Set Legacy Back-end setting "Window position" to "0,0"')
		
#		if QtNetwork.QNetworkConfigurationManager().isOnline() == False:
#			raise osexception(u'Offline')
		
		
		# construct the URL
		if self.var.checkbox == u'yes':
			self.var.url_text_total = self.var.url_text + u'?subject_nr=' + str(self.var.subject_nr)
		else:
			self.var.url_text_total = self.var.url_text
	
		# Here simply prepare a canvas with 'Starting survey' text.
		self.c = canvas(self.experiment)
		#self.c.text(self.var.pygame_window_pos) ##### FOR DEBUGGING >>#DELETE THIS AFTER TESTING!!!!
		self.c.text(u'Starting survey')

	def run(self):

		"""The run phase of the plug-in goes here."""
		
		# Somehow the Survey is only visible in the foreground after line below
		keyboard(self.experiment).get_key(timeout=100)
				
		# self.set_item_onset() sets the time_[item name] variable. Optionally,
		# you can pass a timestamp, such as returned by canvas.show().
		self.set_item_onset(self.c.show())
		
		app = QApplication(sys.argv)
		browser = Browser() 
		browser.web_view.load(QUrl(self.var.url_text_total))
		browser.show()
		app.exec_()
		app.exit()

class Browser(QMainWindow):

		def __init__(self):
			QMainWindow.__init__(self)
			self.setWindowState(Qt.WindowFullScreen);
			self.web_view = QWebView()
			self.setCentralWidget(self.web_view)
			self.web_view.loadFinished.connect(self._load_finished)

		def _load_finished(self):
			if self.web_view.page().findText(u'We thank you for your time spent'):
				self.close()


class qtweb_survey(web_survey, qtautoplugin):

	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		web_survey.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		# If you specify a 'name' for a control in info.json, this control will
		# be available self.[name]. The type of the object depends on the
		# control. A checkbox will be a QCheckBox, a line_edit will be a
		# QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
		# to the setEnabled() slot of the QLineEdit. This has the effect of
		# disabling the QLineEdit when the QCheckBox is uncheckhed. We also
		# explictly set the starting state.
		
		#self.line_edit_widget.setEnabled(self.combobox_widget.currentText()==u'QT: Auto exit survey (no video)')
		self.line_edit_widget.setDisabled(True)
		#self.combobox_widget.currentIndexChanged.connect(
		#	self.line_edit_widget.setDisabled)
