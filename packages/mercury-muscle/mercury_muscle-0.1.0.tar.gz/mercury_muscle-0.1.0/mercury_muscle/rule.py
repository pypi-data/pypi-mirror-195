import re
import math
import numpy as np
import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from tabulate import tabulate

from score import MercuriTable


class RuleEvaluator:
    def __init__(
        self,
        mt: MercuriTable,
        target=None
    ) -> None:
        self.mt = mt
        self.target = target
        self.rules = []

        self.totals_df = None
        self.cm_df = None

    def add_rule(self, query, alias=None):
        self.rules.append(Rule(query, alias))

    def evaluate_cm(self, side="R"):
        if self.target == None:
            raise Exception("RuleEvaluator target must be set")
        
        res_df = pd.DataFrame(columns=["tp", "fp", "tn", "fn", "nan"])
        for r in self.rules:
            res = self._evaluate_rule_target(r.query, side)
            res["Rule"] = r.alias if not r.alias == None else r.query
            res_df = pd.concat([res_df, pd.DataFrame(res)], ignore_index=True)
        self.cm_df = res_df.copy()


    def evaluate_totals(self, side="R"):
        if not side in ["L", "R"]:
            raise ValueError('side must be "R" or "L"')

        res_df = pd.DataFrame(columns=["Rule", "True", "False", "NA"])
        for r in self.rules:
            res = self._evaluate_rule(r.query, side)
            res["Rule"] = r.alias if not r.alias == None else r.query
            res_df = pd.concat([res_df, pd.DataFrame(res)], ignore_index=True)
        self.totals_df = res_df.copy()

    def _evaluate_rule(self, query, side):
        subsets = query.split('->')

        true, false, nan = 0, 0, 0
        for i, sub in enumerate(subsets):
            labels = list(filter(None, re.split("[<>=()|&\d]", sub)))
            labels.sort(key=lambda s: len(s), reverse=True)

            if i == 0 : 
                population = deepcopy(self.mt.patients)
            else:
                population = deepcopy(population_tmp)

            population_tmp = []
            for p in population:
                nan_found = False
                query_subs = sub
                for l in labels:
                    score = getattr(p, f"muscles_{side}")[l].score
                    if np.isnan(score):
                        nan += 1
                        nan_found = True
                        break
                    query_subs = query_subs.replace(l, str(score))

                if nan_found: continue

                query_subs = query_subs.replace("&", " and ").replace("|", " or ")
                if eval(query_subs) == True:
                    if not i == len(subsets) - 1:
                        population_tmp.append(p)
                        continue
                    true += 1
                elif eval(query_subs) == False:
                    if not i == len(subsets) - 1:
                        continue
                    false += 1
                else:
                    raise Exception(
                        f"The evaluated expression returned a value other than True or False: {query_subs}"
                    )

        return {"True": [true], "False": [false], "NA": [nan]}


    def _evaluate_rule_target(self, query, side):
        subsets = query.split('->')

        tp, tn, fp, fn, nan = 0, 0, 0, 0, 0
        for i, sub in enumerate(subsets):
            labels = list(filter(None, re.split("[<>=()|&\d]", sub)))
            labels.sort(key=lambda s: len(s), reverse=True)

            if i == 0 : 
                population = deepcopy(self.mt.patients)
            else:
                population = deepcopy(population_tmp)

            population_tmp = []
            for p in population:
                nan_found = False
                query_subs = sub
                for l in labels:
                    score = getattr(p, f"muscles_{side}")[l].score
                    if np.isnan(score):
                        nan += 1
                        nan_found = True
                        break
                    query_subs = query_subs.replace(l, str(score))

                if nan_found: continue

                query_subs = query_subs.replace("&", " and ").replace("|", " or ")

                if eval(query_subs) == True:
                    if p.disease == self.target and not i == len(subsets) - 1: 
                        population_tmp.append(p)
                        continue
                    elif p.disease == self.target and i == len(subsets) - 1: 
                        tp += 1
                    elif not p.disease == self.target and not i == len(subsets) - 1:
                        continue
                    elif not p.disease == self.target and i == len(subsets) - 1:
                        fp += 1

                elif eval(query_subs) == False:
                    if p.disease == self.target and not i == len(subsets) - 1: 
                        population_tmp.append(p)
                        continue
                    elif p.disease == self.target and i == len(subsets) - 1: 
                        tn += 1
                    elif not p.disease == self.target and not i == len(subsets) - 1:
                        continue
                    elif not p.disease == self.target and i == len(subsets) - 1:
                        fn += 1

                else:
                    raise Exception(
                        f"The evaluated expression returned a value other than True or False: {query_subs}"
                    )

        return {"tp": [tp], "fp": [fp], "tn": [tn], "fn": [fn], "nan": [nan]}
    
    def cm_stats(self):
        if not isinstance(self.cm_df, pd.DataFrame):
            print('The confussion matrix dataframe does not exist. Run evaluate_cm()')
            return

        res = {
            "Rule": [],
            "Accuracy": [],
            "Sensitivity": [],
            "Specificity": [],
            "PPV": [],
            "NPV": [],
            "F1-Score": [],
            "MCC": [],
            "normMCC": [],
            "DOR": [],
            "Population": [],
            "Positives": [],
            "Negatives": [],
        }
        for idx, row in self.cm_df.iterrows():
            tp = row["tp"]
            fp = row["fp"]
            tn = row["tn"]
            fn = row["fn"]

            t = tp + tn + fp + fn

            accuracy = (tp + tn) / (t)
            sensitivity = tp / (tp + fn)
            specificity = tn / (tn + fp)
            ppv = tp / (tp + fp)
            npv = tn / (tn + fn)
            f1_score = (2 * tp) / ((2 * tp) + fp + fn)
            mcc = ((tp * tn) - (fp * fn)) / math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
            norm_mcc = (mcc + 1) / 2
            dor = ((tp + 0.5) * (tn + 0.5)) / ((fp + 0.5) * (fn + 0.5))
            pos = (tp + fn) / t
            neg = (tn + fp) / t

            res["Rule"].append(row["Rule"])
            res["Accuracy"].append(accuracy)
            res["Sensitivity"].append(sensitivity)
            res["Specificity"].append(specificity)
            res["PPV"].append(ppv)
            res["NPV"].append(npv)
            res["F1-Score"].append(f1_score)
            res["MCC"].append(mcc)
            res["normMCC"].append(norm_mcc)
            res["DOR"].append(dor)
            res["Population"].append(t)
            res["Positives"].append(pos)
            res["Negatives"].append(neg)
        return pd.DataFrame(res)

    def show_rules(self) -> pd.DataFrame:
        res = {
            "Alias": [r.alias for r in self.rules],
            "Query": [r.query for r in self.rules]
        }
        return pd.DataFrame(res)
    
    def show_totals(self):
        if isinstance(self.totals_df, pd.DataFrame):
            print(tabulate(self.totals_df, headers="keys", tablefmt="github"))
        else:
            print("Totals not evaluated, run evaluate_totals()")

    def show_cm(self):
        if isinstance(self.cm_df, pd.DataFrame):
            print(tabulate(self.cm_df, headers="keys", tablefmt="github"))
        else:
            print("Confussion Matrixes not evaluated, run evaluate_cm()")
    
    def update_rule(self, idx, alias=None, query=None):
        if not alias == None: self.rules[idx].alias = alias
        if not query == None: self.rules[idx].query = query

class Rule:
    def __init__(self, query: str, alias: str = None) -> None:
        self.query = query
        self.alias = alias
