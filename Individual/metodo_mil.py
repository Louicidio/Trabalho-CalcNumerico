from leitura import avaliar_funcao

def metodo_mil(funcao_str, phi_str, x0, tol=1e-6, max_iter=100):
    
    iteracoes = []
    x = x0
    
    for i in range(max_iter):
        fx = avaliar_funcao(funcao_str, x)
        phi_x = avaliar_funcao(phi_str, x)  # Calcula φ(x) da entrada
        
        x_novo = phi_x  
        erro = abs(x_novo - x)
        
        iteracoes.append((i+1, x, fx, phi_x, erro))
        
        x = x_novo  
        
        if erro < tol:
            fx_final = avaliar_funcao(funcao_str, x)
            phi_x_final = avaliar_funcao(phi_str, x)
            iteracoes.append((i+2, x, fx_final, phi_x_final, 0.0))
            break
        
        if i + 1 >= 50:
            return []
    
    return iteracoes
