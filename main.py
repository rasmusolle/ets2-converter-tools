import hashlib
import os
import subprocess
import sys
import zipfile
from enum import Enum
from pathlib import Path
from conversiontools import ConversionTools

def addDirToZip(zipHandle, path):
	for root, dirs, files in os.walk(path):
		for file in files:
			filePath = os.path.join(root, file)
			inZipPath = filePath.replace(path, "", 1).lstrip("\\/")
			zipHandle.write(filePath, inZipPath)

class Compression(Enum):
	"""Enums for what compression the mod should be packed with.
	FOLDER means that the mod is not packed as an archive file, but be stored unpacked inside of a folder."""
	FOLDER = 0
	NONE = 1
	DEFLATE = 2
	BZIP = 3

class Game(Enum):
	ETS2 = 0
	ATS = 1

class Converter:
	def __init__(self, argConvtool, argOptions = None):
		self.options = {
			"modname": "mymod",
			"compression": Compression.FOLDER,
			"game": Game.ETS2,
			"gameversion": 36,
			"directory": "tests/example_mod/",
			"staticdirectory": None
		}
		self.convtool = argConvtool

	def getUid(self):
		return "ct_" + hashlib.md5(self.options['modname'].encode("UTF-8")).hexdigest()

	@staticmethod
	def createSymlink(src, dest):
		if os.path.isdir(dest):
			os.remove(dest)  # use os.remove instead os.unlink, as we can't remove mklink junction with os.unlink.

		if sys.platform == "win32":
			subprocess.check_call(["mklink", "/J", str(dest), str(src)], shell=True)
		else:
			os.symlink(src, dest)

	def ensureMount(self):
		"""Ensure that the symlink name in /extra_mount.txt exists"""
		with open(Path(self.convtool.getConvPath() + "/extra_mount.txt"), "r+") as file:
			for line in file:
				if self.getUid() in line:
					break
			else:
				file.write("%s" % self.getUid())

	def runConversion(self):
		subprocess.call(str(Path(self.convtool.getConvPath() + "/convert.cmd")))

	def packMod(self):
		zipf = zipfile.ZipFile(Path(os.path.expanduser("~") + "/Documents/Euro Truck Simulator 2/mod/%s.zip" % self.options['modname']), "w", zipfile.ZIP_DEFLATED)
		addDirToZip(zipf, str(Path(self.convtool.getConvPath() + "/rsrc/" + self.getUid() + "/@cache/")))
		zipf.close()

def main():
	convtool = ConversionTools(Game.ETS2, 36)
	convert = Converter(convtool)
	Converter.createSymlink(
		Path(convert.options['directory']),
		Path(convtool.getConvPath() + "/%s/" % convert.getUid()))
	convert.ensureMount()
	convert.runConversion()
	convert.packMod()


if __name__ == "__main__":
	main()
