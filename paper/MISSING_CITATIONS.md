# Citation verification log

No `VERIFY_` placeholder keys remain in the manuscript. All 23 entries were checked during
drafting against primary listings found by web search (PMLR, ICLR proceedings, TMLR/mlanthology,
ACL Anthology, Nature/PMC, IEEE, ACM DOI, arXiv). Direct fetches of aclanthology.org, arxiv.org and
aaai.org were blocked by the drafting sandbox's network policy, so the BibTeX was assembled by hand
from those listings rather than downloaded.

Items a human should still double-check before submission:

| Key | What to check |
|---|---|
| `wolf2020transformers` | Full author list typed from memory of the Anthology entry; search confirmed first authors, last author (Rush), pages 38–45 |
| `dathathri2024scalable` | Author list truncated to "Dathathri, S.; et al." on purpose; expand from the Nature page |
| `bhatt2023cyberseceval` | Author list truncated ("Bhatt et al."); expand from arXiv 2312.04724 |
| `he2023sven` | Page range in CCS'23 proceedings not found; DOI given |
| `mao2025unbiased` | We cite it for reporting perplexity variance across keys; confirm the claim against the paper's tables |
| `lee2024sweet` | We state that plain KGW reduces functional pass rates on code benchmarks; confirm wording against the paper |
| `peng2025cweval` | Workshop proceedings venue string (LLM4Code @ ICSE 2025) |
| `suresh2024robust` | arXiv title differs slightly from the ICLR'24 Tiny Paper title |

Not cited (by design): WeSCE, DualGauge and "approval-to-execution consistency" were requested for an
unrelated IIDE paper; they are not relevant to KGW key auditing and were not added.
