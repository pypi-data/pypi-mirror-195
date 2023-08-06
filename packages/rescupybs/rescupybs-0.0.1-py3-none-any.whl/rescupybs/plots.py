import matplotlib.pyplot as plt

def Nispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r']
#    nbands = len(eigenvalues[0,0,:])
#    for i in range(nbands):
#        if np.min(eigenvalues[0,:,i]) > -0.05:
#            CBM=i
#            VBM = CBM-1
#            break
    plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc=location)
    plt.savefig("band.png", dpi=750, transparent=True, bbox_inches='tight')

def Ispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r', 'k']
    elif len(color) == 1:
        color = [color[0], 'k']

    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']

    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    p_up = plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    p_do = plt.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.savefig("band.png", dpi=750, transparent=True, bbox_inches='tight')

def Dispin(EXPORT, figsize, vertical, eigenvalues, chpts, labels, linestyle, linewidth, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) == 0:
        color = ['r', 'k']
    elif len(color) == 1:
        color = [color[0], 'k']

    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']

    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    ax1.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    ax2.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.set_yticklabels([])
    ax1.set_xlim(chpts[0],chpts[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(chpts[0],chpts[-1])
    ax2.set_ylim(vertical)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_xticks(chpts,labels[:-1]+[''])
    ax2.set_xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig("band.png", dpi=750, transparent=True, bbox_inches='tight')

