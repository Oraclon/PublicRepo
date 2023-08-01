import matplotlib.pyplot as plt;

class PlotData:
    def __init__(self, size= None):
        self.__size= size;
    def BuildPlot(self, index= None, view= None, label= None):
        plt.subplot(5,5, index+ 1, figsize=(200,200)) if not self.__size else plt.subplot(self.__size[0], self.__size[1], index+ 1);
        plt.imshow(view);
        plt.title(label);
        plt.axis('off');

    def ShowPlot(self):
        plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
        plt.show()
