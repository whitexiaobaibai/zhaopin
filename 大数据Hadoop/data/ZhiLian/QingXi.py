# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_html_info(html):
    '''''
    *****************获取网页的有用信息并保存成字典形式****************
    '''
    try:
        soup = BeautifulSoup(html, "lxml")  # 设置解析器为“lxml”
        occ_name = soup.select('div.fixed-inner-box h1')[0]
        com_name = soup.select('div.fixed-inner-box h2 ')[0]
        welfare = soup.select('div.welfare-tab-box')[0]
        wages = soup.select('div.terminalpage-left strong')[0]
        date = soup.select('div.terminalpage-left strong')[2]
        exper = soup.select('div.terminalpage-left strong')[4]
        num = soup.select('div.terminalpage-left strong')[6]
        area = soup.select('div.terminalpage-left strong')[1]
        nature = soup.select('div.terminalpage-left strong')[3]
        Edu = soup.select('div.terminalpage-left strong')[5]
        cate = soup.select('div.terminalpage-left strong')[7]
        com_scale = soup.select('ul.terminal-ul.clearfix li strong')[8]
        com_nature = soup.select('ul.terminal-ul.clearfix li strong')[9]
        com_cate = soup.select('ul.terminal-ul.clearfix li strong')[10]
        com_url = soup.select('div.fixed-inner-box h2 a')[0]
        com_address = soup.select('ul.terminal-ul.clearfix li strong')[-1]
        job_descritions1 = soup.select('div.tab-inner-cont')[0]
        job_descritions=job_descritions1.select('p')[:-1]
        data = {
            "工作名称": occ_name.text.strip(),
            "公司名称": com_name.text,
            "公司网址": com_url.get('href'),
            "福利": welfare.text.strip(),
            "月工资": wages.text.strip(),
            "发布日期": date.text.strip(),
            "经验": exper.text.strip(),
            "人数": num.text.strip(),
            "工作地点": area.text.strip(),
            "工作性质": nature.text.strip(),
            "最低学历": Edu.text.strip(),
            "职位类别": cate.text.strip(),
            "公司规模": com_scale.text.strip(),
            "公司性质": com_nature.text.strip(),
            "公司行业": com_cate.text.strip(),
            "公司地址": com_address.text.strip(),
            "岗位描述": [job_descrition.text.strip() for job_descrition in job_descritions],

        }
        # print(data)
        return (data)
    except Exception:
        pass

# 将全部信息保存成DataFrame形式，去除无用信息
def get_htmls_all_info(path):
    df = pd.DataFrame({

        "工作名称": [],
        "公司名称": [],
        "公司网址": [],
        "福利": [],
        "月工资": [],
        "发布日期": [],
        "经验": [],
        "人数": [],
        "工作地点": [],
        "工作性质": [],
        "最低学历": [],
        "职位类别": [],
        "公司规模": [],
        "公司性质": [],
        "公司行业": [],
        "公司地址": [],
        "岗位描述": [],

    })
    dirs = os.listdir(path)
    for dir in dirs:
        #print(dir)
        if dir.find('swp'):
            dir=dir.strip('.'and '.swp')
        p = os.path.join(path, dir)
        html = open(p).read()
        data = get_html_info(html)
        print(data)
        df = df.append(data, ignore_index=True)
    return df

if __name__ == '__main__':
    path='/data/python_pj2/jobs.zhaopin.com'
    df=get_htmls_all_info(path)
    df.to_csv('/data/python_pj2/bigdata', index=False)
    print(df)