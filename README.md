# Shadowrocket Rules

自動合併上游規則 + 個人補漏的 Shadowrocket 規則集。

每天 UTC 00:00（台港時間早上 8 點）自動從上游抓最新規則，合併個人補漏清單，產生最終的 `.list` 檔案。

> Auto-merged Shadowrocket rule sets (upstream rules + personal patches), rebuilt automatically every day.

---

## 🚀 快速開始 / Quick Start

給拿到節點的人：四步就能上線。
> Just got a node? You're four steps away from going online.

| # | 做什麼 / What | 在哪裡 / Where |
|---|---|---|
| 1 | 安裝 Shadowrocket / Install Shadowrocket | App Store（iOS，付費 / paid）|
| 2 | 點 `ss://` 連結匯入節點 / Tap the `ss://` link to import the node | 連結自動開啟 App / The link opens the app |
| 3 | 訂閱規則配置 / Subscribe to the rule config | 「配置」標籤 / **Config** tab |
| 4 | 選節點並開啟連線 / Pick the node, toggle on | 「首頁」標籤 / **Home** tab |

詳細步驟見下方。
> Full walkthrough below.

---

## 📱 開始之前 / Before You Start

Shadowrocket 是 **iOS 專用** 的付費 App（約 US$2.99），請先到 App Store 搜尋並安裝。
> Shadowrocket is an **iOS-only** paid app (about US$2.99). Search for it in the App Store and install it first.

> [!NOTE]
> Shadowrocket 在中國區 App Store 已下架。若搜尋不到，需要用 **非中國區的 Apple ID**（例如美區、台灣區）才能下載。
> Shadowrocket is not on the China App Store. If you can't find it, use a **non-China Apple ID** (e.g. US or Taiwan) to download it.

---

## 🧭 完整步驟 / Step-by-Step

### 步驟 1 · Step 1：加入節點 / Add your node

管理員會給你一條像這樣的連結：`ss://...@vpn.example.com:port#VPN-user`。用 LINE / Telegram / Mail 把它傳到手機，然後直接**點一下連結**。Shadowrocket 會自動打開並帶出節點資料，按右上角「**儲存 / Save**」即可。也可以改用掃描 QR Code。

> The admin gives you a link that looks like `ss://...@vpn.example.com:port#VPN-user`. Send it to your phone (LINE / Telegram / Mail) and simply **tap it** — Shadowrocket opens with the node already filled in. Tap **Save** (top-right). Scanning a QR code works too.

> [!WARNING]
> 這條 `ss://` 連結等於你的帳號密碼，**請勿公開或轉傳**給別人。
> Treat this `ss://` link like a password — **never share or forward it** publicly.

### 步驟 2 · Step 2：訂閱規則配置 / Subscribe to the rule config

複製這條 URL / Copy this URL:

```
https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/configs/ai-only.conf
```

打開 Shadowrocket → 底部「**配置 / Config**」標籤 → 右上角「**+**」→「**訂閱配置 / Add Subscription**」→ 貼上 URL → 命名為 `AI-Only` → 按「**儲存 / Save**」。

> Open Shadowrocket → bottom **Config** tab → **+** (top-right) → **Add Subscription** → paste the URL → name it `AI-Only` → tap **Save**.

### 步驟 3 · Step 3：套用配置 / Apply the config

在「**配置 / Config**」標籤頁點一下 `AI-Only`，左側出現**勾號 ✓** 就表示生效。

> In the **Config** tab, tap `AI-Only`. A **checkmark ✓** on the left means it's now active.

### 步驟 4 · Step 4：連線 / Connect

回到「**首頁 / Home**」標籤頁 → 點選你的節點 → 打開最上方的**連線開關**。第一次開啟時 iOS 會要求允許新增 VPN 設定，按「**允許 / Allow**」。

> Back on the **Home** tab → tap your node → flip the **connection switch** at the top. The first time, iOS asks permission to add a VPN configuration — tap **Allow**.

🎉 完成！打開 Claude / ChatGPT 試試看。
> 🎉 Done! Open Claude / ChatGPT and give it a try.

---

## ✅ 不用改任何東西 / Nothing to Configure

配置內使用 Shadowrocket 內建關鍵字 `PROXY`，**自動指向你當前選中的節點**。
> The config uses Shadowrocket's built-in `PROXY` keyword, which **always points to whichever node you've selected**.

- 不管你的節點叫 `TokyoGCP-alice`、`TokyoGCP-bob` 還是 `MyVPN`，**都會正常運作** / Works no matter what your node is named
- 不用編輯 conf 檔 / No need to edit the conf file
- 不用替換任何 placeholder / Nothing to fill in or replace
- 順便**攔截廣告與追蹤域名**（REJECT），無痛省流量 / Also **blocks ad & tracker domains** (REJECT) — bonus, no setup

---

## 🔧 常見問題 / Troubleshooting FAQ

### 規則沒生效？ / Rules not taking effect?

- Shadowrocket → 「配置 / Config」→ **下拉刷新**（同步最新規則檔）/ pull down to refresh the latest rules
- 確認該配置左邊有**勾號 ✓**（表示套用中）/ make sure the config shows a ✓
- 把最上方**連線開關**關掉再開 / toggle the connection switch off and on

### 想知道某網站走 VPN 還是直連？ / Which route is a site taking?

