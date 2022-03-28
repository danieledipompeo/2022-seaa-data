from dataset import get_datasets
from pareto import Pareto
from plots import *
from latex import figure

import pandas as pd
from os.path import basename


DATA_DIR = '../data/by_time'
FIGS = '../figs/'

initials = {
    'ttbs':   get_initial(0.657925),
    'cocome': get_initial(0.7630625563279512),
}
initials['train-ticket'] = initials['ttbs']
initials['simplified-cocome'] = initials['cocome']

latex_names = {
    'train-ticket': '\\ttbs',
    'simplified-cocome': '\\ccm',
}

# Read all the paretos from all the subdirs
datasets = get_datasets(DATA_DIR)

# Gather all the configurations we were able to read
configs = pd.DataFrame([d.to_series() for d in datasets])

# Keep only the configurations with 0.95 probpas
configs = configs[configs['prob'] == '0.95']

# Keep only the configurations with 102 maxeval
configs = configs[configs['eval'] == '102']

# For each configuration generate a 2d scatter plot
# that shows how the solutions change when varying the time
bytime_configs = configs[[c for c in configs.columns if c != 'time']]\
        .drop_duplicates()
print(bytime_configs.shape[0], 'configurations:')
print(bytime_configs.to_markdown())
print()
for _, c in bytime_configs.iterrows():
    sel = [d.reference for d in datasets
            if d.reference is not None
            and d.usecase == c['usecase']
            and d.algo == c['algo']
            and d.eval == c['eval']
            and d.prob == c['prob']]
    fig = plot_pareto(sel, 'time', initial=initials[sel[0].usecase],
            save_prefix='{}{}_MaxEval_{}_ProbPAs_{}_Algo_{}'.format(FIGS,
                sel[0].usecase, sel[0].maxeval, sel[0].probpas, sel[0].algo),
            legend_title='Time budget')
    print(figure('plots/{}'.format(basename(fig)),
        'Pareto frontiers for {} computed with {} when varying time'\
                .format(latex_names[sel[0].usecase], sel[0].algo),
        'bytime_{}_{}'.format(sel[0].usecase, sel[0].algo)))

# For each configuration generate a 2d scatter plot
# that shows how the solutions change when varying the algorithm
byalgo_configs = configs[[c for c in configs.columns if c != 'algo']]\
        .drop_duplicates()
print(byalgo_configs.shape[0], 'configurations:')
print(byalgo_configs.to_markdown())
print()
for _, c in byalgo_configs.iterrows():
    sel = [d.reference for d in datasets
            if d.reference is not None
            and d.usecase == c['usecase']
            and d.time == c['time']
            and d.eval == c['eval']
            and d.prob == c['prob']]
    fig = plot_pareto(sel, 'algo', initial=initials[sel[0].usecase],
            save_prefix='{}{}_MaxEval_{}_ProbPAs_{}_Time_{}'.format(FIGS,
                sel[0].usecase, sel[0].maxeval, sel[0].probpas,
                sel[0].time.replace(' ', '_')), legend_title='Algorithm')
    print(figure('plots/{}'.format(basename(fig)),
        'Pareto frontiers for {} obtained by different algorithms with a {} budget'\
                .format(latex_names[sel[0].usecase], sel[0].time),
        'byalgo_{}_{}'.format(sel[0].usecase, sel[0].time.replace(' ', '_'))))
