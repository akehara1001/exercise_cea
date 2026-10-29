param([string]$src, [string]$out, [string]$pdf = "")
# Per paragraph of a docx, read with Word (COM): Word's word count, start and end page, first 50 characters.
# Optionally saves a PDF with SaveAs2(path, 17). Opens the file given (pass a copy outside the work tree).
$ErrorActionPreference = "Stop"
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $d = $w.Documents.Open([string]$src)
  $d.Repaginate()
  $rows = @()
  $n = $d.Paragraphs.Count
  for ($i = 1; $i -le $n; $i++) {
    $p = $d.Paragraphs.Item($i)
    $r = $p.Range
    $t = $r.Text
    if ($t.Length -gt 50) { $t = $t.Substring(0, 50) }
    $rows += [pscustomobject]@{ i = $i; words = $r.ComputeStatistics(0); start_page = $r.Characters.First.Information(3); end_page = $r.Information(3); text = $t }
  }
  $total = $d.ComputeStatistics(2)
  $allwords = $d.ComputeStatistics(0)
  if ($pdf -ne "") { $d.SaveAs2([string]$pdf, 17) }
  $d.Close([ref]0)
  [pscustomobject]@{ pages = $total; words = $allwords; paragraphs = $rows } | ConvertTo-Json -Depth 4 | Out-File -FilePath $out -Encoding utf8
} finally {
  $w.Quit([ref]0)
  Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}
