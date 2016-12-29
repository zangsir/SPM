
import numpy
 
from matplotlib import pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
 
# Generate the data
data = numpy.random.randn(24, 1024)
 
# The PDF document
pdf_pages = PdfPages('histograms.pdf')
 
# Generate the pages
nb_plots = data.shape[0]
nb_plots_per_page = 6
nb_plots_per_page_two=nb_plots_per_page*2
nb_pages = int(numpy.ceil(nb_plots / float(nb_plots_per_page)))
grid_size = (nb_plots_per_page, 2)
row_pos=0
for i, samples in enumerate(data):
    # Create a figure instance (ie. a new page) if needed
    print "i=",i
    if i % nb_plots_per_page == 0:
        fig = plot.figure(figsize=(8.27, 11.69), dpi=100)
        print 'new page'
    if i==0:
        col_pos=0
    elif i%2==0:
        col_pos=0
    else:
        col_pos=1

    

    # Plot stuffs !
    print "row,col:",row_pos,col_pos
    plot.subplot2grid(grid_size, (row_pos, col_pos))
    plot.hist(samples, 32, normed=1, facecolor='#808080', alpha=0.75)
    
    if i%2!=0:
        row_pos+=1
   
    # Close the page if needed
    
    if (i + 1) % nb_plots_per_page == 0 or (i + 1) == nb_plots:
        print 'saved page'
        plot.tight_layout()
        pdf_pages.savefig(fig)
   
# Write the PDF document to the disk
pdf_pages.close()