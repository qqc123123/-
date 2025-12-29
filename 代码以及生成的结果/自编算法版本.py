import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import warnings
import time
import json
warnings.filterwarnings('ignore')

# 1. 创建文件夹
os.makedirs('result(2)', exist_ok=True)

# 2. 加载本地数据集（从第一份代码保存的位置）
data_path = 'data/heart.csv'
if not os.path.exists(data_path):
    print("数据集不存在，请先运行第一份代码下载数据集。")
    exit()

df = pd.read_csv(data_path)
print("数据集基本信息：")
print("样本数:", df.shape[0])
print("特征数:", df.shape[1] - 1)
print("标签分布:\n", df['target'].value_counts())

# 3. 数据预处理（与第一份代码完全一致）
print("\n=== 数据预处理 ===")
# 将标签二值化（原数据中>0表示患病）
df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)

# 处理缺失值
df.replace('?', np.nan, inplace=True)
df = df.dropna()

# 特征与标签分离
X = df.drop('target', axis=1)
y = df['target']

# 划分训练集和测试集（使用sklearn）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 标准化（使用sklearn）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 转换为numpy数组
X_train_np = X_train_scaled
X_test_np = X_test_scaled
y_train_np = y_train.values
y_test_np = y_test.values

# 4. 自主实现逻辑回归算法的核心部分（适中水平）
class ManualLogisticRegression:
    """手动实现的逻辑回归算法（适中水平，包含基本优化）"""
    
    def __init__(self, learning_rate=0.1, n_iterations=1500, regularization=0.02):
        # 使用适中的超参数
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization  # L2正则化
        self.weights = None
        self.bias = None
        self.loss_history = []
        
    def _sigmoid(self, z):
        """Sigmoid函数，包含基本数值稳定处理"""
        # 限制z的范围防止溢出
        z = np.clip(z, -10, 10)  # 使用适中的范围
        return 1 / (1 + np.exp(-z))
    
    def _compute_loss(self, y, y_pred):
        """计算交叉熵损失，包含L2正则化"""
        epsilon = 1e-8  # 防止log(0)
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        
        # 交叉熵损失
        loss = -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))
        
        # 添加L2正则化（简化实现）
        if self.regularization > 0:
            reg_term = (self.regularization / 2) * np.sum(self.weights ** 2)
            loss += reg_term
            
        return loss
    
    def fit(self, X, y):
        """使用梯度下降训练模型（包含简单学习率衰减）"""
        n_samples, n_features = X.shape
        
        # 初始化参数（使用较小的随机值）
        np.random.seed(42)
        self.weights = np.random.normal(0, 0.1, n_features)
        self.bias = 0.0
        
        # 梯度下降
        for i in range(self.n_iterations):
            # 前向传播
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(linear_model)
            
            # 计算梯度
            error = y_pred - y
            
            # 权重梯度（包含正则化项）
            dw = (np.dot(X.T, error) / n_samples) + (self.regularization / n_samples) * self.weights
            # 偏置梯度（通常不添加正则化）
            db = np.sum(error) / n_samples
            
            # 简单的学习率衰减（最后100次迭代减小学习率）
            current_lr = self.learning_rate
            if i > self.n_iterations - 100:
                current_lr = self.learning_rate * 0.5
            
            # 更新参数
            self.weights -= current_lr * dw
            self.bias -= current_lr * db
            
            # 记录损失（每100次迭代）
            if i % 100 == 0:
                loss = self._compute_loss(y, y_pred)
                self.loss_history.append((i, loss))
                
                # 每500次打印一次进度
                if i % 500 == 0:
                    train_pred = (y_pred > 0.5).astype(int)
                    train_acc = np.mean(train_pred == y)
                    print(f"迭代 {i:4d} - 损失: {loss:.4f}, 训练准确率: {train_acc:.4f}")
        
        # 记录最终损失
        final_pred = self._sigmoid(np.dot(X, self.weights) + self.bias)
        final_loss = self._compute_loss(y, final_pred)
        self.loss_history.append((self.n_iterations, final_loss))
        
        print(f"训练完成 - 最终损失: {final_loss:.4f}")
        return self
    
    def predict_proba(self, X):
        """预测概率"""
        linear_model = np.dot(X, self.weights) + self.bias
        return self._sigmoid(linear_model)
    
    def predict(self, X, threshold=0.5):
        """预测类别"""
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)

# 5. 模型训练
print("\n=== 模型训练（自编逻辑回归算法）===")
start_time = time.time()

