# dna_tools.py - 生物信息基础工具

def reverse_complement(dna):
    """返回DNA的反向互补链"""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in dna[::-1])

def gc_content(dna):
    """计算GC含量（百分比）"""
    gc = dna.count('G') + dna.count('C')
    return round(gc / len(dna) * 100, 2)

# 测试代码
if __name__ == "__main__":
    seq = "ATGCGTA"
    print("原始序列:", seq)
    print("反向互补:", reverse_complement(seq))
    print("GC含量:", gc_content(seq), "%")