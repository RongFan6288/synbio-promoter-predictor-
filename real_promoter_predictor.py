# real_promoter_predictor.py - 用真实启动子数据训练模型

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import pandas as pd
import os

# ----------------------------
# 1. 工具函数
# ----------------------------
def dna_to_onehot(seq):
    mapping = {'A': [1,0,0,0], 'T': [0,1,0,0], 'C': [0,0,1,0], 'G': [0,0,0,1]}
    return [mapping.get(base.upper(), [0,0,0,0]) for base in seq]

class PromoterCNN(nn.Module):
    def __init__(self, seq_len=20):
        super().__init__()
        self.conv1 = nn.Conv1d(4, 16, kernel_size=4)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(16 * ((seq_len - 3) // 2), 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x.squeeze()

# ----------------------------
# 2. 加载真实数据
# ----------------------------
def load_real_data(csv_path="ecoli_promoters.csv"):
    df = pd.read_csv(csv_path)
    sequences = []
    labels = []
    
    for _, row in df.iterrows():
        seq = row['sequence']
        label = row['label']
        if len(seq) == 20:  # 确保长度一致
            sequences.append(dna_to_onehot(seq))
            labels.append(float(label))
    
    X = torch.tensor(sequences, dtype=torch.float32).permute(0, 2, 1)
    y = torch.tensor(labels, dtype=torch.float32)
    return X, y

# ----------------------------
# 3. 训练 & 预测
# ----------------------------
def predict_new_sequence(model, seq):
    """预测新序列是否为启动子"""
    if len(seq) != 20:
        raise ValueError("序列必须为20bp！")
    onehot = torch.tensor(dna_to_onehot(seq), dtype=torch.float32)
    onehot = onehot.permute(1, 0).unsqueeze(0)  # (1, 4, 20)
    model.eval()
    with torch.no_grad():
        prob = model(onehot).item()
    return prob

def main():
    # 安装检查
    try:
        import pandas
    except ImportError:
        print("❌ 缺少 pandas！运行：pip install pandas")
        return

    # 加载数据
    X, y = load_real_data()
    print(f"✅ 加载 {len(X)} 条真实启动子数据")

    # 训练模型
    model = PromoterCNN(seq_len=20)
    criterion = nn.BCELoss()  # 二分类用 BCE
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    losses = []
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    # 画 loss 曲线
    plt.figure(figsize=(8, 4))
    plt.plot(losses)
    plt.title("Training Loss (Real Promoter Data)")
    plt.xlabel("Epoch")
    plt.ylabel("Binary Cross-Entropy Loss")
    plt.savefig("real_training_loss.png", dpi=150)
    plt.close()

    # 预测新序列
    test_seq = "TTGACAATATAATGTATTTC"  # 已知强启动子
    prob = predict_new_sequence(model, test_seq)
    print(f"\n🔍 预测序列: {test_seq}")
    print(f"   启动子概率: {prob:.2%}")

    # 再试一个随机序列
    random_seq = "ATGCATGCATGCATGCATGC"
    prob2 = predict_new_sequence(model, random_seq)
    print(f"\n🔍 预测序列: {random_seq}")
    print(f"   启动子概率: {prob2:.2%}")

    print("\n✅ 模型训练完成！图表已保存为 'real_training_loss.png'")

if __name__ == "__main__":
    main()