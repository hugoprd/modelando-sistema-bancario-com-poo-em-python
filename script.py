import textwrap;
from abc import ABC, abstractmethod;
from datetime import datetime;

# ============================================================ CLASSES ============================================================
class Cliente():
    def __init__(self, endereco, contas, cpf):
        self.endereco = endereco;
        self.contas = [];

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta);        

    def adicionar_conta(self, conta):
        self._contas.append(conta);

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco);
        self.cpf = cpf;
        self.nome = nome;
        self.data_nascimento = data_nascimento;

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0;
        self.numero = numero;
        self.agencia = "0001";
        self.cliente = cliente;
        self.historico = Historico();

    @property
    def saldo(self):
        return self._saldo;

    @property
    def numero(self):
        return self._numero;

    @property
    def agencia(self):
        return self._agencia;

    @property
    def cliente(self):
        return self._cliente;

    @property
    def historico(self):
        return self._historico;

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente);

    def sacar(self, valor):
        saldo = self._saldo;

        if valor > saldo:
            print("\nVoce nao possui saldo suficiente. Tente novamente.");
        elif valor > 0:
            self._saldo -= valor;
            print("\nSaque realizado.");
    
            return True;
        else:
            print("\nOperacao falhou. Tente novamente.");

            return False;

    def depositar(self, valor):
        saldo = self._saldo;

        if valor <= 0:
            print("\nTentativa invalida. Pode apenas depositar mais de R$0.00.");
        
            return False;
        else:
            self._saldo += valor;
            print("\nDeposito realizado.");

            return True;

class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, numero, cliente):
        super().__init__(numero, cliente);
        self.limite = 500;
        self.limite_saques = 3;

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        );

        if valor > self._limite:
            print("\nO valor nao pode exceder o limite. Tente novamente mais tarde.");
        elif numero_saques >= self._limite_saques:
            print("\nNumero maximo de saques excedido.");
        else:
            return super().sacar(valor);

    def __str__(self):
        return f"""\n
                Agencia:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
        """;

class Historico:
    def __init__(self):
        self.transacoes = [];
    
    @property
    def transacoes(self):
        return self._transacoes;

    def adicionar_transacao(self, transacao):
        self.transacao.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        );

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass;

    @classmethod
    def registrar(self, conta):
        pass;

class Deposito:
    def __init__(self, valor):
        self.valor = valor;

    @property
    def valor(self):
        return self._valor;

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor);

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self);

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor;

    @property
    def valor(self):
        return self._valor;

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor);

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self);

# ============================================================ VALIDACOES ============================================================
#ver se já existe esse cliente
def verificar_cliente(cpf, clientes):
    clientes_verificados = [cliente for cliente in clientes if cliente.cpf == cpf];
    return clientes_verificados[0] if clientes_verificados else None;

#ver se a string nao possui apenas o mesmo numero
def verificar_numeros(cpf):
    for i in len(cpf):
        if cpf[i] != cpf[0]:
            return False;

    return True;

#ver se existe um cpf igual ao que esta tentando se cadastrar na lista de usuarios cadastrados
#def cpf_igual(cpf):
#    if len(lista_usuarios) == 0:
#        return False;
#    for i in len(lista_usuarios):
#        if lista_usuarios[i].cpf == cpf:
#            return True;
#
#    return False;

#verificar a primeira parte do cpf
def verificar_parte1(cpf1, verificador):
    num = 0;
    aux = 10;
    verN = 0;

    for i in 9:
        numero += int(cpf1[i])*aux;

        aux -= 1;

    resto = numero % 11;

    if resto == 1 or resto == 0:
        verN = 0;
    elif resto >= 2 and resto <= 10:
        verN = 11 - resto;

    return verN == verificador[0];

#verificar a segunda parte do cpf
def verificar_parte2(cpf2, verificador):
    numero = 0;
    aux = 11;
    verN = 0;

    for i in 10:
        numero += int(cpf2[i])*aux;

        aux -= 1;

    resto = numero % 11;

    if resto == 1 or resto == 0:
        verN = 0;
    elif resto >=2 and resto <=10:
        verN = 11 - resto;

    return verN == verificador[1];

#validar cpf da tentativa de cadastro
def validar_cpf(r_cpf):
    if len(r_cpf) == 11:
        if r_cpf.isdigit():
            if verificar_numeros(r_cpf) == False:
                #if cpf_igual(r_cpf) == False:
                    parte1 = r_cpf[1, 10];
                    parte2 = r_cpf[1, 11];
                    verificador_cpf = r_cpf[9, 12];

                    if verificar_parte1(parte1, verificador_cpf) and verificar_parte2(parte2, verificador_cpf):
                        return r_cpf;
                    else:
                        print("\nCPF invalido. Tente novamente.");
                #else:
                #    print(f"\nCPF {r_cpf} ja cadastrado. Tente novamente.");
            else:
                print("\nCPF invalido. Tente novamente.");
        else:
            print("\nCPF invalido. Tente novamente.");
    else:
        print("\nCPF invalido. Tente novamente.");

