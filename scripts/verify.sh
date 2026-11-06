#!/usr/bin/env bash
# verify.sh -- 校验比对输出与基准是否逐字节一致。
#
# 用法:  scripts/verify.sh <你的 .aln 文件> [<你的 .dnd 文件>]
# 例:    cd runs && ../scripts/verify.sh rna_rnasep_1100.aln rna_rnasep_1100.dnd
#
# 本题为确定性整数打分, 正确的优化结果必须与 baseline/ 下的参考输出逐字节一致。

set -u
BASELINE="$(cd "$(dirname "$0")/../baseline" && pwd)"
rc=0
for f in "$@"; do
    if [ ! -f "$f" ]; then
        echo "FAIL: 找不到 $f —— 先运行比对程序生成输出（注意: ClustalW 把输出写在输入文件所在目录）"
        rc=1
        continue
    fi
    b="${BASELINE}/$(basename "$f")"
    if [ ! -f "$b" ]; then
        echo "SKIP: 基准中没有 $(basename "$f")"
        continue
    fi
    if cmp -s "$f" "$b"; then
        echo "PASS: $(basename "$f") 与基准逐字节一致 ✔"
    else
        echo "FAIL: $(basename "$f") 与基准不一致 ✘"
        rc=1
    fi
done
exit $rc
