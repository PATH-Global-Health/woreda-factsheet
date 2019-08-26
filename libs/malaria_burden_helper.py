from reportlab.platypus import TableStyle
from reportlab.lib import colors

from libs.utils import Utils, Align, MAX_HF
from libs.dataset_helper import Dataset


class MalariaBurden():
    @staticmethod
    def get_chart_data(row, woreda_hp):

        woreda_hp = woreda_hp.sort_values(by=['mb_2008_y'])

        if woreda_hp.shape[0] > MAX_HF:

            data = [[Utils.p('  Health Centers', 7, True, align=Align.LEFT), Utils.p(
                'Health Posts', 7, True, align=Align.LEFT), '', '', '', '', '']]

            d = Utils.col2row(woreda_hp)

            for i, r in enumerate(d):
                if i == 0:
                    data.append([MalariaBurden.generate_bar_chart(row), Utils.p(r[0][0], 7, align=Align.LEFT), Utils.p(
                        r[0][1], 7), Utils.p(r[1][0], 7, align=Align.LEFT), Utils.p(r[1][1], 7), Utils.p(r[2][0], 7, align=Align.LEFT), Utils.p(r[2][1], 7)])
                else:
                    data.append(['', Utils.p(r[0][0], 7, align=Align.LEFT), Utils.p(r[0][1], 7), Utils.p(
                        r[1][0], 7, align=Align.LEFT), Utils.p(r[1][1], 7), Utils.p(r[2][0], 7, align=Align.LEFT), Utils.p(r[2][1], 7)])
            return data

        else:
            return [[Utils.p('  Health Centers', 7, True, align=Align.LEFT), Utils.p('  Health Posts', 7, True, align=Align.LEFT)],
                    [MalariaBurden.generate_bar_chart(row), MalariaBurden.generate_hp_bar_chart(woreda_hp)]]

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

    # @staticmethod
    # def generate_hp_bar_chart(row):
    #     woreda_hp = Dataset.merged_woreda_hp_mb()
    #     # & (woreda_hp['mb_2008_y'] > 0)
    #     woreda_hp = woreda_hp[(woreda_hp['woreda'] == row['woreda'])]
    #     sorted_data = woreda_hp.sort_values(by=['mb_2008_y'])

    #     # shorten the name of each health post
    #     categories = sorted_data['name_hp'].apply(lambda x: Utils.short(x))
    #     data = sorted_data['mb_2008_y']

    #     return Utils.generate_bar_chart(categories, data, ylabel="# of malaria cases")

    @staticmethod
    def generate_hp_bar_chart(woreda_hp):
        # shorten the name of each health post
        categories = woreda_hp['name_hp'].apply(lambda x: Utils.short(x))
        data = woreda_hp['mb_2008_y']

        return Utils.generate_bar_chart(categories, data, ylabel="# of malaria cases")

    @staticmethod
    def get_chart_table_style(num_of_hp, num_of_rows):
        if num_of_hp > MAX_HF:
            return TableStyle(
                [  # Charts
                    ('VALIGN', (0, 1), (0, 1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('SPAN', (0, 1), (0, -1)),
                    ('LINEBELOW', (1, 0), (6, 0), 0.5,
                     colors.Color(0/255, 133/255, 183/255)),
                    ('LINEBELOW', (1, 1), (6, num_of_rows-1), 0.5,
                     colors.Color(239.9/255, 249.9/255, 253.5/255)),
                    # Entire table
                    # ('GRID', (0, 0), (-1, -1), 0.5,
                    #  colors.Color(91/255, 91/255, 93/255)),
                ])
        else:
            return TableStyle(
                [  # Charts
                    ('ALIGN', (0, 1), (1, 1), 'CENTER'),
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
