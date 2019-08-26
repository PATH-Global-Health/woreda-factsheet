import numpy as np
from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class HumanResource():

    @staticmethod
    def get_res_data(row):
        return [[Utils.p('III. Human Resource', 10, True, '#0085B7', align=Align.LEFT), '', '', '', ''],
                [Utils.p('Human resource availability',
                         8, True, align=Align.LEFT), '', '', '', ''],
                [' Woreda level', 'Malaria focal person',
                    'HMIS', 'PHEM', 'Pharmacy'],
                ['', Utils.n(row['malfp']), Utils.n(row['hmis']),
                 Utils.n(row['phem']), Utils.n(row['pharm'])]
                ]

    @staticmethod
    def get_res_table_style():

        return TableStyle(
            [('SPAN', (0, 0), (4, 0)),  # Human Resource
             ('BACKGROUND', (0, 0), (4, 0), colors.Color(224/255, 236/255, 244/255)),

             # Human resource availability
             ('SPAN', (0, 1), (4, 1)),

             # Title
             ('ALIGN', (1, 2), (4, 2), 'CENTER'),
             ('LINEBELOW', (0, 2), (4, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('FONTNAME', (0, 2), (4, 2), 'mb'),
             ('FONTSIZE', (0, 2), (0, 2), 8),
             ('FONTSIZE', (1, 2), (4, 2), 7),
             ('TEXTCOLOR', (1, 2), (4, 2), '#5A5A5C'),

             # Table content
             ('ALIGN', (1, 3), (4, 3), 'CENTER'),
             ('LINEBELOW', (0, 3), (4, 3), 0.5,
              colors.Color(0/255, 133/255, 183/255)),
             ('FONTNAME', (1, 3), (4, 3), 'ml'),
             ('FONTSIZE', (1, 3), (4, 3), 7),

             # Table compress
             ('TOPPADDING', (0, 2), (-1, -1), 0),
             ('BOTTOMPADDING', (0, 2), (-1, -1), 0),
             ])

    @staticmethod
    def get_chart_data(row):
        return [[' Health center level', 'Health post level - (Number of HEWs)'],
                [HumanResource.get_stacked_bar_chart(
                    row), HumanResource.generate_hew_bar_chart(row)]
                ]

    @staticmethod
    def get_stacked_bar_chart(row):
        woreda_hc = Dataset.merged_woreda_hc()
        woreda_hc = woreda_hc[woreda_hc['woreda'] == row['woreda']]

        categories = np.array(
            woreda_hc['hfname'].apply(lambda x: Utils.short(x)))
        clinical = np.array(woreda_hc['clncstaff'])
        lab = np.array(woreda_hc['labstaff'])
        pharmacy = np.array(woreda_hc['pharm'])
        phem = np.array(woreda_hc['phem_y'])
        hmis = np.array(woreda_hc['hmis_y'])

        values = [clinical, lab, pharmacy, phem, hmis]
        color_label = [('#009076', 'Clinical'), ('#00dca6', 'Laboratory'),
                       ('#ff483a', 'Pharmacy'), ('#18a1cd', 'PHEM'), ('#15607a', 'HMIS')]

        return Utils.generate_stacked_bar_chart(categories, values, color_label, ylabel='# of staff')

    @staticmethod
    def generate_hew_bar_chart(row):
        woreda_hp = Dataset.merged_woreda_hp()
        woreda_hp = woreda_hp[woreda_hp['woreda'] == row['woreda']]
        sorted_data = woreda_hp.sort_values(by=['total_extension'])

        category = sorted_data['hpname'].apply(lambda x: Utils.short(str(x)))
        data = sorted_data['total_extension']

        return Utils.generate_bar_chart(category, data, ylabel='# of HEWs')

    @staticmethod
    def get_hew_tree_map(row):

        woreda_hp = Dataset.merged_woreda_hp()
        sizes = []
        labels = []
        for index, r in woreda_hp[(woreda_hp['woreda'] == row['woreda']) & (woreda_hp['total_extension'] > 0)].iterrows():
            sizes.append(r['total_extension'])
            labels.append('{}\n{:.0f}'.format(
                Utils.short(r['hpname']), r['total_extension']))

        return Utils.generate_tree_map(labels, sizes)

    @staticmethod
    def get_chart_table_style():
        return TableStyle(
            [  # Title
                ('FONTNAME', (0, 0), (1, 0), 'mb'),
                ('FONTSIZE', (0, 0), (1, 0), 8),
                # Charts
                ('ALIGN', (0, 1), (1, 1), 'CENTER'),
                ('TOPPADDING', (0, 1), (1, 1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                # ('GRID', (0, 0), (-1, -1), 0.5,
                #  colors.Color(91/255, 91/255, 93/255)),
            ])

    @staticmethod
    def get_tw_data(row):
        return [[Utils.p('Trained staff (in previous 12 months) avilability', 8, True, align=Align.LEFT), '', '', '', '', '', '', ''],
                [' Woreda level', 'Vector control', 'Diagnosis', 'Treatment',
                    'Severe case mngt. ', 'IRT', 'iCCM', 'Supply management'],
                ['', Utils.n(row['vect']), Utils.n(row['dx']), Utils.n(row['rx']), Utils.n(
                    row['mxsever']), Utils.n(row['irt']), Utils.n(row['iccm']), Utils.n(row['scm'])]
                ]

    @staticmethod
    def get_tw_table_style():
        return TableStyle(
            [  # Trained staff availability
                ('SPAN', (0, 0), (7, 0)),

                # Title
                ('ALIGN', (1, 1), (7, 1), 'CENTER'),
                ('LINEBELOW', (0, 1), (7, 1), 0.5,
                 colors.Color(0/255, 133/255, 183/255)),
                ('FONTNAME', (0, 1), (7, 1), 'mb'),
                ('FONTSIZE', (0, 1), (0, 1), 8),
                ('FONTSIZE', (1, 1), (7, 1), 7),
                ('TEXTCOLOR', (1, 1), (7, 1), '#5A5A5C'),

                # Table content
                ('ALIGN', (1, 2), (7, 2), 'CENTER'),
                ('LINEBELOW', (0, 2), (7, 2), 0.5,
                 colors.Color(0/255, 133/255, 183/255)),
                ('FONTNAME', (1, 2), (7, 2), 'ml'),
                ('FONTSIZE', (1, 2), (7, 2), 7),

                ('TOPPADDING', (0, 1), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
                # ('GRID', (0, 0), (-1, -1), 0.5,
                #  colors.Color(91/255, 91/255, 93/255)),
            ])

    @staticmethod
    def get_thc_data(row):
        data = [[' Health center level', 'HCs', 'Vector control', 'Diagnosis', 'Treatment',
                 'Severe case mngt.', 'IRT', 'M&E', 'ICCM', 'Supply Management', 'SBCC']]

        woreda_hc = Dataset.merged_woreda_hc()

        for index, r in woreda_hc[woreda_hc['woreda'] == row['woreda']].iterrows():
            data.append(['', Utils.short(r['hfname']), Utils.n(r['vect_y']), Utils.n(r['dx_y']), Utils.n(r['rx_y']), Utils.n(
                r['mxsevr']), Utils.n(r['IRT']), Utils.n(r['sme_y']), Utils.n(r['iccm_y']), Utils.n(r['scm_y']), Utils.n(r['sbcc_y'])])

        return data

    @staticmethod
    def get_thc_table_style(row_len):
        return TableStyle(
            [  # Title
                ('ALIGN', (1, 0), (10, 0), 'CENTER'),
                ('LINEBELOW', (0, 0), (10, 0), 0.5,
                 colors.Color(0/255, 133/255, 183/255)),
                ('FONTNAME', (0, 0), (10, 0), 'mb'),
                ('FONTSIZE', (0, 0), (0, 0), 8),
                ('FONTSIZE', (1, 0), (10, 0), 7),
                ('TEXTCOLOR', (1, 0), (10, 0), '#5A5A5C'),

                # table content
                ('ALIGN', (2, 1), (10, row_len-1), 'CENTER'),
                ('FONTNAME', (1, 1), (10, row_len-1), 'ml'),
                ('FONTSIZE', (1, 1), (10, row_len-1), 7),
                ('LINEBELOW', (0, row_len-1), (10, row_len-1), 0.5,
                 colors.Color(0/255, 133/255, 183/255)),

                # Entire table
                ('TOPPADDING', (0, 1), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
                # ('GRID', (0, 0), (-1, -1), 0.5,
                #  colors.Color(91/255, 91/255, 93/255)),
            ])
