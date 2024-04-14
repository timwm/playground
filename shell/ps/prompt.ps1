<#
$p = Split-Path -leaf -path (Get-Location)
"PS $($p)`n$(
    '>' * 
($nestedPromptLevel + 1)) "
#>

function Global:prompt {
    $Location = Get-Item -Path (Get-Location)
    if ($Location.PSChildName) {
        $LocationName = $Location.PSChildName
    } else {
        $LocationName = $Location.BaseName
    }
    Write-Host -Object "$LocationName>" -NoNewLine -ForegroundColor Black
    Return ' '
}