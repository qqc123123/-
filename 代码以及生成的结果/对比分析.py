import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# 1. 创建文件夹
os.makedirs('contrast', exist_ok=True)

print("=== sklearn版本与自编算法对比分析 ===\n")

# 2. 检查结果文件是否存在
sklearn_result_path = 'result(1)/sklearn_results.json'
manual_result_path = 'result(2)/manual_results.json'

if not os.path.exists(sklearn_result_path):
    print(f"错误: 找不到sklearn结果文件: {sklearn_result_path}")
    print("请先运行第一份代码生成结果。")
    exit()

if not os.path.exists(manual_result_path):
    print(f"错误: 找不到自编算法结果文件: {manual_result_path}")
    print("请先运行第二份代码生成结果。")
    exit()

# 3. 加载结果
print("加载sklearn版本结果...")
with open(sklearn_result_path, 'r', encoding='utf-8') as f:
    sklearn_results = json.load(f)

print("加载自编算法结果...")
with open(manual_result_path, 'r', encoding='utf-8') as f:
    manual_results = json.load(f)

print(f"sklearn训练时间: {sklearn_results.get('training_time', '未记录'):.6f}秒")
print(f"自编算法训练时间: {manual_results.get('training_time', '未记录'):.4f}秒")

# 4. 计算ROC AUC（确保计算方式一致）
def calculate_roc_auc(y_true, y_pred_proba):
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    return auc(fpr, tpr)

# 更新AUC值
sklearn_results['roc_auc'] = calculate_roc_auc(sklearn_results['y_test'], sklearn_results['y_pred_proba'])
manual_results['roc_auc'] = calculate_roc_auc(manual_results['y_test'], manual_results['y_pred_proba'])

# 5. 性能指标对比表格
print("\n" + "="*60)
print("性能指标对比")
print("="*60)

comparison_data = []
metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
metric_names = ['准确率', '精确率', '召回率', 'F1分数', 'ROC AUC']

for metric, name in zip(metrics, metric_names):
    sklearn_val = sklearn_results[metric]
    manual_val = manual_results[metric]
    diff = manual_val - sklearn_val
    diff_percent = (diff / sklearn_val * 100) if sklearn_val != 0 else 0
    
    comparison_data.append({
        '指标': name,
        'sklearn版本': f"{sklearn_val:.4f}",
        '自编算法': f"{manual_val:.4f}",
        '绝对差异': f"{diff:+.4f}",
        '相对差异(%)': f"{diff_percent:+.2f}%"
    })

comparison_df = pd.DataFrame(comparison_data)

print("\n模型性能对比:")
print(comparison_df.to_string(index=False))
print()

# 6. 权重对比
print("\n" + "="*60)
print("模型权重对比")
print("="*60)

sklearn_weights = np.array(sklearn_results['weights'])
manual_weights = np.array(manual_results['weights'])
feature_names = sklearn_results['feature_names']

# 计算权重统计信息
weight_stats = {
    '平均绝对权重 (sklearn)': np.mean(np.abs(sklearn_weights)),
    '平均绝对权重 (自编)': np.mean(np.abs(manual_weights)),
    '权重标准差 (sklearn)': np.std(sklearn_weights),
    '权重标准差 (自编)': np.std(manual_weights),
    '权重相关系数': np.corrcoef(sklearn_weights, manual_weights)[0, 1],
    '最大绝对差异': np.max(np.abs(sklearn_weights - manual_weights)),
    '平均绝对差异': np.mean(np.abs(sklearn_weights - manual_weights))
}

print("权重统计信息:")
for key, value in weight_stats.items():
    if '相关系数' in key:
        print(f"  {key}: {value:.4f}")
    else:
        print(f"  {key}: {value:.6f}")

# 7. 预测结果对比
print("\n" + "="*60)
print("预测结果对比")
print("="*60)

