# Shadowrocket + Tailscale（iPhone）

在 iPhone 上同時使用 Shadowrocket（AI 分流）和 Tailscale（連回自己的電腦、伺服器、NAS）。
> Use Shadowrocket (AI routing) and Tailscale (reach your own computers, servers, NAS) on an iPhone at the same time.

回到 [README](../README.md) · 一般操作見 [Shadowrocket 使用指南](shadowrocket-guide.md)

---

## 為什麼會衝突 / Why they conflict

iOS **一次只能開一個 VPN**。官方 Tailscale App 和 Shadowrocket 都是 VPN：打開其中一個，另一個就會被關掉。
> iOS runs **only one VPN at a time**. The official Tailscale app and Shadowrocket are both VPNs: switching one on switches the other off.

解法是讓 Shadowrocket 當唯一的 VPN，再由它把 Tailscale 的流量送到對的地方。有兩種做法：
> The fix is to keep Shadowrocket as the only VPN and let it send Tailscale traffic to the right place. There are two ways:

| | A · 內建 Tailscale / Built-in Tailscale | B · 經節點 / Through the node |
|---|---|---|
| 做法 / How | Shadowrocket 自己加入 tailnet / Shadowrocket joins the tailnet itself | 節點伺服器已在 tailnet 內，由它代連 / The node server is already in the tailnet and connects for you |
| 適合 / For | 任何有 tailnet 的人 / Anyone with a tailnet | 節點的管理員本人 / The admin of the node |
| Shadowrocket 版本 / version | 2.2.89 或更新 / or newer | 任何版本 / any |
| 手機上要設定 / Set up on the phone | 認證密鑰 + 開關 / Auth key + a switch | 只要訂閱配置 / Only the config |
| 配置 / Config | [`ai-tailscale.conf`](../configs/ai-tailscale.conf) | [`ai-tailnet-via-node.conf`](../configs/ai-tailnet-via-node.conf) |
| 連線路徑 / Path | 手機直連裝置（或經 DERP 中繼）/ Phone to device directly (or through a DERP relay) | 手機 → 節點 → 裝置 / Phone → node → device |
| 手機在 tailnet 內 / Phone is a tailnet device | 是 / Yes | 否 / No |

不確定就選 **A**。你是節點管理員、只想最快連回自己的機器，選 **B**。
> If unsure, pick **A**. If you run the node and only want the quickest way back to your own machines, pick **B**.

> [!NOTE]
> 不需要 AI 分流、只想讓所有流量從某台機器出去？那不需要 Shadowrocket：用官方 Tailscale App 並選一個出口節點（exit node）即可。
> Don't need AI routing and just want all traffic to leave through one machine? You don't need Shadowrocket: use the official Tailscale app with an exit node.

---

## 做法 A：內建 Tailscale / Way A: built-in Tailscale

Shadowrocket 從 2.2.89 起內建 Tailscale 模組，並多了一個規則策略 `TAILSCALE`。
> Since 2.2.89 Shadowrocket has a built-in Tailscale module and a rule policy named `TAILSCALE`.

### 開始之前 / Before you start

- 到 App Store 把 Shadowrocket **更新到最新版**（2.2.93 修了幾個 Tailscale 連線問題）。
  > Update Shadowrocket to the **newest version** in the App Store (2.2.93 fixed several Tailscale connection problems).
- 一個 Tailscale 帳號，裡面至少有一台要連的裝置（電腦、伺服器）並且在線上。
  > A Tailscale account with at least one device you want to reach (computer, server), online.
- 官方 Tailscale App 可以留著，但**不要打開它的開關**。
  > The official Tailscale app can stay installed, but **leave its switch off**.

以下 Shadowrocket 的選項名稱依 App 語言可能略有不同。
> The Shadowrocket labels below may differ slightly with the app language.

### 步驟 1 · Step 1：產生認證密鑰 / Create an auth key

在電腦或手機瀏覽器打開 Tailscale 管理後台：
> Open the Tailscale admin console in a browser:

