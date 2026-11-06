# HPC 多核优化练习 · ClustalW 2.1

> 入门题：给一个诞生于单核时代的经典科学软件做多核优化。

## 背景

ClustalW 是多序列比对（生物信息学基础操作）的奠基软件，1994 年的原始论文是生物学界被引最多的论文之一。本仓库 `src/` 是 ClustalW 2.1（2010 年，LGPL）的原样源码——**整个程序没有一条并行指令**，在你的多核机器上跑起来时，其余核心全部在围观。

## 你的任务

1. 编译并跑出基线（见"快速开始"）；
2. 找出程序热点，把定位证据写进报告（Linux 推荐 `perf` / `gprof` 剖析；任何平台也可以用**计时代码插桩**——在主要阶段外打时间戳统计耗时占比——或代码结构分析代替）；
3. 在**不改变程序输出**的前提下做多核优化（OpenMP / std::thread 均可）；
4. 测量 1 / 2 / 4 / 8 线程加速比，提交代码 diff + 优化报告。

## 环境

- Linux + gcc/g++（8 核以上 CPU；16G 内存绰绰有余，本题峰值内存 < 100 MB）
- 无任何第三方库依赖
- **Windows 用户**：推荐安装 WSL2（管理员 PowerShell 运行 `wsl --install -d Ubuntu`），在 Ubuntu 内按本文档操作——所有命令原样适用。原生 MinGW/MSYS2 也可以编译运行：判题脚本已自动兼容 Windows 换行符，热点定位可用计时代码插桩替代 perf；但 WSL2 的环境与评分机器一致，体验更顺

## 快速开始

```bash
git clone <本仓库 URL> && cd hpc-lab-clustalw
./configure CXX=g++ CXXFLAGS='-O2' && make -j

# 注意: ClustalW 把输出写在"输入文件所在目录", 所以先把输入拷进 runs/ 再跑
mkdir -p runs && cd runs
# 冒烟（参考机器 ~11 s）
cp ../data/rna_rnasep_200.fa . && ../src/clustalw2 -infile=rna_rnasep_200.fa -type=dna
# 自测（参考机器 ~41 s）
cp ../data/rna_rnasep_400.fa . && ../src/clustalw2 -infile=rna_rnasep_400.fa -type=dna
# 全量基线（参考机器 ≈5 min，普通笔记本 ≈9 min）
cp ../data/rna_rnasep_1100.fa . && ../src/clustalw2 -infile=rna_rnasep_1100.fa -type=dna
```

输出 `rna_rnasep_*.aln`（比对结果）与 `rna_rnasep_*.dnd`（指导树）生成在当前目录。

## 正确性判据

本题打分为确定性整数运算：**你的优化版本输出必须与 `baseline/` 中的参考输出逐字节一致**。

```bash
../scripts/verify.sh rna_rnasep_1100.aln rna_rnasep_1100.dnd
```

## 计时与提交

- 每个规模跑 3 次取中位数（脚本会保留各次输出；输入用 runs/ 里已拷贝的副本，避免输出写进 `data/`）：

  ```bash
  ../scripts/bench.sh "../src/clustalw2 -infile=rna_rnasep_1100.fa -type=dna"
  ```

- 提交：代码 diff（或 git 分支）+ 优化报告（热点定位证据、方案说明、加速比表、讨论）
- 报告请附 `lscpu` 输出与编译器版本

## 规则

- 禁止修改 `data/` 中的输入文件或问题规模
- 禁止一切改变输出结果的做法（换算法、跳过计算、预计算结果表）
- 允许：编译器 flag、OpenMP、std::thread、进程级并行等一切不改变输出的手段

## 数据与许可

- 测试数据：Rfam 家族 RF00010（RNase P RNA）真实序列，CC0 许可，详见 `data/DATASET.md`
- 代码：ClustalW 2.1，LGPL-2.1（见 `COPYING` / `COPYING.LESSER`），上游构建说明见 `docs/README-upstream.md`