# 计算预测一致性
y_test_sk = np.array(sklearn_results['y_test'])
y_pred_sk = np.array(sklearn_results['y_pred'])
y_pred_manual = np.array(manual_results['y_pred'])

agreement = np.mean(y_pred_sk == y_pred_manual)
disagreement_indices = np.where(y_pred_sk != y_pred_manual)[0]

print(f"预测一致率: {agreement:.4f} ({agreement*100:.1f}%)")
print(f"不一致样本数: {len(disagreement_indices)} / {len(y_test_sk)}")

# 8. 训练时间对比
print("\n" + "="*60)
print("效率对比")
print("="*60)

if 'training_time' in sklearn_results and 'training_time' in manual_results:
    sklearn_time = sklearn_results['training_time']
    manual_time = manual_results['training_time']
    
    print(f"sklearn训练时间: {sklearn_time:.6f}秒")
    print(f"自编算法训练时间: {manual_time:.4f}秒")
    print(f"时间倍数: 自编算法是sklearn的 {manual_time/sklearn_time:.1f} 倍")
else:
    print("警告: 训练时间数据不完整")

# 9. 生成可视化对比图表
print("\n" + "="*60)
print("生成对比图表...")
print("="*60)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 9.1 综合性能对比图
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('sklearn vs 自编算法 性能对比分析', fontsize=16, y=1.02)

# 9.1.1 性能指标柱状图
ax1 = axes[0, 0]
metrics_values_sk = [sklearn_results[m] for m in metrics[:4]]
metrics_values_ma = [manual_results[m] for m in metrics[:4]]
metric_names_short = ['准确率', '精确率', '召回率', 'F1']

x = np.arange(len(metric_names_short))
width = 0.35

bars1 = ax1.bar(x - width/2, metrics_values_sk, width, label='sklearn', color='skyblue', edgecolor='black')
bars2 = ax1.bar(x + width/2, metrics_values_ma, width, label='自编算法', color='lightcoral', edgecolor='black')

ax1.set_xlabel('指标')
ax1.set_ylabel('得分')
ax1.set_title('主要指标对比', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(metric_names_short)
ax1.set_ylim([0, 1.1])
ax1.legend()
ax1.grid(True, alpha=0.3)

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)

# 9.1.2 ROC曲线对比
ax2 = axes[0, 1]
# sklearn ROC
fpr_sk, tpr_sk, _ = roc_curve(sklearn_results['y_test'], sklearn_results['y_pred_proba'])
roc_auc_sk = sklearn_results['roc_auc']
# 自编算法 ROC
fpr_ma, tpr_ma, _ = roc_curve(manual_results['y_test'], manual_results['y_pred_proba'])
roc_auc_ma = manual_results['roc_auc']

ax2.plot(fpr_sk, tpr_sk, color='blue', lw=2, alpha=0.8, label=f'sklearn (AUC={roc_auc_sk:.3f})')
ax2.plot(fpr_ma, tpr_ma, color='orange', lw=2, alpha=0.8, label=f'自编算法 (AUC={roc_auc_ma:.3f})')
ax2.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', alpha=0.5)

