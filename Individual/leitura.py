import math

def avaliar_funcao(funcao_str, x):
    expr = funcao_str.replace('x', str(x))
    
    expr = expr.replace('e', str(math.e))
    expr = expr.replace('pi', str(math.pi))
    
    expr = expr.replace('sin', 'math.sin')
    expr = expr.replace('cos', 'math.cos')
    expr = expr.replace('tan', 'math.tan')
    expr = expr.replace('asin', 'math.asin') 
    expr = expr.replace('acos', 'math.acos')  
    expr = expr.replace('atan', 'math.atan')  
    
    # IMPORTANTE: ordem importa! log10 e log2 antes de log, ln por último
    expr = expr.replace('log10', 'math.log10') 
    expr = expr.replace('log2', 'math.log2')
    # Por padrão, 'log' sem sufixo é log base 10 em muitos livros    
    expr = expr.replace('log', 'math.log10')
    # ln (logaritmo natural) deve ser substituído POR ÚLTIMO para não conflitar
    expr = expr.replace('ln', 'math.log')      
    
    expr = expr.replace('exp', 'math.exp')      
    expr = expr.replace('sqrt', 'math.sqrt')   
    expr = expr.replace('abs', 'math.fabs')    
    
    expr = expr.replace('^', '**')              
    
    try:
        return eval(expr)
    except:
        return float('inf')

def derivada_numerica(funcao_str, x, h=1e-8):
    fx_mais = avaliar_funcao(funcao_str, x + h)
    fx_menos = avaliar_funcao(funcao_str, x - h)
    return (fx_mais - fx_menos) / (2 * h)

def ler_dados_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]
    
    funcao_str = linhas[0]
    derivada_str = linhas[1] if len(linhas) > 1 else ""
    phi_str = linhas[2] if len(linhas) > 2 else ""  # Lê a função phi
    intervalo = [float(x) for x in linhas[3].split()] if len(linhas) > 3 else [0, 1]
    x0 = float(linhas[4]) if len(linhas) > 4 else 0.5
    x1 = float(linhas[5]) if len(linhas) > 5 else 1.0
    tol = float(linhas[6]) if len(linhas) > 6 else 1e-6
    max_iter = int(linhas[7]) if len(linhas) > 7 else 100
    
    return funcao_str, derivada_str, phi_str, intervalo, x0, x1, tol, max_iter

def salvar_resultados(nome_arquivo, resultados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        
        # Tabela comparativa dos resultados finais
        f.write("TABELA DE COMPARAÇÃO\n")
        f.write("Método\t\t| Valor Final\t| Erro Final\t| f(x) Final\t| Iterações\n")
        f.write("-" * 65 + "\n")
        
        for metodo, dados in resultados.items():
            if dados is None or len(dados) == 0:
                f.write(f"{metodo:<12}\t| nulo\t\t| nulo\t\t| nulo\t\t| nulo\n")
            else:
                ultima_iteracao = dados[-1]
                if metodo in ['Bissecção', 'Regula Falsi']:
                    it, a, b, x_final, fx_final, erro_final = ultima_iteracao
                elif metodo in ['Newton', 'MIL']:
                    it, x_final, fx_final, dfx, erro_final = ultima_iteracao
                elif metodo == 'Secante':
                    it, x_prev, x_final, fx_final, erro_final = ultima_iteracao
                f.write(f"{metodo:<12}\t| {x_final:.6f}\t| {erro_final:.6f}\t| {fx_final:.6f}\t| {it}\n")
        f.write("-" * 65 + "\n\n")
        
        # Saida com todas as iterações
        for metodo, dados in resultados.items():
            f.write(f"Método: {metodo}\n")
            f.write("-" * 40 + "\n")
            
            if dados is None or len(dados) == 0:
                f.write("Método não convergiu (>= 50 iterações)\n\n")
                continue
            
            if metodo in ['Bissecção', 'Regula Falsi']:
                f.write("Iteração\ta\t\tb\t\tx\t\tf(x)\t\tErro\n")
                for iteracao in dados:
                    it, a, b, x, fx, erro = iteracao
                    f.write(f"{it}\t\t{a:.6f}\t{b:.6f}\t{x:.6f}\t{fx:.6f}\t{erro:.6f}\n")
            elif metodo == 'MIL':
                f.write("Iteração\tx\t\tf(x)\t\tφ(x)\t\tErro\n")
                for iteracao in dados:
                    it, x, fx, phi_x, erro = iteracao
                    f.write(f"{it}\t\t{x:.6f}\t{fx:.6f}\t{phi_x:.6f}\t{erro:.6f}\n")
            elif metodo == 'Newton':
                f.write("Iteração\tx\t\tf(x)\t\tf'(x)\t\tErro\n")
                for iteracao in dados:
                    it, x, fx, dfx, erro = iteracao
                    f.write(f"{it}\t\t{x:.6f}\t{fx:.6f}\t{dfx:.6f}\t{erro:.6f}\n")
            elif metodo == 'Secante':
                f.write("Iteração\tx(n-1)\t\tx(n)\t\tf(x(n))\t\tErro\n")
                for iteracao in dados:
                    it, x_prev, x, fx, erro = iteracao
                    f.write(f"{it}\t\t{x_prev:.6f}\t{x:.6f}\t{fx:.6f}\t{erro:.6f}\n")
            
            f.write("\n")
