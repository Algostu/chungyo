from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt


def cursor():
    '''
    Draw Vertical and Horizontal when cursor is on it
    '''
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, facecolor='#FFFFCC')

    x, y = 4*(np.random.rand(2, 100) - .5)
    ax.plot(x, y, 'o')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    # Set useblit=True on most backends for enhanced performance.
    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

    plt.show()

def text():
    fig = plt.figure()
    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_title('axes title')

    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')

    ax.text(3, 8, 'boxed italics text in data coords', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    ax.text(2, 6, r'an equation: $E=mc^2$', fontsize=15)

    ax.text(3, 2, 'unicode: Institut für Festkörperphysik')

    ax.text(0.95, 0.01, 'colored text in axes coords',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='green', fontsize=15)


    ax.plot([2], [1], 'o')
    ax.annotate('annotate', xy=(2, 1), xytext=(3, 4),
                arrowprops=dict(facecolor='black', shrink=0.05))

    ax.axis([0, 10, 0, 10])

    plt.show()

if __name__=='__main__':
    text()
