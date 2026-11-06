# 基线记录（BASELINE.md）

## 生成环境

- 机器：Intel i5-14600KF（14C/20T），Fedora 44，单核运行
- 工具链：gcc/g++ 16.2.1，编译 `./configure CXX=g++ CXXFLAGS='-O2' && make`
- 日期：2026-11-06

## 命令

```bash
./src/clustalw2 -infile=data/rna_rnasep_<N>.fa -type=dna
```

## 实测数据量阶梯（单核）

| N 条 | 基线 | 内存 RSS | 基准输出 |
|------|------|---------|----------|
| 200 | 10.6 s | 4.6 MB | —（冒烟） |
| 400 | 41.0 s | 10.9 MB | `baseline/rna_rnasep_400.aln/.dnd` |
| 1100 | 5:06 | 29.4 MB | `baseline/rna_rnasep_1100.aln/.dnd` |

- 缩放规律：T ≈ 2.53×10⁻⁴·N² 秒（六个实测点偏差 <1%）
- 注意：换数据家族后不可按 L² 外推，须重新实测

## 可复现性

打分为确定性整数运算：同输入多次运行输出**逐字节一致**（已验证）。
不同机器、不同编译器优化级别下输出同样逐字节一致（并行化后浮点不参与打分路径）。

基准输出由上述环境生成，提交前用 `scripts/verify.sh` 比对。
