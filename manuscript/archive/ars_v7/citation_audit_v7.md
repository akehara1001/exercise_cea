# Citation Audit Report（v7；ARS citation_compliance_agent 的格式）

作业记录，不是交付物。交付时随 ars/ 移入 manuscript/archive/ars_v7/。各数取自 make_ledger.py 的输出（check_v7.md 的「参考文献」）与 references_v7.md 第 3、6、8 节。本版文献的增删为 0，文献号也与 v6 完全相同（新的三节只引用已在 Introduction 或 Methods 中出现的文献；tables、figures 的原始比较 0 差）。引用的位置有变：v6 Discussion 的 16 处（句子 × 文献）随整节替换删去，v7 的三节有 23 处。

### Summary

| Metric | Count |
|--------|-------|
| Total in-text citations | 214 个引用（本文 63 个上标 run；表 24、图注 1、补充材料 126） |
| Total reference list entries | 77（与 v6 相同，条目文本与番号逐字相同） |
| Orphan in-text citations (no ref) | 0 |
| Orphan references (no in-text) | 0 |
| Format errors (auto-corrected) | 0（条目由 PubMed 与 Crossref 记录机械生成，make_ledger 逐条比对条目文本） |
| Format errors (flagged for review) | 0 |
| Missing DOIs | 0（无 DOI 的 16 篇都是文件与网页，各有到源页面的核对记录） |
| Self-citation ratio | 0% |
| Sources from last 5 years | 66%（2022–2026，50 / 76；1 篇网页无日期） |

照合件数（规约第 1.3 节）：DOI 61 篇在 doi.org 实测 30x 跳转并与 Crossref 比对（写法差异 11 篇，逐条确认为同一文献）；原著对照 142 条段落全部找到（本文 105 处〔句子 × 文献〕、图注与补充材料的散文 22 处）。本版新加的对照为三节的 23 处：D.3 第 2 句、D.4 第 3、5 句、D.5 第 1、3 句、D.6 第 1–3 句、D.7 第 2 句、Implications 第 1 段第 1 句、Limitations 第 2 段第 1 句。

### Corrections Made

| # | Location | Error | Correction |
|---|----------|-------|-----------|
| — | — | 本版没有订正 | — |

### Items Flagged for Review

| # | Location | Issue | Suggested Action |
|---|----------|-------|-----------------|
| 1 | Limitations 第 2 段第 1 句 | grinda2023 的摘要写诊断期间（2008 至 2020 年）；「largely before immunotherapy and antibody–drug conjugates」是由期间推出的，摘要中没有写 | 报告；原文照插 |
| 2 | Discussion 第 6 段第 1 句 | 一句引 6 篇（ARS 的阈值 5 篇）：运动经济评价的 3 篇综述与结论不一的 3 篇 | 报告；指示的原文 |
| 3 | Introduction 第 3 段第 4 句 | 一句引 12 篇（v6 起） | 报告；指示的原文 |
| 4 | Discussion 第 1、2 段，Implications 第 2 段，Limitations 第 1 段 | 段内无文献（内容来自本研究的表与图） | 报告 |
| 5 | Discussion 第 4 段第 3 句 | 「Trials of exercise in cancer have reported much smaller effects」：courneya2025（HR 0.72）与 courneya2014（HR 0.68，一项试验的探索性追踪） | 报告；与 Table 3 的 HR 0.425 相比均为较小的效应，内容相符 |
| 6 | kn522final2026、esmo2023、jbcs55、tropion2025 | N12、N13 与 jbcs55（原著未见或待确认） | 维持待决 |
| 7 | 超过 10 年的 8 篇 | dent2007、liedtke2008、courneya2007、vanwaart2015、courneya2014、guyot2012、cortes2011、miller2007 | 报告（原始试验报告与方法文献） |

### Corrected Reference List

见 manuscript_v7.docx 的 References（77 条）与 references_v7.md 第 3 节。
