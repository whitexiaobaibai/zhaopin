import pandas as pd
import seaborn as sns
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
fontPath ="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font = fm.FontProperties(fname=fontPath, size=10)
data=pd.read_csv('/data/python_pj3/bigdata')
print(data.shape)
print(data.columns)
# print([data.职位类别.value_counts().index if data.职位类别.value_counts()<10==False:])
data.loc[((data.职位类别=='客户代表')|(data.职位类别=='电话销售')|(data.职位类别=='大客户销售代表')),'职位类别']='销售代表'
月工资=data['月工资'].str.strip('元/月').str.split('-',expand=True)
月工资.columns=['月工资_min','月工资_max']
data['月工资_min']=月工资['月工资_min']
data['月工资_max']=月工资['月工资_max']

data.loc[(data.月工资_min=='面议'),'月工资_min']=0
data.loc[(data.月工资_min=='1000元/月以下' ),'月工资_min']=1
data.loc[(data.月工资_min=='100000元/月以上'),'月工资_min']=7
data.loc[(data.月工资_max.isnull()),'月工资_max']=0
print('****************************************************')
data.月工资_min=data.月工资_min.astype(int)
data.月工资_max=data.月工资_max.astype(int)
月工资_mean=(data.月工资_min+data.月工资_max)/2
data.loc[((data.月工资_min==0) & (data.月工资_max==0) & (data.月工资.notnull()) ),'月工资']=0
data.loc[((data.月工资_min==1) & (data.月工资_max==0) & (data.月工资.notnull()) ),'月工资']=1
data.loc[((data.月工资_min<6000) & (data.月工资_min>8)),'月工资'] = 1
data.loc[((((data.月工资_min>=6000) & (data.月工资_max<=8000)) | ((6000<月工资_mean)&(月工资_mean<8000))) & (data.月工资.notnull())),'月工资'] = 2
data.loc[((((data.月工资_min>=8000) & (data.月工资_max<=10000)) | ((8000<=月工资_mean)&(月工资_mean<10000))) & (data.月工资.notnull()) ),'月工资']=3
data.loc[((((data.月工资_min>=10000) & (data.月工资_max<=20000)) | ((10000<=月工资_mean)&(月工资_mean<20000))) & (data.月工资.notnull())),'月工资']=4
# data.loc[((data.月工资_min>=15000) & (data.月工资_max<=20000) & (data.月工资.notnull()) ),'月工资']=5
data.loc[((((data.月工资_min>=20000) & (data.月工资_max<=30000)) | ((20000<=月工资_mean)&(月工资_mean<30000))) & (data.月工资.notnull()) ),'月工资']=5
data.loc[((((data.月工资_min>=30000) & (data.月工资_max<=50000)) | ((30000<=月工资_mean)&(月工资_mean<50000))) & (data.月工资.notnull())),'月工资']=6
data.loc[(((data.月工资_min>=50000) | (50000<=月工资_mean)) & (data.月工资.notnull()) ),'月工资']=7
data.loc[((data.月工资_min==7) & (data.月工资_max==0) & (data.月工资.notnull()) ),'月工资']=7
print(data.月工资.value_counts(sort=False))

#月工资分布情况
fig=plt.figure()
fracs=data.月工资.value_counts(sort=False)
labels=['面议','6000元/月以下','6000-8000元/月','8000-10000元/月','10000-20000元/月','20000-30000元/月','30000-50000元/月','500000元/月以上 ']
colors = ['palevioletred','turquoise','cadetblue','pink','slategrey','orange','green','red']
explode=[0,0,0,0,0.05,0,0,0]
patchs,l_text,p_text=plt.pie(x=fracs,explode=explode, labels=labels,colors=colors, autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle=0, pctdistance=0.6)
plt.title('月工资分布情况',fontproperties=font)
for t in (l_text+p_text):
    t.set_fontproperties(font)
#各经验等级的月工资情况
data.loc[(data.经验=='3年以上'),'经验']='3-5年'
print("****************************************************")
df=pd.DataFrame([data.经验[data.月工资==i].value_counts().rename(i) for i in range(8)])
print(df)
df.plot(kind='bar',colors=['yellowgreen','lightskyblue','pink','coral','orange','green','palegreen'])
plt.legend(loc='best',prop=font)
plt.xticks(df.index,labels,rotation=15,fontproperties=font)
plt.title('各经验等级的工资分布情况',fontproperties=font)
plt.xlabel('工资等级',fontproperties=font)
plt.ylabel('公司数量',fontproperties=font)
#月工资与学历
print("****************************************************")
df=pd.DataFrame([data.最低学历[data.月工资==i].value_counts().rename(i) for i in range(8)])
print(df)
df.plot(kind='bar',stacked=True,colors=colors)
plt.legend(loc='best',prop=font)
plt.xticks(df.index,labels,rotation=15,fontproperties=font)
plt.title('各学历等级的工资分布情况',fontproperties=font)
plt.xlabel('工资等级',fontproperties=font)
plt.ylabel('公司数量',fontproperties=font)
#月工资与工作地点
print("****************************************************")
df=pd.DataFrame([data.工作地点.str.split('-',expand=True)[0][data.月工资==i].value_counts().rename(i) for i in range(8)]).T
print(df)
colors=['burlywood','yellowgreen','lightskyblue','pink','coral','orange','plum','oldlace']
d=df.plot(kind='bar',stacked=True,colors=colors)
plt.legend(loc='best',prop=font,labels=labels)
print(d.get_legend_handles_labels())
plt.xticks([i for i in range(len(df.index))],df.index,rotation=15,fontproperties=font)
plt.title('工作地点的工资分布情况',fontproperties=font)
plt.xlabel('工资等级',fontproperties=font)
plt.ylabel('公司数量',fontproperties=font)
print(df.values)
plt.show()
