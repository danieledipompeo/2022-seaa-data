from pareto import Pareto

import re
import pandas as pd
from glob import glob


class Dataset:

    def __init__(self, path, usecase, algo, eval, time, prob):
        self.path = path
        self.usecase = usecase
        self.algo = algo
        self.eval = eval
        self.time = time
        self.prob = prob
        self.reference = self.parse_reference()

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\n{}'.format(
                self.usecase, self.algo, self.eval,
                self.prob, self.time, self.path)

    def to_series(self):
        return pd.Series([self.usecase, self.algo, self.eval, self.prob, self.time],
                index=['usecase', 'algo', 'eval', 'prob', 'time'])

    def parse_reference(self):
        for f in glob(self.path + '/referenceFront/*.csv'):
            p = Pareto(f)
            p.time = self.time
            if getattr(p, 'usecase', None) is not None:
                return p
        print('Did not find any reference pareto matching CSV in:', self.path)

def get_datasets(data_dir):
    datasets = []
    r = re.compile(r'.+/(?P<usecase>[^/]+)/(?P<algo>[^/]+)/(?P<eval>[^/]+)/(?P<time>[^/]+)/(?P<prob>[^/]+)$')
    for p in glob(data_dir + '/*/*/*/*/*'):
        m = r.match(p)
        if m is not None:
            d = m.groupdict()
            datasets.append(Dataset(p, d['usecase'], d['algo'],
                d['eval'].split('_')[0], int(int(d['time'])/1000), d['prob']))
    return [d for d in datasets if d.reference is not None]
