from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate
from reportlab.platypus import KeepTogether
from reportlab.platypus.flowables import UseUpSpace
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch,cm
from reportlab.lib.pagesizes import A4
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()


class GTDPageTemplate(PageTemplate):
    def __init__(self, id, pageSize=defaultPageSize):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        border = 1.0*cm

        miniwidth = (self.pageWidth / 2) - 2*border
        miniheight = (self.pageHeight / 2) - 2*border

        # with border, in booklet order (but not rotated)
        #self.f4 = Frame(border, border, miniwidth, miniheight, id='p4')
        #self.f1 = Frame(self.pageWidth/2 + border, border, miniwidth, miniheight, id='p1')
        #self.f2 = Frame(self.pageWidth/2 + border, self.pageHeight/2 + border, miniwidth, miniheight, id='p2')
        #self.f3 = Frame(border, self.pageHeight/2 + border, miniwidth, miniheight, id='p3')

        self.bl = Frame(border, border, miniwidth, miniheight, id='BL')
        self.br = Frame(self.pageWidth/2 + border, border, miniwidth, miniheight, id='BR')
        self.ur = Frame(self.pageWidth/2 + border, self.pageHeight/2 + border, miniwidth, miniheight, id='UR')
        self.ul = Frame(border, self.pageHeight/2 + border, miniwidth, miniheight, id='UL')

        PageTemplate.__init__(self, id, [self.ul, self.ur, self.bl, self.br])
        
class GTDDocTemplate(BaseDocTemplate):
    def __init__(self, file, **kw):
        BaseDocTemplate.__init__(self,file, **kw)

headerstyle = ParagraphStyle(name='listheader', 
        fontName='Helvetica-Bold', fontSize=9, leftIndent=0, firstLineIndent=0,
        spaceAfter = 0)
actionstyle = ParagraphStyle(name='listaction', 
        fontName='Helvetica', fontSize=9, leftIndent=0.5*cm, firstLineIndent=0,
        spaceAfter = 0)
projstyle = ParagraphStyle(name='listproject', 
        fontName='Helvetica-Oblique', fontSize=8, leftIndent=1.5*cm, 
        firstLineIndent=0, spaceAfter = 1)

def print_actionlist(categories, projects, fname):
    doc = GTDDocTemplate(fname, pageSize=A4)
    doc.addPageTemplates(GTDPageTemplate('gtd', doc.pagesize))
    Story = []
    
    style = styles['Normal']
    style.leftIndent = 0.5*cm
    style.firstLineIndent = -0.5*cm
    style.spaceAfter = 0
    style.refresh()

    if categories:
        for k in categories:
            h = Paragraph(str(k).title(), headerstyle)
            contents = [h]
            for action in categories[k]:
                contents.append(Paragraph(action.what, actionstyle))
                contents.append(Paragraph(action.project.title, projstyle))

            p = KeepTogether(contents)
            Story.append(p)
            Story.append(Spacer(1, 0.2*inch))

    if categories and projects:
        Story.append(UseUpSpace())
    if projects:
        for p in projects:
            h = Paragraph(p.title, headerstyle)
            contents = [h]
            for paragraph in p.paras:
                contents.append(Paragraph(paragraph, style))
            #for ac in p.actions:
                #contents.append(Paragraph(ac.what, actionstyle))
            p = KeepTogether(contents)
            Story.append(p)
            Story.append(Spacer(0, 0.6*cm))

    doc.build(Story)


