import json
from sklearn.metrics import confusion_matrix
import numpy as np
from chebai.preprocessing.datasets.tox21 import Tox21Base
import os

path = "/home/glauer/dev/ChEBI_RvNN/.experiments/electra/tox21_without_sempre/"
with open(os.path.join(path, "predictions.json"), "r") as fin:
    results = json.load(fin)
preds, labs = zip(*((row["prediction"], row["labels"]) for row in results))
preds = np.array(preds)
labs = np.array(labs)

lines = []
for dim in range(len(preds[0])):
    lines.append(f"# {Tox21Base.HEADERS[dim]}")
    has_value = labs[:, dim] == None
    p = preds[:, dim][~has_value] > 0.3
    l = labs[:, dim][~has_value]

    cm = confusion_matrix(l.astype(int), p.astype(int))
    lines.append("| | Target: False | Target: True |")
    lines.append(f"| --- | --- | --- |")
    lines.append(f"| Pred: False | {cm[0,0]} | {cm[0,1]} |")
    lines.append(f"| Pred: True | {cm[1,0]} | {cm[1,1]} |")
    lines.append("")

    precision = cm[1, 1] / (cm[1, 1] + cm[0, 1])
    recall = cm[1, 1] / (cm[1, 1] + cm[1, 0])
    lines.append(f"* Precision: {precision}")
    lines.append(f"* Recall: {recall}")
    lines.append("")
    lines.append("")
with open(os.path.join(path, "class-wise.md"), "wt") as fout:
    fout.writelines(x + "\n" for x in lines)
