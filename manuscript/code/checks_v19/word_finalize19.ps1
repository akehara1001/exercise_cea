param([string]$dir, [string]$esmPdf, [string]$orig, [string]$rev, [string]$cmpOut, [string]$author = "Akemi Hara", [string]$out)
# Opens every .docx in $dir (copies outside the work tree) with Word (COM): revisions, comments and page counts.
# Saves the ESM as PDF with SaveAs2(path, 17). Compares $orig with $rev (CompareDocuments, word level, revisions labelled
# with $author) and saves the result as $cmpOut (docx). Writes a JSON summary to $out. Only Word processes started here
# are stopped afterwards.
$ErrorActionPreference = "Stop"
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$rows = @()
try {
  foreach ($f in Get-ChildItem -Path $dir -Filter *.docx) {
    $d = $w.Documents.Open([string]$f.FullName)
    $d.Repaginate()
    $rows += [pscustomobject]@{ file = $f.Name; revisions = $d.Revisions.Count; comments = $d.Comments.Count; pages = $d.ComputeStatistics(2) }
    if ($f.Name -like "ESM*") { $d.SaveAs2([string]$esmPdf, 17) }
    $d.Close([ref]0)
  }
  $o = $w.Documents.Open([string]$orig)
  $r = $w.Documents.Open([string]$rev)
  $c = $w.CompareDocuments($o, $r, 2, 1, $true, $true, $true, $true, $true, $true, $true, $true, $true, $true, $author, $true)
  $nrev = $c.Revisions.Count
  $authors = @($c.Revisions | ForEach-Object { $_.Author } | Sort-Object -Unique)
  $c.SaveAs2([string]$cmpOut, 16)
  $c.Close([ref]0)
  $o.Close([ref]0)
  $r.Close([ref]0)
  [pscustomobject]@{ files = $rows; compare_revisions = $nrev; compare_authors = $authors } | ConvertTo-Json -Depth 4 | Out-File -FilePath $out -Encoding utf8
} finally {
  $w.Quit([ref]0)
  Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}
