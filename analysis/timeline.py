import re
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = '../data/by_time'
QI_csv = '../data/by_time/quality_indicators/qi__optimal.csv'
QI = 'HV'
FIGS = '../figs/'

def timeline(case_study, events, qi, save_prefix=None):
    events = [e for e in events if e['usecase'] == case_study]
    fig, ax = plt.subplots(figsize=(12, 4), constrained_layout=True)

    x = [e['eval_done'] for e in events]
    y = [float(e['qi']) for e in events]
    markerline, stemline, baseline = ax.stem(x, y, basefmt="k-")
    plt.setp(markerline, mec="k", mfc="w", zorder=3)
    plt.setp(stemline, color="0.6")
    markerline.set_ydata([0] * len(y))
    #ax.set_xlim([ax.get_xlim()[0], ax.get_xlim()[1]*1.02])
    #ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1]*1.05])
    ax.set_xlabel('Number of performed evolutions')
    ax.set_ylabel(qi)

    for i, p in enumerate(x):
        c = [e for e in events if e['eval_done'] == p and float(e['qi']) == y[i]][0]
        ax.annotate('{}\n{} min'.format(c['algo'],
            int(int(c['time'])/1000/60)), xy=(p+.2, y[i]-.035))

    filename = '{}_timeline.pdf'.format(save_prefix)
    plt.savefig(filename)
    print('Saved to: {}'.format(filename))

case_studies = {
    'ttbs': 'train-ticket',
    'cocome': 'simplified-cocome',
}

# Read the quality indicators
qi = pd.read_csv(QI_csv)

# Look for the 'algo_perf_stats.csv' files
events = []
r = re.compile(r'.+/(?P<usecase>[^/]+)/(?P<algo>[^/]+)/(?P<eval>[^/]+)/(?P<time>[^/]+)/(?P<prob>[^/]+)$')
for p in glob(DATA_DIR + '/*/*/*/*/*'):
    m = r.match(p)
    if m is not None:
        d = m.groupdict()
        if d['prob'] == '0.95' and d['eval'] == '102_eval':
            # Get the quality indicator
            # FIXME now I take the first one
            d['qi'] = qi[
                (qi['case_study'] == case_studies[d['usecase']]) &
                (qi['prob_pas'] == int(d['prob'][2:])) &
                (qi['algorithm'] == d['algo'].replace('-', '').lower()) &
                (qi['search_budget'] == 'sb_{}'.format(d['time'])) &
                (qi['max_eval'] == int(d['eval'].split('_')[0])) &
                (qi['q_indicator'] == QI)].iloc[0]['value']
            d['eval_done'] = sum(1 for line in open(p + '/algo_perf_stats.csv')) - 1
            events.append(d)

for cs in case_studies.keys():
    timeline(cs, events, QI, save_prefix='{}{}_{}'.format(FIGS, cs, QI))
