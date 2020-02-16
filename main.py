from enum import Enum
from conversiontools import ConversionTools
from pathlib import Path
import os
import subprocess
import sys
import hashlib

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
			"modname": "My mod!",
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
		with open(Path(self.convtool.getConvPath() + "/extra_mount.txt"), "a") as file:
			for line in file:
				if self.getUid() in line:
					break
			else:
				file.write("%s" % self.getUid())

	def runConversion(self):
		subprocess.call(Path(self.convtool.getConvPath() + "/convert.cmd"))

def main():
	convtool = ConversionTools(Game.ETS2, 36)
	convert = Converter(convtool)
	Converter.createSymlink(
		Path(convert.options['directory']),
		Path(convtool.getConvPath() + "/%s/" % convert.getUid()))
	convert.ensureMount()
	convert.runConversion()


if __name__ == "__main__":
	main()
