import time
import os
import sys
import shutil
import polars as pl


from threading import Thread
from datetime import datetime

from src.GreenalizeParser.GreenalizeParser import GreenalizeParser

from src.ProgressBar.ProgressBar import ProgressBar

from src.Minifiers.ApkMinify import ApkMinify

from src.Decompilers.Dex2jar import Dex2jar
from src.Decompilers.Jadx import Jadx

from src.Analyzers.Earmo import Earmo
from src.Analyzers.Kadabra import Kadabra
from src.Analyzers.AndroidManifestAnalyzer import AndroidManifestAnalyzer
from src.Analyzers.Lint import Lint
from src.Analyzers.ADoctor import ADoctor
from src.Analyzers.Paprika import Paprika
from src.Analyzers.Relda2 import Relda2

from src.AppInfo.AppInfo import AppInfo

from src.Reports.TextReportWriter import TextReportWriter
from src.Reports.JsonReportWriter import JsonReportWriter

from src.Stats.Stats import Stats

class Greenalize():
    def __init__(self, greenalizeParser):
        self.greenalizeParser = greenalizeParser
        self.status = False

    def analyze(self):
        print("")
        t1 = time.time()

        progressBar = ProgressBar()

        apkPath = self.greenalizeParser.getApkPath()
        apkName = self.greenalizeParser.getApkName()
        apkCategory = self.greenalizeParser.getApkCategory()
        apkSize = round(os.path.getsize(apkPath) / 1024**2, 2)

        analyzers = self.greenalizeParser.getAnalyzers()

        progressBar.smoothUpdate(20, "Jadx Decompiling APK!")
        task_t1 = time.time()
        jadx = Jadx(apkPath)
        jadx.decompile()
        numberOfFiles = jadx.getNumberOfFiles()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Jadx - {task_t2:.2f} s", jadx.getStatus())
        progressBar.smoothUpdate(30, "Jadx Decompiling APK!!")

        dex2jarOutputPath = "output/" + apkName + "/dex2jar/" + apkName + "-dex2jar.jar"
        jadxOutputPath = "output/" + apkName + "/jadx/"

        appInfo = AppInfo(apkName, apkCategory, apkSize, numberOfFiles)

        """
        progressBar.smoothUpdate(30, "EARMO Analyzing!")
        task_t1 = time.time()
        earmo = Earmo(apkName, f"{jadxOutputPath}minified")
        if "Earmo" in analyzers:
            earmo.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"EARMO - {task_t2:.2f} s", earmo.getStatus())
        progressBar.smoothUpdate(40, "EARMO Analyzing!")

        progressBar.smoothUpdate(40, "Kadabra Analyzing!")
        task_t1 = time.time()
        kadabra = Kadabra(apkName, f"{jadxOutputPath}minified")
        if "Kadabra" in analyzers:
            kadabra.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Kadabra - {task_t2:.2f} s", kadabra.getStatus())
        progressBar.smoothUpdate(50, "Kadabra Analyzing!")

        progressBar.smoothUpdate(50, "AndroidManifestAnalyzer Analyzing!")
        task_t1 = time.time()
        androidManifestAnalyzer = AndroidManifestAnalyzer(apkName, jadxOutputPath)
        if "AndroidManifestAnalyzer" in analyzers:
            androidManifestAnalyzer.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"AndroidManifestAnalyzer - {task_t2:.2f} s", androidManifestAnalyzer.getStatus())
        progressBar.smoothUpdate(60, "AndroidManifestAnalyzer Analyzing!")

        progressBar.smoothUpdate(60, "Lint Analyzing!")
        task_t1 = time.time()
        lint = Lint(apkName, jadxOutputPath)
        if "Lint" in analyzers:
            lint.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Lint - {task_t2:.2f} s", lint.getStatus())
        progressBar.smoothUpdate(70, "Lint Analyzing!")

        progressBar.smoothUpdate(70, "aDoctor Analyzing!")
        task_t1 = time.time()
        aDoctor = ADoctor(apkName, jadxOutputPath)
        if "ADoctor" in analyzers:
            aDoctor.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"aDoctor - {task_t2:.2f} s", aDoctor.getStatus())
        progressBar.smoothUpdate(80, "aDoctor Analyzing!")

        progressBar.smoothUpdate(80, "Paprika Analyzing!")
        task_t1 = time.time()
        paprika = Paprika(apkName, apkPath)
        if "Paprika" in analyzers:
            paprika.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Paprika - {task_t2:.2f} s", paprika.getStatus())
        progressBar.smoothUpdate(90, "Paprika Analyzing!")

        progressBar.smoothUpdate(90, "Relda2 Analyzing!")
        task_t1 = time.time()
        relda2 = Relda2(apkName, apkPath)
        if "Relda2" in analyzers:
            relda2.analyze()
        task_t2 = time.time() - task_t1
        progressBar.finishMessage(f"Relda2 - {task_t2:.2f} s", relda2.getStatus())
        progressBar.smoothUpdate(100, "Relda2 Analyzing!")

        t2 = time.time() - t1
        print(f"\n\nElapsed time: {t2:.2f} s\n")

        appInfo.setTime(t2)

        textReportWriter = TextReportWriter(appInfo, androidManifestAnalyzer, earmo, kadabra, lint, aDoctor, paprika, relda2)
        textReportWriter.write()

        jsonReportWriter = JsonReportWriter(appInfo, androidManifestAnalyzer, earmo, kadabra, lint, aDoctor, paprika, relda2)
        jsonReportWriter.write()

        stats = Stats()
        data = {}
        data["appName"] = apkName
        data["category"] = apkCategory
        data["size"] = apkSize
        data["numberOfFiles"] = numberOfFiles
        data["time"] = t2
        data["earmo"] = earmo.getResult()
        data["kadabra"] = kadabra.getResult()
        data["lint"] = lint.getResult()
        data["adoctor"] = aDoctor.getResult()
        data["paprika"] = paprika.getResult()
        data["relda2"] = relda2.getResult()
        data_aux = androidManifestAnalyzer.getResult()
        data["activities"], data["permissions"], data["services"], data["providers"] = data_aux["activities"], data_aux["permissions"], data_aux["services"], data_aux["providers"]
        stats.addData(data)
        """

        self.status = True

    def getStatus(self):
        return self.status