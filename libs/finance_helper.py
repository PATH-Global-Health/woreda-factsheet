from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class FinanceHelper():

    @staticmethod
    def get_data(row):
        data = [[Utils.p('IV. Finance', 10, True, '#0085B7', align=Align.LEFT), '', '', '', ''],
                [Utils.p('Woreda', 8, True, align=Align.LEFT), '', '', Utils.p(
                    'Health center', 8, True, align=Align.LEFT), ''],
                [Utils.p('Woreda allocate funds for malaria activities', 7, align=Align.LEFT),
                    Utils.p(row['bgt'], 7, align=Align.LEFT), '', '', Utils.p('Participate in health insurance', 7, True, '#5A5A5C')]
                ]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append(['', '', '', Utils.p(
                Utils.short(r['hfname']), 7, align=Align.LEFT), Utils.p('Yes' if r['insu'] == 1 else 'No', 7)])

        return data

    @staticmethod
    def get_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (4, 0)),  # Finance
             ('BACKGROUND', (0, 0), (4, 0), colors.Color(224/255, 236/255, 244/255)),

             # title
             ('LINEBELOW', (0, 1), (1, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 1), (4, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 2), (4, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             # last line
             ('LINEBELOW', (0, row_len-1), (1, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, row_len - 1), (4, row_len - 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Compress
             ('TOPPADDING', (0, 2), (-1, -1), 0),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0),
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])
