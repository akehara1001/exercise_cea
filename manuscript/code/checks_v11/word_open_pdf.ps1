param([string]$src, [string]$pdf = "")
# Opens a docx with Word (COM), reports pages, revisions and comments, optionally saves a PDF with SaveAs2(path, 17).
$ErrorActionPreference = "Stop"
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $d = $w.Documents.Open([string]$src)
  $d.Repaginate()
  "pages=" + $d.ComputeStatistics(2) + " revisions=" + $d.Revisions.Count + " comments=" + $d.Comments.Count + " words=" + $d.ComputeStatistics(0)
  if ($pdf -ne "") { $d.SaveAs2([string]$pdf, 17); "pdf written" }
  $d.Close([ref]0)
} finally {
  $w.Quit([ref]0)
  Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}