```
https://login.tailscale.com/admin/settings/keys
```

按「**Generate auth key**」，這樣設定：
> Select **Generate auth key** and set:

| 選項 / Option | 設定 / Value | 原因 / Why |
|---|---|---|
| Reusable | 開 / On | 重新連線時可能再用到同一把密鑰 / The same key may be needed again on a reconnect |
| Ephemeral | 關 / Off | 開了的話手機離線就會被移出 tailnet / If on, the phone is removed from the tailnet whenever it goes offline |
| Expiration | 90 days | 最長就是 90 天 / 90 days is the maximum |

按「**Generate key**」，複製那串 `tskey-auth-...`（只會顯示一次）。
> Select **Generate key** and copy the `tskey-auth-...` string (it is shown only once).

> [!WARNING]
> 這把密鑰可以把任何裝置加進你的 tailnet，**等同密碼**。不要貼到聊天群組、不要寫進配置檔、不要 push 到 GitHub。
> This key can add any device to your tailnet. **Treat it like a password**: never post it in a chat group, never put it in a config file, never push it to GitHub.

### 步驟 2 · Step 2：在 Shadowrocket 填入密鑰 / Enter the key in Shadowrocket

Shadowrocket → 底部「**設定 / Settings**」→「**Tailscale**」：
> Shadowrocket → bottom **Settings** tab → **Tailscale**:

1. 「**認證密鑰 / Auth Key**」貼上剛才的 `tskey-auth-...`
   > Paste the `tskey-auth-...` into **Auth Key**
2. 打開「**啟用 / Enable**」
   > Switch **Enable** on
