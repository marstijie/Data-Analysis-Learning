# -*- coding: utf-8 -*-
# ============ 1. 环境准备和库导入 ============
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体和图表样式
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 特征名称映射字典
feature_name_mapping = {
    'phone_no_m': '用户唯一标识',
    'city_name': '归属地市',
    'county_name': '归属区县',
    'idcard_cnt': '身份证关联卡数',

    # ARPU特征
    'arpu_201908': '2019年8月月均消费额',
    'arpu_201909': '2019年9月月均消费额',
    'arpu_201910': '2019年10月月均消费额',
    'arpu_201911': '2019年11月月均消费额',
    'arpu_201912': '2019年12月月均消费额',
    'arpu_202001': '2020年1月月均消费额',
    'arpu_202002': '2020年2月月均消费额',
    'arpu_202003': '2020年3月月均消费额',

    'label': '用户标签',

    # 通话行为特征
    'voc_call_dur_count': '总通话次数',
    'voc_call_dur_sum': '总通话时长(秒)',
    'voc_call_dur_mean': '平均通话时长',
    'voc_opposite_no_m_nunique': '联系人数量',
    'voc_call_type_1_cnt_sum': '主叫次数',
    'voc_call_type_2_cnt_sum': '被叫次数',
    'voc_imei_m_nunique': '使用设备数量',

    # 短信行为特征
    'sms_sms_send_cnt_sum': '短信发送总量',
    'sms_sms_recv_cnt_sum': '短信接收总量',
    'sms_opposite_no_m_count': '短信交互总次数',
    'sms_opposite_no_m_nunique': '短信交互不同人数',
    'sms_request_datetime_count': '短信记录总条数',

    # APP行为特征
    'app_busi_name_count': 'APP使用总记录数',
    'app_busi_name_nunique': 'APP使用多样性',
    'app_flow_sum': '总流量消耗(MB)',
    'app_flow_mean': '平均每次使用流量',

    # 衍生特征
    'arpu_avg': '平均消费额',
    'city_name_encoded': '地市编码',
    'county_name_encoded': '区县编码'
}

# ============ 2. 数据加载和预处理 ============
data = pd.read_csv('total.csv', encoding='gb18030')

# 确保数值特征非负
numeric_cols = data.select_dtypes(include=[np.number]).columns
data[numeric_cols] = data[numeric_cols].clip(lower=0)

# 分离正常用户和异常用户数据
normal_users = data[data['label'] == 0]
fraud_users = data[data['label'] == 1]

print("数据基本信息：")
print(f"数据形状: {data.shape}")
print(f"正常用户: {len(normal_users)} ({len(normal_users) / len(data) * 100:.1f}%)")
print(f"异常用户: {len(fraud_users)} ({len(fraud_users) / len(data) * 100:.1f}%)")


