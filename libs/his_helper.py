from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class HIS():

    @staticmethod
    def get_data(row):
        data = [[Utils.p('V. Health Information System', 10, True, '#0085B7', align=Align.LEFT), '', '', '', '', '', ''],
                [Utils.p('Woreda', 8, True, align=Align.LEFT), '', '', Utils.p(
                    'Health center', 8, True, align=Align.LEFT), '', '', ''],
                [Utils.p('Have malaria epidemic monitoring charts', 7, align=Align.LEFT),
                 Utils.p(row['chart'], 7), '', '', Utils.p('Have epidemic chart', 7,  True, '#5A5A5C', align=Align.LEFT), Utils.p('Calculate API', 7,  True, '#5A5A5C', align=Align.LEFT), Utils.p('Calculate TPR', 7,  True, '#5A5A5C', align=Align.LEFT)],
                [Utils.p('Calculate Total Positive Rate(TPR)', 7, align=Align.LEFT),
                 Utils.p(row['tpr'], 7), '', '', '', '', ''],
                [Utils.p('Calculate Annual Parasitic Incidence(API)', 7, align=Align.LEFT),
                 Utils.p(row['api'], 7), '', '', '', '', ''],
                [Utils.p('Include NGO and private Health Facilities in PHEM report', 7, align=Align.LEFT),
                 Utils.p(row['priv'], 7), '', '', '', '', '']
                ]

        woreda_hc = Dataset.merged_woreda_hc()

        i = 0
        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            if i < 3:
                data[i+3][3] = Utils.p(Utils.short(r['hfname']),
                                       7, align=Align.LEFT)
                data[i+3][4] = Utils.p(r['chart_y'], 7)
                data[i+3][5] = Utils.p(r['api_y'], 7)
                data[i+3][6] = Utils.p(r['tpr_y'], 7)
            else:
                data.append(['', '', '', Utils.p(Utils.short(r['hfname']), 7, align=Align.LEFT), Utils.p(
                    r['chart_y'], 7), Utils.p(r['api_y'], 7), Utils.p(r['tpr_y'], 7)])
            i += 1
        return data

    @staticmethod
    def get_table_style(row_len):
        return TableStyle(
            [('SPAN', (0, 0), (6, 0)),  # Finance
             ('BACKGROUND', (0, 0), (6, 0), colors.Color(224/255, 236/255, 244/255)),

             ('LINEBELOW', (0, 1), (1, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 1), (6, 1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, 2), (6, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (0, row_len-1), (1, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (3, row_len-1), (6, row_len-1), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             ('TOPPADDING', (0, 2), (-1, -1), 0.2),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0.2),
             #('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255))
             ])
