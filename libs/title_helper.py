from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

from libs.utils import Utils, Align


class Title():

    @staticmethod
    def get_data(row):
        wname = Utils.p(row['wname'], 26, False, '#0085B7', Align.LEFT)
        region_zone = '{}, {}'.format(row['region'], row['zone'])

        return [[wname, region_zone]]

    @staticmethod
    def get_table_style():
        return TableStyle(
            [('LINEBELOW', (0, 0), (-1, -1), 1, colors.Color(0, 133/255, 183/255)),
             ("BOTTOMPADDING", (0, 0), (0, 0), 22),
             ("TEXTCOLOR", (1, 0), (1, 0),
              colors.Color(0, 133/255, 183/255)),
             ("ALIGN", (1, 0), (1, 0), 'RIGHT'),
             #  ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])

    @staticmethod
    def header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # header
        canvas.drawImage('assets/images/FMOH.png',
                         doc.leftMargin + 10, doc.height + doc.topMargin, 48, 48)
        canvas.drawImage('assets/images/EPHI.png',
                         doc.leftMargin + doc.width - 53, doc.height + doc.topMargin, 48, 48)

        header = Utils.p('Malaria Elimination Baseline', 18, True, '#0085B7')
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin,
                      doc.height + doc.topMargin + h + 20)

        header = Utils.p(
            'Woreda Factsheet', 16, False, '#0085B7')
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin,
                      doc.height + doc.topMargin + h)

        canvas.setLineWidth(.3)
        #canvas.setStrokeColorRGB(0, 1, 0.3)
        canvas.line(doc.leftMargin + 5.5, doc.bottomMargin-15,
                    doc.width+14, doc.bottomMargin-15)

        # Footer
        canvas.drawImage('assets/images/SMMES.png',
                         doc.leftMargin + 5, doc.bottomMargin - 45, 158, 25)
        canvas.drawImage('assets/images/WHO.png',
                         doc.leftMargin + 188, doc.bottomMargin - 45, 63, 23)  # 188:- 158 + 25 +5
        canvas.drawImage('assets/images/CHAI.png',
                         doc.leftMargin + 276, doc.bottomMargin - 45, 43, 23)  # 276:- 188 + 63 + 25
        canvas.drawImage('assets/images/TU.png',
                         doc.leftMargin + 344, doc.bottomMargin - 45, 63, 23)  # 344:- 276 + 43 + 25
        canvas.drawImage('assets/images/PATH.png',
                         doc.leftMargin + 432, doc.bottomMargin - 45, 49, 19)  # 432:- 344 + 63 + 50

        # Page number
        canvas.setFont("mb", 7)
        canvas.setFillColor('#0085B7')
        page_num = canvas.getPageNumber()
        page_num_text = 'Page {}'.format(page_num)
        # 524:- 158 + 50 + 43 + 50 + 63 + 50 + 110
        canvas.drawRightString(doc.leftMargin + 524,
                               doc.bottomMargin - 40, page_num_text)

        # Release the canvas
        canvas.restoreState()
