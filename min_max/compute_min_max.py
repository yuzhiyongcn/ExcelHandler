import pandas as pd
import sys


def compute_max_min(file):
    df = pd.read_csv(
        file,
        encoding="gbk",
        header=0,
        index_col=0,
        sep=',',
        names=[
            'Time',
            '330温度',
            '330湿度',
            '329温度',
            '329湿度',
            '327温度',
            '327湿度',
            '328温度',
            '328湿度',
        ],
    )

    df.loc['最大值'] = df.apply(lambda x: x.max())
    df.loc['最小值'] = df.apply(lambda x: x.min())
    df.loc['差值'] = df.apply(lambda x: float(x.max()) - float(x.min()))
    df.to_csv(
        'new-' + file,
        encoding="gbk",
    )
    pass


if __name__ == '__main__':
    file = sys.argv[1]
    compute_max_min(file)