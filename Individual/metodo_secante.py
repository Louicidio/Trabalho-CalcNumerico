from leitura import avaliar_funcao

def metodo_secante(funcao_str, x0, x1, tol=1e-6, max_iter=100):
   
    iteracoes = []
    
    for i in range(max_iter):
        fx0 = avaliar_funcao(funcao_str, x0)
        fx1 = avaliar_funcao(funcao_str, x1)
        
        denominador = fx1 - fx0
        if abs(denominador) < 1e-12:
            print(f"AVISO: Secante parou na iteração {i+1} - denominador muito pequeno")
            break
        
        try:
            x_novo = x1 - fx1 * (x1 - x0) / denominador
        except ZeroDivisionError:
            print(f"ERRO: Divisão por zero na Secante na iteração {i+1}")
            break
            
        erro = abs(x_novo - x1)
        
        iteracoes.append((i+1, x0, x1, fx1, erro))
        
        x0, x1 = x1, x_novo  # Atualizar x0 e x1
        
        if erro < tol:
            # Adicionar uma última iteração com o x convergido
            fx1_final = avaliar_funcao(funcao_str, x1)
            iteracoes.append((i+2, x0, x1, fx1_final, 0.0))
            break
        
        # Retorna vazio se atingir 50 iterações
        if i + 1 >= 50:
            return []
    
    return iteracoes
