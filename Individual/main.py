from leitura import ler_dados_arquivo, salvar_resultados
from metodo_bisseccao import metodo_bisseccao
from metodo_newton import metodo_newton
from metodo_secante import metodo_secante
from metodo_regula_falsi import metodo_regula_falsi
from metodo_mil import metodo_mil

def main():
    arquivo_entrada = 'entrada.txt'  
    arquivo_saida = 'resultados.txt'  
    
    funcao_str, derivada_str, phi_str, intervalo, x0, x1, tol, max_iter = ler_dados_arquivo(arquivo_entrada)
    a, b = intervalo
    
    resultados = {}
    
    # Execução de todos os métodos
    print("Executando métodos numéricos...")
    
    resultados['MIL'] = metodo_mil(funcao_str, phi_str, x0, tol, max_iter)
    print("✓ MIL concluído")
    
    resultados['Bissecção'] = metodo_bisseccao(funcao_str, a, b, tol, max_iter)
    print("✓ Bissecção concluído")
    
    resultados['Newton'] = metodo_newton(funcao_str, derivada_str, x0, tol, max_iter)
    print("✓ Newton concluído")
    
    resultados['Secante'] = metodo_secante(funcao_str, x0, x1, tol, max_iter)
    print("✓ Secante concluído")
    
    resultados['Regula Falsi'] = metodo_regula_falsi(funcao_str, a, b, tol, max_iter)
    print("✓ Regula Falsi concluído")
    
    # Salvamento dos resultados
    salvar_resultados(arquivo_saida, resultados)
    print(f"\nResultados salvos em '{arquivo_saida}'")

if __name__ == "__main__":
    main()
