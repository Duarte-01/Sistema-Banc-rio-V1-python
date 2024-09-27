import textwrap

menu = """
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[ex] Excluir conta
[exuser] Excluir usuario
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def criar_usuario(usuarios):
    cpf = input("digite o cpf(somente número): ")
    
    if len(cpf) < 8:
        print("O cpf precisa ter pelo menos 8 dígitos")
        return
    
    usuario = filtar_usuarios(cpf,usuarios)
    
    if usuario:
        print("@@@já existe um usuário com esse cpf@@@")
        return
    else:
        nome = input("digite seu nome: ")
        data_nasc = input("digite sua data de nascimento no modelo dd-mm-aa: ")
        endereco = input("digite seu endereço: ")
        usuarios.append({"cpf": cpf, "nome" : nome,  "data_nasc": data_nasc, "endereço": endereco})
        
        print("usuário criado com sucesso!")

def filtar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(usuarios, numero_conta, agencia):
    cpf = input("Digite seu cpf para criar uma conta: ")
    usuario = filtar_usuarios(cpf, usuarios)
    
    if usuario:
        print("conta criada com sucesso!")
        return {"usuario": usuario, "agencia": agencia, "numero_conta": numero_conta}
    else:
        print("usuário não encontrado")
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\ Agencia: {conta['agencia']}
                C/C:\t\t {conta['numero_conta']}
                Títular: {conta['usuario']['nome']}"""
        print("=" * 100)
        print(textwrap.dedent(linha))
        
def excluir_conta(cpf, contas):
    # Filtra as contas do usuário com o CPF fornecido
    contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
    
    # Verifica se o usuário tem contas associadas
    if not contas_usuario:
        print("Não existem contas para excluir para este usuário.")
        return contas
    
    # Exibe as contas do usuário e permite que ele escolha qual excluir
    print("Contas encontradas para este usuário:")
    for i, conta in enumerate(contas_usuario, start=1):
        print(f"{i}. Agência: {conta['agencia']}, Conta: {conta['numero_conta']}")
    
    # Solicita a escolha do usuário
    escolha = input(f"Selecione o número da conta que deseja excluir separado por vígula ex:(1,2,3) (1-{len(contas_usuario)}): ")
    escolhas = escolha.split(",")
    
    # Verifica se a escolha é válida
    contas_validas = []
    for escolha in escolhas:
        try:
            idx = int(escolha.strip())
            if 1 <= idx <= len(contas_usuario):
                contas_validas.append(idx)
            else:
                print("o número não está no range demonstrado escolha novamente")
        except ValueError:
            print(" o valor digitado não é um número valido")
                                                                                                         
    contas_validas.sort(reverse=True)
    
    # Remove as contas selecionadas da lista principal de contas
    for idx in contas_validas:                                               
        conta_selecionada = contas_usuario[idx - 1]                                                                  
        contas.remove(conta_selecionada)
        print(f"Conta {conta_selecionada['numero_conta']} excluída com sucesso!")
    
    return contas


def excluir_usuario(cpf, usuarios, contas):
    usuario_encontrado = False
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
             usuarios.remove(usuario)
             excluir_conta(cpf, contas)
             usuario_encontrado = True
             print("usuário excluído com sucesso!")
             break
                
    if not usuario_encontrado:
        print("não existem usuários para excluir")
    return usuarios
        
        

def depositar(valor, saldo, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, valor, saldo, limite, numero_saques, limite_saques, extrato):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def tirar_extrato(contas, saldo, extrato): 
    print("\n================ EXTRATO ================")   
    if not contas:
        print("nehuma conta encontrada")
    else:
        for conta in contas:
            conta_usuario = f"Títular: {conta['usuario']['nome']}"
            print(conta_usuario)
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    return saldo, extrato


def main(): #função principal do programa
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    numero_conta = 1

    while True: #looping principal da função main o qual apresenta a interface ao usuário na variável "menu" no início do código
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(valor, saldo, extrato)
      
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(valor=valor, saldo=saldo, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES, extrato=extrato)

        elif opcao == "e":
            saldo, extrato = tirar_extrato(contas, saldo, extrato=extrato)
        
        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            #numero_conta = len(contas) + 1
            conta = criar_conta(usuarios, numero_conta, AGENCIA)
        
            if conta:
                contas.append(conta)
                numero_conta += 1
        
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "ex":
            cpf = input("Digite o cpf do usuário para a conta ser excluida: ")
            excluir_conta(cpf, contas)
            
        elif opcao == "exuser":
            cpf = input("Digite o cpf do usuário para o usuário ser excluido: ")
            excluir_usuario(cpf, usuarios)
        

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
main()
