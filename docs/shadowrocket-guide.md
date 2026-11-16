# Shadowrocket 使用指南 / Shadowrocket Guide

裝好之後的日常操作：怎麼看流量走哪裡、怎麼更新規則、怎麼保持連線。第一次安裝請先看 [README 的快速開始](../README.md)。
> Everyday use after the first setup: see where traffic goes, update the rules, stay connected. For the first install, start with the [Quick Start in the README](../README.md).

選項名稱依 App 語言可能略有不同。
> Labels may differ slightly with the app language.

---

## 四個分頁 / The four tabs

| 分頁 / Tab | 用途 / What it is for |
|---|---|
| 首頁 / Home | 節點清單、連線開關、全局路由 / Node list, connection switch, global routing |
| 配置 / Config | 規則配置：訂閱、切換、更新 / Rule configs: subscribe, switch, update |
| 資料 / Data | 連線記錄：每個請求走了哪個策略 / Logs: which policy each request used |
| 設定 / Settings | App 設定：Tailscale、UDP、自動更新、按需求連線 / App settings: Tailscale, UDP, auto update, on demand |

---

## 全局路由：一定要選「配置」/ Global routing: keep it on "Config"

「首頁」的「**全局路由 / Global Routing**」決定規則有沒有作用：
> **Global Routing** on the Home tab decides whether the rules apply:

| 模式 / Mode | 效果 / Effect |
|---|---|
| **配置 / Config** | 依規則分流：AI 走節點，其他直連。**本倉庫的配置要用這個。** / Split by the rules: AI through the node, the rest direct. **Use this with the configs of this repo.** |
| 代理 / Proxy | 全部流量都走節點（規則不看）/ Everything through the node (rules ignored) |
| 直連 / Direct | 全部不走節點（AI 會用真實 IP）/ Nothing through the node (AI sees your real IP) |
| 場景 / Scene | 依 Wi-Fi / 行動網路自動切換上面的模式 / Switches between the modes by Wi-Fi / cellular |

AI 打不開、或其他網站變慢，第一件事先看這裡是不是「配置」。
> If AI won't open, or other sites got slow, first check that this says **Config**.

---

## 這個倉庫的配置 / The configs in this repo

一次只啟用一個（左邊有 ✓ 的那個）。
> Only one is active at a time (the one with the ✓).

| 配置 / Config | AI | 廣告 / Ads | Tailscale | 需要節點 / Needs a node |
|---|---|---|---|---|
| [`ai-only.conf`](../configs/ai-only.conf) | 走節點 / node | – | – | 是 / Yes |
| [`adblock.conf`](../configs/adblock.conf) | – | 擋 / blocked | – | 否 / No |
| [`ai-tailscale.conf`](../configs/ai-tailscale.conf) | 走節點 / node | – | 內建 Tailscale / built-in | 是 / Yes |
| [`ai-tailnet-via-node.conf`](../configs/ai-tailnet-via-node.conf) | 走節點 / node | – | 經節點 / through the node | 是，且節點在 tailnet 內 / Yes, and the node is in the tailnet |
| [`asia-direct.conf`](../configs/asia-direct.conf) | 走節點 / node | – | 經節點 / through the node | 是 / Yes |

前四個配置：AI 以外的流量全部直連。`asia-direct.conf` 不同：東亞、東南亞直連，**其他地區也走節點**，見 [亞洲直連教學](asia-direct.md)。
> With the first four configs everything except AI goes direct. `asia-direct.conf` differs: East and Southeast Asia go direct and **the rest of the world also uses the node**, see the [Asia-direct tutorial](asia-direct.md).

AI 配置想同時擋廣告：用「包含配置」把 `adblock.conf` 合併進來，見 [README](../README.md)。Tailscale 的設定見 [Tailscale 教學](tailscale.md)。
> To add ad-blocking to an AI config, merge `adblock.conf` with *Include Configuration*, see the [README](../README.md). For Tailscale see the [Tailscale tutorial](tailscale.md).

---

## 規則怎麼判斷 / How rules are matched

- **由上往下**，第一條符合的規則就生效，後面的不再看。
  > **Top to bottom**; the first rule that matches wins and the rest are skipped.
- 域名類規則（`DOMAIN`、`DOMAIN-SUFFIX`…）先於 IP 類規則（`IP-CIDR`、`GEOIP`）。
  > Domain rules (`DOMAIN`, `DOMAIN-SUFFIX`…) are checked before IP rules (`IP-CIDR`, `GEOIP`).
- 都不符合的，交給最後一行 `FINAL`（本倉庫是 `DIRECT`）。
  > Whatever matches nothing goes to the last line, `FINAL` (`DIRECT` in this repo).

