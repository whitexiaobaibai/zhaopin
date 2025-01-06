import pandas as pd
import re
import numpy as np
import jieba
import jieba.analyse
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()


#加载数据
data=pd.read_csv('/data/python_pj4/bigdata',header=None,names=[ '人数', '公司名称', '公司地址', '公司性质', '公司网址', '公司行业', '公司规模',
       '发布日期', '岗位描述', '工作名称', '工作地点', '工作性质', '最低学历', '月工资', '福利', '经验', '网址',
       '职位类别'])
data=data[1:]

# 使用pandas中的方法,取出岗位描述列中符合的内容
job_des=data.岗位描述.str.strip("[]").str.replace(',','').str.replace("'","").str.replace(r'\\xa0','').str.replace(' '*3 or ' '*4,'|').str.split('|',expand=True)[0]
# print(job_des)

#jieba分词，并统计词频
zidian={}
r1=re.compile(r'\w') #使用正则表达式,筛选[A-Za-z0-9_]
r2=re.compile(r'[^\d]') #使用正则表达式,筛选[0-9_]
r4=re.compile(r'[^_]')
r3=re.compile(r'[\u4e00-\u9fa5]') #使用正则表达式,筛选纯中文
stopkeyword=[line.strip() for line in open('/home/hadoop/stopword').readlines()] #加载停用词
bogs=[] #用于存储长的英文语句
for i in job_des:
    seg_list = jieba.cut(i)
    # print('Dafault Mode:', ' '.join(seg_list))
    for word in seg_list:
        if word not in stopkeyword and r1.match(word) and r2.match(word)and r3.match(word)==None and r4.match(word): #筛选语句中的英文
            word=word.lower() #小写化所有词
            if len(word)>=10:
                bogs.append(word)
            elif len(word)!=1 or word in ['c','r']:
                #统计词频
                if word in zidian:
                    zidian[word]+=1
                else:
                    zidian[word]=1

#将字典的值逆序
zidian=sorted(zidian.items(),key=lambda item:item[1],reverse=True)
zidian=pd.DataFrame(zidian,columns=['skill_name','num'])
zidian.loc[(zidian.skill_name=='r'),'skill_name']="R"
zidian.loc[(zidian.skill_name=='c'),'skill_name']="C"
df=zidian[zidian.num>70]

#用于分割长语句中的关键词
def cut(sentences,words):
    itr=[]
    for st in sentences:
        for word in words:
            if st.find(word)!=-1:
                itr.append(word)
                cut(st.split(word),words)
    return itr


#将分割词的词频累计到‘zidian’中
word_bogs=cut(bogs,df.skill_name)
for word_bog in word_bogs:
    if word_bog in list(zidian.skill_name):
        zidian.loc[zidian.skill_name==word_bog,'num']+=1
# zidian.to_csv('/data/zhilian/job_des')
print(zidian)

#将zidian中数据导入到mysql数据库中
conn=create_engine('mysql+mysqldb://root:strongs@localhost:3306/zhilian?charset=utf8')
pd.io.sql.to_sql(zidian,name='job_des',con=conn,schema='zhilian',if_exists='append',index=False)