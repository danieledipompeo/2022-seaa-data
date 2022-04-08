def figure(path, caption, label):
    template =\
'''
\\begin{{figure}}
  \\centering
  \\includegraphics[width=.94\\linewidth]{{{}}}
  \\caption{{{}}}
  \\label{{fig:{}}}
\\end{{figure}}
'''
    return template.format(path, caption, label)

def tests_table(df):
    def mwu(x):
        if x >= 0.0001:
            x = round(x, 4)
            return '\textbf{{{}}}'.format(x) if x <= 0.05 else x
        else:
            return '\textbf{$<$0.0001}'
    df['MWU p'] = df['MWU p'].apply(mwu)
    df['vda'] = df.apply(lambda r: '({}) \ebar{{{}}}{{{}}}'\
            .format(r['magn.'], round(r['vda'], 4), round(abs(r['vda']-0.5), 4)),
            axis=1)
    df.drop(['magn.'], axis=1, inplace=True)
    df.columns = df.columns.str.replace('time', 'Budget')
    df.columns = df.columns.str.replace('algo', 'Algor.')
    df.rename(columns={'vda': '\\vda'}, inplace=True)
    print(df.to_latex(escape=False, index=False))

def HV_table(df):
    df = df.sort_values(by=['algo', 'time'])
    df = df[df['time'] != 0]
    df['time'] = df['time'].apply(lambda x: '{} min'.format(int(x / 1000 / 60)))
    df['algo'] = df['algo'].apply(lambda x: '\\' + x.lower()[:4])
    df['qi avg'] = df['qi avg'].apply(lambda x: round(x, 4))
    df['qi stdev'] = df['qi stdev'].apply(lambda x: round(x, 4))
    df = df[['algo', 'time', 'qi avg', 'qi stdev']]
    print(df.to_markdown())
    print(df.to_latex(escape=False, index=False))
