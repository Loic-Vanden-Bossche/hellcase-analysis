$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
$session.Cookies.Add((New-Object System.Net.Cookie("spin_wheel_stat_cookie", "eyJpdiI6IkhSYjZwR0RqK3NVeGJpQUlBa21SVEE9PSIsInZhbHVlIjoicjJyQ3RvYU9TVWZiSkFDVXFlV0pYMXYvMnZHWGtkU3JMVFdwdWIzRUdzaHNDZkxzNWM4K0lVL0h0aXZ0dnJEeERDNjYvb0JTOU83ZXdveGhCc1k3U21vQWszbGk3UU1zRWRLS2dFYW1iQVA4MVp2VDcxd05TVDZiYzl5aW0yNDciLCJtYWMiOiJlMTRjZjliZGI3NWFmMWMwZTIzMDYzZDlkMTU0YWM1MGQ1ZWJkN2ZkYjM0ZmE1ZmYwMTZiMjFmN2Q2NDhlZWExIiwidGFnIjoiIn0%3D", "/", ".hellcase.com")))
$session.Cookies.Add((New-Object System.Net.Cookie("return_url", "eyJpdiI6Ik1scnNkU0RsZzEvRjQyWndoQ2pUNlE9PSIsInZhbHVlIjoiNWdnV0ZmYmNZVnRXSXRERTIxcVVpc3FyWC8wem5JdDA3RUFHZVI4M2h6RS9qcFR6R01NVndrUmxIbjBuQkdybGhoZG5JSkMzTVZ0K1NxMlcweU1zdk5kWW9VUjhHdk4zOS90eEFRMTJNUkk9IiwibWFjIjoiZGMxNjllYWM4OWEyMjdmYTQ0NDFlNTc2NGIzOTU3ZGFlYjkzZDI1YTNlYTE3ZmJmMzA0MGRiNmI5OWQ0M2VlNyIsInRhZyI6IiJ9", "/", ".hellcase.com")))
$session.Cookies.Add((New-Object System.Net.Cookie("remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d", "eyJpdiI6IlJRd1ByVnQxSm9UMG15MG1STVhEM1E9PSIsInZhbHVlIjoiL0p0QnprNDIxc3VYUU1pV0lXZ21XNDNVcERrZFJVamZaYUdpSnNyMVE0VGhjS3RYZE9KZUx3cUNEWnQ2UzQ3aXBVWGxmRzNKM3FJbHhTdC9uVTdXV3hHMkVJRkJ1ZG14T0RlUVZnZFU1c0JtaEtxbzFRbDFCRlJiMkVtY3IwVnlBZCtVU0hRNEIxZVRUWHpma3lkNG9BPT0iLCJtYWMiOiJlMzAxMWNkMTk4Y2QwMmZiMjQ5MTFmNmVmY2U1MjdiYjI2Y2M2M2M1NWM1MzNlMzFiNjJhMTI3MzIwMWEwNGNjIiwidGFnIjoiIn0%3D", "/", ".hellcase.com")))
$session.Cookies.Add((New-Object System.Net.Cookie("hellcase_session", "PBr6WSjruCyJYUEp0HugYL81pUzKlB5FWCDQldbB", "/", ".hellcase.com")))
$session.Cookies.Add((New-Object System.Net.Cookie("XSRF-TOKEN", "eyJpdiI6IjNEVXp0RFZ0ZStGODNCZlZRS212SGc9PSIsInZhbHVlIjoiSUROc3VSRlZNK0kvOTFsckNDSnRXS2tnem55NWlBNHNtTjJ5eGVVMzhIdGJNN1VqdGpkejMxdDRQd040L3F0cmNhTmh0UGNzS3JjOFBKNUxXczBXSVh4b3RsWGhjK2lVN3B5NGNYLytIbUxXdUpLOUoxSUlLOXBlSW9NZ3B1RGIiLCJtYWMiOiIzMGI4YzU2NzQ2YzVjMDZlNjM5OTQ3MDRmM2JjMzdhYzEwYzE5ZTZhZTI0MDQ3MDEzN2JjMzkzNmE4NWI5ZTBlIiwidGFnIjoiIn0%3D", "/", ".hellcase.com")))
$response = Invoke-WebRequest -Uri "https://api.hellcase.com/upgrade/make" `
-Method "POST" `
-WebSession $session `
-Headers @{
"authority"="api.hellcase.com"
  "method"="POST"
  "path"="/upgrade/make"
  "scheme"="https"
  "accept"="application/json, text/plain, */*"
  "accept-encoding"="gzip, deflate"
  "accept-language"="fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
  "origin"="https://hellcase.com"
  "priority"="u=1, i"
  "referer"="https://hellcase.com/fr/upgrade?item-from=711131027:csgo"
  "sec-ch-ua"="`"Google Chrome`";v=`"137`", `"Chromium`";v=`"137`", `"Not/A)Brand`";v=`"24`""
  "sec-ch-ua-mobile"="?0"
  "sec-ch-ua-platform"="`"Windows`""
  "sec-fetch-dest"="empty"
  "sec-fetch-mode"="cors"
  "sec-fetch-site"="same-site"
  "x-csrf-token"="cOUvcQ4H7pBMFQJH9Unn599EoYUmXJ1fGoi88baQ"
  "x-frontend-version"="25_6_2025_351fd"
  "x-requested-with"="XMLHttpRequest"
  "x-xsrf-token"="eyJpdiI6IjNEVXp0RFZ0ZStGODNCZlZRS212SGc9PSIsInZhbHVlIjoiSUROc3VSRlZNK0kvOTFsckNDSnRXS2tnem55NWlBNHNtTjJ5eGVVMzhIdGJNN1VqdGpkejMxdDRQd040L3F0cmNhTmh0UGNzS3JjOFBKNUxXczBXSVh4b3RsWGhjK2lVN3B5NGNYLytIbUxXdUpLOUoxSUlLOXBlSW9NZ3B1RGIiLCJtYWMiOiIzMGI4YzU2NzQ2YzVjMDZlNjM5OTQ3MDRmM2JjMzdhYzEwYzE5ZTZhZTI0MDQ3MDEzN2JjMzkzNmE4NWI5ZTBlIiwidGFnIjoiIn0="
} `
-ContentType "application/x-www-form-urlencoded" `
-Body "chance=90&balance=0&old_items%5B0%5D%5Bid%5D=711131027&old_items%5B0%5D%5Bgame%5D=csgo&new_items%5B0%5D%5Bid%5D=6426&new_items%5B0%5D%5Bgame%5D=csgo&type=item_balance&direction=over"

$response.Content | Out-File -FilePath "response.json"

$response.Headers["Content-Encoding"]