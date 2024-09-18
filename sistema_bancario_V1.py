menu = """
[d] para depositar
[s] para sacar
[e] para exibir o extrato
[q] para sair
"""
LIMITE_SAQUES = 3
numero_saques = 0
valor_max_saque = 500
saldo = 0
extrato = ""


while True:
    opcao = input(menu).strip().lower()
    
    if opcao == "d":
        valor = float(input("digite o valor que deseja depositar: "))
        if valor < 0:
            print("digite um valor válido")
        else:
            saldo += valor
            extrato += f"Depósito: R$ {valor}\n"
            
    elif opcao == "s":
        valor = float(input("digite o valor que deseja sacar: "))
        
        excedeu_saldo = valor > saldo
        
        excedeu_saque = numero_saques >= LIMITE_SAQUES
        
        excedeu_limite = valor > valor_max_saque
        
        if excedeu_saque:
            print("número de saques excedido")
        elif valor < 0:
            print("digite um valor válido")
        elif excedeu_limite:
            print("o valor excedeu o limite")
        elif excedeu_saldo:
            print("saldo insuficiente")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor}\n"
            numero_saques += 1
            
    elif opcao == "e":
        print("=================EXTRATO=================\n") 
        print("não foram realizadas movimentações")if not extrato else print(extrato)
        print(f"saldo: R$ {saldo}\n ========================================")
            
    elif opcao == "q":
        break
            
    
        
        