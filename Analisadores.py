from sys import exit

lista_erros_imprimir = [
    '\nErro Léxico na linha {}: Identificador {x} invalido\n',
    '\nErro Semantico na linha {}:\nA variavel {x} já foi declarada\n',
    '\nErro Semantico na linha {}:\nA variavel {x} não foi declarada\n',
    '\nErro Semantico Linha {}:\nNão é possivel fazer uma operação de {x} com {y}\n',
    '\nErro de Sintaxe na linha:{} \nEsperava palavra reservada "var"\n',
    '\nErro de Sintaxe na linha {}: \n Esperava-se o tipo da variavel\n',
    '\nErro de Sintaxe na linha {}: Esperava-se declaração de variavel\n',
    '\nErro de Sintaxe na linha {}: \nEsperava-se atribuição de tipos\n',
    '\nErro de Sintaxe na linha {}: \nEsperava-se palavra reservada "then"\n',
    '\nErro de sintaxe na linha {}: \nEsperava-se uma atribuição\n',
    '\nErro na linha {}: \nExpressão não reconhecida\n',
    '\nErro de Sintaxe na linha {}: \nEsperava-se uma variavel\n',
    '\nErro Sintatico: Não há tokens suficientes\n'

]


class Lexico:
    def __init__(self):
        self.tokens, self.tokens_id, self.tokens_linhas = [], [], []
        self.erros = []
        self.linha = 1
        self.dicionario = {
            'var': 'TOKEN_VAR', 'integer': 'TOKEN_INTEGER', 'real': 'TOKEN_REAL',
            'if': 'TOKEN_IF', 'then': 'TOKEN_THEN', ':': 'TOKEN_DPONTOS',
            ',': 'TOKEN_VIRGULA', ';': 'TOKEN_PTVIRGULA', ':=': 'TOKEN_DPTSIGUAL',
            '+': 'TOKEN_MAIS'
        }

    def gerar_token(self,token):
        try:
            return self.dicionario[token]
        except KeyError:
            if (token.isalnum() and token[0].isalpha()) or verifica_int(token) or verifica_double(token):
                self.tokens_id.append(token)
                return 'TOKEN_ID'
            else:
                self.erros.append((self.linha, token))


    def tokenizar(self, arquivo):
        arquivo = arquivo.replace(':', ' : ')
        arquivo = arquivo.replace(': =', ' := ')
        arquivo = arquivo.replace('+', ' + ')
        arquivo = arquivo.replace(',', ' , ')
        arquivo = arquivo.replace(';', ' ; ')
        arquivo = arquivo.replace('\n', ' \n ')
        arquivo = arquivo.split(' ')

        for palavra in arquivo:
            if palavra == '\n':
                self.linha += 1
            elif palavra != "":
                self.tokens.append(self.gerar_token(palavra))
                self.tokens_linhas.append(self.linha)

        self.tokens_linhas.append(self.linha)

        if len(self.erros) >0:
            erro=lista_erros_imprimir[0]
            for i in self.erros:
                erro = erro.replace('{}', i[0])
                erro = erro.replace('{x}', i[1])

            print(erro)
            raise ValueError(erro)

##FIM DO ANALISADOR LÉXICO

class Semantico:
    def __init__(self):
        self.lista_inserir, self.lista_comparar = [],[]
        self.tab_simb = {}
        self.tipos = {'TOKEN_INTEGER': 'INTEGER', 'TOKEN_REAL': 'REAL'}
        self.bool_erro = False

    def inserir_token(self, token):
        self.lista_inserir.append(token)

    def inserir_tipo(self, tipo):
        for i in self.lista_inserir:
            try:
                var = self.tab_simb[i[0]]
                erro = lista_erros_imprimir[1]
                erro = erro.replace('{}', i[0])
                erro = erro.replace('{x}', var)
                raise ValueError(erro)
            except KeyError:
                self.tab_simb[i[0]] = self.tipos[tipo]
            finally:
                self.lista_inserir = []

    def busca(self, id):
        if verifica_int(id[0]):
            self.tab_simb[id[0]] = 'INTEGER'
            self.lista_comparar.append(('INTEGER', id[1]))
        elif verifica_double(id[0]):
            self.tab_simb[id[0]] = 'REAL'
            self.lista_comparar.append(('REAL', id[1]))
        else:
            try:
                var = self.tab_simb[id[0]]
                self.lista_comparar.append((var, id[1]))
            except:
                erro = lista_erros_imprimir[2]
                erro = erro.replace('{}', str(id[1]))
                erro = erro.replace('{x}', id[0])
                raise ValueError(erro)
        #print(self.lista_comparar)

    def verifica_tipo(self):
        tipoA = self.lista_comparar[0][0]
        for i in self.lista_comparar[1:]:
            if i[0] == tipoA:
                continue
            else:
                erro = lista_erros_imprimir[3]
                erro = erro.replace('{}', str(i[1]))
                erro = erro.replace('{x}', tipoA)
                erro = erro.replace('{y}', str(i[0]))
                raise ValueError(erro)
        self.lista_comparar=[]


