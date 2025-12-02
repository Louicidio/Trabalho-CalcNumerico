# interface
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from fractions import Fraction
from metodos_eliminacao_gauss import eliminacao_gauss_sem_pivoteamento, eliminacao_gauss_pivoteamento_parcial, eliminacao_gauss_pivoteamento_completo
from metodos_fatoracao import fatoracao_lu, fatoracao_cholesky
from metodos_iterativos import gauss_jacobi, gauss_seidel



def converter_para_float(valor_str):

    valor_str = valor_str.strip()
    
    if '/' in valor_str:
        frac = Fraction(valor_str)
        return float(frac)
    else:
        return float(valor_str)


class InterfaceGrafica:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 2 - Cálculo Numérico")
        self.root.geometry("1000x700")
        
        self.A = None
        self.b = None
        
        self.criar_interface()
    
    def criar_interface(self):
        """Criar a interface gráfica"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== SEÇÃO 1: CARREGAR DADOS =====
        frame_dados = ttk.LabelFrame(main_frame, text="1. Carregar Sistema Linear", padding="10")
        frame_dados.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(frame_dados, text="Carregar A e b juntos", 
                   command=self.carregar_sistema_completo).grid(row=0, column=0, padx=5)
        ttk.Button(frame_dados, text="Carregar A separada", 
                   command=self.carregar_matriz_a).grid(row=0, column=1, padx=5)
        ttk.Button(frame_dados, text="Carregar b separado", 
                   command=self.carregar_vetor_b).grid(row=0, column=2, padx=5)
        ttk.Button(frame_dados, text="Inserir manualmente", 
                   command=self.inserir_manual).grid(row=0, column=3, padx=5)
        
        self.label_status = ttk.Label(frame_dados, text="Nenhum sistema carregado", foreground="red")
        self.label_status.grid(row=1, column=0, columnspan=4, pady=5)
        
        # ===== SEÇÃO 2: SELECIONAR MÉTODO =====
        frame_metodo = ttk.LabelFrame(main_frame, text="2. Selecionar Método", padding="10")
        frame_metodo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.metodo_var = tk.StringVar(value="gauss_sem_piv")
        
        metodos = [
            ("Eliminação de Gauss (sem pivoteamento)", "gauss_sem_piv"),
            ("Pivoteamento Parcial", "gauss_piv_parcial"),
            ("Pivoteamento Completo", "gauss_piv_completo"),
            ("Fatoração LU", "fatoracao_lu"),
            ("Fatoração de Cholesky", "fatoracao_cholesky"),
            ("Método de Gauss-Jacobi", "gauss_jacobi"),
            ("Método de Gauss-Seidel", "gauss_seidel")
        ]
        
        for i, (texto, valor) in enumerate(metodos):
            ttk.Radiobutton(frame_metodo, text=texto, variable=self.metodo_var, 
                           value=valor).grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)
        
        # Parâmetros para métodos iterativos
        frame_params = ttk.Frame(frame_metodo)
        frame_params.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame_params, text="Tolerância:").grid(row=0, column=0, padx=5)
        self.tol_var = tk.StringVar(value="1e-6")
        ttk.Entry(frame_params, textvariable=self.tol_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_params, text="Máx. Iterações:").grid(row=0, column=2, padx=5)
        self.max_iter_var = tk.StringVar(value="1000")
        ttk.Entry(frame_params, textvariable=self.max_iter_var, width=10).grid(row=0, column=3, padx=5)
        
        self.mostrar_passos_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_params, text="Mostrar passos detalhados", 
                       variable=self.mostrar_passos_var).grid(row=0, column=4, padx=10)
        
        # Botão resolver
        ttk.Button(frame_metodo, text="RESOLVER SISTEMA", 
                   command=self.resolver_sistema, 
                   style="Accent.TButton").grid(row=5, column=0, columnspan=2, pady=10)
        
        # ===== SEÇÃO 3: RESULTADOS =====
        frame_resultados = ttk.LabelFrame(main_frame, text="3. Resultados", padding="10")
        frame_resultados.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        self.texto_resultado = scrolledtext.ScrolledText(frame_resultados, wrap=tk.WORD, 
                                                          width=100, height=20, font=("Courier", 9))
        self.texto_resultado.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def carregar_sistema_completo(self):
        """Carregar matriz A e vetor b de um único arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo com sistema completo [A|b]",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Ler arquivo linha por linha e processar frações
                with open(arquivo, 'r') as f:
                    linhas = f.readlines()
                
                dados = []
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):  # Ignorar linhas vazias e comentários
                        valores = linha.split()
                        linha_convertida = [converter_para_float(v) for v in valores]
                        dados.append(linha_convertida)
                
                dados = np.array(dados, dtype=float)
                self.A = dados[:, :-1]
                self.b = dados[:, -1]
                
                n = len(self.b)
                self.label_status.config(
                    text=f"Sistema carregado: {n}x{n} (A) e {n}x1 (b)", 
                    foreground="green"
                )
                messagebox.showinfo("Sucesso", f"Sistema {n}x{n} carregado com sucesso!\nFrações foram convertidas automaticamente.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}\n\nDica: Use frações no formato a/b (exemplo: 1/2, -3/4)")
    
    def carregar_matriz_a(self):
        """Carregar apenas a matriz A"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo com matriz A",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Ler arquivo linha por linha e processar frações
                with open(arquivo, 'r') as f:
                    linhas = f.readlines()
                
                dados = []
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        valores = linha.split()
                        linha_convertida = [converter_para_float(v) for v in valores]
                        dados.append(linha_convertida)
                
                self.A = np.array(dados, dtype=float)
                n = len(self.A)
                
                if self.b is not None and len(self.b) == n:
                    self.label_status.config(
                        text=f"Sistema carregado: {n}x{n} (A) e {n}x1 (b)", 
                        foreground="green"
                    )
                else:
                    self.label_status.config(
                        text=f"Matriz A carregada: {n}x{n}. Carregue vetor b.", 
                        foreground="orange"
                    )
                
                messagebox.showinfo("Sucesso", f"Matriz A {n}x{n} carregada!\nFrações foram convertidas automaticamente.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}\n\nDica: Use frações no formato a/b (exemplo: 1/2, -3/4)")
    
    def carregar_vetor_b(self):
        """Carregar apenas o vetor b"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo com vetor b",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Ler arquivo linha por linha e processar frações
                with open(arquivo, 'r') as f:
                    linhas = f.readlines()
                
                valores = []
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        # Pode ter múltiplos valores na mesma linha ou um por linha
                        for v in linha.split():
                            valores.append(converter_para_float(v))
                
                self.b = np.array(valores, dtype=float)
                n = len(self.b)
                
                if self.A is not None and len(self.A) == n:
                    self.label_status.config(
                        text=f"Sistema carregado: {n}x{n} (A) e {n}x1 (b)", 
                        foreground="green"
                    )
                else:
                    self.label_status.config(
                        text=f"Vetor b carregado: {n}x1. Carregue matriz A.", 
                        foreground="orange"
                    )
                
                messagebox.showinfo("Sucesso", f"Vetor b {n}x1 carregado!\nFrações foram convertidas automaticamente.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}\n\nDica: Use frações no formato a/b (exemplo: 1/2, -3/4)")
    
    def inserir_manual(self):
        """Inserir sistema manualmente"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Inserir Sistema Manualmente")
        dialog.geometry("650x550")
        
        ttk.Label(dialog, text="Digite a matriz aumentada [A|b] (uma linha por linha):").pack(pady=5)
        ttk.Label(dialog, text="Aceita frações no formato a/b\n\nExemplo com números decimais (2x2):\n2 1 5\n1 3 8\n\nExemplo com frações (2x2):\n1/2 1/3 5\n2 -1/4 8", 
                 font=("Courier", 9), justify=tk.LEFT).pack(pady=5)
        
        texto = scrolledtext.ScrolledText(dialog, width=60, height=15)
        texto.pack(pady=10, padx=10)
        
        def processar():
            try:
                linhas = texto.get("1.0", tk.END).strip().split('\n')
                dados = []
                for linha in linhas:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        # Converter cada valor (suporta frações)
                        valores = linha.split()
                        linha_convertida = [converter_para_float(v) for v in valores]
                        dados.append(linha_convertida)
                
                dados = np.array(dados, dtype=float)
                self.A = dados[:, :-1]
                self.b = dados[:, -1]
                
                n = len(self.b)
                self.label_status.config(
                    text=f"Sistema carregado: {n}x{n} (A) e {n}x1 (b)", 
                    foreground="green"
                )
                
                messagebox.showinfo("Sucesso", f"Sistema {n}x{n} inserido com sucesso!\nFrações foram convertidas automaticamente.")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar dados:\n{str(e)}\n\nDica: Use frações no formato a/b (exemplo: 1/2, -3/4)")
        
        ttk.Button(dialog, text="Confirmar", command=processar).pack(pady=10)
    
    def resolver_sistema(self):
        """Resolver o sistema com o método selecionado"""
        if self.A is None or self.b is None:
            messagebox.showerror("Erro", "Carregue um sistema linear primeiro!")
            return
        
        if len(self.A) != len(self.b):
            messagebox.showerror("Erro", "Dimensões incompatíveis entre A e b!")
            return
        
        metodo = self.metodo_var.get()
        mostrar_passos = self.mostrar_passos_var.get()
        
        self.texto_resultado.delete('1.0', tk.END)
        self.texto_resultado.insert(tk.END, "Processando...\n")
        self.root.update()
        
        resultado = None
        
        try:
            if metodo == "gauss_sem_piv":
                resultado = eliminacao_gauss_sem_pivoteamento(
                    self.A, self.b, mostrar_passos
                )
            elif metodo == "gauss_piv_parcial":
                resultado = eliminacao_gauss_pivoteamento_parcial(
                    self.A, self.b, mostrar_passos
                )
            elif metodo == "gauss_piv_completo":
                resultado = eliminacao_gauss_pivoteamento_completo(
                    self.A, self.b, mostrar_passos
                )
            elif metodo == "fatoracao_lu":
                resultado = fatoracao_lu(
                    self.A, self.b, mostrar_passos
                )
            elif metodo == "fatoracao_cholesky":
                resultado = fatoracao_cholesky(
                    self.A, self.b, mostrar_passos
                )
            elif metodo == "gauss_jacobi":
                tol = float(self.tol_var.get())
                max_iter = int(self.max_iter_var.get())
                resultado = gauss_jacobi(
                    self.A, self.b, tol=tol, max_iter=max_iter, mostrar_passos=mostrar_passos
                )
            elif metodo == "gauss_seidel":
                tol = float(self.tol_var.get())
                max_iter = int(self.max_iter_var.get())
                resultado = gauss_seidel(
                    self.A, self.b, tol=tol, max_iter=max_iter, mostrar_passos=mostrar_passos
                )
            
            self.exibir_resultado(resultado, metodo)
            
        except Exception as e:
            self.texto_resultado.delete('1.0', tk.END)
            self.texto_resultado.insert(tk.END, f"ERRO INESPERADO:\n{str(e)}")
    
    def exibir_resultado(self, resultado, metodo):
        """Exibir resultado na interface"""
        self.texto_resultado.delete('1.0', tk.END)
        
        # Título
        nomes_metodos = {
            "gauss_sem_piv": "Eliminação de Gauss (sem pivoteamento)",
            "gauss_piv_parcial": "Eliminação de Gauss com Pivoteamento Parcial",
            "gauss_piv_completo": "Eliminação de Gauss com Pivoteamento Completo",
            "fatoracao_lu": "Fatoração LU",
            "fatoracao_cholesky": "Fatoração de Cholesky",
            "gauss_jacobi": "Método de Gauss-Jacobi",
            "gauss_seidel": "Método de Gauss-Seidel"
        }
        
        self.texto_resultado.insert(tk.END, "="*80 + "\n")
        self.texto_resultado.insert(tk.END, f"MÉTODO: {nomes_metodos[metodo]}\n")
        self.texto_resultado.insert(tk.END, "="*80 + "\n\n")
        
        # Sistema
        self.texto_resultado.insert(tk.END, "Sistema Linear:\n")
        self.texto_resultado.insert(tk.END, f"A = \n{self.A}\n\n")
        self.texto_resultado.insert(tk.END, f"b = {self.b}\n\n")
        self.texto_resultado.insert(tk.END, "-"*80 + "\n\n")
        
        if resultado['sucesso']:
            # Solução
            self.texto_resultado.insert(tk.END, "SOLUÇÃO:\n", "destaque")
            for i, xi in enumerate(resultado['solucao']):
                self.texto_resultado.insert(tk.END, f"x[{i+1}] = {xi:.10f}\n")
            
            self.texto_resultado.insert(tk.END, f"\nVetor solução: {resultado['solucao']}\n\n")
            
            # Informações adicionais
            if resultado['iteracoes'] is not None:
                self.texto_resultado.insert(tk.END, f"Número de iterações: {resultado['iteracoes']}\n")
                if 'erro_final' in resultado:
                    self.texto_resultado.insert(tk.END, f"Erro final: {resultado['erro_final']:.10e}\n")
            
            self.texto_resultado.insert(tk.END, f"Tempo de execução: {resultado['tempo']:.6f} segundos\n\n")
            
            # Verificação
            residuo = np.linalg.norm(np.dot(self.A, resultado['solucao']) - self.b)
            self.texto_resultado.insert(tk.END, f"Resíduo ||Ax - b||: {residuo:.10e}\n\n")
            
            # Passos detalhados
            if resultado['passos']:
                self.texto_resultado.insert(tk.END, "-"*80 + "\n")
                self.texto_resultado.insert(tk.END, "PASSOS DETALHADOS:\n\n")
                self.texto_resultado.insert(tk.END, resultado['passos'])
        
        else:
            # Erro
            self.texto_resultado.insert(tk.END, "ERRO:\n", "erro")
            self.texto_resultado.insert(tk.END, f"{resultado['erro']}\n\n")
            
            if 'solucao_parcial' in resultado:
                self.texto_resultado.insert(tk.END, "Solução parcial (não convergiu):\n")
                self.texto_resultado.insert(tk.END, f"{resultado['solucao_parcial']}\n\n")
            
            if 'iteracoes' in resultado:
                self.texto_resultado.insert(tk.END, f"Iterações realizadas: {resultado['iteracoes']}\n")
            
            self.texto_resultado.insert(tk.END, f"Tempo de execução: {resultado['tempo']:.6f} segundos\n")
        
        # Configurar tags
        self.texto_resultado.tag_config("destaque", foreground="green", font=("Courier", 10, "bold"))
        self.texto_resultado.tag_config("erro", foreground="red", font=("Courier", 10, "bold"))


def main():
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()


if __name__ == "__main__":
    main()
