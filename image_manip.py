'''
Created on 19 Jan 2016

@author: time2
'''
try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import matplotlib.pyplot as plt



class TexPngConverter(object):
    '''
    classdocs
    '''


    def __init__(self, fontsize=12, dpi=300, format_='png'):
        '''
        Constructor
        '''
        self._fontsize = fontsize
        self._dpi = dpi
        self._format = format_
    
    def render_latex(self,formula, output_file):
        """
        renders tex formula into a png image
        """
        plt.rc('text', usetex=True)
        fig = plt.figure()
        text = fig.text(0, 0, r'${}$'.format(formula), fontsize=self._fontsize)
    
        fig.savefig(BytesIO(), dpi=self._dpi)  # triggers rendering
    
        bbox = text.get_window_extent()
        width, height = bbox.size / float(self._dpi) + 0.05
        fig.set_size_inches((width, height))
    
        dy = (bbox.ymin / float(self._dpi)) / height
        text.set_position((0, -dy))
    
        
        fig.savefig(output_file, dpi=self._dpi, transparent = True, format = self._format)  
        plt.close(fig)
        
        
        return output_file

if __name__=="__main__":
    rend = TexPngConverter()
    rend.render_latex(r"\frac{n!}{k!(n-k)!}=E=1=mc^2", "teo.png")
    
