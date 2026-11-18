# Notation (single source of truth; macros in `notes/macros.tex`)

| Symbol | Macro | Meaning | Value in this study |
|---|---|---|---|
| $M$ | – | causal code LM | Qwen2.5-Coder-7B-Instruct |
| $\mathcal{V}$ | `\V` | vocabulary | model tokenizer |
| $\ell_t,\tilde\ell_t$ | – | logits before / after KGW bias at step $t$ | – |
| $\kappa$ | – | watermark key (hashing key) | SHA-256-derived signed 63-bit |
| $\varnothing$ | `\Base` | unwatermarked arm | – |
| $\mathcal{K}, \mathcal{K}_n$ | `\K` | key space; sampled set of $n$ keys | $n=10$ (pilot), 100 (planned) |
| $\gamma$ | – | greenlist ratio | 0.25 (primary); 0.50 calibration |
| $\delta$ | – | logit bias | 2.0 (primary); 1, 3 calibration |
| $h$ | – | context width | 1 |
| $G_t$ | `\G` | green list at step $t$ | $\lfloor\gamma|\mathcal{V}|\rfloor$ tokens |
| $T$ | – | number of scored tokens | per output |
| $g$ | – | number of green scored tokens | per output |
| $z_\kappa(y)$ | – | KGW detector z-score, Eq. (2) | – |
| $z^\star$ | – | detection threshold | 4 |
| $p$ | – | per-token green probability under key $\kappa$ (Assumption 1) | – |
| $T_{\min}(p)$ | – | min. length for $\mathbb{E}[z]\ge z^\star$, Eq. (4) | – |
| $T_{\mathrm{temp}}$ | – | sampling temperature | 0.7 (top-$p$ 0.95) |
| $\tau\in\mathcal{T}$ | `\T` | task | 24 pilot / 240 primary |
| $s\in\mathcal{S}$ | `\Sd` | sampling seed | {17, 29, 43} |
| $F, S, Y$ | `\Fn, \Sec, \Y` | functional, security ($\{0,1,\bot\}$), secure-and-functional | – |
| $\mu_\kappa$ | – | task/seed-averaged rate of $Y$ for arm $\kappa$ | – |
| $\Delta_k$ | – | per-key effect $\mu_{\kappa_k}-\mu_\varnothing$ | – |
| $\Delta$ | `\ATE` | average KGW effect | – |
| $\sigma^2_{\mathcal{K}}$ | – | between-key variance of $\mu_\kappa$ | – |
| $\bar v$ | – | mean within-key sampling variance | – |
