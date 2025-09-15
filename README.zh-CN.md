codon-recoder
================

语言： [English](README.md) | 中文

将 DNA 序列在保持阅读框不变的前提下，回译为给定的目标氨基酸序列，尽可能最少修改核苷酸。提供命令行工具和 Python API。

项目
- 许可证：MIT（见 `LICENSE`）
- 贡献指南：见 `CONTRIBUTING.md`

特性
- 逐密码子最小更改（哈明距离）
- 平局处理策略（优先第三位 wobble、优选密码子）
- 输出逐密码子变更报告（可写 TSV/JSON）
- 严格输入校验与清晰报错

安装
- 本地开发安装：`pip install -e .`

命令行用法（CLI）
- 基本用法：`codon-recoder --dna ATGGCCGCT --aa MAA`
- 输出报告：`codon-recoder --dna dna.txt --aa aa.txt --report report.tsv`
- 主要参数：
  - `--dna` 或 `--dna-file`：输入 DNA（A/T/G/C，长度为3的倍数）
  - `--aa` 或 `--aa-file`：目标氨基酸序列（终止子用 `_` 或 `*`）
  - `--tie-break {wobble,freq}`：平局时的策略（默认：wobble，优先第三位变化）
  - `--report`：输出路径（根据扩展名写 TSV 或 JSON）
  - `--quiet`：安静模式，不打印摘要
  - `--allow-internal-stop`：允许内部终止子（默认禁止）

Python API
```python
from codon_recode import recode_by_aa_min_changes, dna2aa

new_dna, report = recode_by_aa_min_changes(
    mut_aa="MKT_",   # 终止子可用 '_' 或 '*'
    dna="ATGAAAACGAAA",
    tie_break="wobble",
)
print(new_dna)
print(dna2aa(new_dna))
```

注意事项
- 使用标准遗传密码；终止子为 `_`（CLI 也接受 `*`）。
- 默认禁止内部终止子；如需允许请加 `--allow-internal-stop`。
- 不做物种特异的密码子优化；平局仅用内置“优选密码子”打破。

输入格式
- 支持纯序列或 FASTA 文件（`>` 开头的标题行会被忽略）。
- 忽略空白和换行，自动统一为大写。
- 要求 AA 长度等于 DNA 密码子数量（`len(dna) / 3`）。

开发
- 运行测试：`pytest -q`
- 在受限环境（无法写缓存/临时目录）下：
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q --capture=no -p no:cacheprovider`

示例（5个案例）
- 案例1 — 恒等（无需变更）
  - 命令：`codon-recoder --dna ATGAAAACG --aa MKT`
  - 输出：
    - new DNA: `ATGAAAACG`
    - AA(before): `MKT`
    - AA(after): `MKT`
    - Codons changed: `0 / 3`; Nucleotide changes: `0`

- 案例2 — 单一氨基酸变更（K→N，第三位 wobble 更改）
  - 命令：`codon-recoder --dna ATGAAAACG --aa MNT`
  - 输出：
    - new DNA: `ATGAACACG`
    - AA(before): `MKT`
    - AA(after): `MNT`
    - Codons changed: `1 / 3`; Nucleotide changes: `1`

- 案例3 — 非 wobble 的最小更改（A→P，第一位变化）
  - 命令：`codon-recoder --dna GCT --aa P`
  - 输出：
    - new DNA: `CCT`
    - AA(before): `A`
    - AA(after): `P`
    - Codons changed: `1 / 1`; Nucleotide changes: `1`

- 案例4 — 接受 `*` 作为终止子
  - 命令：`codon-recoder --dna ATGTAA --aa M*`
  - 输出：
    - new DNA: `ATGTAA`
    - AA(before): `M_`
    - AA(after): `M_`
    - Codons changed: `0 / 2`; Nucleotide changes: `0`

- 案例5 — 内部终止子：默认报错；加开关允许
  - 报错：`codon-recoder --dna ATGAAAACG --aa M*T`
    - 报错信息：`ValueError: Internal stop codon in mut_aa is forbidden`
  - 允许：`codon-recoder --dna ATGAAAACG --aa M*T --allow-internal-stop`
    - new DNA: `ATGTAAACG`
    - AA(before): `MKT`
    - AA(after): `M_T`
    - Codons changed: `1 / 3`; Nucleotide changes: `1`

支持与联系
- 中国（微信）：
  - 合作/加我（扫码）：

    ![微信加我](img/addme.jpg)
  - 打赏/请我喝咖啡（微信收款码）：

    ![微信打赏](img/dashang.jpg)
- 海外/国际常用方式（按需选择）：

  - Buy Me a Coffee: https://buymeacoffee.com/bowen007
  - 联系方式：邮件（xiongbojian007@gmail.com

以上链接中的占位符请替换为你的实际账户与链接。