#validar nome da tentativa de cadastro
def validar_nome(r_nome):
    if not r_nome.isdigit():
        return r_nome;
    else:
        print("\nNome invalido. Tente novamente.");

#validar data de nascimento da tentativa de cadastro
def validar_data(r_data):
    if len(r_data) == 8:
        dia = r_data[1:2];
        mes = r_data[3:4];
        ano = r_data[5:8];

        data += "/".join(dia);
        data += "/".join(mes);
        data += "/".join(ano);

        return data;
    else:
        print("Data invalida. Tente novamente.");

# ============================================================ MENU ============================================================
def menu_geral():
    menu = """\n
        =============== MENU ===============
        [1]\tDepositar
        [2]\tSacar
        [3]\tExtrato
        [4]\tNova Conta
        [5]\tListar Contas
        [6]\tNovo Usuario
        [S]\tSair
        ==> """
    
    return input(textwrap.dedent(menu));

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente nao possui conta");
        return;
    
    return cliente.contas[0];

# ============================================================ TRANSACOES ============================================================
def depositar(clientes):
    resposta_cpf = input("\nDigite seu CPF: ");
    cliente = verificar_cliente(resposta_cpf, clientes);

    if not cliente:
        print("\nCliente nao encontrado.");
        return;

    valor = float(input("\nDigite a quantidade que voce quer depositar: "));
    transacao = Deposito(valor);
    conta = recuperar_conta_cliente(cliente);

    if not conta:
        return;

    cliente.realizar_transacao(conta, transacao);

def sacar(clientes):
    resposta_cpf = input("\nDigite seu CPF: ");
    cliente = verificar_cliente(resposta_cpf, clientes);

    if not cliente:
        print("\nCliente nao encontrado.");
        return;

    valor = float(input("\nDigite a quantidade que voce quer sacar: "));
    transacao = Saque(valor);

    conta = recuperar_conta_cliente(cliente);
    if not conta:
        return;

    cliente.realizar_transacao(conta, transacao);

# ============================================================ EXTRATO ============================================================
def exibir_extrato(clientes):
    resposta_cpf = input("\nDigite o seu CPF: ");
    cliente = verificar_cliente(resposta_cpf, clientes);

    if not cliente:
        print("\nCliente nao encontrado.");
        return;

    conta = recuperar_conta_cliente(cliente);
    if not conta:
        return;

    print("\n======== EXTRATO ========");
    transacoes = conta.historico.transacoes;

    extrato = ""
    if not transacoes:
        extrato = "\nNao houve movimentacoes.";
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\tR${transacao["valor"]:.2f}.";

    print(extrato);
    print(f"\nSaldo:\tR${conta.saldo:.2f}.");
    print("\n=========================");

# ============================================================ CONTA ============================================================
def criar_cliente(clientes):
    resposta_cpf = input("\nDigite o seu CPF: ");
    cliente = verificar_cliente(resposta_cpf);

    if cliente:
        print("\nEsse CPF ja foi cadastrado.");
        return;

    resposta_nome = input("\nDigite o seu nome: ");
    resposta_data = input("\nDigite sua data de nascimento (dd/mm/aaaa): ");
    resposta_endereco = input("\nDigite o seu endereco (logradouro, numero - bairro - cidade/sigla estado): ");

    cliente = PessoaFisica(cpf = resposta_cpf, nome = resposta_nome, data_nascimento = resposta_data, endereco = resposta_endereco);

    clientes.append(cliente);
    print("\nCliente criado com sucesso.");

def criar_conta(numero_conta, clientes, contas):
    resposta_cpf = input("\nDigite seu CPF: ");
    cliente = verificar_cliente(resposta_cpf, clientes);

    if not cliente:
        print("\nCliente nao encontrado.");
        return;

    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta);
    contas.append(conta);
    cliente.contas.append(conta);

    print("\nConta criada com sucesso.");

def listar_contas(contas):
    for conta in contas:
        print(textwrap.dedent(str(conta)));

# ============================================================ MAIN ============================================================
def main():
    clientes = [];
    contas = [];

    while True:
        resp = menu_geral();

        if resp == 1:
            depositar(clientes);
        elif resp == 2:
            sacar(clientes);
        elif resp == 3:
            exibir_extrato(clientes);
        elif resp == 4:
            criar_cliente(clientes);
        elif resp == 5:
            numero_conta = len(contas) +1;
            criar_conta(numero_conta, clientes, contas);
        elif resp == 6:
            listar_contas(contas);
        elif resp == "S" or resp == "s":
            break;
        else:
            print("\nResposta invalida. Tente novamente.");

main();