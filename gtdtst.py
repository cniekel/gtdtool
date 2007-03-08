from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate
from reportlab.platypus import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch,cm
from reportlab.lib.pagesizes import A4
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()


class GTDPageTemplate(PageTemplate):
    def __init__(self, id, pageSize=defaultPageSize):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        border = 0.3*cm

        miniwidth = (self.pageWidth / 2) - 2*border
        miniheight = (self.pageHeight / 2) - 2*border

        #self.f4 = Frame(border, border, miniwidth, miniheight, id='p4')
        #self.f1 = Frame(self.pageWidth/2 + border, border, miniwidth, miniheight, id='p1')
        #self.f2 = Frame(self.pageWidth/2 + border, self.pageHeight/2 + border, miniwidth, miniheight, id='p2')
        #self.f3 = Frame(border, self.pageHeight/2 + border, miniwidth, miniheight, id='p3')
        self.f4 = Frame(0, 0, miniwidth, miniheight, id='p4')
        self.f1 = Frame(miniwidth, 0, miniwidth, miniheight, id='p1')
        self.f2 = Frame(miniwidth, miniheight, miniwidth, miniheight, id='p2')
        self.f3 = Frame(0, miniheight, miniwidth, miniheight, id='p3')

        PageTemplate.__init__(self, id, [self.f1, self.f2, self.f3, self.f4])
        
class GTDDocTemplate(BaseDocTemplate):
    def __init__(self, file, **kw):
        BaseDocTemplate.__init__(self,file, **kw)

def myPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75*inch, 'Page %d %s' % (doc.page, 'test'))

def go():
    doc = GTDDocTemplate('phello.pdf', pageSize=A4)
    doc.addPageTemplates(GTDPageTemplate('gtd', doc.pagesize))
    Story=[]
    style = styles['Normal']
    style.leftIndent = 0.75*inch
    style.firstLineIndent = 0
    style.spaceAfter = 3
    style.refresh()
    style.listAttrs()
    for i in range(8):
        bogustext = ('This is <br>paragraph <font color="red"><i>number</i></font> %s' % i) * 20
        p = KeepTogether([Paragraph('Yo %d'%i, style), Paragraph(bogustext, style)])
        Story.append(p)
        Story.append(Spacer(1, 0.2*inch))
    doc.build(Story)#, onFirstPage=myPages, onLaterPages=myPages)

if __name__ == '__main__':
    go()
