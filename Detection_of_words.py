import pandas as pd
from pandasgui import show
import re

df = pd.read_excel('results11.xls')
df_unique = df.drop_duplicates(subset=['Satz', 'Kontext'])  # remove dublicates from excel list

#find all word in post
def test_and_cond(text):
    result = re.findall('meine', text)
    return " ".join(result)

def test_and_cond1(text):
    result = re.findall('finde', text)
    return " ".join(result)

def test_and_cond2(text):
    result = re.findall('denke', text)
    return " ".join(result)

def test_and_cond3(text):
    result = re.findall('meinung', text)
    return " ".join(result)

def test_and_cond4(text):
    result = re.findall('feedback', text)
    return " ".join(result)

def test_and_cond5(text):
    result = re.findall('innovation', text)
    return " ".join(result)

def test_and_cond6(text):
    result = re.findall('idee', text)
    return " ".join(result)

def test_and_cond7(text):
    result = re.findall('tipp', text)
    return " ".join(result)

def test_and_cond8(text):
    result = re.findall('verbessern', text)
    return " ".join(result)


def test_and_cond9(text):
    result = re.findall('verändern', text)
    return " ".join(result)

def test_and_cond10(text):
    result = re.findall('innovativ', text)
    return " ".join(result)

df_unique['meine'] = df_unique['Satz'].apply(lambda x: test_and_cond(x))
df_unique['finde'] = df_unique['Satz'].apply(lambda x: test_and_cond1(x))
df_unique['denke'] = df_unique['Satz'].apply(lambda x: test_and_cond2(x))
df_unique['meinung'] = df_unique['Satz'].apply(lambda x: test_and_cond3(x))
df_unique['feedback'] = df_unique['Satz'].apply(lambda x: test_and_cond4(x))
df_unique['innovation'] = df_unique['Satz'].apply(lambda x: test_and_cond5(x))
df_unique['idee'] = df_unique['Satz'].apply(lambda x: test_and_cond6(x))
df_unique['tipp'] = df_unique['Satz'].apply(lambda x: test_and_cond7(x))
df_unique['verbessern'] = df_unique['Satz'].apply(lambda x: test_and_cond8(x))
df_unique['verändern'] = df_unique['Satz'].apply(lambda x: test_and_cond9(x))
df_unique['innovativ'] = df_unique['Satz'].apply(lambda x: test_and_cond10(x))

df_unique.to_excel("results11_neu.xlsx")