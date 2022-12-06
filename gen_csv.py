import csv
from io import StringIO
    
    
class csv_gen():
    def create_nko (self, data):

        for sheet in data['sheets']:
            assert len(sheet['data']) >= 1, 'Данные не переданы для генерации csv файла'
            
            file = StringIO()
            writer = csv.writer(file,delimiter =';')

            writer.writerow(sheet['header'])

            for array in sheet['data']:
                assert len(array) == len(sheet['header']), 'Кол-во записей в массиве для заполнения csv файла не совпадает с заголовками'
                writer.writerow(array)
        return file.getvalue()