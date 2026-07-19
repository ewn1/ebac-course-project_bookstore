# ==============================================================================
# AUTOMAÇÃO DE COMANDOS COM MAKEFILE
# ==============================================================================
# O 'make' lê este arquivo e executa as instruções no terminal do WSL/Linux.
#
# REGRA DE OURO DA SINTAXE:
# Toda linha de comando (abaixo do nome do atalho) DEVE ser recuada obrigatoriamente 
# usando a tecla TAB. Se você usar espaços normais, o Makefile vai quebrar!

# ------------------------------------------------------------------------------
# Atalho: 'make format'
# Função: Formata todo o código do projeto seguindo o padrão estrito do Black.
# ------------------------------------------------------------------------------
format:
	docker compose exec web black .
	# EXPLICAÇÃO:
	# 'docker compose exec web': Diz ao Docker para entrar no container 'web' ativo.
	# 'black .': Roda o formatador Black na pasta atual (.) para corrigir espaçamentos,
	#            aspas e quebras de linha automaticamente nos arquivos Python.

# ------------------------------------------------------------------------------
# Atalho: 'make lint'
# Função: Analisa o código procurando erros lógicos, variáveis mortas ou desvios da PEP 8.
# ------------------------------------------------------------------------------
lint:
	docker compose exec web flake8 .
	# EXPLICAÇÃO:
	# 'flake8 .': Roda o inspetor (linter) de código. Ele não altera os arquivos; 
	#             ele apenas imprime na tela uma lista de alertas se você importou algo
	#             e não usou, ou se quebrou alguma regra de estilo do Python.

# ------------------------------------------------------------------------------
# Atalho: 'make test'
# Função: Roda a suíte de testes automatizados do Django de forma rápida.
# ------------------------------------------------------------------------------
test:
	docker compose exec web python manage.py test
	# EXPLICAÇÃO:
	# 'python manage.py test': Executa o gerenciador de testes nativo do Django.
	#                          Com o 'make test', você economiza dezenas de toques no 
	#                          teclado toda vez que quiser validar se o código quebrou algo.