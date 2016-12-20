import os
import site
import importlib
import sys

class ModuleInstallation():
	
	def __init__(self, moduleToCheck, l_packagesToCheck=None, moduleVersion=None):
		self.pythonVersion = sys.version_info
		self.nameOS = os.name
		self.answersYN = (['yes', 'y'], ['no', 'n'])
		self.module = moduleToCheck
		self.moduleVersionUsed = moduleVersion
		self.packages = l_packagesToCheck
		self.pipVerification = False

	def getPythonVersion(self):
		return self.pythonVersion

	def getNameOS(self):
		return self.nameOS

	def getAnswersYN(self):
		return self.answersYN

	def getModule(self):
		return self.module

	def getModuleVersionUsed(self):
		return self.moduleVersionUsed

	def getPackages(self):
		return self.packages

	def getPipVerification(self):
		return self.pipVerification

	def setPipVerification(self, boolean):
		self.pipVerification = boolean

	#Check if module is installed
	#		if installed, check if needed packages are installed
	# 		if not, instal it, then refresh the python package path (with reload(site)) to use "import module" in packages check, then run packages check
	def checkModuleInstallation(self):

		if self.getPipVerification() == False:
			print("Check if pip is installed.")
			self.checkpipInstall()
		print("###\nCheck if " + self.getModule() + " is installed :")

		try:
			moduleImported = importlib.import_module(self.getModule())
			version = moduleImported.__version__
			print(self.getModule() + " (version " + version + ") is installed.")

			if self.getModuleVersionUsed() is None :
				if self.getPackages() is not None :
					self.checkAndInstallPackages()

			elif version < self.getModuleVersionUsed() :
				print("You are using an old version of " + self.getModule() + ". It can result in error with our scripts.")
				self.moduleUninstall()
				self.moduleInstall()
				if self.getPythonVersion() < (3,0,0):
					reload(site)
				elif self.getPythonVersion() > (3,0,0):
					importlib.reload(site)

				if self.getPackages() is not None :
					self.checkAndInstallPackages()

			elif version >= self.getModuleVersionUsed()  :
				print("You are using a recent version of " + self.getModule() + ".")
				if self.getPackages() is not None :
					self.checkAndInstallPackages()

		except (ImportError):
			print("No " + self.getModule() + " module installed.")
			self.moduleInstall()
			if self.getPythonVersion() < (3,0,0):
				reload(site)
			elif self.getPythonVersion() > (3,0,0):
				importlib.reload(site)

			if self.getPackages() is not None :
				self.checkAndInstallPackages()

	#Check if pip is installed and install it if not.
	def checkpipInstall(self):
		try:
			os.system('pip --version')
			print("pip is installed.")
			self.setPipVerification(True)
		except:
			print("###\npip is going to be installed.""")
			if self.getNameOS() == 'nt':
				os.system("easy_install urllib3")
				import urllib
				urllib.urlretrieve ("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
				if self.getPythonVersion() < (3,0,0):
					os.system('python get-pip.py')
				elif self.getPythonVersion() > (3,0,0):
					os.system('python3 get-pip.py')
				os.remove("get-pip.py")
				self.setPipVerification(True)
			else:
				if self.getPythonVersion() < (3,0,0):
					os.system('sudo apt-get install python-pip')
					self.setPipVerification(True)
				elif self.getPythonVersion() > (3,0,0):
					os.system('sudo apt-get install python3-pip')
					self.setPipVerification(True)

	#Uninstall previous version of the module.
	def moduleUninstall(self):
		sentenceChoice = self.getModule() + " older version is going to be uninstalled, do you want to proceed(y/n)?\n"
		if self.getPythonVersion() < (3,0,0):
			choice = raw_input(sentenceChoice).lower()
		elif self.getPythonVersion() > (3,0,0):
			choice = input(sentenceChoice).lower()

		if choice  in self.getAnswersYN()[0] :
			print("###\n" + self.getModule() +" older version is going to be uninstalled, pip needs privilege to correctly uninstall " + self.getModule() +".")
			if self.getNameOS() == 'nt':
				print("###\nYou are using windows, does your cmd runs with administrator right?")
				print("###\nIf not pip can't install or uninstall packages.")
				os.system('python -m pip uninstall ' + self.getModule())
			else:
					if self.getPythonVersion() < (3,0,0):
						os.system('sudo pip uninstall ' + self.getModule())
					elif self.getPythonVersion() > (3,0,0):
						os.system('sudo pip3 uninstall ' + self.getModule())

		elif choice in self.getAnswersYN()[1]:
			pass

		elif choice not in self.getAnswersYN():
			print("\nUncorrect answer, please rewrite it.\n")
			self.moduleUninstall()

	#Install module, needs permission
	#If pip is not installed, the script will install it
	def moduleInstall(self):
		sentenceChocie = self.getModule() + " is going to be installed, do you want to proceed(y/n)?\n"
		if self.getPythonVersion() < (3,0,0):
			choice = raw_input(sentenceChocie).lower()
		elif self.getPythonVersion() > (3,0,0):
			choice = input(sentenceChocie).lower()

		if choice  in self.getAnswersYN()[0] :
			print("###\n" + self.getModule() + " will be installed, pip needs sudo privilege to correctly install " + self.getModule() + ".")
			if self.getNameOS() == 'nt':
				os.system('python -m pip install ' + self.getModule())
			else:
					if self.getPythonVersion() < (3,0,0):
						os.system('sudo pip install ' + self.getModule())
					elif self.getPythonVersion() > (3,0,0):
						os.system('sudo pip3 install ' + self.getModule())

		elif choice in self.getAnswersYN()[1]:
			pass

		elif choice not in self.getAnswersYN():
			print("\nUncorrect answer, please rewrite it.\n")
			self.moduleInstall()

	#Check and install module needed packages
	def checkAndInstallPackages(self):
		print("###\nNow " + self.getModule() + " packages needed will be checked and installed if not present.")
		moduleImported = importlib.import_module(self.getModule())
		for package in self.getPackages():
			moduleImported.download(package)
