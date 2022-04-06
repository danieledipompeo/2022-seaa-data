from glob import glob
import numpy as np
import pandas as pd
import re
from os.path import basename
from scipy.stats import mannwhitneyu, rankdata
from itertools import permutations, combinations
from latex import tests_table

DATA_DIR = '../data/by_time/quality_indicators'

algo_names = {'nsgaii': '\\nsga', 'pesa2': '\\pesa', 'spea2': '\\spea'}

class Experiment:
    def __init__(self, file):
        self.file = file
        self.values = np.loadtxt(file, delimiter = '\n\n', dtype=float)
        m = re.match(r'qi__(?P<algo>[^-]+)-(?P<casestudy>.+)-bytime-(?P<time>\d+)__HV.csv', basename(file))
        if m is not None:
            for k, v in m.groupdict().items():
                setattr(self, k, v)
        else:
            print('Cannot parse {}.'.format(file))

        self.time = '{} min'.format(int(int(self.time) / 1000 / 60))
        self.algo = algo_names[self.algo]

def a12(sample1, sample2):
    m = len(sample1)
    n = len(sample2)
    r1 = sum(rankdata(np.concatenate([sample1,sample2]))[:m])
    return (2 * r1 - m * (m + 1)) / (2 * n * m)

def interpret_a12(a12):
    levels = [0.147, 0.33, 0.474]
    magnitude = ["N", "S", "M", "L"]
    scaled_a12 = (a12 - 0.5) * 2
    return magnitude[np.searchsorted(levels, abs(scaled_a12))]

def compare(exps, group_by, criteria):
    group = set([getattr(e, group_by) for e in exps])
    res = []
    for g in group:
        exps_by_group = [e for e in exps if getattr(e, group_by) == g]
        pms = combinations(exps_by_group, r=2)
        for pm in pms:
            mwu = mannwhitneyu(pm[0].values, pm[1].values)
            a12_ = a12(pm[0].values, pm[1].values)
            a12_m = interpret_a12(a12_)
            res.append([g, getattr(pm[0], criteria), getattr(pm[1], criteria),
                mwu.pvalue, a12_, a12_m])
    df = pd.DataFrame(res, columns=[group_by, criteria + ' 1', criteria + ' 2',
            'MWU p', 'vda', 'magn.'])
    df.sort_values([group_by, criteria + ' 1', criteria + ' 2'], inplace=True)
    return df

exps = [Experiment(f) for f in glob('{}/qi__*-*-*-[0-9]*__HV.csv'.format(DATA_DIR))]

for cs in set([e.casestudy for e in exps]):
    exps_by_cs = [e for e in exps if e.casestudy == cs]
    print('-----', cs)

    # Compare time
    df = compare(exps_by_cs, 'algo', 'time')
    print(df.to_markdown(index=False))
    print()
    tests_table(df)
    print()

    # Compare algorithms
    df = compare(exps_by_cs, 'time', 'algo')
    print(df.to_markdown(index=False))
    print()
    tests_table(df)
    print()

    print()