每條規則最後一欄是**策略**：
> The last field of each rule is the **policy**:

| 策略 / Policy | 意思 / Meaning |
|---|---|
| `PROXY` | 走你在首頁選中的節點 / Through the node selected on Home |
| `DIRECT` | 直連，不經節點 / Direct, no node |
| `REJECT` | 擋掉 / Blocked |
| `TAILSCALE` | 走內建 Tailscale（2.2.89 起）/ Through the built-in Tailscale (2.2.89 or newer) |

---

## 看某個網站走哪條路 / See which route a site takes

**看記錄 / From the logs**

1. 「資料 / Data」→「代理 / Proxy」→ 打開「**啟用日誌記錄 / Enable Logging**」。
   > **Data** → **Proxy** → switch **Enable Logging** on.
2. 打開那個網站或 App，再回到這一頁。
   > Open the site or app, then come back to this page.
3. 每筆記錄會顯示網址和命中的策略（`PROXY` / `DIRECT` / `REJECT` / `TAILSCALE`）。
   > Each entry shows the address and the policy that matched (`PROXY` / `DIRECT` / `REJECT` / `TAILSCALE`).

**不用真的連線 / Without connecting**

「配置 / Config」→「**測試規則 / Test Rule**」→ 輸入網址，會顯示命中的規則與策略。
> **Config** → **Test Rule** → enter an address; it shows the matching rule and policy.

---

## 更新規則 / Update the rules

規則每天自動重建。手機上有三種更新方式：
> The rules are rebuilt every day. Three ways to update on the phone:

- **手動**：「配置」分頁下拉刷新，或點配置 →「更新配置 / Update」。
  > **By hand**: pull down on the Config tab, or tap the config → **Update**.
- **自動**：「設定」→「自動更新 / Auto Update」→「配置 / Config」→ 打開「自動後台更新」，間隔選 1 天。
  > **Automatic**: **Settings** → **Auto Update** → **Config** → switch background update on, interval 1 day.
- 自動更新需要 iOS 的「**設定 → 一般 → 背景 App 重新整理**」對 Shadowrocket 是開的；從多工畫面滑掉 App 後，背景更新不會跑。
  > Auto update needs iOS **Settings → General → Background App Refresh** on for Shadowrocket; after you swipe the app away, background updates do not run.

> [!WARNING]
> 更新訂閱的配置會**蓋掉你在手機上對它做的修改**。想長期加規則，請管理員加進倉庫，或用自己的本機配置。
> Updating a subscribed config **overwrites the edits you made to it on the phone**. For a lasting rule, ask the admin to add it to the repo, or use a local config of your own.

---

## 自己臨時加一條規則 / Add a rule yourself (temporary)

- 從記錄加：「資料 → 代理」點一筆記錄 → 右上角「**•••**」→ 選類型加成規則。
  > From a log entry: **Data → Proxy**, tap an entry → **•••** (top-right) → add it as a rule.
- 手動加：配置右邊的「**ⓘ**」→「規則 / Rules」→ 右上角「**+**」→ 選類型（多半是 `DOMAIN-SUFFIX`）和策略（`PROXY`）。
  > By hand: the **ⓘ** next to the config → **Rules** → **+** (top-right) → choose the type (usually `DOMAIN-SUFFIX`) and the policy (`PROXY`).

下次更新配置時會消失（見上一節）。
> It disappears at the next config update (see above).

---

## 保持連線 / Stay connected

「設定」→「**按需求連線 / On Demand**」→ 打開「**始終開啟 / Always On**」：意外斷線或重開機後會自動重新連上。
> **Settings** → **On Demand** → switch **Always On** on: it reconnects by itself after a drop or a restart.

---

## 其他設定 / Other settings

| 設定 / Setting | 位置 / Where | 建議 / Suggested |
|---|---|---|
| UDP 轉發 / UDP forwarding | 設定 → UDP → 啟用轉發 | 語音通話、遠端桌面類 App 不通時打開 / Switch on when voice or remote-desktop apps fail |
| 代理類型 / Proxy type | 設定 → 代理 → 代理類型 | 保持預設 / Leave the default |
| Tailscale | 設定 → Tailscale | 見 [Tailscale 教學](tailscale.md) / See the [Tailscale tutorial](tailscale.md) |
| 節點測速 / Node test | 首頁 → 連通性測試 | 顯示延遲；逾時代表節點連不上 / Shows latency; a timeout means the node is unreachable |

---

## 參考資料 / Sources

- [Shadowrocket 使用手冊（社群維護）](https://github.com/LOWERTOP/Shadowrocket)：本頁的選項名稱與行為依據此手冊整理，未逐項在 iPhone 上實測。
  > The option names and behaviour on this page follow this community handbook; they were not each checked on an iPhone.