Shadowrocket → 底部「**資料 / Logs**」→「**連線 / Connections**」，看每筆連線右側的標示：
> Shadowrocket → bottom **Logs** → **Connections**, then read the label on the right of each entry:

- `PROXY` = 走 VPN / via VPN ✅
- `DIRECT` = 直連 / direct ✅
- `REJECT` = 被擋 / blocked

### Claude / OpenAI 用 Google 帳號登入卡住？ / Google sign-in stuck?

可能是某個 `googleapis` 子域沒在規則內。把該域名截圖傳給管理員，加進 `extras/ai-extras.list` 即可。
> A `googleapis` subdomain may be missing from the rules. Screenshot the domain and send it to the admin to add it into `extras/ai-extras.list`.

### App Store 找不到 Shadowrocket？ / Can't find Shadowrocket in the App Store?

中國區已下架，需改用非中國區的 Apple ID。
> It's been removed from the China App Store — switch to a non-China Apple ID.

### 某個網站 / App 打不開，是不是被廣告規則誤殺？ / A site or app won't load — blocked by the ad rules?

配置會攔截廣告與追蹤域名，偶爾可能誤殺正常網站。先到「**資料 / Logs → 連線 / Connections**」確認該域名是不是 `REJECT`，把域名截圖傳給管理員放行即可。
> The config blocks ad/tracker domains and occasionally catches a legit site. Check **Logs → Connections** to see if the domain shows `REJECT`, then screenshot it to the admin to allow-list.

---

## 📂 倉庫目錄結構

```
shadowrocket-rules/
├── .github/workflows/
│   └── update-rules.yml          自動化腳本（不用動）
├── sources/
│   ├── ai.txt                    AI 服務上游來源（每行一個 URL）
│   └── adblock.txt               廣告攔截上游來源
├── extras/
│   ├── ai-extras.list            AI 個人補漏清單（手動維護）
│   └── adblock-extras.list       廣告攔截個人補漏清單
├── configs/
│   └── ai-only.conf              即用配置（客戶端訂閱這個）
├── ai.list                       自動產生：AI 規則 ← 配置內部引用 (PROXY)
├── adblock.list                  自動產生：廣告規則 ← 配置內部引用 (REJECT)
└── README.md
```

---

## ✏️ 維護者操作（給管理員看）

### 想加新 AI 網站？

編輯 `extras/ai-extras.list`，加一行例如：

```
DOMAIN-SUFFIX,newsite.com
```

`git push` 後 GitHub Actions 自動觸發，幾分鐘內 `ai.list` 更新。
客戶端 Shadowrocket 下拉刷新配置即可生效。

### 想加新上游來源？

編輯 `sources/ai.txt`，加一行 URL。

### 想新增另一類規則（例如 work.list）？

1. 建立 `sources/work.txt`，列上游 URL
2. （選擇性）建立 `extras/work-extras.list`，列個人補漏
3. push → Actions 自動產生 `work.list`
4. 在 `configs/ai-only.conf` 加一行 `RULE-SET,...../work.list,PROXY`

**命名規則**：`sources/X.txt` 對應產生 `X.list`，補漏檔名固定為 `X-extras.list`

### 廣告攔截：誤殺放行 / 加擋 / 換清單

- **某網站被誤殺想放行**：到 `configs/ai-only.conf` 的「Layer 3 緊急補丁區」加一行 `DOMAIN-SUFFIX,網站.com,DIRECT`（在 adblock RULE-SET 之上，先匹配先生效），push 後客戶端下拉刷新即可。
- **想多擋某個廣告域名**：寫進 `extras/adblock-extras.list`，會自動合併進 `adblock.list`（策略 REJECT）。
- **覺得擋得不夠多**：把 `sources/adblock.txt` 的 `AdvertisingLite` 換成完整版 `Advertising`（域名更多，但誤殺機率較高），或多加一行 `Privacy` / `Hijacking` 清單。

### 手動觸發更新

到 GitHub repo → Actions → "Update Shadowrocket Rules" → "Run workflow"。

---

## 📚 規則類型參考

| 類型 | 範例 | 說明 |
|---|---|---|
| `DOMAIN` | `DOMAIN,gemini.google.com` | 完全相等 |
| `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX,openai.com` | 結尾相符（含子域名） |
| `DOMAIN-KEYWORD` | `DOMAIN-KEYWORD,openai` | 包含關鍵字 |
| `IP-CIDR` | `IP-CIDR,1.2.3.0/24` | IP 範圍 |
| `USER-AGENT` | `USER-AGENT,Claude*` | 依 App 識別 |

---

## ⚠️ 注意事項

- 規則檔（`.list`）內**不要**寫 `,PROXY` 或 `,DIRECT` 等策略，策略由引用它的 `.conf` 決定
- `.conf` 內的規則匹配是「由上往下」，第一個匹配的就生效
- 修改 `sources/` 或 `extras/` 後 push 才會觸發更新
- 此 repo 為公開（Public），規則內容不含敏感資訊
- **節點密碼絕對不要 push 上來**

---

## 🔗 上游來源致謝

- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) - 中文圈最完整的 iOS 分流規則
- [xiaolai/anthropic-claude-surge-rules-set](https://github.com/xiaolai/anthropic-claude-surge-rules-set) - Claude 深度規則（含 IP 段）
- [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) - 英文社群維護的 OpenAI 域名清單
