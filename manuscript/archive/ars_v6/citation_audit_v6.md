# Citation Audit Report（执笔第 4 步 v6；ARS citation_compliance_agent 的格式）

作业记录，不是交付物。交付时随 ars/ 移入 manuscript/archive/ars_v6/。各数取自 make_ledger.py 的输出（check_v6.md 的「参考文献」）与 references_v6.md 第 3、6、8、9 节。本版文献的增删为 0；Introduction 第 3 段换成指示的原文后，ax2023 由 v5 的 39 号移到 26 号，原 26–38 号顺延一位（number_refs.py 按阅读顺序重编，本文、表注、图注与补充材料同时更新）。

### Summary

| Metric | Count |
|--------|-------|
| Total in-text citations | 212 个引用（本文 61 个上标 run；表 24、图注 1、补充材料 126） |
| Total reference list entries | 77（与 v5 相同的 77 条，条目文本逐字相同，只是 26–39 号的顺序变了） |
| Orphan in-text citations (no ref) | 0 |
| Orphan references (no in-text) | 0 |
| Format errors (auto-corrected) | 0（条目由 PubMed 与 Crossref 记录机械生成，make_ledger 逐条比对条目文本） |
| Format errors (flagged for review) | 0 |
| Missing DOIs | 0（无 DOI 的 16 篇都是文件与网页，各有到源页面的核对记录） |
| Self-citation ratio | 0% |
| Sources from last 5 years | 66%（2022–2026，50 / 76；1 篇网页无日期） |

照合件数（规约第 1.3 节）：DOI 61 篇在 doi.org 实测 30x 跳转并与 Crossref 比对（写法差异 11 篇，逐条确认为同一文献）；原著对照 135 条段落全部找到（本文 98 处〔句子 × 文献〕、图注与补充材料的散文 22 处）。本版新加的对照：Introduction 第 3 段 4 句的 20 处（原有引用的句号变了，逐条重配）、Discussion 第 3 至 7 段的 16 处，其中 CC 补写的两句（D.4 第 2 句、D.6 第 3 句）的原句见 references_v6.md 第 9 节。

### Corrections Made

| # | Location | Error | Correction |
|---|----------|-------|-----------|
| — | — | 本版没有订正 | — |

### Items Flagged for Review

| # | Location | Issue | Suggested Action |
|---|----------|-------|-----------------|
| 1 | Limitations 第 5 句 | 「a French cohort treated largely before immunotherapy and antibody–drug conjugates were available」是关于 ESME 队列的事实，句中没有引文。grinda2023 的摘要写「All ESME patients diagnosed between 2008 and 2020」，内容相符 | 由用户决定是否在句末引 grinda2023（已在文献表中，不增文献） |
| 2 | Discussion 第 6 段第 2 句 | 「valued an effect on disease-free survival over the long term」：chan2026 的基准时间范围为 5 年，情景为 10 年 | 报告；原文照插 |
| 3 | Introduction 第 3 段第 4 句 | 一句引 12 篇（KEYNOTE-522 方案的 4 篇、日本的 7 篇、C2H 一览 1 篇；ARS 的阈值 5 篇） | 报告；指示的原文 |
| 4 | Discussion 第 1、2 段，Implications，Limitations | 段内无文献（ARS：方法记述或本研究自身的分析可无引用）；所述内容都来自本研究的表与图 | 报告 |
| 5 | kn522final2026、esmo2023、jbcs55、tropion2025 | v5 起的 N12、N13 与 jbcs55（原著未见或待确认） | 维持待决 |
| 6 | 超过 10 年的 8 篇 | dent2007、liedtke2008、courneya2007、vanwaart2015、courneya2014、guyot2012、cortes2011、miller2007 | 报告（原始试验报告与方法文献） |

### Corrected Reference List

见 manuscript_v6.docx 的 References（77 条）与 references_v6.md 第 3 节。
