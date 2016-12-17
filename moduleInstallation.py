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

	#Check if module is installed
	#		if installed, check if needed packages are installed
	# 		if not, instal it, then refresh the python package path (with reload(site)) to use "import module" in packages check, then run packages check
	def checkModuleInstallation(self):

		if self.pipVerification == False:
			print("Check if pip is installed.")
			self.checkpipInstall()
		print("###\nCheck if " + self.module + " is installed :")

		try:
			moduleImported = importlib.import_module(self.module)
			version = moduleImported.__version__
			print(self.module + " (version " + version + ") is installed.")

			if self.moduleVersionUsed is None :
				if self.packages is not None :
					self.checkAndInstallPackages()

			elif version < self.moduleVersionUsed :
				print("You are using an old version of " + self.module + ". It can result in error with our scripts.")
				self.moduleUninstall()
				self.moduleInstall()
				if self.pythonVersion < (3,0,0): 
					reload(site)
				elif self.pythonVersion > (3,0,0): 
					importlib.reload(site)

				if self.packages is not None :
					self.checkAndInstallPackages()

			elif version >= self.moduleVersionUsed  :
				print("You are using a recent version of " + self.module + ".")
				if self.packages is not None :
					self.checkAndInstallPackages()

		except (ImportError):
			print("No " + self.module + " module installed.")
			self.moduleInstall()
			if self.pythonVersion < (3,0,0): 
				reload(site)
			elif self.pythonVersion > (3,0,0):
				importlib.reload(site)

			if self.packages is not None :
				self.checkAndInstallPackages()

	#Check if pip is installed and install it if not.
	def checkpipInstall(self):
		try:
			os.system('pip --version')
			print("pip is installed.")
			self.pipVerification = True
		except:
			print("###\npip is going to be installed.""")
			if self.nameOS == 'nt':
				os.system("easy_install urllib3")
				import urllib
				urllib.urlretrieve ("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
				if self.pythonVersion < (3,0,0):
					os.system('python get-pip.py')
				elif self.pythonVersion > (3,0,0):
					os.system('python3 get-pip.py')
				os.remove("get-pip.py")
				self.pipVerification = True
			else:
				if self.pythonVersion < (3,0,0):
					os.system('sudo apt-get install python-pip')
					self.pipVerification = True
				elif self.pythonVersion > (3,0,0):
					os.system('sudo apt-get install python3-pip')
					self.pipVerification = True

	#Uninstall previous version of the module.
	def moduleUninstall(self):
		sentenceChoice = self.module + " older version is going to be uninstalled, do you want to proceed(y/n)?\n"
		if self.pythonVersion < (3,0,0): 
			choice = raw_input(sentenceChoice).lower()
		elif self.pythonVersion > (3,0,0):
			choice = input(sentenceChoice).lower()

		if choice  in self.answersYN[0] :
			print("###\n" + self.module +" older version is going to be uninstalled, pip needs privilege to correctly uninstall " + self.module +".")
			if self.nameOS == 'nt':
				print("###\nYou are using windows, does your cmd runs with administrator right?")
				print("###\nIf not pip can't install or uninstall packages.")
				os.system('python -m pip uninstall ' + self.module)
			else:
					if self.pythonVersion < (3,0,0):
						os.system('sudo pip uninstall ' + self.module)
					elif self.pythonVersion > (3,0,0):
						os.system('sudo pip3 uninstall ' + self.module)

		elif choice in self.answersYN[1]:
			pass

		elif choice not in self.answersYN:
			print("\nUncorrect answer, please rewrite it.\n")
			self.moduleUninstall()

	#Install module, needs permission
	#If pip is not installed, the script will install it
	def moduleInstall(self):
		sentenceChocie = self.module + " is going to be installed, do you want to proceed(y/n)?\n"
		if self.pythonVersion < (3,0,0): 
			choice = raw_input(sentenceChocie).lower()
		elif self.pythonVersion > (3,0,0):
			choice = input(sentenceChocie).lower()

		if choice  in self.answersYN[0] :
			print("###\n" + self.module + " will be installed, pip needs sudo privilege to correctly install " + self.module + ".")
			if self.nameOS == 'nt':
				os.system('python -m pip install ' + self.module)
			else:
					if self.pythonVersion < (3,0,0):
						os.system('sudo pip install ' + self.module)
					elif self.pythonVersion > (3,0,0):
						os.system('sudo pip3 install ' + self.module)

		elif choice in self.answersYN[1]:
			pass

		elif choice not in self.answersYN:
			print("\nUncorrect answer, please rewrite it.\n")
			self.moduleInstall()

	#Check and install module needed packages
	def checkAndInstallPackages(self):
		print("###\nNow " + self.module + " packages needed will be checked and installed if not present.")
		moduleImported = importlib.import_module(self.module)
		for package in self.packages:
			moduleImported.download(package)
