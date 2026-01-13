# parse_fasta.py - 读取FASTA文件并分析

def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as f:
        header = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    sequences[header] = ''.join(seq)
                header = line[1:].split()[0]
                seq = []
            else:
                seq.append(line)
        if header:
            sequences[header] = ''.join(seq)
    return sequences

def gc_content(dna):
    dna = dna.upper()
    gc = dna.count('G') + dna.count('C')
    if len(dna) == 0:
        return 0.0
    return round(gc / len(dna) * 100, 2)

if __name__ == "__main__":
    data = read_fasta("RNA_small.fasta")
    print(f"共读取 {len(data)} 条序列\n")
    for i, (header, seq) in enumerate(list(data.items())[:3]):
        print(f"序列 {i+1}: {header}")
        print(f"  长度: {len(seq)} nt")
        print(f"  前20个碱基: {seq[:20]}...")
        print(f"  GC含量: {gc_content(seq)} %\n")