# promoter_predictor.py - 启动子活性预测模型（CNN + 可视化）

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import random
import os

# ----------------------------
# 1. DNA 序列编码工具
# ----------------------------
def dna_to_onehot(seq):
    """将DNA序列转为 one-hot 编码 (A=0, T=1, C=2, G=3)"""
    mapping = {'A': [1,0,0,0], 'T': [0,1,0,0], 'C': [0,0,1,0], 'G': [0,0,0,1]}
    return [mapping.get(base.upper(), [0,0,0,0]) for base in seq]

def generate_promoter_data(n_samples=1000, seq_len=50):
    """生成模拟启动子数据（含TATA box的序列活性更高）"""
    sequences = []
    labels = []
    bases = "ATCG"
    
    for _ in range(n_samples):
        # 随机生成序列
        seq = ''.join(random.choices(bases, k=seq_len))
        
        # 如果包含 "TATA"，则标签高（活性强）
        if "TATA" in seq:
            label = random.uniform(0.7, 1.0)  # 高活性
        else:
            label = random.uniform(0.0, 0.3)  # 低活性
        
        sequences.append(dna_to_onehot(seq))
        labels.append(label)
    
    return torch.tensor(sequences, dtype=torch.float32), \
           torch.tensor(labels, dtype=torch.float32)

# ----------------------------
# 2. CNN 模型定义
# ----------------------------
class PromoterCNN(nn.Module):
    def __init__(self, seq_len=50):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=4, out_channels=16, kernel_size=5)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(16 * ((seq_len - 4) // 2), 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape: (batch, 4, seq_len)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x.squeeze()

# ----------------------------
# 3. 训练函数
# ----------------------------
def train_model():
    # 超参数
    SEQ_LEN = 50
    BATCH_SIZE = 32
    EPOCHS = 50
    LR = 0.001

    # 生成数据
    X, y = generate_promoter_data(n_samples=1000, seq_len=SEQ_LEN)
    X = X.permute(0, 2, 1)  # 转为 (batch, channels=4, seq_len)

    # 创建模型
    model = PromoterCNN(seq_len=SEQ_LEN)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    # 训练循环
    losses = []
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        
        for i in range(0, len(X), BATCH_SIZE):
            batch_x = X[i:i+BATCH_SIZE]
            batch_y = y[i:i+BATCH_SIZE]
            
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / (len(X) // BATCH_SIZE)
        losses.append(avg_loss)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {avg_loss:.4f}")

    # 保存损失曲线图
    plt.figure(figsize=(8, 5))
    plt.plot(losses, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.title('Promoter Activity Prediction - Training Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_loss.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\n✅ 训练完成！损失曲线已保存为 'training_loss.png'")
    print("💡 提示：在 VS Code 左侧点击该文件即可预览图表！")

# ----------------------------
# 4. 主程序入口
# ----------------------------
if __name__ == "__main__":
    # 检查是否安装了必要库
    try:
        import torch
        import matplotlib
    except ImportError as e:
        print("❌ 缺少依赖库！请运行以下命令安装：")
        print("pip install torch matplotlib")
        exit(1)
    
    train_model()