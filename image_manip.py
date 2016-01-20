"""
Created on 19 Jan 2016

@author: time2
"""

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


import matplotlib.pyplot as plt



class TexPngConverter(object):
    """
    Convert Tex code to png images
    """


    def __init__(self, fontsize=12, dpi=300, format_='png'):
        """
        Initialises rendering settings
        """
        self._fontsize = fontsize
        self._dpi = dpi
        self._format = format_
    
    #TODO:
    #it appears pyplot doesn't release the figure unless you do it explicitly (which
    #thought was done by fig.close()?) so it may be leaking memory
    def render_latex(self,formula, output_file):
        """
        renders tex formula into a png image
        pyplot automatically renders text attached to figures
        as tex which is the technique used. the rest of the code
        is about removing all the unwanted bits such as the 
        figure itself from the image
        """
        
        #set pyplot to render tex found in text
        plt.rc('text', usetex=True)
        
        #create a figure on which display the text
        fig = plt.figure()
        
        #add text
        text = fig.text(0, 0, r'${}$'.format(formula), fontsize=self._fontsize)
    
        fig.savefig(BytesIO(), dpi=self._dpi)  # triggers rendering
        
        #get size of window
        bbox = text.get_window_extent()
        
        #scale according to dpi - soz about the imperial units
        width, height = bbox.size / float(self._dpi) + 0.05
        fig.set_size_inches((width, height))
        
        #move the text to the edge of the box
        dy = (bbox.ymin / float(self._dpi)) / height
        text.set_position((0, -dy))
    
        #write the file out
        fig.savefig(output_file, dpi=self._dpi, transparent = True, format = self._format)  
        
        #we're done with the figure now - close it
        plt.close(fig)
        
        #return file name - unnecessary but why not
        return output_file

"""
if __name__=="__main__":
    rend = TexPngConverter()
    rend.render_latex(r"\frac{n!}{k!(n-k)!}=1=mc^2", "teo.png")
"""
    
