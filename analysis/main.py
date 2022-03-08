from dataset import get_datasets
from pareto import Pareto
from plots import *

import pandas as pd


DATA_DIR = '../data/by_time'
FIGS = '../figs/'

initials = {
    'ttbs':   get_initial(0.657925),
    'cocome': get_initial(0.7630625563279512),
}

# Read all the paretos from all the subdirs
datasets = get_datasets(DATA_DIR)

# Gather all the configurations we were able to read
configs = pd.DataFrame([d.to_series() for d in datasets])
configs = configs[[c for c in configs.columns if c != 'time']]\
        .drop_duplicates()

# Keep only the configurations with 0.95 probpas
configs = configs[configs['prob'] == '0.95']

# Print the configurations
print(configs.shape[0], 'configurations:')
print(configs.to_markdown())
print()

# For each configuration generate a 2d scatter plot
# that shows how the solutions change when varying the time
for _, c in configs.iterrows():
    print(c.to_markdown())
    sel = [d.reference for d in datasets
            if d.reference is not None
            and d.usecase == c['usecase']
            and d.algo == c['algo']
            and d.eval == c['eval']
            and d.prob == c['prob']]
    for d in sel:
        print(d.file)
    plot_pareto(sel, 'time', initial=initials['ttbs'],
            save_prefix='{}{}_MaxEval_{}_ProbPAs_{}_Algo_{}'.format(FIGS,
                sel[0].usecase, sel[0].maxeval, sel[0].probpas, sel[0].algo))
    print()