3. 其他選項先保持預設（見下方[選項說明](#選項說明--options)）
   > Leave the other options at their defaults (see [Options](#選項說明--options) below)

### 步驟 3 · Step 3：訂閱 Tailscale 版配置 / Subscribe to the Tailscale config

複製這條 URL / Copy this URL:

```
https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/configs/ai-tailscale.conf
```

訂閱方式跟 [README 步驟 2](../README.md) 一樣：「**配置 / Config**」標籤 → 右上角「**+**」→「**訂閱配置 / Add Subscription**」→ 貼上 URL → 命名為 `AI-Tailscale` → 儲存，然後**點一下它**讓左邊出現勾號 ✓。
> Subscribe the same way as [README Step 2](../README.md): **Config** tab → **+** (top-right) → **Add Subscription** → paste the URL → name it `AI-Tailscale` → save, then **tap it** so the ✓ appears.

它取代 `AI-Only`（內容相同，只多了 Tailscale 規則），不用兩個都勾。
> It replaces `AI-Only` (same content plus the Tailscale rules); you don't need both.

### 步驟 4 · Step 4：連線並確認 / Connect and check

1. 「**首頁 / Home**」→ 確認「全局路由 / Global Routing」是「**配置 / Config**」→ 選節點 → 打開連線開關。
   > **Home** → make sure **Global Routing** is **Config** → pick your node → switch the connection on.
2. 回到「設定 → Tailscale」：狀態顯示已連線，並列出你 tailnet 裡的裝置。
   > Back in **Settings → Tailscale**: the status shows connected and lists the devices in your tailnet.
3. Tailscale 管理後台的 **Machines** 頁會多出一台新裝置（這支 iPhone 的 Shadowrocket）。
   > The **Machines** page of the Tailscale admin console shows a new device (Shadowrocket on this iPhone).
4. 用 Safari 或 SSH App 連一台裝置：`http://100.x.y.z:連接埠` 或 `裝置名.tailXXXXX.ts.net`。
   > Reach a device with Safari or an SSH app: `http://100.x.y.z:port` or `device-name.tailXXXXX.ts.net`.
5. 打開 Claude / ChatGPT，確認 AI 仍然走節點。
   > Open Claude / ChatGPT and check that AI still goes through the node.

> [!TIP]
> 不要用 ping 測試：Shadowrocket 會自動回覆 ping，結果不準。請用真的服務（網頁、SSH、遠端桌面）測。
> Don't test with ping: Shadowrocket answers pings itself, so the result means nothing. Test with a real service (web page, SSH, remote desktop).

### 密鑰到期怎麼辦 / When the key expires

- 認證密鑰最長 90 天。已經加入的裝置**不會**因為密鑰到期而失效。
  > An auth key lasts at most 90 days. A device that already joined does **not** stop working when the key expires.
- 裝置本身的金鑰預設 180 天到期。想避免：管理後台 **Machines** → 該裝置的「**…**」→「**Disable key expiry**」。
  > The device's own key expires after 180 days by default. To avoid that: admin console **Machines** → the device's **…** menu → **Disable key expiry**.
- 哪天 Tailscale 突然連不上：產生一把新密鑰，重做步驟 2。
  > If Tailscale stops connecting one day: create a new key and repeat Step 2.

### 選項說明 / Options

「設定 → Tailscale」裡的其他選項：
> The other options in **Settings → Tailscale**:

| 選項 / Option | 建議 / Suggested | 作用 / What it does |
|---|---|---|
| 低電量模式 / Low Power Mode | 開（省電）/ On (saves battery) | 閒置時釋放網路資源，需要時自動重連 / Releases network resources when idle and reconnects when needed |
| 控制伺服器 URL / Control Server URL | 留空 / Empty | 只有自架控制伺服器才要填 / Only for a self-hosted control server |
| 出口節點 / Exit Node | 留空 / Empty | 預設只處理 tailnet 流量，不使用出口節點 / By default only tailnet traffic is handled; no exit node |
| 始終使用 DERP / Always Use DERP | 關 / Off | 強制走中繼、停用直連，會變慢 / Forces relays and disables direct connections; slower |
| 使用 Tailscale 子網 / Use Tailscale Subnets | 關 / Off | 要連 `100.x` 以外的內網位址才需要，見下方 / Needed only to reach addresses outside `100.x`, see below |

### 進階：連回家裡 / 公司的區網 / Advanced: reach a home or office LAN

想用 `192.168.x.x` 這類位址連回家裡的裝置（Tailscale 的 subnet route）。以下來自其他使用者的回報，本倉庫沒有實測：
> To reach home devices by addresses like `192.168.x.x` (a Tailscale subnet route). The following comes from other users' reports and was not tested for this repo:

1. 家裡那台 Tailscale 裝置要先廣播子網（`tailscale set --advertise-routes=192.168.50.0/24`）並在管理後台核准。
   > The Tailscale device at home must advertise the subnet (`tailscale set --advertise-routes=192.168.50.0/24`) and be approved in the admin console.
2. Shadowrocket「設定 → Tailscale」打開「**使用 Tailscale 子網**」。有使用者回報還需要把「**出口節點**」填成家裡那台的 `100.x.y.z`。
   > In **Settings → Tailscale** switch **Use Tailscale Subnets** on. Some users report that **Exit Node** must also be set to the home device's `100.x.y.z`.
3. 配置要改兩處，所以要用自己的本機副本（訂閱的配置更新時會蓋掉你的修改）：`bypass-tun` 拿掉 `192.168.0.0/16`，並加一條規則 `IP-CIDR,192.168.50.0/24,TAILSCALE,no-resolve`。
   > The config needs two changes, so use your own local copy (updating a subscribed config overwrites your edits): remove `192.168.0.0/16` from `bypass-tun`, and add the rule `IP-CIDR,192.168.50.0/24,TAILSCALE,no-resolve`.

---

## 做法 B：經節點進 tailnet / Way B: through the node

節點伺服器本身就是 tailnet 的一員時，手機完全不需要 Tailscale：把 Tailscale 位址的流量交給節點，節點用它自己的 Tailscale 去連。
> When the node server is itself a member of the tailnet, the phone needs no Tailscale at all: hand traffic for Tailscale addresses to the node, and the node connects with its own Tailscale.

### 前提 / Requirements

- 你選的節點那台伺服器已安裝 Tailscale 並加入**你的** tailnet。
  > The server behind the node you select runs Tailscale and is in **your** tailnet.
- 要用 `*.ts.net` 名稱的話，伺服器要開著 Tailscale DNS（預設就是開的）。
  > To use `*.ts.net` names, the server must have Tailscale DNS on (the default).

### 步驟 / Steps

複製這條 URL / Copy this URL:

```
https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/configs/ai-tailnet-via-node.conf
```

「**配置 / Config**」→「**+**」→「**訂閱配置 / Add Subscription**」→ 貼上 → 命名為 `AI-Tailnet-Node` → 儲存 → 點一下讓它出現勾號 ✓ → 「首頁」選節點並連線。
> **Config** → **+** → **Add Subscription** → paste → name it `AI-Tailnet-Node` → save → tap it so the ✓ appears → on **Home** pick the node and connect.

然後用 `100.x.y.z` 或 `裝置名.tailXXXXX.ts.net` 連你的裝置。
> Then reach your devices by `100.x.y.z` or `device-name.tailXXXXX.ts.net`.

### 限制 / Limits

- 對內網裝置來說，連線來自**節點伺服器**，不是手機；Tailscale 的存取規則（ACL）看到的是節點。
  > To the tailnet devices the connection comes from the **node server**, not the phone; Tailscale access rules (ACLs) see the node.
- 內網流量會繞經節點，速度取決於節點。
  > Tailnet traffic detours through the node, so speed depends on the node.
- 其他裝置無法主動連到這支手機。
  > Other devices cannot reach this phone.

> [!WARNING]
> **給節點管理員**：只要節點伺服器在 tailnet 裡，**每一個拿到該伺服器 `ss://` 連結的人**都能做同樣的事，不需要這份配置：他們在自己的 Shadowrocket 加一條規則，就能經節點連到你的 tailnet 裝置，以及伺服器上只綁 `127.0.0.1` 的服務。如果節點有分給別人用，請在伺服器端擋掉（例如 `ss-server --acl` 封鎖 `127.0.0.0/8`、`10.0.0.0/8`、`100.64.0.0/10`、`169.254.0.0/16`、`172.16.0.0/12`、`192.168.0.0/16`），只留自己那個帳號可以進內網。
> **For node admins**: once the node server is in the tailnet, **everyone who holds an `ss://` link for that server** can do the same without this config: one rule in their own Shadowrocket lets them reach your tailnet devices through the node, and also services on the server that listen only on `127.0.0.1`. If other people use the node, block this on the server (for example `ss-server --acl` blocking `127.0.0.0/8`, `10.0.0.0/8`, `100.64.0.0/10`, `169.254.0.0/16`, `172.16.0.0/12`, `192.168.0.0/16`) and leave tailnet access to your own account only.

---

## 確認走哪條路 / Check which route is used

Shadowrocket →「**資料 / Data**」→「**代理 / Proxy**」→ 打開「**啟用日誌記錄 / Enable Logging**」，連一次裝置後回來看記錄，每筆會顯示命中的策略：
> Shadowrocket → **Data** → **Proxy** → switch **Enable Logging** on, reach a device once, then read the entries; each one shows the policy that matched:

| 目的地 / Destination | 做法 A / Way A | 做法 B / Way B |
|---|---|---|
| `100.x.y.z`、`*.ts.net` | `TAILSCALE` | `PROXY` |
| Claude、ChatGPT… | `PROXY` | `PROXY` |
| 其他 / Everything else | `DIRECT` | `DIRECT` |

---

## 常見問題 / Troubleshooting

| 狀況 / Symptom | 處理 / What to do |
|---|---|
| 設定裡沒有 Tailscale / No Tailscale entry in Settings | Shadowrocket 太舊，到 App Store 更新（需要 2.2.89 或更新）。 / Shadowrocket is too old; update it in the App Store (2.2.89 or newer). |
| Tailscale 顯示已連線，但 `100.x` 連不上 / Tailscale shows connected but `100.x` is unreachable | 確認啟用的是 `AI-Tailscale`（左邊有 ✓）。在別的配置裡，`100.64.0.0/10` 通常列在「TUN 旁路路由」(`bypass-tun`)，要拿掉。 / Make sure `AI-Tailscale` is the active config (✓). In other configs `100.64.0.0/10` is usually listed under TUN bypass routes (`bypass-tun`) and must be removed. |
| 一直停在「正在連線」/ Stuck on "connecting" | 密鑰是否過期或貼錯；關掉再打開「啟用」；把連線開關關掉再開；確認官方 Tailscale App 是關的。 / Check that the key is not expired or mistyped; switch **Enable** off and on; toggle the connection; make sure the official Tailscale app is off. |
| 連得上但很卡 / Connects but very slow | 多半是打洞失敗、改走 DERP 中繼。確認「始終使用 DERP」是關的，換個網路（Wi-Fi / 行動網路）再試。 / Usually direct connection failed and a DERP relay is used. Make sure **Always Use DERP** is off and try another network (Wi-Fi / cellular). |
| 只打裝置短名（如 `my-pc`）連不上 / A short name (such as `my-pc`) does not work | 規則只認 `*.ts.net`：請用完整名稱 `my-pc.tailXXXXX.ts.net` 或 `100.x` 位址。完整名稱可在 Tailscale 管理後台的 Machines 頁看到。 / The rule matches `*.ts.net` only: use the full name `my-pc.tailXXXXX.ts.net` or the `100.x` address. The full name is on the Machines page of the admin console. |
| 遠端桌面、遊戲串流等用 UDP 的 App 不通 / Apps that use UDP (remote desktop, game streaming) fail | 「設定 → UDP → 啟用轉發」要打開。仍不行就改用該 App 的 TCP 模式或直接填 `100.x` 位址。 / Switch **Settings → UDP → Enable Forwarding** on. If it still fails, use the app's TCP mode or enter the `100.x` address directly. |
| 做法 B 連不上 / Way B cannot connect | 確認節點伺服器在 tailnet 內而且線上；確認首頁選的是那個節點。 / Check that the node server is in the tailnet and online, and that this node is the one selected on Home. |
| 打開官方 Tailscale App 後 Shadowrocket 斷了 / Shadowrocket disconnects after opening the official Tailscale app | 正常：iOS 只允許一個 VPN。關掉 Tailscale App 的開關，再打開 Shadowrocket。 / Expected: iOS allows one VPN. Switch the Tailscale app off and Shadowrocket back on. |

---

## 已驗證與未驗證 / What was tested

- **已測（2026-11-16）**：做法 B 的伺服器端。一台在 tailnet 內的 Shadowsocks 節點（shadowsocks-libev 3.3.5）能代連 tailnet 的 `100.x` 位址，也能解析 `*.ts.net` 名稱。
  > **Tested (2026-11-16)**: the server side of Way B. A Shadowsocks node inside a tailnet (shadowsocks-libev 3.3.5) reached tailnet `100.x` addresses and resolved `*.ts.net` names.
- **未在 iPhone 上實測**：兩種做法在手機上的步驟。做法 A 的選項與規則依據 Shadowrocket 使用手冊與使用者回報整理。照做後有出入，請回報給管理員。
  > **Not tested on an iPhone**: the phone steps of both ways. The options and rules of Way A follow the Shadowrocket handbook and user reports. If something differs, tell the admin.

## 參考資料 / Sources

- [Shadowrocket 使用手冊：Tailscale](https://github.com/LOWERTOP/Shadowrocket#tailscale)（選項、`TAILSCALE` 策略、2.2.89 起支援）
- [Tailscale：auth keys](https://tailscale.com/docs/features/access-control/auth-keys)
- [Tailscale：Can I use Tailscale alongside other VPNs?](https://tailscale.com/docs/reference/faq/other-vpns)
- [Tailscale：subnet routers](https://tailscale.com/docs/features/subnet-routers)
- 使用者回報 / user reports：[V2EX 1225970](https://v2ex.com/t/1225970)、[V2EX 1231877](https://www.v2ex.com/t/1231877)
