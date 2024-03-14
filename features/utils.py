import string
import math
import numpy as np

def shannon_entropy(text):
    """
    Adapted from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    by way of truffleHog (https://github.com/dxa4481/truffleHog)
    """
    if not text:
        return 0
    entropy = 0
    for x in string.printable:
        p_x = float(text.count(x)) / len(text)
        if p_x > 0:
            entropy += - p_x * math.log(p_x,2)
    return entropy



def shannon_entropy_lines_outliers(lines):
    # lines = code.split('\n')
    # entropy = [shannon_entropy(line) for line in lines]
    if len(lines)==1:
        return 0

    Q1 = np.percentile(lines, 25 ) 
    Q3 = np.percentile(lines, 75) 
    IQR = Q3 - Q1 
    low_lim = Q1 - 1.5 * IQR
    up_lim = Q3 + 1.5 * IQR
    outliers =[]
    for x in lines:
        if ((x> up_lim) or (x<low_lim)):
            outliers.append(x)
    
    return(len(outliers))


def gl4_converter(x):

    output = ''
    
    for s in x:
        if s in string.ascii_lowercase:
           output+='L'
        elif s in string.ascii_uppercase:
            output+='U'
        elif s in string.digits:
            output+='D'
        elif s in string.punctuation:
            output+='S'
        else:
            pass
    return(output)