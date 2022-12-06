import xlwt
from io import BytesIO

class exel_gen():
    def generate_excel(self, data):
        f = BytesIO()
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.bold = True   
        style0 = xlwt.XFStyle()
        style0.font = font0
        
        wb = xlwt.Workbook()
        for sheet in data['sheets']:
            assert len(sheet['data']) >= 1, 'Данные не переданы для генерации xlsx файла'
            ws = wb.add_sheet(sheet['name'])
            for header in sheet['header']:
                ws.write(0, sheet['header'].index(header), header)
            for row in sheet['data']:
                assert len(row) == len(sheet['header']), 'Длина строки для таблицы не совпадает с длинною заголовков таблицы'.format(len(row), len(sheet['header']))
                for cell in row:
                    ws.write(sheet['data'].index(row)+1, row.index(cell), cell)
        wb.save(f)
        return f.getvalue()