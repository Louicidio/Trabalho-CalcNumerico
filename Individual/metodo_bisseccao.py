from leitura import avaliar_funcao

def metodo_bisseccao(funcao_str, a, b, tol=1e-6, max_iter=100):
    
    k = 0
    iteracoes = []
    
    fa = avaliar_funcao(funcao_str, a)
    fb = avaliar_funcao(funcao_str, b)
    
    # Loop principal
    while k < max_iter:
        k += 1
        
        # Calcula o meio
        meio = (a + b) / 2
        fmeio = avaliar_funcao(funcao_str, meio)
        fa = avaliar_funcao(funcao_str, a)
        
        # Adiciona iteração ANTES de atualizar o intervalo
        iteracoes.append((k, a, b, meio, fmeio, abs(b - a)))
        
        # Atualiza o intervalo
        if fa * fmeio < 0:
            b = meio
        else:
            a = meio
        
        # Verifica convergência APÓS atualizar (usa o novo intervalo)
        if abs(b - a) < tol:
            break
        
        if k >= 50:
            return []
    
    return iteracoes
