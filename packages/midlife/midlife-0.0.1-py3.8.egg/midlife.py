import pandas as pd
import matplotlib.pyplot as plt
import subprocess as sp
sp.call('wget -nc https://data.cdc.gov/api/views/chcz-j2du/rows.csv', shell=True)
d=pd.read_csv('rows.csv')
years=d.Year.unique()
a1=[]
a2=[]
a3=[]
a4=[]
a5=[]
for i in years:
 a=d.loc[(d.Year==i) &
  (d['Sex']=='All Sexes') & (d['Age Group']=='40-44 years'),'Total Deaths']
 a1.append(a)
 a=d.loc[(d.Year==i) &
  (d['Sex']=='All Sexes') & (d['Age Group']=='45-49 years'),'Total Deaths']
 a2.append(a)
 a=d.loc[(d.Year==i) &
  (d['Sex']=='All Sexes') & (d['Age Group']=='50-54 years'),'Total Deaths']
 a3.append(a)
 a=d.loc[(d.Year==i) &
  (d['Sex']=='All Sexes') & (d['Age Group']=='55-59 years'),'Total Deaths']
 a4.append(a)
 a=d.loc[(d.Year==i) &
  (d['Sex']=='All Sexes') & (d['Age Group']=='60-64 years'),'Total Deaths']
 a5.append(a)
def main():
 plt.ylim([0,300000])
 plt.plot(years,a1,':k')
 plt.plot(years,a2,'-k')
 plt.plot(years,a3,'--k')
 plt.plot(years,a4,'-.k')
 plt.plot(years,a5,':k',linewidth=2)
 plt.legend(('40-44 years','45-49 years','50-54 years','55-59 years','60-64 years'))
 plt.title('Impact of COVID-19 on montality of midlife')
 plt.savefig('midlife.png')
main()
plt.show()
