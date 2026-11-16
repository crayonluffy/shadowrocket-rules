# 亞洲直連，其他走節點 / Asia direct, the rest through the node

iPhone、Windows、Mac 用同一套規則：東亞和東南亞的網站用你原本的網路直連，其他地區（美洲、歐洲…）從你選的出口節點出去。
> One set of rules for iPhone, Windows and Mac: sites in East and Southeast Asia use your own connection; everything else (Americas, Europe…) leaves through the exit node you pick.

回到 [README](../README.md) · [Shadowrocket + Tailscale 教學](tailscale.md) · [Shadowrocket 使用指南](shadowrocket-guide.md)

---

## 流量怎麼走 / Where traffic goes

由上往下，第一條符合的生效：
> Top to bottom; the first match wins:

| # | 目的地 / Destination | 走哪裡 / Route |
|---|---|---|
| 1 | Tailscale 內網（`100.x`、`*.ts.net`）/ Tailscale addresses | 內網 / tailnet |
| 2 | AI 服務（Claude、ChatGPT、Gemini…）/ AI services | **出口節點 / exit node**，不論伺服器在哪 / wherever the server is |
| 3 | 區域網路 / Local network | 直連 / direct |
| 4 | 伺服器 IP 在東亞、東南亞 / Server IP in East or Southeast Asia | **直連 / direct**（你原本的 IP / your own IP） |
| 5 | 其他全部 / Everything else | **出口節點 / exit node** |

「亞洲」包含 / "Asia" means: 中國 CN、香港 HK、澳門 MO、台灣 TW、日本 JP、南韓 KR、北韓 KP、蒙古 MN、新加坡 SG、馬來西亞 MY、泰國 TH、越南 VN、印尼 ID、菲律賓 PH、汶萊 BN、柬埔寨 KH、寮國 LA、緬甸 MM、東帝汶 TL。

> [!IMPORTANT]
> 判斷依據是**伺服器 IP 的所在地**，不是公司所在地。美國網站若使用亞洲的 CDN 機房，會被當成亞洲而**直連**（對方看到你原本的 IP）。一定要走節點的網站請管理員加進 AI 清單。
> The decision uses **where the server's IP is**, not where the company is. A US site served from a CDN location in Asia counts as Asia and goes **direct** (it sees your own IP). Ask the admin to add any site that must always use the node to the AI list.

### 出口節點 / The exit node

出口就是你的 `ss://` 節點。有兩個節點（例如東京、新加坡）時，由你隨時切換：
> The exit is your `ss://` node. With two nodes (for example Tokyo and Singapore) you switch whenever you like:

- iPhone：在 Shadowrocket「首頁」點選節點 / tap the node on the Shadowrocket **Home** tab
- Windows、Mac：在 Clash Verge「代理」頁的 `Exit` 群組選節點 / pick the node in the `Exit` group on the Clash Verge **Proxies** page

兩個出口本身都在亞洲，所以亞洲以外的網站會看到東京或新加坡的 IP。
> Both exits are in Asia themselves, so sites outside Asia see a Tokyo or Singapore address.

> [!NOTE]
> 為什麼不用 Tailscale 的「出口節點」功能？它只能整台裝置全開或全關，不能依地區分流。所以由 Shadowrocket / Clash Verge 依規則分流，出口則是同一批伺服器上的 Shadowsocks 節點，效果相同。
> Why not Tailscale's own "exit node" feature? It is all or nothing for the whole device and cannot split by region. So Shadowrocket / Clash Verge split by rule, and the exit is the Shadowsocks node on the same servers: the result is the same.

---

## iPhone：Shadowrocket

1. 把兩個節點的 `ss://` 連結都匯入（點連結即可，見 [README 步驟 1](../README.md)）。
   > Import the `ss://` links of both nodes (tap each link, see [README Step 1](../README.md)).
2. 訂閱這個配置並點選它（左邊出現 ✓），取代 `AI-Only`：
   > Subscribe to this config and tap it (✓ appears); it replaces `AI-Only`:

   ```
   https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/configs/asia-direct.conf
   ```

   「配置 / Config」→「+」→「訂閱配置 / Add Subscription」→ 貼上 → 命名為 `Asia-Direct` → 儲存。
   > **Config** → **+** → **Add Subscription** → paste → name it `Asia-Direct` → save.
3. 「首頁」：全局路由選「**配置 / Config**」，點選要當出口的節點，打開連線開關。
   > **Home**: set Global Routing to **Config**, tap the node you want as exit, switch the connection on.

這個配置也包含經節點進 Tailscale 內網的規則（節點伺服器在 tailnet 內時有效）。
> This config also carries the rules that reach the Tailscale network through the node (works when the node server is in the tailnet).

---

## Windows、Mac：Clash Verge

### 1. 管理員：產生個人設定檔 / Admin: build the personal profile

每個人的設定檔內含節點密碼，所以不放在這個公開倉庫，由管理員用腳本產生後私下傳給對方：
> Each profile holds node passwords, so it is not in this public repo. The admin builds it with the script and sends it privately:

```
python3 scripts/make-clash-profile.py -o private/clash-alice.yaml 'ss://...東京...' 'ss://...新加坡...'
```

