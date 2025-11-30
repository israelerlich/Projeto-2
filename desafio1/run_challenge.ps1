Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# inserindo as variáveis básicas
$rede = "minha-rede-customizada"
$nome_server = "container-servidor"
$nome_client = "container-cliente"
$imagem = "meu-servidor-web"

function Invoke-Docker {
	param(
		[Parameter(Mandatory = $true)]
		[string[]] $Arguments
	)

	& docker @Arguments
	if ($LASTEXITCODE -ne 0) {
		throw "Falhou: docker $($Arguments -join ' ')"
	}
}

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

function Wait-WithMessage {
	param([int] $Seconds)

	Write-Host "Esperando $Seconds segundo(s)..."
	Start-Sleep -Seconds $Seconds
}

try {
	Write-Host "Limpando containers e redes antigas..."
	Remove-DockerResource @("rm", "-f", $nome_server, $nome_client)
	Remove-DockerResource @("network", "rm", $rede)

	Write-Host "Criando a rede..."
	Invoke-Docker @("network", "create", $rede)

	Write-Host "Criando a imagem do servidor..."
	Invoke-Docker @("build", "-t", $imagem, "./server")

	Write-Host "Subindo o servidor..."
	Invoke-Docker @("run", "-d", "--name", $nome_server, "--network", $rede, "-p", "8080:8080", $imagem)

	Wait-WithMessage -Seconds 5

	Write-Host "Preparando comando do cliente..."
	$clientCommand = "apk add --no-cache curl && while true; do echo 'Chamando servidor...'; curl -v http://${nome_server}:8080; sleep 5; done"
	Write-Host "Comando que vai rodar: $clientCommand"

	Write-Host "Subindo o cliente..."
	Invoke-Docker @("run", "-d", "--name", $nome_client, "--network", $rede, "alpine:latest", "/bin/sh", "-c", $clientCommand)

	Wait-WithMessage -Seconds 20

	Write-Host "`n--- Logs do Cliente (10 linhas) ---"
	Invoke-Docker @("logs", "--tail", "10", $nome_client)

	Write-Host "`n--- Logs do Servidor (10 linhas) ---"
	Invoke-Docker @("logs", "--tail", "10", $nome_server)

	Write-Host "`nPronto! Tudo rodando."
	Write-Host "Pra limpar tudo depois, roda o script cleanup.ps1 ou:"
	Write-Host "docker rm -f $nome_server $nome_client"
}
catch {
	Write-Warning "Algo deu errado: $($_.Exception.Message)"
	Write-Warning "Confere os passos acima; nada foi limpo automaticamente."
	exit 1
}
