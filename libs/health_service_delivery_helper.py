from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class HSD():

    @staticmethod
    def get_data(row):

        data = [[Utils.p('VII. Health Service Delivery', 10, True, '#0085B7', align=Align.LEFT), '', '', '', '', '', '', '', ''],
                [Utils.p('Availability of Manuals and Guideline at',
                         8, True, align=Align.LEFT), '', '', '', '', '', '', '', ''],
                ['', Utils.p('Laboraotory diagnosis of malaria', 7, True, '#5A5A5C'), Utils.p('External qauallity assessment', 7, True, '#5A5A5C'), Utils.p('Bloold sample collection', 7, True, '#5A5A5C'), Utils.p('Giemsa preparation', 7, True, '#5A5A5C'),  Utils.p(
                    'Blood film prepartion', 7, True, '#5A5A5C'), Utils.p('Blood film staining', 7, True, '#5A5A5C'), Utils.p('Microscopy job aid', 7, True, '#5A5A5C'), Utils.p('Malaria treatment', 7, True, '#5A5A5C')],
                [Utils.p('Woreda', 7, align=Align.LEFT), Utils.em(row['labdxbk'], False), Utils.em(row['eqabk'], False), Utils.em(row['smplcolbk'], False), Utils.em(
                    row['gmsbk'], False), Utils.em(row['bfbk'], False), Utils.em(row['bfsbk'], False), Utils.em(row['micjbk'], False), Utils.em(row['malrxbk'], False)]
                ]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append([Utils.p(Utils.short(r['hfname']), 7, align=Align.LEFT), Utils.em(r['labdxbk_y'], False), Utils.em(r['eqabk_y'], False), Utils.em(r['splcolbk'], False), Utils.em(
                r['gmsbk_y'], False), Utils.em(r['bfbk_y'], False), Utils.em(r['bfsbk_y'], False), Utils.em(r['micbk_y'], False), Utils.em(r['malrxbk_y'], False)])

        return data

    @staticmethod
    def get_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (8, 0)),  # HSD
             ('BACKGROUND', (0, 0), (8, 0), colors.Color(224/255, 236/255, 244/255)),

             # Availability of Manuals and Guideline at woreda
             ('SPAN', (0, 1), (8, 1)),
             # Title bar
             ('LINEBELOW', (0, 2), (8, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             # Last line
             ('LINEBELOW', (0, row_len-1), (8, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             ('TOPPADDING', (0, 2), (-1, -1), 0.2),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0.2),
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])

    @staticmethod
    def get_dx_hc_data(row):
        data = [
            [Utils.p('Malaria diagnosis method used by HCs',
                     8, True, align=Align.LEFT), '', '', ''],
            ['', Utils.p('Microscop', 7, True, '#5A5A5C'), Utils.p(
                'RDT', 7, True, '#5A5A5C'), Utils.p('Both', 7, True, '#5A5A5C')]
        ]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append([Utils.p(r['hfname'], 7, align=Align.LEFT), Utils.p(
                r['dxmic'], 7), Utils.p(r['dxrdt'], 7), Utils.p(r['dxboth'], 7)])

        return data

    @staticmethod
    def get_dx_hc_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (3, 0)),  # Malaria diagnosis method used by HCs

             # Title bar
             ('LINEBELOW', (0, 1), (3, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             # Last line
             ('LINEBELOW', (0, row_len-1), (3, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             ('TOPPADDING', (0, 2), (-1, -1), 0.2),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0.2),
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])
