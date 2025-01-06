import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
fontPath ="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font = fm.FontProperties(fname=fontPath, size=10)

data=pd.read_csv('/data/python_pj3/bigdata')
data = data.dropna()
data = data.reset_index()
new_data = data[['公司规模','公司性质','经验','公司行业','职位类别','工作地点','最低学历','月工资']]

# 自定义一个函数来处理字符串
new_data = new_data[new_data['月工资'] != '面议']
new_data = new_data.reset_index()
def split_salary_range(salary):
    if salary.endswith('元/月以下'):
        # 移除'元/月以下'并转换为整数，然后返回一个列表，包含0和该数字
        return [0, int(salary[:-6])]
    else:
        # 分割范围并转换为整数列表
        parts = salary.replace('元/月', '').split('-')
        if len(parts) == 2:
            start, end = map(int, parts)
            return [start, end]
        else:
            # 如果数据格式不正确
            return None
# 应用自定义函数到DataFrame的列
new_data['月工资'] = new_data['月工资'].apply(split_salary_range)
new_data = new_data[new_data['月工资'].notna()].reset_index()

new_data = new_data.astype(str)
# 初始化LabelEncoder
label_encoder = LabelEncoder()
# 将'最低学历'列的字符串转换为整数
tmp_data = pd.DataFrame()
tmp_data['公司规模'] = label_encoder.fit_transform(new_data['公司规模'])
tmp_data['公司性质'] = label_encoder.fit_transform(new_data['公司性质'])
tmp_data['经验'] = label_encoder.fit_transform(new_data['经验'])
tmp_data['公司行业'] = label_encoder.fit_transform(new_data['公司行业'])
tmp_data['职位类别'] = label_encoder.fit_transform(new_data['职位类别'])
tmp_data['工作地点'] = label_encoder.fit_transform(new_data['工作地点'])
tmp_data['最低学历'] = label_encoder.fit_transform(new_data['最低学历'])

# 使用OneHotEncoder
onehot = OneHotEncoder(sparse=False)
company_size_onehot = onehot.fit_transform(tmp_data[['公司规模']])
company_property_onehot = onehot.fit_transform(tmp_data[['公司性质']])
experience_onehot = onehot.fit_transform(tmp_data[['经验']])
company_industry_onehot = onehot.fit_transform(tmp_data[['公司行业']])
job_category_onehot = onehot.fit_transform(tmp_data[['职位类别']])
work_place_onehot = onehot.fit_transform(tmp_data[['工作地点']])
education_onehot = onehot.fit_transform(tmp_data[['最低学历']])


salay=np.array([eval(i)for i in new_data['月工资']])
X = np.hstack((company_size_onehot, company_property_onehot, experience_onehot, company_industry_onehot,
               job_category_onehot,work_place_onehot,education_onehot))  # skills_padded,
y = salay
# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

RFM = RandomForestRegressor(n_estimators=100, random_state=1)
RFM.fit(X_train, y_train)

# 进行预测
y_pred = RFM.predict(X_test)

result_data = {
    '真实值': y_test,
    '预测值': y_pred
}
print(result_data)

from sklearn.metrics import mean_squared_error

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")

import matplotlib.pyplot as plt

# 绘制散点图
plt.scatter(y_test, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)  # 绘制完美拟合线
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.show()