import os
import pandas as pd
from sigfig import round


class NumberConverter():
    CONVERT_COLUMNS = 'convert_columns'
    VALID_NUMBER = 'valid_number'

    def __init__(self, config_file='config.ini', source='source', dest='converted') -> None:
        self.config = self.read_config(config_file)
        self.source = source
        self.dest = dest
        pass

    def read_config(self, file):
        config = {}
        with open(file, 'r') as f:
            for line in f.readlines():
                items = line.strip().split('=')
                key = items[0].strip()
                value = items[1].strip()
                if key == self.CONVERT_COLUMNS:
                    config[self.CONVERT_COLUMNS] = value.split(',')
                elif key == self.VALID_NUMBER:
                    config[self.VALID_NUMBER] = int(value)
        return config

    def convert_all(self):
        current = os.getcwd()
        source = os.path.join(current, self.source)
        for f in os.listdir(source):
            if os.path.isfile(os.path.join(source, f)) and f.endswith('.xlsx'):
                file = os.path.join(current, self.source, f)
                data = self.convert(file)
                data.to_excel(os.path.join(current, self.dest, 'converted_' + f[:-4] + 'xlsx'), index=False, encoding='utf-8')
                print('文件 {} 处理成功'.format(f))

    def convert(self, file):
        df = pd.read_excel(file, header=0)
        for col in df.columns:
            if col in self.config[self.CONVERT_COLUMNS]:
                df[col] = df[col].apply(self.convert_v2)
        return df

    def convert_number(self, num):
        try:
            n = float(num)
            return str(round(n, sigfigs=self.config[self.VALID_NUMBER]))
        except Exception as e:
            return num

    def get_num_of_valid(self, num_str):
        n = num_str.replace('.', '')
        while n.startswith('0'):
            n = n[1:]
        return self.config[self.VALID_NUMBER] - len(n)

    def convert_v2(self, num):
        n = self.convert_number(num)
        try:
            float(n)
            valid_number = self.get_num_of_valid(n)
            if valid_number > 0:
                return n + '0' * valid_number
            else:
                return n
        except Exception as e:
            return n


# ***************** main *****************
if __name__ == '__main__':
    converter = NumberConverter()
    converter.convert_all()
    # print(converter.convert_v2(1.0004))