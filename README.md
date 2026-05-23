# Shadowrocket Rules

自動合併上游規則 + 個人補漏的 Shadowrocket 規則集。

每天 UTC 00:00（台港時間早上 8 點）自動從上游抓最新規則，合併個人補漏清單，產生最終的 `.list` 檔案。

---

## 🚀 使用方式

### 1. 訂閱規則（在 Shadowrocket 配置檔的 `[Rule]` 區段）

```ini
RULE-SET,https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/shadowrocket-rules/main/ai.list,Proxy
```

### 2. 完整配置範本

見 `configs/ai-only.conf`，把裡面的 `YOUR_GITHUB_USERNAME` 和 `TokyoGCP-yourname` 換成自己的即可。

---

## 📂 目錄結構

```
shadowrocket-rules/
├── .github/workflows/
│   └── update-rules.yml          自動化腳本(不用動)
├── sources/
│   └── ai.txt                    上游來源清單(每行一個 URL)
├── extras/
│   └── ai-extras.list            個人補漏清單(手動維護)
├── configs/
│   └── ai-only.conf              即用配置範本
├── ai.list                       自動產生的最終清單 ← 客戶端訂閱這個
└── README.md
```

---

## ✏️ 想做什麼？

### 想加新規則（個人補漏）

編輯 `extras/ai-extras.list`，加上一行例如：

```
DOMAIN-SUFFIX,newsite.com
```

`git push` 後，GitHub Actions 會自動觸發，幾分鐘內 `ai.list` 就會更新。

### 想加新上游來源

編輯 `sources/ai.txt`，加上一行 URL。

### 想新增另一類規則（例如 work.list）

1. 建立 `sources/work.txt`，列上游 URL
2. （選擇性）建立 `extras/work-extras.list`，列個人補漏
3. push → Actions 會自動產生 `work.list`
4. 在客戶端 `.conf` 加上 `RULE-SET,...../work.list,Proxy`

**命名規則**：`sources/X.txt` 對應產生 `X.list`，補漏檔名固定為 `X-extras.list`

### 手動觸發更新

到 GitHub repo → Actions → "Update Shadowrocket Rules" → "Run workflow"。

---

## 🔧 維護建議

- **發現網站打不開？** 在 Shadowrocket「資料」→「連線」查該域名走 PROXY 還是 DIRECT
- **走 DIRECT 但希望走 PROXY** → 把該域名加到 `extras/ai-extras.list`
- **不確定上游有沒有收錄** → 加進補漏清單最保險，重複的話 Shadowrocket 會自動跳過

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

- 規則檔（`.list`）內**不要**寫 `,Proxy` 或 `,DIRECT` 等策略，策略由引用它的 `.conf` 決定
- `.conf` 內的規則匹配是「由上往下」，第一個匹配的就生效
- 修改 `extras/` 後 push 才會觸發更新，僅 push 其他變更不會
