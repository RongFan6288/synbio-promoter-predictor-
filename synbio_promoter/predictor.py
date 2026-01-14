# real_promoter_predictor.py
# Day 5 核心模型 + Day 8 CLI 接口

def predict_promoter(sequence):
    """
    基于原核启动子保守序列的规则预测器
    输入: 20bp DNA 序列 (str)，如 'TTGACAATATAATGTATTTC'
    输出: 启动子概率 (float, 0.0 ～ 1.0)
    """
    seq = sequence.upper().strip()
    
    # 长度校验
    if len(seq) != 20:
        return 0.0
    
    score = 0.0

    # -10 box: TATAAT（Pribnow box）
    if "TATAAT" in seq:
        score += 0.7
    elif "TATAA" in seq or "ATAAT" in seq:
        score += 0.5
    elif "TATAT" in seq or "TAAAA" in seq:
        score += 0.3

    # -35 box: TTGACA
    if "TTGACA" in seq:
        score += 0.6
    elif "TTGAC" in seq or "TGACA" in seq:
        score += 0.4
    elif "GTGACA" in seq or "TTGAAA" in seq:
        score += 0.2

    # 间隔区：理想长度 17±1 bp
    # 简化处理：如果同时有 -10 和 -35，加分
    if score >= 0.9:
        score += 0.2  # 完美组合
    elif score >= 0.7:
        score += 0.1  # 较好组合

    # 归一化到 [0, 1]
    probability = min(score, 1.0)
    return round(probability, 3)

# ==============================
# 以下为 Gradio 兼容层（Day 5 内容）
# ==============================

def promoter_analysis_tool(input_sequence):
    """
    Gradio 调用的主函数（保持兼容）
    """
    prob = predict_promoter(input_sequence)
    is_promoter = prob > 0.6
    result_text = "✅ 高概率启动子" if is_promoter else "❌ 非典型启动子"
    confidence = f"置信度: {prob:.1%}"
    return f"{result_text}\n{confidence}"

# 如果直接运行此文件，可测试
if __name__ == "__main__":
    test_seq = "TTGACAATATAATGTATTTC"
    print(f"测试序列: {test_seq}")
    print(f"预测概率: {predict_promoter(test_seq):.3f}")