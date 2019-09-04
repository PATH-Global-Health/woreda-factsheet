from reportlab.platypus import TableStyle, Image
from reportlab.lib import colors

from libs.utils import Utils, Align
from libs.dataset_helper import Dataset


class GeneralInfo():
    @staticmethod
    def generate_map(row):
        selected_district = Dataset.district_map[Dataset.district_map['wcode']
                                                 == row['woreda']]

        return Utils.generate_map(Dataset.region_map, Dataset.district_map, selected_district)

    @staticmethod
    def get_data(row):
        return [['', '', GeneralInfo.generate_map(row)],  # Utils.p('Contact person: {}'.format('+251...'), 7, True)
                [Utils.p('I. General Information', 10,
                         True, '#0085B7', align=Align.LEFT), '', ''],
                [Utils.p('Number of Health Facilities', 8,
                         True, align=Align.LEFT), '', ''],
                [Utils.p('Health Centers', align=Align.LEFT),
                 Utils.p(row['num_HC']), ''],
                [Utils.p('Health Posts', align=Align.LEFT),
                 Utils.p(row['num_HP']), ''],
                [Utils.p('Population - 2008 EC', align=Align.LEFT),
                 Utils.p(row['pop2008']), '']
                ]

    @staticmethod
    def get_table_style():
        return TableStyle(
            [('SPAN', (0, 1), (1, 1)),  # General Info
             # General Info
             ('BACKGROUND', (0, 1), (1, 1), colors.Color(224/255, 236/255, 244/255)),

             # Num of health facilities
             ('SPAN', (0, 2), (1, 2)),
             ('LINEBELOW', (0, 2), (1, 2), 0.5,
              colors.Color(0/255, 133/255, 183/255)),

             # Map
             ('SPAN', (-1, -6), (-1, -1)),
             ('VALIGN', (-1, -6), (-1, -1), 'TOP'),

             # Entire table
             # ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(91/255, 91/255, 93/255)),
             ])
