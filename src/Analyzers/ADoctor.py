from src.Analyzers.Analyzer import Analyzer

from src.EnergyAntiPatterns.DebuggableRelease import DebuggableRelease
from src.EnergyAntiPatterns.SlowLoop import SlowLoop
from src.EnergyAntiPatterns.DataTransmissionWithoutCompression import DataTransmissionWithoutCompression
from src.EnergyAntiPatterns.InefficientDataFormatAndParser import InefficientDataFormatAndParser
from src.EnergyAntiPatterns.InefficientDataStructure import InefficientDataStructure
from src.EnergyAntiPatterns.InefficientSQLQuery import InefficientSQLQuery
from src.EnergyAntiPatterns.InternalGetterAndSetter import InternalGetterAndSetter
from src.EnergyAntiPatterns.LeakingThread import LeakingThread
from src.EnergyAntiPatterns.LeakingInnerClass import LeakingInnerClass
from src.EnergyAntiPatterns.NoLowMemoryResolver import NoLowMemoryResolver
from src.EnergyAntiPatterns.UnclosedClosable import UnclosedClosable
from src.EnergyAntiPatterns.DurableWakelock import DurableWakelock
from src.EnergyAntiPatterns.MemberIgnoringMethod import MemberIgnoringMethod
from src.EnergyAntiPatterns.PublicData import PublicData
from src.EnergyAntiPatterns.RigidAlarmManager import RigidAlarmManager

from src.EnergyAntiPatterns.UnknownAntiPattern import UnknownAntiPattern

import subprocess
import os
import shutil
import json

import polars as pl

class ADoctor(Analyzer):
    def __init__(self, apkName, path):
        super().__init__(apkName, path)

        self.outputPath = "output/" + self.apkName + "/aDoctor/"

        self.outputFile = self.outputPath + "results.csv"

        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        self.antiPatternTypes = {
            "DTWC": DataTransmissionWithoutCompression,
            "DR": DebuggableRelease,
            "DW": DurableWakelock,
            "IDFP": InefficientDataFormatAndParser,
            "IDS": InefficientDataStructure,
            "ISQLQ": InefficientSQLQuery,
            "IGS": InternalGetterAndSetter,
            "LIC": LeakingInnerClass,
            "LT": LeakingThread,
            "MIM": MemberIgnoringMethod,
            "NLMR": NoLowMemoryResolver,
            "PD": PublicData,
            "RAM": RigidAlarmManager,
            "SL": SlowLoop,
            "UC": UnclosedClosable
        }

        self.patterns = []

    def analyze(self):
        if not os.path.exists(f"{self.outputPath}logs/"):
            os.makedirs(f"{self.outputPath}logs/")
        stdoutFile = open(f"{self.outputPath}logs/out.txt", "w+")
        stderrFile = open(f"{self.outputPath}logs/err.txt", "w+")

        result = subprocess.run(["cmd", "/c", "java", "-jar", "tools/aDoctor/aDoctor.jar", self.path, self.outputFile, "111111111111111"], stdout=stdoutFile, stderr=stderrFile)

        self.extractResults()

        stdoutFile.close()
        stderrFile.close()

        self.status = 1

    def toReport(self):
        return f"aDoctor: {len(self.patterns)}\n"

    def toJson(self):
        data = { "ADoctor": len(self.patterns) }
        return data

    def getResult(self):
        return len(self.patterns)

    def extractResults(self):
        patterns = []

        results = pl.read_csv(self.outputFile)

        for antiPatternType, antiPattern in self.antiPatternTypes.items():
            n = pl.sum(results.get_column(antiPatternType))
            if n == None: continue
            for i in range(pl.sum(results.get_column(antiPatternType))):
                patterns.append(antiPattern)

        self.patterns = patterns
