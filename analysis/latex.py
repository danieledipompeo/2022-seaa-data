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

# \newcommand{\vda}{$\hat{A}_{12}$\xspace}
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
