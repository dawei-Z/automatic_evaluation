import pandas as pd
import timeit


def get_hindex(citation_list):
    """Get h-index of given citation data"""
    i = 1
    for eachcite in citation_list:
        if i >= eachcite:
            hindex = i - 1
            return hindex
        else:
            i += 1


def data_cleaning():
    """Clean the empty columns which will created in reindexing the DataFrame and h-index is NaN"""
    with open('list.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            temp_df = pd.read_csv('uniData\\' + line.rstrip() + '.csv')
            temp_df = temp_df.drop('Unnamed: 0', 1)
            temp_df = temp_df.dropna()
            with open('uniData\\' + line.rstrip() + '.csv', 'w', encoding='utf-8') as file:
                temp_df.to_csv(file)


def manipulate_hhindex():
    """Manipulate the data and output result in hhindex pattern"""
    data_cleaning()
    df = pd.DataFrame()
    result_dataset = pd.DataFrame()
    with open('list.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            temp_df = pd.read_csv('uniData\\' + line.rstrip() + '.csv')
            temp_df = temp_df.sort_values(by=['hindex'], ascending=False)
            i = 0
            for hindex in temp_df['hindex']:
                if i > int(hindex):
                    hhindex = i - 1
                else:
                    i += 1
            temp_series = pd.Series({'university': line.rstrip(),
                                    'hhindex': hhindex})
            df = df.append([temp_series])
    df = df.sort_values(by=['hhindex'], ascending=False)
    df = df.reset_index()
    df = df.drop('index', 1)
    for index, row in df.iterrows():
        dif = difference(row['university'], index + 1)
        new_series = pd.Series({'university': row['university'],
                               'hhindex': row['hhindex'],
                               'difference': dif})
        result_dataset = result_dataset.append(new_series, ignore_index=True)
    return result_dataset


def manipulate_avg():
    """Manipulate data and output result in average pattern"""
    data_cleaning()
    df = pd.DataFrame()
    result_dataset = pd.DataFrame()
    with open('list.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            sum = 0
            temp_df = pd.read_csv('uniData\\' + line.rstrip() + '.csv')
            useful_data = temp_df.where(temp_df['hindex'] > 5)
            useful_data = useful_data.drop('Unnamed: 0', 1)
            useful_data = useful_data.dropna()
            for hindex in useful_data['hindex']:
                sum += hindex
            count = len(temp_df.index)
            avg = sum / count
            temp_series = pd.Series({'university': line.rstrip(),
                                     'hindex_average': avg})
            df = df.append(temp_series, ignore_index=True)
    df = df.sort_values(by=['hindex_average'], ascending=False)
    df = df.reset_index()
    df = df.drop('index', 1)
    for index, row in df.iterrows():
        dif = difference(row['university'], index + 1)
        new_series = pd.Series({'university': row['university'],
                               'hindex_average': row['hindex_average'],
                               'difference': dif})
        result_dataset = result_dataset.append(new_series, ignore_index=True)
    return result_dataset


def validation():
    """Validate the collected data"""
    with open('list.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            temp_df = pd.read_csv('uniData\\' + line.rstrip() + '.csv')
            length = len(temp_df.index)



def difference(uniName, currentIndex):
    """Return the difference between the new rank and original rank(REF 2014)"""
    with open('list.txt', 'r', encoding='utf-8-sig') as f:
        i = 1
        for line in f:
            if line.rstrip() == uniName:
                return int(i - currentIndex)
            else:
                i += 1


def run():
    with open('FinalResult_pattern1.csv', 'w', encoding='utf-8') as f1:
        temp_data = manipulate_hhindex()
        temp_data.to_csv(f1)
    with open('FinalResult_pattern2.csv', 'w', encoding='utf-8') as f2:
        sub_data = manipulate_avg()
        sub_data.to_csv(f2)
    print("DONE!")


print(timeit.timeit(run, number=1))
