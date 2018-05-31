import re
import urllib.request
import urllib.error
import sys
import time
import random
from collections import OrderedDict

def fetch(url, shuffle=False):
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []

    eq = url.rfind('=') + 1
    cPL = url[eq:]

    yTUBE = urllib.request.urlopen(url).read()
    sTUBE = str(yTUBE)

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)

    if mat:
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

        final_list = list(OrderedDict.fromkeys(final_url))
        if shuffle: random.shuffle(final_list)

        return final_list
    else:
        raise Exception('No videos found in playlist')
