from src.Analyzers.Analyzer import Analyzer

import os


class Relda2(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/relda2/"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.patterns = []

    def analyze(self):

        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "python2", "tools/relda2/Relda2.py", "-f", "-r", f"{self.outputPath}", f"{self.path}"], stdout=stdoutFile, stderr=stderrFile)

        stdoutFile.close()
        stderrFile.close()

        self.status = True

    def toReport(self):
        return f"Relda2: {len(self.patterns)}\n"

    def getResult(self):
        return len(self.patterns)
