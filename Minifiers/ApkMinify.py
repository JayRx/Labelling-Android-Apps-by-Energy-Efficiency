import subprocess
import os

from Minifiers.Minifier import Minifier

class ApkMinify(Minifier):
    def __init__(self, apkPath):
        super().__init__(apkPath)

    def minify(self):
        result = subprocess.run(["cmd", "/c", "java", "-jar", "apkMinify.jar", self.apkPath, "-o", self.outputPath, "-i", "Landroid", "Lcom"])
        #print(result.stdout)
