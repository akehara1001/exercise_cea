param([string]$src, [string]$out)
# Pages of every paragraph of a docx, read with Word (COM): start and end page, first 60 characters.
$ErrorActionPreference = "Stop"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $d = $w.Documents.Open($src, $false, $true)
  $d.Repaginate()
  $rows = @()
  $n = $d.Paragraphs.Count
  for ($i = 1; $i -le $n; $i++) {
    $p = $d.Paragraphs.Item($i)
    $t = $p.Range.Text
    if ($t.Length -gt 60) { $t = $t.Substring(0, 60) }
    $rows += [pscustomobject]@{ i = $i; start_page = $p.Range.Characters.First.Information(3); end_page = $p.Range.Information(3); text = $t }
  }
  $total = $d.ComputeStatistics(2)
  $d.Close([ref]0)
  [pscustomobject]@{ pages = $total; paragraphs = $rows } | ConvertTo-Json -Depth 4 | Out-File -FilePath $out -Encoding utf8
} finally {
  $w.Quit()
}
