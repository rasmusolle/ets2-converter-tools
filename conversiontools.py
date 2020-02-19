from enum import Enum
from pathlib import Path
import wget
import zipfile

class ConvStatus(Enum):
	CONV_VERSION_NOT_FOUND = 0
	CONV_VERSION_FOUND = 1

class ConversionTools:
	"""This class makes sure that the wanted version conversion tools are downloaded and initialized"""
	def __init__(self, game, version, convver = None):
		self.game = game
		if convver:
			self.version = convver
		else:
			self.version = self._gameVerToConvVer(version)
		self.versionStr = self._convVerToString(".")
		self.status = self._checkConv()
		if not self.status == ConvStatus.CONV_VERSION_FOUND:
			self._dlConv()

	def _gameVerToConvVer(self, version):
		if version == 30:
			return [2,5]
		if version == 31:
			return [2,6]
		if version <= 34: # ETS2 1.32-1.34
			return [2,7]
		if version == 35:
			return [2,8]
		if version == 36:
			return [2,10]
		raise UserWarning("gameVerToConvVer(): Unsupported ETS2 version: "+version)

	def _convVerToString(self, separator = "."):
		out = ""
		for versionDigit in self.version:
			# URL uses underscore as version digit separator
			if not out == "": out = out + separator
			out = out + str(versionDigit)
		return out

	def _checkConv(self):
		path = Path("scsconv/"+self.versionStr)
		if path.is_file():
			return ConvStatus.CONV_VERSION_FOUND
		return ConvStatus.CONV_VERSION_NOT_FOUND

	def _dlConv(self):
		versionUrl = self._convVerToString("_")
		convFile = Path("scsconv/conversion_tools_%s.zip" % versionUrl)
		if not convFile.is_file():
			wget.download("http://download.eurotrucksimulator2.com/conversion_tools_%s.zip" % versionUrl, "scsconv")

		with zipfile.ZipFile(convFile,"r") as file:
			file.extractall(Path("scsconv/%s/" % self.versionStr))

	def getConvPath(self):
		return str(Path("scsconv/%s/" % self.versionStr))
