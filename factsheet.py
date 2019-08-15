from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from tqdm import tqdm

from libs.dataset_helper import Dataset
from libs.general_info_helper import GeneralInfo
from libs.human_resource_helper import HumanResource
from libs.malaria_burden_helper import MalariaBurden
from libs.finance_helper import FinanceHelper
from libs.title_helper import Title
from libs.his_helper import HIS
from libs.supply_chain_helper import SCM
from libs.health_service_delivery_helper import HSD


class FactSheet:
    def __init__(self):
        self.fact_sheet_pdf = 'output/factsheet.pdf'
        self.__doc = None
        self.__story = []

        pdfmetrics.registerFont(
            TTFont('mb', 'assets/fonts/Oswald-Regular.ttf'))

        pdfmetrics.registerFont(
            TTFont('ml', 'assets/fonts/MyriadPro-Light.ttf'))

    def __generate_title(self, row):
        data = Title.get_data(row)

        t = Table(data, colWidths='*')
        t.setStyle(Title.get_table_style())
        self.__story.append(t)

    def __generate_general_info(self, row):
        data = GeneralInfo.get_data(row)

        t = Table(data, colWidths='*',  spaceBefore=0)
        # ,rowHeights=[6*mm]*len(data))
        t.setStyle(GeneralInfo.get_table_style())
        self.__story.append(t)

    def __generate_malaria_burden(self, row):
        data = MalariaBurden.get_summary_data(row)

        t = Table(data, colWidths='*',  spaceBefore=0)
        t.setStyle(MalariaBurden.get_table_style())
        self.__story.append(t)

        data = MalariaBurden.get_chart_data(row)
        t = Table(data, colWidths='*',  spaceBefore=2)
        t.setStyle(MalariaBurden.get_chart_table_style())
        self.__story.append(t)

    def __generate_hr(self, row):
        data = HumanResource.get_res_data(row)
        t = Table(data, colWidths='*',  spaceBefore=0)
        t.setStyle(HumanResource.get_res_table_style())
        self.__story.append(t)

        data = HumanResource.get_chart_data(row)
        t = Table(data, colWidths='*',  spaceBefore=10)
        t.setStyle(HumanResource.get_chart_table_style())
        self.__story.append(t)

        data = HumanResource.get_tw_data(row)
        t = Table(data, colWidths='*',  spaceBefore=5)
        t.setStyle(HumanResource.get_tw_table_style())
        self.__story.append(t)

        data = HumanResource.get_thc_data(row)
        t = Table(data, colWidths='*',  spaceBefore=10)
        t.setStyle(HumanResource.get_thc_table_style(data.__len__()))
        self.__story.append(t)

    def __generate_finance(self, row):
        data = FinanceHelper.get_data(row)
        t = Table(data, colWidths=[75*mm, 18*mm, 5*mm,
                                   None, None],  spaceBefore=10)
        t.setStyle(FinanceHelper.get_table_style(data.__len__()))
        self.__story.append(t)

    def __generate_his(self, row):
        data = HIS.get_data(row)
        t = Table(data, colWidths=[75*mm, None, 5*mm,
                                   35*mm, 23*mm, None, None],  spaceBefore=10)
        t.setStyle(HIS.get_table_style(data.__len__()))
        self.__story.append(t)

    def __generate_scm(self, row):
        data = SCM.get_data(row)
        t = Table(data, colWidths=[75*mm, 18*mm, 5 *
                                   mm, None, None], spaceBefore=10)
        t.setStyle(SCM.get_table_style(data.__len__()))
        self.__story.append(t)

        data = SCM.get_stock_out_data(row)
        t = Table(data, colWidths=[30*mm, None, None,
                                   None, None, None, None, 25*mm], spaceBefore=5)
        t.setStyle(SCM.get_stock_out_table_style(data.__len__()))
        self.__story.append(t)

    def __generate_hsd(self, row):
        data = HSD.get_data(row)
        t = Table(data, colWidths='*', spaceBefore=10)
        t.setStyle(HSD.get_table_style(data.__len__()))
        self.__story.append(t)

        data = HSD.get_dx_hc_data(row)
        t = Table(data, colWidths='*', spaceBefore=5)
        t.setStyle(HSD.get_dx_hc_table_style(data.__len__()))
        self.__story.append(t)

    def generate(self):
        self.__doc = SimpleDocTemplate(self.fact_sheet_pdf, pagesize=A4,
                                       rightMargin=20, leftMargin=20,
                                       topMargin=54, bottomMargin=50)

        Dataset.woreda.sort_values(
            by=['region', 'zone', 'wname'], inplace=True)

        i = 0
        total = len(Dataset.woreda)
        for index, row in tqdm(Dataset.woreda.iterrows(), total=total):
            self.__generate_title(row)
            self.__generate_general_info(row)
            self.__generate_malaria_burden(row)
            self.__generate_hr(row)
            self.__generate_finance(row)
            self.__generate_his(row)
            self.__generate_scm(row)
            self.__generate_hsd(row)
            self.__story.append(PageBreak())
            # i += 1
            # if i == 25:
            #     break

        print('Writing to {}. Please wait...'.format(
            self.fact_sheet_pdf))
        self.__doc.build(self.__story, onFirstPage=Title.header_footer,
                         onLaterPages=Title.header_footer)
        print('Done')


if __name__ == "__main__":
    factsheet = FactSheet()
    factsheet.generate()