# ============ 3. 基础分布分析 ============
def plot_basic_distributions():
    """绘制基础分布图"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 3.1 用户分布饼图
    plt.figure(figsize=(8, 6))
    sizes = [len(normal_users), len(fraud_users)]
    labels = ['正常用户', '异常用户']
    colors = ['#66b3ff', '#ff9999']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.05, 0.05))
    plt.title('用户分布情况', fontsize=16, pad=20)
    plt.axis('equal')
    plt.savefig('01_user_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 3.2 地域分布对比
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # 城市分布
    city_normal = normal_users['city_name'].value_counts().head(10)
    city_fraud = fraud_users['city_name'].value_counts().head(10)

    x = np.arange(len(city_normal))
    axes[0].bar(x - 0.2, city_normal.values, 0.4, alpha=0.7, color='#66b3ff', label='正常用户')
    axes[0].bar(x + 0.2, city_fraud.values, 0.4, alpha=0.7, color='#ff9999', label='异常用户')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(city_normal.index, rotation=45)
    axes[0].set_title('城市分布对比')
    axes[0].set_ylabel('用户数量')
    axes[0].legend()

    # 区县分布
    county_normal = normal_users['county_name'].value_counts().head(10)
    county_fraud = fraud_users['county_name'].value_counts().head(10)

    x = np.arange(len(county_normal))
    axes[1].bar(x - 0.2, county_normal.values, 0.4, alpha=0.7, color='#66b3ff')
    axes[1].bar(x + 0.2, county_fraud.values, 0.4, alpha=0.7, color='#ff9999')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(county_normal.index, rotation=45)
    axes[1].set_title('区县分布对比')
    axes[1].set_ylabel('用户数量')

    plt.tight_layout()
    plt.savefig('02_geographical_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 4. 通话行为特征对比 ============
def plot_voice_features_comparison():
    """绘制通话行为特征对比"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    voice_features = [
        'voc_call_dur_count', 'voc_call_dur_sum', 'voc_call_dur_mean',
        'voc_opposite_no_m_nunique', 'voc_call_type_1_cnt_sum',
        'voc_call_type_2_cnt_sum', 'voc_imei_m_nunique'
    ]

    # 获取中文特征名
    voice_features_cn = [feature_name_mapping[feat] for feat in voice_features]

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()

    for i, (feature, feature_cn) in enumerate(zip(voice_features, voice_features_cn)):
        if i < len(axes):
            # 箱线图对比
            data_to_plot = [normal_users[feature].dropna(), fraud_users[feature].dropna()]
            box_plot = axes[i].boxplot(data_to_plot, labels=['正常', '异常'], patch_artist=True)

            # 设置箱体颜色
            colors = ['#66b3ff', '#ff9999']
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)

            axes[i].set_title(f'{feature_cn}', fontsize=12)
            axes[i].set_ylabel('特征值')
            axes[i].grid(True, alpha=0.3)

    # 隐藏多余的子图
    for i in range(len(voice_features), len(axes)):
        axes[i].set_visible(False)

    plt.suptitle('通话行为特征对比分析', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('03_voice_features_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 5. 短信行为特征对比 ============
def plot_sms_features_comparison():
    """绘制短信行为特征对比"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    sms_features = [
        'sms_sms_send_cnt_sum', 'sms_sms_recv_cnt_sum', 'sms_opposite_no_m_count',
        'sms_opposite_no_m_nunique', 'sms_request_datetime_count'
    ]

    # 获取中文特征名
    sms_features_cn = [feature_name_mapping[feat] for feat in sms_features]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()

    for i, (feature, feature_cn) in enumerate(zip(sms_features, sms_features_cn)):
        if i < len(axes):
            # 核密度估计对比
            normal_vals = normal_users[feature].dropna()
            fraud_vals = fraud_users[feature].dropna()

            if len(normal_vals) > 1 and len(fraud_vals) > 1:
                # 对数据进行对数变换以便更好可视化
                normal_log = np.log1p(normal_vals)
                fraud_log = np.log1p(fraud_vals)

                axes[i].hist(normal_log, bins=30, alpha=0.7, density=True, color='#66b3ff', label='正常用户')
                axes[i].hist(fraud_log, bins=30, alpha=0.7, density=True, color='#ff9999', label='异常用户')
                axes[i].set_title(f'{feature_cn}', fontsize=12)
                axes[i].set_xlabel('特征值(对数变换)')
                axes[i].set_ylabel('密度')
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)

    plt.suptitle('短信行为特征对比分析', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('04_sms_features_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 6. APP行为特征对比 ============
def plot_app_features_comparison():
    """绘制APP行为特征对比"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    app_features = [
        'app_busi_name_count', 'app_busi_name_nunique', 'app_flow_sum', 'app_flow_mean'
    ]

    # 获取中文特征名
    app_features_cn = [feature_name_mapping[feat] for feat in app_features]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, (feature, feature_cn) in enumerate(zip(app_features, app_features_cn)):
        if i < len(axes):
            # 小提琴图对比
            data_combined = pd.concat([
                normal_users[[feature]].assign(type='正常用户'),
                fraud_users[[feature]].assign(type='异常用户')
            ])

            sns.violinplot(data=data_combined, x='type', y=feature, ax=axes[i],
                           palette=['#66b3ff', '#ff9999'])
            axes[i].set_title(feature_cn, fontsize=12)
            axes[i].set_xlabel('用户类型')
            axes[i].set_ylabel('特征值')
            axes[i].grid(True, alpha=0.3)

    plt.suptitle('APP行为特征对比分析', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('05_app_features_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 7. 消费行为特征对比 ============
def plot_consumption_behavior_analysis():
    """绘制消费行为分析"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    arpu_features = [
        'arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201911',
        'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003'
    ]

    # 创建时间序列对比图
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # 计算每月的平均消费
    months = ['2019-08', '2019-09', '2019-10', '2019-11',
              '2019-12', '2020-01', '2020-02', '2020-03']

    normal_monthly_avg = [normal_users[feature].mean() for feature in arpu_features]
    fraud_monthly_avg = [fraud_users[feature].mean() for feature in arpu_features]

    axes[0].plot(months, normal_monthly_avg, marker='o', linewidth=2, markersize=8, label='正常用户', color='#66b3ff')
    axes[0].plot(months, fraud_monthly_avg, marker='s', linewidth=2, markersize=8, label='异常用户', color='#ff9999')
    axes[0].set_title('月均消费趋势对比')
    axes[0].set_xlabel('月份')
    axes[0].set_ylabel('平均消费金额(元)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)

    # 计算总消费额
    normal_total = normal_users[arpu_features].sum(axis=1).mean()
    fraud_total = fraud_users[arpu_features].sum(axis=1).mean()

    # 条形图对比
    categories = ['平均月消费', '总消费额', '消费波动']
    normal_values = [np.mean(normal_monthly_avg), normal_total, np.std(normal_monthly_avg)]
    fraud_values = [np.mean(fraud_monthly_avg), fraud_total, np.std(fraud_monthly_avg)]

    x = np.arange(len(categories))
    width = 0.35

    axes[1].bar(x - width / 2, normal_values, width, label='正常用户', color='#66b3ff', alpha=0.8)
    axes[1].bar(x + width / 2, fraud_values, width, label='异常用户', color='#ff9999', alpha=0.8)
    axes[1].set_title('消费行为综合对比')
    axes[1].set_xlabel('指标')
    axes[1].set_ylabel('金额(元)')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(categories)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # 添加数值标签
    for i, (nv, fv) in enumerate(zip(normal_values, fraud_values)):
        axes[1].text(i - width / 2, nv, f'{nv:.1f}', ha='center', va='bottom')
        axes[1].text(i + width / 2, fv, f'{fv:.1f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('06_consumption_behavior_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 8. 特征重要性分析 ============
def calculate_feature_importance():
    """计算特征重要性"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 准备数据
    analysis_data = data.copy()

    # 对分类变量进行编码
    le_city = LabelEncoder()
    le_county = LabelEncoder()

    analysis_data['city_name_encoded'] = le_city.fit_transform(analysis_data['city_name'])
    analysis_data['county_name_encoded'] = le_county.fit_transform(analysis_data['county_name'])

    # 计算ARPU特征的平均值
    arpu_features = ['arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201911',
                     'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003']
    analysis_data['arpu_avg'] = analysis_data[arpu_features].mean(axis=1)

    # 选择用于分析的特征
    feature_columns = [
        'idcard_cnt', 'city_name_encoded', 'county_name_encoded',
        'voc_call_dur_count', 'voc_call_dur_sum', 'voc_call_dur_mean',
        'voc_opposite_no_m_nunique', 'voc_call_type_1_cnt_sum',
        'voc_call_type_2_cnt_sum', 'voc_imei_m_nunique',
        'sms_sms_send_cnt_sum', 'sms_sms_recv_cnt_sum', 'sms_opposite_no_m_count',
        'sms_opposite_no_m_nunique', 'sms_request_datetime_count',
        'app_busi_name_count', 'app_busi_name_nunique', 'app_flow_sum', 'app_flow_mean',
        'arpu_avg'
    ]

    # 计算特征重要性（使用t检验的效应大小）
    feature_importance = []
    p_values = []

    for feature in feature_columns:
        normal_vals = analysis_data.loc[analysis_data['label'] == 0, feature].dropna()
        fraud_vals = analysis_data.loc[analysis_data['label'] == 1, feature].dropna()

        if len(normal_vals) > 1 and len(fraud_vals) > 1:
            t_stat, p_val = stats.ttest_ind(normal_vals, fraud_vals, equal_var=False)
            # 计算效应大小（Cohen's d）
            pooled_std = np.sqrt(((len(normal_vals) - 1) * np.var(normal_vals) +
                                  (len(fraud_vals) - 1) * np.var(fraud_vals)) /
                                 (len(normal_vals) + len(fraud_vals) - 2))
            cohens_d = (np.mean(fraud_vals) - np.mean(normal_vals)) / pooled_std if pooled_std > 0 else 0

            feature_importance.append(abs(cohens_d))
            p_values.append(p_val)
        else:
            feature_importance.append(0)
            p_values.append(1)

    # 创建特征重要性DataFrame
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': feature_importance,
        'p_value': p_values
    }).sort_values('importance', ascending=False)

    # 将特征名转换为中文
    feature_importance_df['feature_cn'] = feature_importance_df['feature'].map(lambda x: feature_name_mapping.get(x, x))

    return feature_importance_df, arpu_features


def plot_feature_importance(feature_importance_df):
    """绘制特征重要性图"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 特征重要性排序图
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(feature_importance_df)), feature_importance_df['importance'],
                    color=['#ff9999' if imp > np.median(feature_importance_df['importance']) else '#66b3ff'
                           for imp in feature_importance_df['importance']])

    # 使用中文特征名
    plt.yticks(range(len(feature_importance_df)), feature_importance_df['feature_cn'])
    plt.xlabel('特征重要性（效应大小）')
    plt.title('特征重要性排序（基于效应大小）')
    plt.gca().invert_yaxis()

    # 添加数值标签
    for i, v in enumerate(feature_importance_df['importance']):
        plt.text(v + 0.01, i, f'{v:.2f}', va='center')

    plt.tight_layout()
    plt.savefig('07_feature_importance_ranking.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 9. 重要特征雷达图 ============
def plot_radar_chart1(feature_importance_df, arpu_features):
    """绘制重要特征雷达图"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 选择前8个最重要特征
    top_features = feature_importance_df.head(8)['feature'].tolist()

    # 特征名称映射
    radar_feature_mapping = {
        'idcard_cnt': '身份证关联卡数',
        'sms_sms_recv_cnt_sum': '短信接收总量',
        'voc_opposite_no_m_nunique': '联系人数量',
        'voc_call_type_2_cnt_sum': '被叫次数',
        'voc_imei_m_nunique': '使用设备数量',
        'app_busi_name_count': 'APP使用总记录数',
        'app_busi_name_nunique': 'APP使用多样性',
        'app_flow_mean': '平均每次使用流量',
        'arpu_avg': '平均消费额',
        'sms_sms_send_cnt_sum': '短信发送总量',
        'voc_call_type_1_cnt_sum': '主叫次数',
        'voc_call_dur_count': '总通话次数'
    }

    # 计算正常用户和异常用户在这些特征上的平均值
    normal_avg = []
    fraud_avg = []
    feature_names = []

    for feature in top_features:
        if feature in ['city_name_encoded', 'county_name_encoded']:
            continue  # 跳过编码后的地域特征

        if feature in data.columns:
            normal_avg.append(normal_users[feature].mean())
            fraud_avg.append(fraud_users[feature].mean())
        elif feature == 'arpu_avg':
            normal_avg.append(normal_users[arpu_features].mean().mean())
            fraud_avg.append(fraud_users[arpu_features].mean().mean())
        else:
            continue

        feature_names.append(radar_feature_mapping.get(feature, feature))

    # 数据标准化
    scaler = MinMaxScaler()
    combined_data = np.array([normal_avg, fraud_avg])
    normalized_data = scaler.fit_transform(combined_data.T).T

    # 创建雷达图
    from math import pi

    N = len(feature_names)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))

    # 绘制正常用户
    normal_values = list(normalized_data[0]) + [list(normalized_data[0])[0]]
    ax.plot(angles, normal_values, linewidth=2, linestyle='solid', label='正常用户', color='#66b3ff')
    ax.fill(angles, normal_values, alpha=0.25, color='#66b3ff')

    # 绘制异常用户
    fraud_values = list(normalized_data[1]) + [list(normalized_data[1])[0]]
    ax.plot(angles, fraud_values, linewidth=2, linestyle='solid', label='异常用户', color='#ff9999')
    ax.fill(angles, fraud_values, alpha=0.25, color='#ff9999')

    # 添加特征标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_names, fontsize=10)
    ax.set_title('重要特征对比雷达图', size=16, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

    plt.tight_layout()
    plt.savefig('08_top_features_radar_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

###一开始我计算了正常用户和异常用户的平均值，并进行了标准化，这里可能由于标准化后数据分布集中在某个区间，导致差异不明显。
#优化如下
#1.特征排序优化：计算每个特征的差异度，按差异度从大到小排序，将差异最大的特征放在前面
#2.独立标准化：每个特征独立进行最小-最大标准化
#3.差异增强：使用sigmoid函数增强差异，将中心点设为0.5，放大两端差异，添加非线性变换使小差异更明显
def plot_radar_chart2(feature_importance_df, arpu_features):
    """绘制重要特征雷达图 - 优化版"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False

    # 选择最重要的8个特征
    top_features = feature_importance_df.head(8)['feature'].tolist()

    # 特征名称映射
    radar_feature_mapping = {
        'idcard_cnt': '身份证关联卡数',
        'sms_sms_recv_cnt_sum': '短信接收总量',
        'voc_opposite_no_m_nunique': '联系人数量',
        'voc_call_type_2_cnt_sum': '被叫次数',
        'voc_imei_m_nunique': '使用设备数量',
        'app_busi_name_count': 'APP使用总记录数',
        'app_busi_name_nunique': 'APP使用多样性',
        'app_flow_mean': '平均每次使用流量',
        'arpu_avg': '平均消费额',
        'sms_sms_send_cnt_sum': '短信发送总量',
        'voc_call_type_1_cnt_sum': '主叫次数',
        'voc_call_dur_count': '总通话次数'
    }

    # 计算正常用户和异常用户在这些特征上的平均值
    normal_avg = []
    fraud_avg = []
    feature_names = []

    for feature in top_features:
        if feature in ['city_name_encoded', 'county_name_encoded']:
            continue

        if feature in data.columns:
            normal_avg.append(normal_users[feature].mean())
            fraud_avg.append(fraud_users[feature].mean())
        elif feature == 'arpu_avg':
            normal_avg.append(normal_users[arpu_features].mean().mean())
            fraud_avg.append(fraud_users[arpu_features].mean().mean())
        else:
            continue

        feature_names.append(radar_feature_mapping.get(feature, feature))

    # 计算差异度并排序
    differences = [abs(f - n) / (f + n + 1e-8) for f, n in zip(fraud_avg, normal_avg)]

    # 按差异度从大到小排序
    sorted_indices = np.argsort(differences)[::-1]
    feature_names = [feature_names[i] for i in sorted_indices]
    normal_avg = [normal_avg[i] for i in sorted_indices]
    fraud_avg = [fraud_avg[i] for i in sorted_indices]

    # 对每个特征进行独立标准化，使差异更明显
    scaled_normal = []
    scaled_fraud = []

    for n_val, f_val in zip(normal_avg, fraud_avg):
        if n_val == 0 and f_val == 0:
            scaled_normal.append(0)
            scaled_fraud.append(0)
        else:
            max_val = max(n_val, f_val)
            min_val = min(n_val, f_val)

            if max_val == min_val:
                # 如果值相同，设为0.5
                scaled_normal.append(0.5)
                scaled_fraud.append(0.5)
            else:
                # 使用非线性缩放增强差异
                scaled_normal.append((n_val - min_val) / (max_val - min_val))
                scaled_fraud.append((f_val - min_val) / (max_val - min_val))

    # 进一步放大差异
    scaled_normal = np.array(scaled_normal)
    scaled_fraud = np.array(scaled_fraud)

    # 应用sigmoid函数增强差异可见性
    def enhance_difference(x, center=0.5, scale=2.0):
        return 1 / (1 + np.exp(-scale * (x - center)))

    enhanced_normal = enhance_difference(scaled_normal, center=0.5, scale=3.0)
    enhanced_fraud = enhance_difference(scaled_fraud, center=0.5, scale=3.0)

    # 创建雷达图
    from math import pi

    N = len(feature_names)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(16, 12), subplot_kw=dict(projection='polar'))

    # 设置网格
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # 绘制正常用户
    normal_values = list(enhanced_normal) + [enhanced_normal[0]]
    ax.plot(angles, normal_values, linewidth=3, linestyle='solid',
            label='正常用户', color='#3498db', marker='o', markersize=8)
    ax.fill(angles, normal_values, alpha=0.3, color='#3498db')

    # 绘制异常用户
    fraud_values = list(enhanced_fraud) + [enhanced_fraud[0]]
    ax.plot(angles, fraud_values, linewidth=3, linestyle='solid',
            label='异常用户', color='#e74c3c', marker='s', markersize=8)
    ax.fill(angles, fraud_values, alpha=0.3, color='#e74c3c')

    # 设置特征标签位置和样式
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_names, fontsize=11, fontweight='bold')

    # 优化标签位置，避免重叠
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        if angle in (0, pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # 设置径向网格
    ax.set_rlabel_position(0)

    # 设置径向刻度，使用更精细的刻度
    max_value = max(enhanced_normal.max(), enhanced_fraud.max())
    y_ticks = np.linspace(0, 1, 6)
    ax.set_ylim(0, 1.1)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{tick:.1f}' for tick in y_ticks], fontsize=9)
    ax.grid(True, alpha=0.3)

    # 添加网格线
    ax.xaxis.grid(True, color='gray', alpha=0.3, linestyle='--')
    ax.yaxis.grid(True, color='gray', alpha=0.3, linestyle='--')

    # 添加标题和图例
    ax.set_title('重要特征对比雷达图\n正常用户 vs 异常用户',
                 size=18, pad=30, fontweight='bold', color='#2c3e50')

    # 将图例放在右上角
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1),
              fontsize=12, frameon=True, framealpha=0.9,
              edgecolor='gray', fancybox=True)

    # 添加差异说明文本
    max_diff_index = np.argmax(np.abs(enhanced_fraud - enhanced_normal))
    max_diff_feature = feature_names[max_diff_index]
    max_diff_value = abs(enhanced_fraud[max_diff_index] - enhanced_normal[max_diff_index])

    # 添加数据标签
    for i, (angle, n_val, f_val, feature) in enumerate(
            zip(angles[:-1], enhanced_normal, enhanced_fraud, feature_names)):
        # 正常用户标签
        ax.annotate(f'N:{n_val:.2f}',
                    xy=(angle, n_val),
                    xytext=(angle, n_val + 0.05),
                    ha='center', va='center',
                    fontsize=8, color='#3498db',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='#3498db'))

        # 异常用户标签
        ax.annotate(f'F:{f_val:.2f}',
                    xy=(angle, f_val),
                    xytext=(angle, f_val - 0.05),
                    ha='center', va='center',
                    fontsize=8, color='#e74c3c',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='#e74c3c'))

    # 添加中心文本
    center_text = f"最大差异特征:\n{max_diff_feature}\n差异度: {max_diff_value:.2f}"
    ax.annotate(center_text, xy=(0, 0), xytext=(0, -0.1),
                ha='center', va='center',
                fontsize=10, color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa', alpha=0.9, edgecolor='gray'))

    plt.tight_layout()
    plt.savefig('09_top_features_radar_chart_enhanced.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

    # 打印特征对比数据
    print("特征对比数据（原始值）:")
    print("-" * 60)
    print(f"{'特征名称':<20} {'正常用户均值':<15} {'异常用户均值':<15} {'差异比率':<10}")
    print("-" * 60)

    for i, feature in enumerate(feature_names):
        n_orig = normal_avg[i]
        f_orig = fraud_avg[i]
        if n_orig != 0:
            ratio = f_orig / n_orig
        else:
            ratio = float('inf') if f_orig > 0 else 1.0
        print(f"{feature:<20} {n_orig:<15.2f} {f_orig:<15.2f} {ratio:<10.2f}")

    print("-" * 60)
# ============ 10. 特征相关性热力图 ============
def plot_correlation_heatmap():
    """绘制特征相关性热力图"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 选择数值型特征
    numeric_features = [
        'idcard_cnt', 'voc_call_dur_count', 'voc_call_dur_sum', 'voc_call_dur_mean',
        'voc_opposite_no_m_nunique', 'voc_call_type_1_cnt_sum',
        'voc_call_type_2_cnt_sum', 'voc_imei_m_nunique',
        'sms_sms_send_cnt_sum', 'sms_sms_recv_cnt_sum', 'sms_opposite_no_m_count',
        'sms_opposite_no_m_nunique', 'sms_request_datetime_count',
        'app_busi_name_count', 'app_busi_name_nunique', 'app_flow_sum', 'app_flow_mean'
    ]

    # 添加ARPU平均值
    arpu_features = ['arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201911',
                     'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003']
    data['arpu_avg'] = data[arpu_features].mean(axis=1)
    numeric_features.append('arpu_avg')

    # 获取中文特征名
    numeric_features_cn = [feature_name_mapping[feat] for feat in numeric_features]

    # 计算相关性矩阵
    correlation_data = data[numeric_features].corr()

    # 创建相关性热力图
    plt.figure(figsize=(15, 12))
    mask = np.triu(np.ones_like(correlation_data, dtype=bool))  # 只显示下半部分
    sns.heatmap(correlation_data, mask=mask, annot=False, cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": .8})

    # 设置中文特征名
    plt.xticks(range(len(numeric_features_cn)), numeric_features_cn, rotation=45, ha='right')
    plt.yticks(range(len(numeric_features_cn)), numeric_features_cn, rotation=0)

    plt.title('特征相关性热力图', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('10_feature_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 11. 梯度提升树模型分析 ============
def gbdt_analysis():
    """梯度提升树模型分析"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 准备数据
    X = data[[
        'idcard_cnt', 'voc_call_dur_count', 'voc_call_dur_sum', 'voc_call_dur_mean',
        'voc_opposite_no_m_nunique', 'voc_call_type_1_cnt_sum',
        'voc_call_type_2_cnt_sum', 'voc_imei_m_nunique',
        'sms_sms_send_cnt_sum', 'sms_sms_recv_cnt_sum', 'sms_opposite_no_m_count',
        'sms_opposite_no_m_nunique', 'sms_request_datetime_count',
        'app_busi_name_count', 'app_busi_name_nunique', 'app_flow_sum', 'app_flow_mean'
    ]]

    # 添加ARPU平均值
    arpu_features = ['arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201911',
                     'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003']
    X['arpu_avg'] = data[arpu_features].mean(axis=1)

    y = data['label']

    # 处理缺失值
    X = X.fillna(X.mean())

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 训练梯度提升树模型
    gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)

    # 获取特征重要性
    feature_importance_gb = gb_model.feature_importances_

    # 创建基于GBDT的特征重要性图
    feature_importance_gb_df = pd.DataFrame({
        'feature': X.columns.tolist(),
        'importance': feature_importance_gb
    }).sort_values('importance', ascending=False)

    # 添加中文特征名
    feature_importance_gb_df['feature_cn'] = feature_importance_gb_df['feature'].map(
        lambda x: feature_name_mapping.get(x, x))

    # 绘制特征重要性
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(feature_importance_gb_df)), feature_importance_gb_df['importance'],
                    color=['#ff9999' if imp > np.median(feature_importance_gb_df['importance']) else '#66b3ff'
                           for imp in feature_importance_gb_df['importance']])

    # 使用中文特征名
    plt.yticks(range(len(feature_importance_gb_df)), feature_importance_gb_df['feature_cn'])
    plt.xlabel('特征重要性（GBDT）')
    plt.title('基于梯度提升树的特征重要性排序')
    plt.gca().invert_yaxis()

    # 添加数值标签
    for i, v in enumerate(feature_importance_gb_df['importance']):
        plt.text(v + 0.001, i, f'{v:.3f}', va='center')

    plt.tight_layout()
    plt.savefig('11_gbdt_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 模型性能评估
    y_pred = gb_model.predict(X_test)
    accuracy = gb_model.score(X_test, y_test)

    print(f"\n模型性能评估:")
    print(f"准确率: {accuracy:.4f}")
    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=['正常用户', '异常用户']))

    # 绘制混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['正常', '异常'], yticklabels=['正常', '异常'])
    plt.xlabel('预测标签')
    plt.ylabel('真实标签')
    plt.title(f'混淆矩阵\n准确率: {accuracy:.3f}')
    plt.tight_layout()
    plt.savefig('12_confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

    return gb_model, feature_importance_gb_df, accuracy


# ============ 12. 综合对比图 ============
def plot_key_findings_summary(feature_importance_df, gb_model_accuracy):
    """绘制关键发现总结图"""
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False
    # 选择最重要的5个特征
    top_5_features = feature_importance_df.head(5)['feature'].tolist()

    # 特征名称映射
    summary_feature_mapping = {
        'idcard_cnt': '身份证关联卡数',
        'voc_opposite_no_m_nunique': '联系人数量',
        'sms_sms_send_cnt_sum': '短信发送总量',
        'voc_call_type_1_cnt_sum': '主叫次数',
        'voc_call_dur_count': '总通话次数',
        'arpu_avg': '平均消费额',
        'sms_request_datetime_count': '短信记录总条数',
        'voc_call_type_2_cnt_sum': '被叫次数',
        'voc_imei_m_nunique': '使用设备数量',
        'app_busi_name_count': 'APP使用总记录数',
        'app_busi_name_nunique': 'APP使用多样性',
        'sms_sms_recv_cnt_sum': '短信接收总量',
        'voc_call_dur_mean': '平均通话时长',
        'voc_call_dur_sum': '总通话时长',
        'sms_opposite_no_m_count': '短信交互总次数',
        'sms_opposite_no_m_nunique': '短信交互不同人数',
        'app_flow_sum': '总流量消耗',
        'app_flow_mean': '平均每次使用流量'
    }

    top_5_names = [summary_feature_mapping.get(f, f) for f in top_5_features]

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    for i, (feature, name) in enumerate(zip(top_5_features, top_5_names)):
        if i < len(axes):
            # 箱线图对比
            if feature in data.columns:
                data_to_plot = [normal_users[feature].dropna(), fraud_users[feature].dropna()]
            else:
                # 处理衍生特征
                arpu_features = ['arpu_201908', 'arpu_201909', 'arpu_201910', 'arpu_201911',
                                 'arpu_201912', 'arpu_202001', 'arpu_202002', 'arpu_202003']
                if feature == 'arpu_avg':
                    data_to_plot = [
                        normal_users[arpu_features].mean(axis=1).dropna(),
                        fraud_users[arpu_features].mean(axis=1).dropna()
                    ]
                else:
                    continue

            box_plot = axes[i].boxplot(data_to_plot, labels=['正常用户', '异常用户'], patch_artist=True)

            # 设置箱体颜色
            colors = ['#66b3ff', '#ff9999']
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)

            axes[i].set_title(f'{name}\n特征对比', fontsize=12)
            axes[i].set_ylabel('特征值')
            axes[i].grid(True, alpha=0.3)

    # 添加模型性能总结
    axes[5].axis('off')
    summary_text = f"""
电信诈骗用户行为模式分析总结

数据概况:
- 总样本数: {len(data):,}条
- 正常用户: {len(normal_users):,}条 ({len(normal_users) / len(data) * 100:.1f}%)
- 异常用户: {len(fraud_users):,}条 ({len(fraud_users) / len(data) * 100:.1f}%)

关键发现:
1. 身份证关联卡数: 异常用户群身份证关联卡数明显高于正常用户
5. APP使用总记录: 异常用户APP总使用记录极低
4. APP使用多样性: 异常用户群APP使用多样性显著低于正常用户
4. 短信接收量: 异常用户群接收短信数量明显小于正常用户
5. 联系人数量: 异常用户群联系人数量较多

模型性能:
- 基于GBDT的识别准确率: {gb_model_accuracy:.3f}
"""

    axes[5].text(0.05, 0.5, summary_text, transform=axes[5].transAxes, fontsize=12,
                 verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))

    plt.suptitle('最重要特征的用户行为对比分析', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig('13_key_findings_summary.png', dpi=300, bbox_inches='tight')
    plt.show()


# ============ 13. 主程序执行 ============
def main():
    """主函数"""
    print("开始执行电信诈骗数据分析可视化...")

    # 1. 基础分布分析
    print("正在绘制基础分布图...")
    plot_basic_distributions()

    # 2. 通话行为特征对比
    print("正在绘制通话行为特征对比...")
    plot_voice_features_comparison()

    # 3. 短信行为特征对比
    print("正在绘制短信行为特征对比...")
    plot_sms_features_comparison()

    # 4. APP行为特征对比
    print("正在绘制APP行为特征对比...")
    plot_app_features_comparison()

    # 5. 消费行为特征对比
    print("正在绘制消费行为分析...")
    plot_consumption_behavior_analysis()

    # 6. 特征重要性分析
    print("正在计算特征重要性...")
    feature_importance_df, arpu_features = calculate_feature_importance()
    plot_feature_importance(feature_importance_df)

    # 7. 重要特征雷达图
    print("正在绘制重要特征雷达图...")
    plot_radar_chart1(feature_importance_df, arpu_features)

    # 8. 重要特征雷达图（优化后）
    print("正在绘制重要特征雷达图（优化后）...")
    plot_radar_chart2(feature_importance_df, arpu_features)

    # 9. 特征相关性热力图
    print("正在绘制特征相关性热力图...")
    plot_correlation_heatmap()

    # 10. 梯度提升树模型分析
    print("正在训练梯度提升树模型...")
    gb_model, gb_importance_df, accuracy = gbdt_analysis()

    # 11. 综合对比图
    print("正在绘制综合对比图...")
    plot_key_findings_summary(feature_importance_df, accuracy)

    print("分析完成！所有图表已保存到当前目录。")

    # 打印总结
    print("\n" + "=" * 60)
    print("分析总结:")
    print("=" * 60)
    print(f"1. 数据规模: {len(data)}条记录，正常:异常 ≈ 1:2")
    print(f"2. 最重要特征: {', '.join(feature_importance_df.head(3)['feature_cn'].tolist())}")
    print(f"3. 模型性能: GBDT准确率 = {accuracy:.3f}")
    print(f"4. 生成的图表: 12张高清PNG图片，可直接用于PPT展示")
    print("=" * 60)


# 运行主程序
if __name__ == "__main__":
    main()