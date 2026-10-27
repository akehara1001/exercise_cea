# Citation Audit Report（执笔第 3 步 v5；ARS citation_compliance_agent 的格式）

作业记录，不是交付物。交付时随 ars/ 移入 manuscript/archive/。各数取自 make_ledger.py 的输出（check_v5.md 的 REFERENCES）与 references_v5.md 第 3、6、8 节。

### Summary

| Metric | Count |
|--------|-------|
| Total in-text citations | 202 个引用（本文 51 个上标 run；表、图注与补充材料 151 个） |
| Total reference list entries | 77 |
| Orphan in-text citations (no ref) | 0 |
| Orphan references (no in-text) | 0 |
| Format errors (auto-corrected) | 0（条目由 PubMed 与 Crossref 记录机械生成，make_ledger 逐条比对条目文本） |
| Format errors (flagged for review) | 0 |
| Missing DOIs | 0（无 DOI 的 16 篇都是文件与网页，各有到源页面的核对记录） |
| Self-citation ratio | 0% |
| Sources from last 5 years | 66%（2022–2026，50 / 76；1 篇网页无日期） |

照合件数（规约第 1.3 节）：DOI 61 篇全部在 doi.org 实测 30x 跳转并与 Crossref 比对（写法差异 11 篇，逐条确认为同一文献）；原著对照 119 条段落全部找到（ok 109、corroborated 2、report 4、provided 4）。

### Corrections Made

| # | Location | Error | Correction |
|---|----------|-------|-----------|
| 1 | Methods, Study background 第 3 段第 1 句 | 截点列表漏了 23 March 2023（该截点的值用于选分布族，Supplementary Methods S1 引 esmo2023） | 加入该截点并引 esmo2023 |
| 2 | Methods, Variables 第 3 段第 2 句 | 购买力平价换算句引了加拿大银行的汇率（汇率只用于上限） | 只引世界银行；汇率的引用留在 Table 1 与 S2 的出处栏 |
| 3 | Methods, Statistical analysis 第 6 段第 2 句 | 「utility value sets from … Australia」：PBAC 的公开摘要未写价值集 | 改为「utility values scored with the United States and United Kingdom value sets and those of the Australian reimbursement submission」 |
| 4 | Supplementary Table S7、S9、S10 的脚注 | 输入表的编号仍为 v4 的 S1（v5 为 S2） | 改为 S2，并新增检查（references_to_input_table_wrong_number） |
| 5 | 会议摘要 ohtera2018、esmo2023 | DOI 只取了 Crossref 记录，没有 doi.org 的实测记录 | 实测（302），记录于 refs/doi_head_abstracts.json；make_ledger 改为对这类条目也要求实测 |

### Items Flagged for Review

| # | Location | Issue | Suggested Action |
|---|----------|-------|-----------------|
| 1 | kn522final2026 | 按 pCR 分层的 7 年 EFS 不在摘要中，读自会议报道 | 尾崎先生确认原始出处（docs/model_spec.md 第 87 行的同类事项） |
| 2 | esmo2023 | 摘要原文未取得（HTTP 403），数值读自 OncLive | 同上 |
| 3 | jbcs55 | 会员限定资料，数值由尾崎先生提供，原表未见 | 原表到后核对 |
| 4 | tropion2025 | 参数表未写日期，选了 2025-10-19 的新闻稿 | 尾崎先生确认 |
| 5 | Supplementary Table S10 | 行名「Utility value set: Australia」：PBAC 的公开摘要未写价值集 | 待决（行名的改法由用户定） |
| 6 | I.3 第 6 句 | 一句引 7 篇（ARS 的阈值 5 篇）：列举检出的全部日本分析 | 保留（内容所需），报告 |
| 7 | 超过 10 年的 8 篇 | dent2007、liedtke2008、courneya2007、vanwaart2015、courneya2014、guyot2012、cortes2011、miller2007 | 报告（原始试验报告与方法文献） |

### Corrected Reference List

见 manuscript_v5.docx 的 References（77 条）与 references_v5.md 第 3 节。
