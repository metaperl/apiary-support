from datetime import datetime

import os
import matplotlib.pyplot as plt

def save(path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.

    Parameters
    ----------
    path : string
        The path (and filename, without the extension) to save the
        figure to.

    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.

    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.

    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.

    """

    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)

    if verbose:
        print("Saving figure to '%s'..." % savepath),

    # Actually save the figure
    plt.savefig(savepath)

    # Close it
    if close:
        plt.close()

    if verbose:
        print("Done")


def datetime_as_file(instrument,timeframe,traded=False):
    if traded:
        flag = 'Traded'
    else:
        flag = ''
    n = datetime.now()
    s = "data/{0.year}/{0.month:02}/{0.day:02}/{1}-{2}-{3}-{0.hour:02}:{0.minute:02}".format(n, flag, instrument,timeframe)
    print s
    return s
