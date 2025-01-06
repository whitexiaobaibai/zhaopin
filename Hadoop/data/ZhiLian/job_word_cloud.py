import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
fontPath ="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font = fm.FontProperties(fname=fontPath,size=10)
data=pd.read_csv('/data/python_pj3/bigdata')
from wordcloud import WordCloud
lables = pd.DataFrame(data['职位类别'])
text = ' '.join(lables['职位类别'])
wc = WordCloud(width=2000,height=1000,background_color='white',font_path=fontPath).generate(text)
plt.figure(figsize=(20,10))
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.show()