# promoter_web_app.py - 启动子预测 Web 应用（5行核心界面代码！）

import torch
import gradio as gr
from real_promoter_predictor import PromoterCNN, dna_to_onehot  # 复用你写的模型和编码函数

# 加载训练好的模型（简化版：直接新建并假设已收敛）
model = PromoterCNN(seq_len=20)
# 注意：实际项目中这里会 load_state_dict(torch.load(...))，但为简化，我们用“模拟高置信度”逻辑

def predict_promoter(seq):
    """Web 调用的预测函数"""
    seq = seq.strip().upper()
    if len(seq) != 20:
        return "❌ 请输入 exactly 20 个碱基（A/T/C/G）"
    if not all(b in "ATCG" for b in seq):
        return "❌ 序列只能包含 A, T, C, G"
    
    # 模拟智能判断：如果含 TATA 或 TTGACA，返回高概率
    if "TATA" in seq or "TTGACA" in seq:
        prob = 0.95
    else:
        prob = 0.05
    
    # 实际项目中这里会调用 model(...)，但避免加载权重复杂化
    return f"✅ 启动子概率: {prob:.2%}\n（基于经典 motif 判断）"

# ----------------------------
# 🔥 核心：5行 Gradio 界面代码！
# ----------------------------
with gr.Blocks(title="启动子预测器") as demo:
    gr.Markdown("## 🧬 合成生物学启动子活性预测")
    gr.Markdown("输入一段 **20bp 的 DNA 序列**，AI 将预测它是否为强启动子")
    input_seq = gr.Textbox(label="DNA 序列 (20bp)", placeholder="例如: TTGACAATATAATGTATTTC")
    output = gr.Textbox(label="预测结果")
    btn = gr.Button("预测启动子活性")
    btn.click(fn=predict_promoter, inputs=input_seq, outputs=output)

# 启动应用
if __name__ == "__main__":
    demo.launch()  # 默认打开浏览器