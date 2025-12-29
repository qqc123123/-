import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import time
import json
import warnings
warnings.filterwarnings('ignore')

# 1. 创建文件夹
os.makedirs('data', exist_ok=True)
os.makedirs('result(1)', exist_ok=True)

# 2. 下载数据集（UCI Heart Disease）
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
]
data_path = 'data/heart.csv'

if not os.path.exists(data_path):
    df = pd.read_csv(url, header=None, names=columns)
    df.to_csv(data_path, index=False)
    print("数据集下载完成并保存至:", data_path)
else:
    df = pd.read_csv(data_path)
    print("数据集已存在，直接加载。")

print("数据集基本信息：")
print("样本数:", df.shape[0])
print("特征数:", df.shape[1] - 1)
print("标签分布:\n", df['target'].value_counts())

# 3. 数据预处理
print("\n=== 数据预处理 ===")
# 将标签二值化（原数据中>0表示患病）
df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)

# 处理缺失值（该数据集中用'?'表示缺失）
df.replace('?', np.nan, inplace=True)
df = df.dropna()

# 特征与标签分离
X = df.drop('target', axis=1)
y = df['target']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 模型训练（逻辑回归）
print("\n=== 模型训练（逻辑回归）===")
start_time = time.time()

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

end_time = time.time()
training_time = end_time - start_time
print(f"训练时间: {training_time:.4f} 秒") 

# 5. 预测与评估
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n=== 模型评估 ===")
print("准确率 (Accuracy):", accuracy_score(y_test, y_pred))
print("精确率 (Precision):", precision_score(y_test, y_pred))
print("召回率 (Recall):", recall_score(y_test, y_pred))
print("F1分数 (F1-Score):", f1_score(y_test, y_pred))
print("\n分类报告:\n", classification_report(y_test, y_pred))

# 6. 可视化

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 6.1 混淆矩阵
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['健康', '患病'], yticklabels=['健康', '患病'])
plt.title('混淆矩阵 - sklearn')
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.savefig('result(1)/confusion_matrix.png')
plt.close()

# 6.2 ROC曲线
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('假正率')
plt.ylabel('真正率')
plt.title('ROC曲线 - sklearn')
plt.legend(loc='lower right')
plt.savefig('result(1)/roc_curve.png')
plt.close()

# 6.3 特征重要性（逻辑回归系数）
features = X.columns
coef = model.coef_[0]
importance = pd.DataFrame({'特征': features, '系数': coef})
importance = importance.sort_values(by='系数', key=abs, ascending=False)

plt.figure(figsize=(8,6))
plt.barh(importance['特征'], importance['系数'])
plt.xlabel('系数绝对值')
plt.title('特征重要性（逻辑回归系数）')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('result(1)/feature_importance.png')
plt.close()

# 6.4 学习曲线
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(
    model, X_train_scaled, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10)
)
train_mean = np.mean(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)

plt.figure(figsize=(6,5))
plt.plot(train_sizes, train_mean, label='训练准确率')
plt.plot(train_sizes, val_mean, label='验证准确率')
plt.xlabel('训练样本数')
plt.ylabel('准确率')
plt.title('学习曲线 - sklearn')
plt.legend()
plt.grid()
plt.savefig('result(1)/learning_curve.png')
plt.close()

print("\n所有可视化图表已保存至 'result(1)' 文件夹。")
print("=== 分析完成 ===")

# 在第一份代码的最后添加以下内容（在print语句之后）：

# 保存sklearn模型结果到文件


sklearn_results = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1': f1_score(y_test, y_pred),
    'roc_auc': roc_auc,
    'training_time': training_time,
    'y_test': y_test.tolist() if hasattr(y_test, 'tolist') else y_test.values.tolist(),
    'y_pred': y_pred.tolist(),
    'y_pred_proba': y_pred_proba.tolist(),
    'weights': model.coef_[0].tolist(),
    'bias': model.intercept_[0].tolist() if hasattr(model.intercept_[0], 'tolist') else [float(model.intercept_[0])],
    'feature_names': X.columns.tolist()
}

# 保存为JSON文件
with open('result(1)/sklearn_results.json', 'w', encoding='utf-8') as f:
    json.dump(sklearn_results, f, ensure_ascii=False, indent=2)

print("sklearn模型结果已保存至 'result(1)/sklearn_results.json'")