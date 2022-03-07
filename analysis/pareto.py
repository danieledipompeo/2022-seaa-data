import re
from glob import glob
from os.path import basename

import pandas as pd

DATA_DIR = '../data/'
REF_PARETOS = DATA_DIR + 'reference_paretos/'

class Pareto:

    def __init__(self, file):
        self.file = file
        self.parse_filename()
        if getattr(self, 'usecase', None) is not None:
            self.read_rf()

    def parse_filename(self):
        m = re.match(r'(?P<usecase>[^_]+)__BRF_clone_(?P<brf_clone>[^_]+)__moc_(?P<brf_moc>[^_]+)__mcnn_(?P<brf_mcnn>[^_]+)__moncnn_(?P<brf_moncnn>[^_]+)__MaxEval_(?P<maxeval>[^_]+)__ProbPAs_(?P<probpas>0\.\d+)\.(?P<algo>[^_]+)\.csv', basename(self.file))
        if m is not None:
            for k, v in m.groupdict().items():
                setattr(self, k, v)

    def read_rf(self):
        df = pd.read_csv(self.file,
                names=['perfQ', '#changes', '#PAs', 'reliability'])
        self.df = Pareto.fix_perfq_rel(df)
        return self.df

    @staticmethod
    def fix_perfq_rel(df):
        if 'perfQ' in df:
            df['perfQ'] = df['perfQ'] * -1
        if 'reliability' in df:
            df['reliability'] = df['reliability'] * -1
        return df
