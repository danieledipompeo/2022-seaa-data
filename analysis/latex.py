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
