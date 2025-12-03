import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from metodo_bisseccao import metodo_bisseccao
from metodo_newton import metodo_newton
from metodo_secante import metodo_secante
from metodo_regula_falsi import metodo_regula_falsi
from metodo_mil import metodo_mil
from leitura import salvar_resultados
from datetime import datetime

class InterfaceCalculoNumerico:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("800x800")
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.main_frame, text="Função f(x):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.funcao_entry = ttk.Entry(self.main_frame, width=50)
        self.funcao_entry.grid(row=0, column=1, pady=5, padx=5)
        self.funcao_entry.insert(0, "x**3 - 9*x + 3")
        
        ttk.Label(self.main_frame, text="Derivada f'(x):").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        derivada_frame = ttk.Frame(self.main_frame)
        derivada_frame.grid(row=1, column=1, pady=5, sticky=tk.W)
        
        self.derivada_entry = ttk.Entry(derivada_frame, width=40)
        self.derivada_entry.pack(side=tk.LEFT, padx=5)
        self.derivada_entry.insert(0, "3*x**2 - 9")
        
        # Checkbox para derivada automática
        self.auto_derivada_var = tk.BooleanVar(value=False)
        self.auto_derivada_check = ttk.Checkbutton(
            derivada_frame, 
            text="Calcular automaticamente", 
            variable=self.auto_derivada_var,
            command=self.toggle_derivada_auto
        )
        self.auto_derivada_check.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.main_frame, text="Função φ(x) (MIL):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phi_entry = ttk.Entry(self.main_frame, width=50)
        self.phi_entry.grid(row=2, column=1, pady=5, padx=5)
        self.phi_entry.insert(0, "(9*x - 3)**(1/3)")
        
        intervalo_frame = ttk.Frame(self.main_frame)
        intervalo_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Label(intervalo_frame, text="Intervalo [a, b]:").pack(side=tk.LEFT, padx=5)
        self.a_entry = ttk.Entry(intervalo_frame, width=10)
        self.a_entry.pack(side=tk.LEFT, padx=5)
        self.a_entry.insert(0, "0")
        
        ttk.Label(intervalo_frame, text="até").pack(side=tk.LEFT)
        self.b_entry = ttk.Entry(intervalo_frame, width=10)
        self.b_entry.pack(side=tk.LEFT, padx=5)
        self.b_entry.insert(0, "1")
        
        valores_frame = ttk.Frame(self.main_frame)
        valores_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Label(valores_frame, text="x0:").pack(side=tk.LEFT, padx=5)
        self.x0_entry = ttk.Entry(valores_frame, width=10)
        self.x0_entry.pack(side=tk.LEFT, padx=5)
        self.x0_entry.insert(0, "0.5")
        
        ttk.Label(valores_frame, text="x1:").pack(side=tk.LEFT, padx=5)
        self.x1_entry = ttk.Entry(valores_frame, width=10)
        self.x1_entry.pack(side=tk.LEFT, padx=5)
        self.x1_entry.insert(0, "1.0")
        
        param_frame = ttk.Frame(self.main_frame)
        param_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Label(param_frame, text="Tolerância:").pack(side=tk.LEFT, padx=5)
        self.tol_entry = ttk.Entry(param_frame, width=10)
        self.tol_entry.pack(side=tk.LEFT, padx=5)
        self.tol_entry.insert(0, "1e-6")
        
        ttk.Label(param_frame, text="Iterações máx:").pack(side=tk.LEFT, padx=5)
        self.max_iter_entry = ttk.Entry(param_frame, width=10)
        self.max_iter_entry.pack(side=tk.LEFT, padx=5)
        self.max_iter_entry.insert(0, "100")
        
        ttk.Button(self.main_frame, text="Calcular", command=self.calcular).grid(row=6, column=0, columnspan=2, pady=20)
        
        # Criar abas para resultados
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=7, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.aba_final = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_final, text="Resultados Finais")
        
        ttk.Label(self.aba_final, text="Comparação dos Resultados:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.resultado_final_text = scrolledtext.ScrolledText(self.aba_final, width=100, height=25, font=('Courier', 9))
        self.resultado_final_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.aba_iteracoes = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_iteracoes, text="Iterações Detalhadas")
        
        ttk.Label(self.aba_iteracoes, text="Histórico de Iterações:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.resultado_iteracoes_text = scrolledtext.ScrolledText(self.aba_iteracoes, width=100, height=25, font=('Courier', 9))
        self.resultado_iteracoes_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    def toggle_derivada_auto(self):
        if self.auto_derivada_var.get():
            self.derivada_entry.delete(0, tk.END)
            self.derivada_entry.insert(0, "auto")
            self.derivada_entry.config(state='disabled')
        else:
            self.derivada_entry.config(state='normal')
            if self.derivada_entry.get() == "auto":
                self.derivada_entry.delete(0, tk.END)
        
    def calcular(self):
        try:
            funcao_str = self.funcao_entry.get()
            derivada_str = self.derivada_entry.get()
            phi_str = self.phi_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())
            
            # Executar métodos
            resultados = {}
            resultados['MIL'] = metodo_mil(funcao_str, phi_str, x0, tol, max_iter)
            resultados['Bissecção'] = metodo_bisseccao(funcao_str, a, b, tol, max_iter)
            resultados['Newton'] = metodo_newton(funcao_str, derivada_str, x0, tol, max_iter)
            resultados['Secante'] = metodo_secante(funcao_str, x0, x1, tol, max_iter)
            resultados['Regula Falsi'] = metodo_regula_falsi(funcao_str, a, b, tol, max_iter)
            
            # Formatar resultados
            self.mostrar_resultados_finais(resultados)
            self.mostrar_iteracoes_detalhadas(resultados)
            
            # Salvar resultados em arquivo txt
            self.salvar_resultados_interface(resultados, funcao_str, derivada_str, phi_str, a, b, x0, x1, tol, max_iter)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {str(e)}")
    
    def mostrar_resultados_finais(self, resultados):
        self.resultado_final_text.delete(1.0, tk.END)
        
        # Cabeçalho
        header = f"{'Método':<15} | {'Valor Final':<12} | {'Erro Final':<12} | {'f(x) Final':<12} | {'Iterações':<10}\n"
        self.resultado_final_text.insert(tk.END, header)
        self.resultado_final_text.insert(tk.END, "=" * 85 + "\n")
        
        # Resultados de cada método
        for metodo, dados in resultados.items():
            if dados is None or len(dados) == 0:
                linha = f"{metodo:<15} | {'nulo':<12} | {'nulo':<12} | {'nulo':<12} | {'>=50':<10}\n"
            else:
                ultima_iteracao = dados[-1]
                if metodo in ['Bissecção', 'Regula Falsi']:
                    it, a, b, x_final, fx_final, erro_final = ultima_iteracao
                elif metodo in ['Newton', 'MIL']:
                    it, x_final, fx_final, dfx, erro_final = ultima_iteracao
                elif metodo == 'Secante':
                    it, x_prev, x_final, fx_final, erro_final = ultima_iteracao
                
                linha = f"{metodo:<15} | {x_final:<12.6f} | {erro_final:<12.6e} | {fx_final:<12.6e} | {it:<10}\n"
            
            self.resultado_final_text.insert(tk.END, linha)
        
        self.resultado_final_text.insert(tk.END, "=" * 85 + "\n")
    
    def mostrar_iteracoes_detalhadas(self, resultados):
        self.resultado_iteracoes_text.delete(1.0, tk.END)
        
        for metodo, dados in resultados.items():
            self.resultado_iteracoes_text.insert(tk.END, f"\n{'='*80}\n")
            self.resultado_iteracoes_text.insert(tk.END, f"MÉTODO: {metodo}\n")
            self.resultado_iteracoes_text.insert(tk.END, f"{'='*80}\n")
            
            if dados is None or len(dados) == 0:
                self.resultado_iteracoes_text.insert(tk.END, "⚠ Método não convergiu (>= 50 iterações)\n\n")
                continue
            
            # Formatar iterações de acordo com o método
            if metodo in ['Bissecção', 'Regula Falsi']:
                header = f"{'It':<5} | {'a':<12} | {'b':<12} | {'x':<12} | {'f(x)':<12} | {'Erro':<12}\n"
                self.resultado_iteracoes_text.insert(tk.END, header)
                self.resultado_iteracoes_text.insert(tk.END, "-" * 80 + "\n")
                
                for iteracao in dados:
                    it, a, b, x, fx, erro = iteracao
                    linha = f"{it:<5} | {a:<12.6f} | {b:<12.6f} | {x:<12.6f} | {fx:<12.6e} | {erro:<12.6e}\n"
                    self.resultado_iteracoes_text.insert(tk.END, linha)
                    
            elif metodo == 'MIL':
                header = f"{'It':<5} | {'x':<12} | {'f(x)':<12} | {'φ(x)':<12} | {'Erro':<12}\n"
                self.resultado_iteracoes_text.insert(tk.END, header)
                self.resultado_iteracoes_text.insert(tk.END, "-" * 65 + "\n")
                
                for iteracao in dados:
                    it, x, fx, phi_x, erro = iteracao
                    linha = f"{it:<5} | {x:<12.6f} | {fx:<12.6e} | {phi_x:<12.6f} | {erro:<12.6e}\n"
                    self.resultado_iteracoes_text.insert(tk.END, linha)
                    
            elif metodo == 'Newton':
                header = f"{'It':<5} | {'x':<12} | {'f(x)':<12} | {'f\'(x)':<12} | {'Erro':<12}\n"
                self.resultado_iteracoes_text.insert(tk.END, header)
                self.resultado_iteracoes_text.insert(tk.END, "-" * 65 + "\n")
                
                for iteracao in dados:
                    it, x, fx, dfx, erro = iteracao
                    linha = f"{it:<5} | {x:<12.6f} | {fx:<12.6e} | {dfx:<12.6f} | {erro:<12.6e}\n"
                    self.resultado_iteracoes_text.insert(tk.END, linha)
                    
            elif metodo == 'Secante':
                header = f"{'It':<5} | {'x(n-1)':<12} | {'x(n)':<12} | {'f(x(n))':<12} | {'Erro':<12}\n"
                self.resultado_iteracoes_text.insert(tk.END, header)
                self.resultado_iteracoes_text.insert(tk.END, "-" * 65 + "\n")
                
                for iteracao in dados:
                    it, x_prev, x, fx, erro = iteracao
                    linha = f"{it:<5} | {x_prev:<12.6f} | {x:<12.6f} | {fx:<12.6e} | {erro:<12.6e}\n"
                    self.resultado_iteracoes_text.insert(tk.END, linha)
            
            self.resultado_iteracoes_text.insert(tk.END, "\n")
    
    def salvar_resultados_interface(self, resultados, funcao_str, derivada_str, phi_str, a, b, x0, x1, tol, max_iter):
        try:
            # Nome de arquivo fixo (sempre o mesmo)
            nome_arquivo = "resultados_interface.txt"
            
            # Salvar usando a função existente
            salvar_resultados(nome_arquivo, resultados)
            
            # Adicionar informações adicionais no início do arquivo
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                conteudo_original = f.read()
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("RESULTADOS DOS MÉTODOS NUMÉRICOS - INTERFACE\n")
                f.write("=" * 80 + "\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                f.write("PARÂMETROS DE ENTRADA:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Função f(x):       {funcao_str}\n")
                f.write(f"Derivada f'(x):    {derivada_str}\n")
                f.write(f"Função φ(x) (MIL): {phi_str}\n")
                f.write(f"Intervalo [a, b]:  [{a}, {b}]\n")
                f.write(f"Valores iniciais:  x0 = {x0}, x1 = {x1}\n")
                f.write(f"Tolerância:        {tol}\n")
                f.write(f"Iterações máx:     {max_iter}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(conteudo_original)
            
            print(f" Resultados salvos em: {nome_arquivo}")
            
        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao salvar arquivo: {str(e)}\nOs resultados continuam visíveis na interface.")

def main():
    root = tk.Tk()
    app = InterfaceCalculoNumerico(root)
    root.mainloop()

if __name__ == "__main__":
    main()