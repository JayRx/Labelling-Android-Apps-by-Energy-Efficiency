import polars as pl
import numpy as np
import json

df = pl.read_csv("results.csv")

categoryDfs = df.partition_by("Category")

def makeThresholds(n, mean):
    finalList = []

    for i in range(n):
        percentage = i / n
        value = round(mean * percentage / 0.50)
        finalList.append(value)

    return finalList

def computeLabel(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            return len(thresholds)-i+1

    return 1

def objectListToList(list, key):
    finalList = []
    for item in list:
        val = item[key]
        finalList.append(val)
    return finalList

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def modelTool(categoryDf, categoryName, min, max, tool):

    #categoryDf.sort(tool)
    #sum = pl.sum(categoryDf.get_column(tool))
    #mean = sum / apps
    #max = max.select(pl.col(tool)).item()
    #min = min.select(pl.col(tool)).item()
    #median = pl.median(df[tool])

    values = np.array(categoryDf[tool].to_list())

    #print(f"------------ {tool} ------------")
    #print(f"Min: {values.min()} Max: {values.max()} Mean: {values.mean()} Median: {np.median(values)}")

    newL = reject_outliers(values)
    #print(f"Min: {newL.min()} Max: {newL.max()} Mean: {newL.mean()}")

    thresholds = makeThresholds(5, newL.mean())
    f = open(f"thresholds/{categoryName}_{tool}.json", "w")
    data = {"thresholds": thresholds}
    f.write(json.dumps(data))
    f.close()


for categoryDf in categoryDfs:
    categoryName = pl.first(categoryDf["Category"])
    apps = pl.count(categoryDf["Name"])

    max = categoryDf.max()
    min = categoryDf.min()

    modelTool(categoryDf, categoryName, min, max, "Earmo")
    modelTool(categoryDf, categoryName, min, max, "Kadabra")
    modelTool(categoryDf, categoryName, min, max, "Lint")
    modelTool(categoryDf, categoryName, min, max, "ADoctor")
    modelTool(categoryDf, categoryName, min, max, "Paprika")
    modelTool(categoryDf, categoryName, min, max, "Relda2")


    """
    print(f"\n-------------------- {categoryName} ----------------------")
    print(f"Apps: {apps}")
    print(f"Earmo - Sum: {EarmoSum} Mean: {EarmoMean:.2f} Max: {EarmoMax} Min: {EarmoMin}")
    print(f"Kadabra - Sum: {kadabraSum} Mean: {kadabraMean:.2f} Max: {kadabraMax} Min: {kadabraMin}")
    print(f"lintSum - Sum: {lintSum} Mean: {lintMean:.2f} Max: {lintMax} Min: {lintMin}")
    print(f"aDoctor - Sum: {aDoctorSum} Mean: {aDoctorMean:.2f} Max: {aDoctorMax} Min: {aDoctorMin}")
    print(f"Paprika - Sum: {paprikaSum} Mean: {paprikaMean:.2f} Max: {paprikaMax} Min: {paprikaMin}")
    print(f"relda2Sum - Sum: {relda2Sum} Mean: {relda2Mean:.2f} Max: {relda2Max} Min: {relda2Min}")
    """

    #print(computeLabel(10, thresholds))
