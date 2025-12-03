from leitura import avaliar_funcao, derivada_numerica

def metodo_newton(funcao_str, derivada_str, x0, tol=1e-6, max_iter=100):
    
    iteracoes = []
    x = x0
    usa_derivada_numerica = (not derivada_str or derivada_str.lower() == "auto")
    
    for i in range(max_iter):
        fx = avaliar_funcao(funcao_str, x)
        
        # Calcular derivada: analítica ou numérica
        if usa_derivada_numerica:
            dfx = derivada_numerica(funcao_str, x)
        else:
            dfx = avaliar_funcao(derivada_str, x)
        
        if abs(dfx) < 1e-12:
            break
            
        x_novo = x - fx / dfx
        erro = abs(x_novo - x)
        
        # Registra: (iteração, x_novo, f(x_antes), f'(x_antes), erro)
        # O x_novo é o resultado da iteração, que será usado na próxima
        iteracoes.append((i+1, x_novo, fx, dfx, erro))
        
        # Atualiza x para a próxima iteração
        x = x_novo
        
        # Verifica convergência
        if erro < tol:
            break
        
        if i + 1 >= 50:
            return []
    
    return iteracoes
