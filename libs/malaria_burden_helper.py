from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class MalariaBurden():
    @staticmethod
    def get_chart_data(row):
        return [['Health Centers', 'Health Posts'],
                [MalariaBurden.generate_bar_chart(row), MalariaBurden.generate_hp_bar_chart(row)]]

    @staticmethod
    def generate_bar_chart(row):
        woreda_hc = Dataset.merged_woreda_hc_mb()
        woreda_hc = woreda_hc[woreda_hc['woreda'] == row['woreda']]
        sorted_data = woreda_hc.sort_values(by=['mb_2008_y'])

        category = sorted_data['name_hc'].apply(lambda x: Utils.short(x))
        data = sorted_data['mb_2008_y']

        return Utils.generate_bar_chart(category, data, ylabel='# of malaria cases')

    @staticmethod
    def generate_pie_chart(row):
        woreda_hp = Dataset.merged_woreda_hp_mb()
        categories, data = Utils.rearrange(woreda_hp[(woreda_hp['woreda'] == row['woreda'])
                                                     & (woreda_hp['mb_2008_y'] > 0)], 'name_hp', 'mb_2008_y')
        # shorten the name of each health post
        categories = categories.apply(lambda x: Utils.short(x))

        return Utils.generate_pie_chart(categories, data)

    @staticmethod
    def generate_hp_bar_chart(row):
        woreda_hp = Dataset.merged_woreda_hp_mb()
        woreda_hp = woreda_hp[(woreda_hp['woreda'] == row['woreda']) & (
            woreda_hp['mb_2008_y'] > 0)]
        sorted_data = woreda_hp.sort_values(by=['mb_2008_y'])

        # shorten the name of each health post
        categories = sorted_data['name_hp'].apply(lambda x: Utils.short(x))
        data = sorted_data['mb_2008_y']

        return Utils.generate_bar_chart(categories, data, ylabel="# of malaria cases")

    @staticmethod
    def get_chart_table_style():
        return TableStyle(
            [  # Title bar
                ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
                ('TEXTCOLOR', (0, 0), (1, 0), '#5A5A5C'),
                ('FONTNAME', (0, 0), (1, 0), 'mb'),
                ('FONTSIZE', (0, 0), (1, 0), 7),

                # Charts
                ('VALIGN', (0, 1), (1, 1), 'TOP'),
                ('TOPPADDING', (0, 1), (1, 1), 0),
                ('BOTTOMPADDING', (0, 1), (1, 1), 0),
                # Entire table
                # ('GRID', (0, 0), (-1, -1), 0.5,
                #  colors.Color(91/255, 91/255, 93/255)),
            ])

    @staticmethod
    def get_summary_data(row):
        woreda_hc = Dataset.merged_woreda_hc_mb()
        woreda_hc = woreda_hc[woreda_hc['woreda'] == row['woreda']].sum()

        woreda_hp = Dataset.merged_woreda_hp_mb()
        woreda_hp = woreda_hp[woreda_hp['woreda'] == row['woreda']].sum()

        return [[Utils.p('II. Baseline Malaria Burden, 2008 EFY', 10,
                         True, '#0085B7', align=Align.LEFT), '', '', ''],
                [Utils.p('Malaria cases reported by', 8, True, align=Align.LEFT), Utils.p('Health Centers', 7, True, '#5A5A5C'), Utils.p(
                    'Health Posts', 7, True, '#5A5A5C'), Utils.p('Total', 7, True, '#5A5A5C')],
                ['', Utils.p(woreda_hc['mb_2008_y']), Utils.p(woreda_hp['mb_2008_y']), Utils.p(
                    woreda_hc['mb_2008_y'] + woreda_hp['mb_2008_y'])]
                ]

    @staticmethod
    def get_table_style():
        return TableStyle(
            [('SPAN', (0, 0), (3, 0)),  # Baseline
             ('BACKGROUND', (0, 0), (3, 0), colors.Color(224/255, 236/255, 244/255)),

             # Title bar
             ('LINEBELOW', (0, 1), (3, 1), 0.5,
                colors.Color(0/255, 133/255, 183/255)),
             ('LINEBELOW', (0, 2), (3, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Entire table
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255)),
             ])
