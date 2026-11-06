# 数据集说明（DATASET.md）

## 来源

[Rfam](https://rfam.org) 家族 **RF00010 —— RNase P RNA**（核糖核酸酶 P 的 RNA 亚基，跨细菌/古菌/真核三域）。

- 原始下载：`https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/fasta_files/RF00010.fa.gz`（8942 条）
- 许可：**CC0**（公有领域），可自由分发
- 引用：Rfam 数据库（当前版本见 Rfam 官网 NAR 数据库刊文）

## 清洗与抽样

由 `scripts/make_rna_dataset.py`（固定 seed=20261106，可复现）：

1. 大写化，仅保留 ACGTN，U→T（ClustalW 核酸打分）
2. 剔除长度 <150 或 >700 nt、歧义碱基 >2% 的序列
3. 去精确重复（8942 → 8820）
4. 固定种子随机抽样 N 条

均长 382 nt（范围 173~522），带真实 indel 与高度分歧。
**注意**：序列不可全部等长，否则 ClustalW 会把输入当"已比对块"走捷径。

## 冻结文件

| 文件 | N | 用途 |
|------|---|------|
| `rna_rnasep_200.fa` | 200 | 冒烟 |
| `rna_rnasep_400.fa` | 400 | 学生自测 |
| `rna_rnasep_1100.fa` | 1100 | 全量基线（≈5 min @ 参考机器） |

三个文件为独立抽样，互不包含。**题目数据已冻结**：优化练习中禁止修改。