也可以直接接 `ss-list` 的輸出（腳本會挑出裡面的 `ss://` 連結）：
> Or pipe the output of `ss-list` (the script picks out the `ss://` links):

```
sudo ss-list alice | python3 scripts/make-clash-profile.py -o private/clash-alice.yaml -
```

> [!WARNING]
> 產生的 `.yaml` 等同密碼，請用加密通訊軟體傳送。`private/` 已被 git 忽略，不要把它 push 上來。
> The generated `.yaml` is as sensitive as a password; send it with an encrypted messenger. `private/` is ignored by git; never push it.

### 2. 安裝並匯入 / Install and import

1. 安裝 [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)（Windows、macOS 都有）。
   > Install [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases) (available for Windows and macOS).
2. 打開「**訂閱 / Profiles**」頁，把收到的 `.yaml` 檔**拖進視窗**（或按「新建 / New」→ 類型選 Local → 選檔案）。
   > Open the **Profiles** page and **drag the `.yaml` file into the window** (or **New** → type Local → choose the file).
3. 點一下這個設定檔讓它變成使用中。
   > Click the profile to make it the active one.
4. 「**代理 / Proxies**」頁：模式選「**規則 / Rule**」；在 `Exit` 群組選東京或新加坡。
   > **Proxies** page: mode **Rule**; in the `Exit` group pick Tokyo or Singapore.
5. 「**設定 / Settings**」頁：打開「**系統代理 / System Proxy**」。
   > **Settings** page: switch **System Proxy** on.

### 3. 和 Tailscale 一起用 / Together with Tailscale

電腦上 Tailscale 和 Clash Verge 可以同時開（電腦沒有 iPhone 的單一 VPN 限制）。Tailscale App 照常開著，**不要**在 Tailscale 裡選出口節點。
> On a computer Tailscale and Clash Verge can both be on (no one-VPN limit as on the iPhone). Keep the Tailscale app running and do **not** select an exit node in Tailscale.

- `Tailnet` 群組選 `DIRECT`（預設）：`100.x` 位址交給這台電腦的 Tailscale。
  > `Tailnet` group on `DIRECT` (default): `100.x` addresses are left to this computer's Tailscale.
- 這台電腦沒裝 Tailscale：`Tailnet` 群組改選 `Exit`，經節點進內網。
  > No Tailscale on this computer: set the `Tailnet` group to `Exit` to go in through the node.
- 建議用「系統代理」，不要開「虛擬網卡 / TUN 模式」：TUN 模式會和 Tailscale 搶路由與 DNS。
  > Use **System Proxy**, not **TUN mode**: TUN mode competes with Tailscale for routes and DNS.
- `*.ts.net` 名稱連不上時，改用 `100.x` 位址，或把 `Tailnet` 群組改成 `Exit`。
  > If a `*.ts.net` name does not resolve, use the `100.x` address, or set the `Tailnet` group to `Exit`.

---

## 確認 / Check

| 測試 / Test | 預期 / Expected |
|---|---|
| 打開 `https://ipinfo.io`（美國的服務）/ Open `https://ipinfo.io` (a US service) | 顯示出口節點的 IP（東京或新加坡）/ Shows the exit node's address (Tokyo or Singapore) |
| 打開一個本地（亞洲）網站 / Open a local (Asian) site | 記錄顯示 `DIRECT` / The log shows `DIRECT` |
| 打開 Claude / ChatGPT | 記錄顯示走節點 / The log shows the node |

看記錄 / Where the log is:
- Shadowrocket：「資料 → 代理」（先打開「啟用日誌記錄」）/ **Data → Proxy** (switch **Enable Logging** on first)
- Clash Verge：「**連線 / Connections**」頁，每筆連線會顯示命中的規則與節點 / the **Connections** page shows the matched rule and node for each connection

---

## 已驗證與未驗證 / What was tested

- **已測 / Tested**：`scripts/make-clash-profile.py`（三種 `ss://` 連結格式，產生的 YAML 可解析）；`scripts/check.py` 會確認 Shadowrocket 配置與 Clash 範本的國家清單、保底規則一致。
  > `scripts/make-clash-profile.py` (three `ss://` link forms; the generated YAML parses); `scripts/check.py` confirms the Shadowrocket config and the Clash template carry the same country list and failsafe rules.
- **未測 / Not tested**：設定檔沒有在 Clash Verge / mihomo 裡實際跑過，Shadowrocket 配置也沒有在 iPhone 上跑過。Clash Verge 的操作步驟依其說明文件整理。第一次使用請照上面「確認」一節檢查，有出入請回報給管理員。
  > The profile was not run in Clash Verge / mihomo, and the Shadowrocket config was not run on an iPhone. The Clash Verge steps follow its documentation. Run the checks above on first use and tell the admin if something differs.

## 參考資料 / Sources

- [mihomo：rule-providers](https://wiki.metacubex.one/en/config/rule-providers/)、[proxy-groups](https://wiki.metacubex.one/en/config/proxy-groups/)
- [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)
- [Tailscale：exit nodes](https://tailscale.com/docs/features/exit-nodes)
