Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$NetworkName = "minha-rede-customizada"
$ServerContainer = "container-servidor"
$ClientContainer = "container-cliente"

function Remove-DockerResource {
	param([string[]] $Arguments)

	try {
		& docker @Arguments 2>$null | Out-Null
	}
	catch {
		$global:LASTEXITCODE = 0
		return
	}

	if ($LASTEXITCODE -ne 0) {
		$global:LASTEXITCODE = 0
	}
}

try {
	Write-Host "Parando e removendo containers..." -ForegroundColor Yellow
	Remove-DockerResource @("rm", "-f", $ServerContainer, $ClientContainer)

	Write-Host "Removendo rede customizada..." -ForegroundColor Yellow
	Remove-DockerResource @("network", "rm", $NetworkName)

	Write-Host "Limpeza concluída!" -ForegroundColor Green
}
catch {
	Write-Warning "Não consegui limpar tudo: $($_.Exception.Message)"
	Write-Warning "Verifica se o Docker está ativo e tenta de novo."
	exit 1
}