manual_model = ManualLogisticRegression(
    learning_rate=0.15,      # 稍大的学习率
    n_iterations=1200,       # 适中的迭代次数
    regularization=0.02      # 轻微的正则化
)

manual_model.fit(X_train_np, y_train_np)

end_time = time.time()
training_time = end_time - start_time
print(f"训练时间: {training_time:.4f} 秒")

# 6. 预测与评估
y_pred_manual = manual_model.predict(X_test_np)
y_pred_proba_manual = manual_model.predict_proba(X_test_np)

print("\n=== 模型评估 ===")
accuracy_manual = accuracy_score(y_test, y_pred_manual)
precision_manual = precision_score(y_test, y_pred_manual)
recall_manual = recall_score(y_test, y_pred_manual)
f1_manual = f1_score(y_test, y_pred_manual)

print(f"准确率 (Accuracy): {accuracy_manual:.4f}")
print(f"精确率 (Precision): {precision_manual:.4f}")
print(f"召回率 (Recall): {recall_manual:.4f}")
print(f"F1分数 (F1-Score): {f1_manual:.4f}")
print("\n分类报告:\n", classification_report(y_test, y_pred_manual))

# 7. 可视化（与第一份代码保持一致）

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 7.1 混淆矩阵
cm = confusion_matrix(y_test, y_pred_manual)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', xticklabels=['健康', '患病'], yticklabels=['健康', '患病'])
plt.title('混淆矩阵 - 自编算法')
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.savefig('result(2)/confusion_matrix.png')
plt.close()

# 7.2 ROC曲线
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba_manual)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, color='darkgreen', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('假正率')
plt.ylabel('真正率')
plt.title('ROC曲线 - 自编算法')
plt.legend(loc='lower right')
plt.savefig('result(2)/roc_curve.png')
plt.close()

# 7.3 特征重要性（权重系数）
features = X.columns
coef = manual_model.weights
importance = pd.DataFrame({'特征': features, '系数': coef})
importance = importance.sort_values(by='系数', key=abs, ascending=False)

plt.figure(figsize=(8,6))
bars = plt.barh(importance['特征'], importance['系数'], color='orange', alpha=0.7)
plt.xlabel('系数值')
plt.title('特征重要性（自编算法权重系数）')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('result(2)/feature_importance.png')
plt.close()

# 7.4 损失曲线
if manual_model.loss_history:
    iterations = [item[0] for item in manual_model.loss_history]
    losses = [item[1] for item in manual_model.loss_history]
    
    plt.figure(figsize=(8,5))
    plt.plot(iterations, losses, marker='o', markersize=4, linestyle='-', linewidth=2, color='purple')
    plt.xlabel('迭代次数')
    plt.ylabel('损失值')
    plt.title('训练损失曲线 - 自编算法')
    plt.grid(True, alpha=0.3)
    plt.savefig('result(2)/loss_curve.png')
    plt.close()

# 7.5 预测概率分布
plt.figure(figsize=(10, 6))
healthy_probs = y_pred_proba_manual[y_test_np == 0]
disease_probs = y_pred_proba_manual[y_test_np == 1]

plt.hist(healthy_probs, bins=15, alpha=0.6, label='实际健康', color='blue', edgecolor='black')
plt.hist(disease_probs, bins=15, alpha=0.6, label='实际患病', color='red', edgecolor='black')
plt.xlabel('预测概率')
plt.ylabel('样本数')
plt.title('预测概率分布 - 自编算法')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('result(2)/probability_distribution.png')
plt.close()

print("\n所有可视化图表已保存至 'result(2)' 文件夹。")

# 8. 保存结果用于对比
manual_results = {
    'accuracy': float(accuracy_manual),
    'precision': float(precision_manual),
    'recall': float(recall_manual),
    'f1': float(f1_manual),
    'roc_auc': float(roc_auc),
    'y_test': y_test_np.tolist(),
    'y_pred': y_pred_manual.tolist(),
    'y_pred_proba': y_pred_proba_manual.tolist(),
    'weights': manual_model.weights.tolist(),
    'bias': float(manual_model.bias),
    'feature_names': X.columns.tolist(),
    'training_time': float(training_time),
    'loss_history': manual_model.loss_history
}

# 保存为JSON文件
with open('result(2)/manual_results.json', 'w', encoding='utf-8') as f:
    json.dump(manual_results, f, ensure_ascii=False, indent=2)

print("自编模型结果已保存至 'result(2)/manual_results.json'")
print("=== 自编算法分析完成 ===")