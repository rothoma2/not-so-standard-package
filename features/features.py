import numpy as np
from features.utils import shannon_entropy, shannon_entropy_lines_outliers, gl4_converter



class SnippetStats:

    def __init__(self):
        self.entropy_list = None
        self.outliers = None

    def set_snippet(self,snippet):
        self.snippet = snippet
        self.gl4 = gl4_converter(snippet)

    def shannon_entropy__file(self) -> float:
        gl4 = gl4_converter(self.snippet)
        return(shannon_entropy(gl4))

    def line_entropy(self):
         lines = [line for line in self.snippet.split('\n')]
         self.entropy_list = [shannon_entropy(gl4_converter(line)) for line in lines]

    def shannon_entropy__outliers(self) -> int:
        lines = [line for line in self.snippet.split('\n')]
        lines = [shannon_entropy(gl4_converter(line)) for line in lines]
        out = shannon_entropy_lines_outliers(lines)
        # self.entropy_list = out['entropy']
        
        return(out)

    def shannon_entropy__mean(self) -> float:
        return(np.mean(self.entropy_list))
    
    def shannon_entropy__median(self) -> float:
        return(np.median(self.entropy_list))
    
    def shannon_entropy__variance(self) -> float:
        return(np.var(self.entropy_list))
    
    def shannon_entropy__max(self) -> float:
        return(np.max(self.entropy_list))

    def shannon_entropy__1Q(self) -> float:
        Q1 = np.percentile(self.entropy_list, 25) 
        return(Q1)
    
    def shannon_entropy__3Q(self) -> float:
        Q3 = np.percentile(self.entropy_list, 75) 
        return(Q3)