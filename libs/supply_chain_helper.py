from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class SCM():

    @staticmethod
    def get_data(row):

        data = [[Utils.p('VI. Supply Chain Management', 10, True, '#0085B7', align=Align.LEFT), '', '', '', ''],
                [Utils.p('Woreda', 8, True, align=Align.LEFT), '', '', Utils.p(
                    'Health center', 8, True, align=Align.LEFT), ''],
                [Utils.p('Uses Integrated Pharmaceutical Logistics System (IPLS)', 7, align=Align.LEFT), Utils.p(
                    row['ipls'], 7), '', '', Utils.p('IPLS use', 7, True, '#5A5A5C')],
                ]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append(['', '', '', Utils.p(Utils.short(
                r['hfname']), 7, align=Align.LEFT), Utils.p(r['ipls_y'], 7)])

        return data

    @staticmethod
    def get_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (4, 0)),  # SCM
             ('BACKGROUND', (0, 0), (4, 0), colors.Color(224/255, 236/255, 244/255)),

             ('LINEBELOW', (0, 1), (1, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 1), (4, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 2), (4, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (0, row_len-1), (1, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, row_len-1), (4, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             ('TOPPADDING', (0, 2), (-1, -1), 0.2),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0.2),
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])

    @staticmethod
    def get_stock_out_data(row):
        data = [
            [Utils.p('Stocked out of commodities in the last 6 months at',
                     8, True, align=Align.LEFT), '', '', '', '', '', '', ''],
            ['', Utils.p('Giemsa', 7, True, '#5A5A5C'), Utils.p('RDT', 7, True, '#5A5A5C'), Utils.p('Coartum', 7, True, '#5A5A5C'), Utils.p('Chloroquine tablet', 7, True, '#5A5A5C'), Utils.p(
                'Chloroquine syrups', 7, True, '#5A5A5C'), Utils.p('Artesunate Injection', 7, True, '#5A5A5C'), Utils.p('Artesunate suppository', 7, True, '#5A5A5C')],
            [Utils.p('Woreda', 7, align=Align.LEFT), Utils.em(row['gmsa']), Utils.em(row['rdt']), Utils.em(row['crtm']), Utils.em(
                row['chlrqntb']), Utils.em(row['chlrqnsyp']), Utils.em(row['artsntinj']), Utils.em(row['artsntsp'])]
        ]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append([Utils.p(Utils.short(r['hfname']), 7, align=Align.LEFT), Utils.em(r['gmsa_y']), Utils.em(r['rdt_y']), Utils.em(r['crtm_y']), Utils.em(
                r['chlrqntb_y']), Utils.em(r['chlrqnsyp_y']), Utils.em(r['artsntinj_y']), Utils.em(r['artsntsp_y'])])

        return data

    @staticmethod
    def get_stock_out_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (7, 0)),  # SCM

             ('LINEBELOW', (0, 0), (7, 0), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (0, 1), (7, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (0, row_len-1), (7, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             ('TOPPADDING', (0, 2), (-1, -1), 0.2),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0.2),
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])