##FIM  ANALISADOR SEMANTICO

class Sintatico:
    def __init__(self, tokens, linhas):
        self.tokens_id, self.tokens, self.linhas = [], tokens, linhas
        self.posicao = 0
        self.semantico = Semantico()

    #As proximas funcoes definem as regras da gramatica

    def Z(self):
        retorno = self.I() + self.S()
        if self.semantico.bool_erro:
            exit(0)
        print('Sintaxe Validada\nSemantica Validada')
        return retorno

    def I(self):
        if self.tokens[self.posicao] == 'TOKEN_VAR':
            self.posicao += 1
            return self.D()
        else:
            erro = lista_erros_imprimir[4].replace('{}', str(self.linhas[self.posicao]))
            ValueError(erro)
            print(erro)
            exit(0)

    def D(self):
        retorno = self.L()
        if self.tokens[self.posicao] == 'TOKEN_DPONTOS':
            self.posicao += 1
            retorno += self.K()
            retorno = retorno + self.O()
            return retorno
        else:
            erro = lista_erros_imprimir[5].replace('{}', str(self.linhas[self.posicao]))
            print(erro)
            ValueError(erro)
            exit(0)

    def L(self):
        if self.tokens[self.posicao] == 'TOKEN_ID':
            self.semantico.inserir_token((self.tokens_id[0], self.linhas[self.posicao]))
            self.tokens_id.pop(0)
            self.posicao += 1
            return self.X()
        else:
            erro = lista_erros_imprimir[6].replace('{}', str(self.linhas[self.posicao]))
            print(erro)
            ValueError(erro)
            exit(0)

    def X(self):
        if self.tokens[self.posicao] == 'TOKEN_VIRGULA':
            self.posicao += 1
            return self.L()
        return ""

    def K(self):
        if not (self.tokens[self.posicao] == 'TOKEN_INTEGER' or self.tokens[self.posicao] == 'TOKEN_REAL'):
            erro = lista_erros_imprimir[7].replace('{}', str(self.linhas[self.posicao]))
            print(erro)
            ValueError(erro)
            exit(0)

        self.semantico.inserir_tipo(self.tokens[self.posicao])

        self.posicao += 1
        return ""

    def O(self):
        if self.tokens[self.posicao] == 'TOKEN_PTVIRGULA':
            self.posicao += 1
            return self.D()
        return ""

    def S(self):
        retorno = ""
        if self.tokens[self.posicao] == 'TOKEN_IF':
            self.posicao += 1
            retorno = self.E()
            if self.tokens[self.posicao] == 'TOKEN_THEN':
                self.posicao += 1
                retorno += self.S()
            else:
                erro = lista_erros_imprimir[8].replace('{}', str(self.linhas[self.posicao]))
                print(erro)
                ValueError(erro)
                exit(0)
        elif self.tokens[self.posicao] == 'TOKEN_ID':
            self.semantico.busca((self.tokens_id[0], self.linhas[self.posicao]))
            self.tokens_id.pop(0)
            self.posicao += 1
            if self.tokens[self.posicao] == 'TOKEN_DPTSIGUAL':
                self.posicao += 1
                retorno += self.E()
            else:
                erro = lista_erros_imprimir[9].replace('{}', str(self.linhas[self.posicao]))
                print(erro)
                ValueError(erro)
                exit(0)
        elif self.posicao == len(self.tokens) - 1:
            pass
        else:
            erro = lista_erros_imprimir[10].replace('{}', str(self.linhas[self.posicao]))
            print(erro)
            ValueError(erro)
            exit(0)
        return retorno

    def E(self):
        return self.T() + self.R()

    def T(self):
        if self.tokens[self.posicao] == 'TOKEN_ID':
            self.semantico.busca((self.tokens_id[0], self.linhas[self.posicao]))
            self.tokens_id.pop(0)
            self.posicao += 1
            return ""
        else:
            erro = lista_erros_imprimir[11].replace('{}', str(self.linhas[self.posicao]))
            print(erro)
            ValueError(erro)
            exit(0)

    def R(self):
        if self.posicao < len(self.tokens):
            if self.tokens[self.posicao] == 'TOKEN_MAIS':
                self.posicao += 1
                return self.E()

        self.semantico.verifica_tipo()
        return ""

    def executar(self, tokens_id):
        self.tokens_id = tokens_id
        try:
            self.Z()
        except IndexError:
            erro = lista_erros_imprimir[12]
            print(erro)
            ValueError(erro)






def verifica_int(token):
    if token == int:
        return True
    else:
        return False

def verifica_double(token):
    if token == float:
        return True
    else:
        return False

