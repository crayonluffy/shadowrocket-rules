# Shadowrocket Rules

自動合併上游規則 + 個人補漏的 Shadowrocket 規則集。

每天 UTC 00:00（台港時間早上 8 點 / 泰國時間早上 7 點）自動從上游抓最新規則，合併個人補漏清單，產生最終的 `.list` 檔案。

---

## 🚀 客戶端使用方式（給拿到節點的人）

### 步驟 1：在 Shadowrocket 加入節點

把站長給你的 `ss://` 連結用 LINE / Telegram / Mail 傳到手機，**點擊連結**，Shadowrocket 會自動匯入節點，按「儲存」即可。

或者掃描 QR Code。

### 步驟 2：訂閱規則配置

複製此 URL：

```
https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/configs/ai-only.conf
```

打開 Shadowrocket → 底部「**配置**」標籤 → 右上角「**+**」→「**訂閱配置**」→ 貼上 URL → 命名為 `AI-Only` → 儲存。

### 步驟 3：套用配置

「配置」標籤頁 → 點選 `AI-Only` → 左側出現勾號表示生效。

### 步驟 4：連線

回到「首頁」標籤頁 → 點選你的節點 → 開啟最上方連線開關。

---

## ✅ 不用改任何東西

配置內使用 Shadowrocket 內建關鍵字 `PROXY`，**自動指向你當前選中的節點**。

- 不管你的節點叫 `TokyoGCP-alice`、`TokyoGCP-bob` 還是 `MyVPN`，**都會正常運作**
- 不用編輯 conf 檔
- 不用替換任何 placeholder

---

## 📂 倉庫目錄結構

```
shadowrocket-rules/
├── .github/workflows/
│   └── update-rules.yml          自動化腳本（不用動）
├── sources/
│   └── ai.txt                    上游來源清單（每行一個 URL）
├── extras/
│   └── ai-extras.list            個人補漏清單（手動維護）
├── configs/
│   └── ai-only.conf              即用配置（客戶端訂閱這個）
├── ai.list                       自動產生的合併規則 ← 配置內部引用
└── README.md
```

---

## ✏️ 維護者操作（給站長看）

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

### 手動觸發更新

到 GitHub repo → Actions → "Update Shadowrocket Rules" → "Run workflow"。

---

## 🔧 客戶端除錯建議

### 規則沒生效？

- Shadowrocket → 「配置」→ 下拉刷新（同步最新規則檔）
- 確認左邊有勾號（表示套用中）
- 重啟 VPN 開關

### 想知道某網站走了 VPN 還是直連？

- Shadowrocket → 底部「**資料**」→「**連線**」
- 看每筆連線右側標示：
  - `PROXY` = 走 VPN ✅
  - `DIRECT` = 直連 ✅
  - `REJECT` = 被擋

### Claude / OpenAI 用 Google 帳號登入卡住？

可能是某個 `googleapis` 子域沒在規則內。把該域名截圖傳給站長，加進 `extras/ai-extras.list` 即可。

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
