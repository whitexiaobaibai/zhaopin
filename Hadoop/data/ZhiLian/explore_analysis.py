import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

fontPath ="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font = fm.FontProperties(fname=fontPath, size=10)


data=pd.read_csv('/data/python_pj3/bigdata',)
print(data.shape,data.columns)
data.loc[(data.经验=='3年以上'),'经验'] = '3-5年'

#公司规模分布情况
plt.figure(figsize=(20,15))
plt.subplot2grid((2,3),(0,0))
a=data['公司规模'].value_counts().plot(kind='barh',title='公司规模分布情况',color='pink')
a.xaxis.get_label().set_fontproperties(font)
a.yaxis.get_label().set_fontproperties(font)
a.legend(loc='best',prop=font)
for label in ([a.title]+a.get_xticklabels()+a.get_yticklabels()):
    label.set_fontproperties(font)


#公司性质分布情况
plt.subplot2grid((2,3),(0,1))
b=data['公司性质'].value_counts().plot(kind='barh',title='公司性质分布情况',color='orange')
b.xaxis.get_label().set_fontproperties(font)
b.yaxis.get_label().set_fontproperties(font)
b.legend(loc='best',prop=font)
for label in ([b.title]+b.get_xticklabels()+b.get_yticklabels()):
    label.set_fontproperties(font)


#经验分布情况
# plt.subplot2grid((2,2),(1,0),colspan=2)
plt.subplot2grid((2,3),(0,2))
c=data['经验'].value_counts().plot(kind='barh',title='经验分布情况',color='tomato')
c.xaxis.get_label().set_fontproperties(font)
c.yaxis.get_label().set_fontproperties(font)
c.legend(loc='best',prop=font)
for label in ([c.title]+c.get_xticklabels()+c.get_yticklabels()):
    label.set_fontproperties(font)


#公司行业分布情况
plt.subplot2grid((2,3),(1,0))
d=data['公司行业'].value_counts().sort_values(ascending=False).head(10).plot(kind='barh',title='公司行业分布情况',color='turquoise')
d.yaxis.get_label().set_fontproperties(font)
d.legend(loc='best',prop=font)
for label in ([d.title]+d.get_xticklabels()+d.get_yticklabels()):
    label.set_fontproperties(font)


#职位类别分布情况
plt.subplot2grid((2,3),(1,1))
d=data['职位类别'].value_counts().sort_values(ascending=False).head(10).plot(kind='barh',title='职位类别分布情况',color='cadetblue')
d.xaxis.get_label().set_fontproperties(font)
d.yaxis.get_label().set_fontproperties(font)
d.legend(loc='best',prop=font)
for label in ([d.title]+d.get_xticklabels()+d.get_yticklabels()):
    label.set_fontproperties(font)


#工作地点分布情况
plt.subplot2grid((2,3),(1,2))
d=data['工作地点'].str.split('-',expand=True)[0].value_counts().plot(kind='bar',title='工作地点分布情况',color='palevioletred',label='工作地点')
d.xaxis.get_label().set_fontproperties(font)
d.yaxis.get_label().set_fontproperties(font)
d.legend(loc='best',prop=font)
# print(d.get_legend_handles_labels())
for label in ([d.title]+d.get_xticklabels()+d.get_yticklabels()):
    label.set_fontproperties(font)
plt.show()