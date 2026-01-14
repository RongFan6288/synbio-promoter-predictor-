# promoter_cli.py
import argparse
import pandas as pd
import os
from .predictor import predict_promoter 

def read_fasta(file_path):
    """读取 FASTA 文件，返回 (id, sequence) 列表"""
    sequences = []
    current_id = None
    current_seq = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id is not None:
                    sequences.append((current_id, ''.join(current_seq).upper()))
                current_id = line[1:].split()[0]  # 取第一个词作为 ID
                current_seq = []
            else:
                current_seq.append(line)
        # 添加最后一条序列
        if current_id is not None:
            sequences.append((current_id, ''.join(current_seq).upper()))
    return sequences

def main():
    parser = argparse.ArgumentParser(description="启动子活性预测命令行工具")
    parser.add_argument("--fasta", required=True, help="输入 FASTA 文件路径")
    parser.add_argument("--output", default="promoter_predictions.csv", help="输出 CSV 路径")
    args = parser.parse_args()

    # 读取 FASTA
    seqs = read_fasta(args.fasta)
    print(f"✅ 读取到 {len(seqs)} 条序列")

    # 预测每条序列
    results = []
    for seq_id, seq in seqs:
        seq_clean = seq.replace(' ', '').replace('\n', '')
        if len(seq_clean) != 20:
            print(f"⚠️ 跳过 {seq_id}：长度为 {len(seq_clean)}，非 20bp")
            continue
        prob = predict_promoter(seq_clean)
        results.append({
            "sequence_id": seq_id,
            "sequence": seq_clean,
            "promoter_probability": round(prob * 100, 1)
        })

    # 保存结果
    df = pd.DataFrame(results)
    df.to_csv(args.output, index=False)
    print(f"✅ 预测完成！结果已保存至: {args.output}")

if __name__ == "__main__":
    main()