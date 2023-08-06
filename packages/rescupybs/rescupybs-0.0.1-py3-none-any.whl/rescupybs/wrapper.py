import argparse, os, re, platform, glob
import matplotlib.pyplot as plt
from rescupybs import plots, functions
from rescupybs import __version__

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams["mathtext.fontset"] = 'cm'

def main():
    parser = argparse.ArgumentParser(description='Plot the band structure from rescuplus calculation result *.json file',
                                     epilog='''
Example:
rescupybs
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version",      version="rescupybs "+__version__+" from "+os.path.dirname(__file__)+' (python'+platform.python_version()+')')
    parser.add_argument('-s', "--size",       type=float, nargs=2,   help='figure size: width, height')
    parser.add_argument('-b', "--divided",    action='store_true',   help="plot the up and down spin in divided subplot")
    parser.add_argument('-y', "--vertical",   type=float, nargs=2,   help="vertical axis")
    parser.add_argument('-g', "--legend",     type=str,  nargs=1,    help="legend labels")
    parser.add_argument('-a', "--location",   type=str.lower,        default='best',
                                                                     choices=['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                                                     help="arrange the legend location, default best")
    parser.add_argument('-k', "--linestyle",  type=str, nargs='+',   default=['-'],
                                                                     help="linestyle: solid, dashed, dashdot, dotted or tuple; default solid")
    parser.add_argument('-W', "--linewidth",  type=str, nargs='+',   default=['0.8'], help="linewidth, default 0.8")
    parser.add_argument('-c', "--color",      type=str,              nargs='+', default=[],
                                                                     help="plot colors: b, blue; g, green; r, red; c, cyan; m, magenta; y, yellow; k, black; w, white")
    parser.add_argument('-i', "--input",      type=str,              nargs='+', default=[], help="plot figure from .json or .dat file")
    parser.add_argument('-o', "--output",     type=str,              default="BAND.png", help="plot figure filename")
    parser.add_argument('-l', "--labels",     type=str.upper,        nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-f', "--font",       type=str,              default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels_f = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    linestyle = []
    for i in args.linestyle:
        if len(i) > 2 and i[0] == '(' and i[-1] == ')':
            linestyle.append(eval(i))
        elif len(i.split('*')) == 2:
            j = i.split('*')
            linestyle = linestyle + [j[0]] * int(j[1])
        else:
            linestyle.append(i)

    linewidth = []
    for i in args.linewidth:
        if len(i.split('*')) == 2:
            j = i.split('*')
            linewidth = linewidth + [float(j[0])] * int(j[1])
        else:
            linewidth.append(float(i))

    color = []
    for i in args.color:
        j = i.split('*')
        if len(j) == 2:
            color = color + [j[0]] * int(j[1])
        else:
            color.append(i)

    if not args.vertical:
        vertical = [-5.0, 5.0]
    else:
        vertical = args.vertical

    plt.rcParams['font.family'] = '%s'%args.font

    if not args.input:
        input = ['nano_bs_out.json']
    else:
        input = [f for i in args.input for f in glob.glob(i)]

    if len(input) == 1:
        if os.path.exists(input[0]):
            if input[0].split('.')[-1].lower() == 'json':
                bs_file = input[0]
                eigenvalues, chpts, labels, formula = functions.bs_json_read(bs_file)
                if labels_f:
                    labels = labels_f
                legend = args.legend
                if not legend:
                    formula_l = [i.strip() for i in re.split('\(|\)', formula) if i.strip()]
                    formula = ''
                    for i in formula_l:
                        if i.isdigit():
                            for j in i:
                                formula = formula + '$_' + j + '$'
                        else:
                            formula = formula + i
                    legend = [formula]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if len(eigenvalues) == 1:
                    plots.Nispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and not args.divided:
                    plots.Ispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)
                elif len(eigenvalues) == 2 and args.divided:
                    plots.Dispin(args.output, args.size, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, args.location, color)

#       elif args.input.split('.')[-1] == 'dat':

                


