# 🧬 启动子活性预测器

一个基于深度学习的合成生物学工具，用于预测 DNA 序列是否为强启动子。

## ✨ 功能
- 输入 20bp DNA 序列
- 输出启动子概率（%）
- Web 界面交互（Gradio）

## 🚀 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动 Web 应用：
   ```bash
   python promoter_web_app.py
   ```

3. 在浏览器打开：http://127.0.0.1:7860

## 📂 项目结构
- `real_promoter_predictor.py`：真实数据训练逻辑
- `promoter_web_app.py`：Web 界面
- `ecoli_promoters.csv`：大肠杆菌启动子数据集

## 🧪 示例序列
- 强启动子：`TTGACAATATAATGTATTTC` → ～95%
- 非启动子：`ATGCATGCATGCATGCATGC` → ～5%