ax2.set_xlabel('假正率')
ax2.set_ylabel('真正率')
ax2.set_title('ROC曲线对比', fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

# 9.1.3 权重对比散点图
ax3 = axes[1, 0]
sklearn_weights = np.array(sklearn_results['weights'])
manual_weights = np.array(manual_results['weights'])

scatter = ax3.scatter(sklearn_weights, manual_weights, alpha=0.7, s=80, 
                     c=np.abs(sklearn_weights - manual_weights), cmap='coolwarm', edgecolors='black')

# 添加对角线
max_val = max(np.max(np.abs(sklearn_weights)), np.max(np.abs(manual_weights))) * 1.1
ax3.plot([-max_val, max_val], [-max_val, max_val], 'r--', alpha=0.5, label='理想匹配线')

ax3.set_xlabel('sklearn权重')
ax3.set_ylabel('自编算法权重')
ax3.set_title('权重系数对比', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax3, label='绝对差异')

# 9.1.4 训练时间对比
ax4 = axes[1, 1]
if 'training_time' in sklearn_results and 'training_time' in manual_results:
    times = [sklearn_results['training_time'], manual_results['training_time']]
    labels = ['sklearn', '自编算法']
    colors = ['lightgreen', 'gold']
    
    bars = ax4.bar(labels, times, color=colors, edgecolor='black', width=0.6)
    
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{height:.4f}s', ha='center', va='bottom', fontsize=10)
    
    ax4.set_ylabel('训练时间(秒)')
    ax4.set_title('训练时间对比', fontweight='bold')
    ax4.grid(True, alpha=0.3)
else:
    ax4.text(0.5, 0.5, '训练时间数据缺失', ha='center', va='center', fontsize=12)
    ax4.set_title('训练时间对比', fontweight='bold')

plt.tight_layout()
plt.savefig('contrast/comprehensive_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# 9.2 保存详细对比数据
print("\n" + "="*60)
print("对比结果总结")
print("="*60)

# 创建总结字典
efficiency_comparison = {}
if 'training_time' in sklearn_results and 'training_time' in manual_results:
    efficiency_comparison = {
        'sklearn训练时间': float(sklearn_results['training_time']),
        '自编算法训练时间': float(manual_results['training_time']),
        '时间倍数': float(manual_results['training_time'] / sklearn_results['training_time'])
    }
else:
    efficiency_comparison = {
        'sklearn训练时间': '未记录' if 'training_time' not in sklearn_results else float(sklearn_results['training_time']),
        '自编算法训练时间': '未记录' if 'training_time' not in manual_results else float(manual_results['training_time'])
    }

summary = {
    '性能对比': comparison_df.to_dict('records'),
    '权重统计': weight_stats,
    '预测一致性': {
        '一致率': float(agreement),
        '不一致样本数': int(len(disagreement_indices)),
        '总样本数': int(len(y_test_sk))
    },
    '效率对比': efficiency_comparison
}

# 保存为JSON
with open('contrast/comparison_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

# 10. 打印最终的对比结果
print("\n最终对比结果:")
print("-" * 40)

print("\n1. 准确率对比:")
print(f"   sklearn: {sklearn_results['accuracy']:.4f}")
print(f"   自编算法: {manual_results['accuracy']:.4f}")
print(f"   差异: {manual_results['accuracy'] - sklearn_results['accuracy']:+.4f}")

print("\n2. ROC AUC对比:")
print(f"   sklearn: {sklearn_results['roc_auc']:.4f}")
print(f"   自编算法: {manual_results['roc_auc']:.4f}")
print(f"   差异: {manual_results['roc_auc'] - sklearn_results['roc_auc']:+.4f}")

print("\n3. 权重一致性:")
print(f"   相关系数: {weight_stats['权重相关系数']:.4f}")
print(f"   平均绝对差异: {weight_stats['平均绝对差异']:.6f}")

print("\n4. 预测一致性:")
print(f"   预测一致率: {agreement:.4f} ({agreement*100:.1f}%)")
print(f"   不一致样本: {len(disagreement_indices)} / {len(y_test_sk)}")

if 'training_time' in sklearn_results and 'training_time' in manual_results:
    print("\n5. 效率对比:")
    print(f"   sklearn训练时间: {sklearn_results['training_time']:.6f}秒")
    print(f"   自编算法训练时间: {manual_results['training_time']:.4f}秒")
    print(f"   时间倍数: {manual_results['training_time']/sklearn_results['training_time']:.1f}倍")

print("\n" + "="*60)
print("对比分析完成!")
print("="*60)
print("\n生成的对比文件:")
print(f"  1. contrast/comprehensive_comparison.png - 综合对比图")
print(f"  2. contrast/comparison_summary.json - 对比总结数据")