from Analisadores import Lexico
from Analisadores import Sintatico

nomeArquivo = input("Digite o nome do arquivo a ser compilado: ")
print(nomeArquivo)

with open(nomeArquivo, 'r') as file:
    try:
        a_lexico = Lexico()
        a_lexico.tokenizar(file.read())
        controle = input("Deseja ver os tokens? Digite S ou N\n")
        if controle == 'S':
            print(a_lexico.tokens)
        a_sintatico = Sintatico(a_lexico.tokens, a_lexico.tokens_linhas)
        a_sintatico.executar(a_lexico.tokens_id)
    except ValueError as error:
        print(error)
    finally:
        file.close()
