from leitura import avaliar_funcao

def metodo_regula_falsi(funcao_str, a, b, tol=1e-6, max_iter=100):
  
    iteracoes = []
    
    for i in range(max_iter):
        fa = avaliar_funcao(funcao_str, a)
        fb = avaliar_funcao(funcao_str, b)
        
        denominador = fb - fa
        if abs(denominador) < 1e-12:
            print(f"AVISO: Regula Falsi parou na iteração {i+1} - denominador muito pequeno")
            break
        
        try:
            x = a - fa * (b - a) / denominador
        except ZeroDivisionError:
            print(f"ERRO: Divisão por zero na Regula Falsi na iteração {i+1}")
            break
            
        fx = avaliar_funcao(funcao_str, x)
        
        erro = abs(fx)
        iteracoes.append((i+1, a, b, x, fx, erro))
        
        if erro < tol:
            break
            
        if fa * fx < 0:
            b = x
        else:
            a = x
        
        # Retorna vazio se atingir 50 iterações ou mais
        if i + 1 >= 50:
            return []
    
    return iteracoes
