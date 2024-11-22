import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def calcular_limite():
    try:
        funcao_str = entrada_funcao.get()
        ponto_str = entrada_ponto.get()
        x = sp.symbols('x')
        funcao = sp.sympify(funcao_str)
        if ponto_str.lower() == '∞':
            ponto = sp.oo
        else:
            ponto = float(ponto_str)
        limite = sp.limit(funcao, x, ponto)
        resultado.config(text=f"Limite: {limite}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no cálculo do limite: {e}")
        resultado.config(text="Limite: Erro")

def gerar_grafico():
    try:
        funcao_str = entrada_funcao.get()
        x = sp.symbols('x')
        funcao = sp.sympify(funcao_str)
        
        limite_esquerdo = float(entrada_limite_esquerdo.get())
        limite_direito = float(entrada_limite_direito.get())
        
        x_vals = np.linspace(limite_esquerdo, limite_direito, 400)
        y_vals = np.array([float(funcao.subs(x, val).evalf()) if funcao.subs(x, val).is_real else np.nan for val in x_vals])
        
        top_level_window = tk.Toplevel(janela)
        top_level_window.title(f"Gráfico de {funcao_str}")
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x_vals, y_vals, label=str(funcao))
        
        ponto_str = entrada_ponto.get()
        if ponto_str.lower() != '∞':
            ponto = float(ponto_str)
            limite = sp.limit(funcao, x, ponto)
            y_ponto = funcao.subs(x, ponto)
            if y_ponto.is_real:
                ax.scatter([ponto], [float(y_ponto.evalf())], color='red', zorder=5, label=f"Limite em x={ponto}")
        
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_xlim([x_vals.min() - 1, x_vals.max() + 1])
        ax.set_ylim([y_vals.min() - 1, y_vals.max() + 1])
        
        ax.set_title(f"Gráfico de {funcao_str}")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=top_level_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        # Exibe uma mensagem de erro com o motivo específico
        print(f"Erro ao gerar o gráfico: {e}")
        messagebox.showerror("Erro", f"Erro ao gerar o gráfico. Motivo: {e}")

def mostrar_exemplo():
    exemplos = [
        {"funcao": "(x**2 - 1)/(x - 1)", "ponto": "1"},
        {"funcao": "sin(x)/x", "ponto": "0"},
        {"funcao": "(3*x**2 + 5)/(x**2 - 2)", "ponto": "∞"},
        {"funcao": "x/(x+1)", "ponto": "∞"},
        {"funcao": "x**2 - 4", "ponto": "2"},
        {"funcao": "(x**2 - 2*x)/(x - 1)", "ponto": "1"},
        {"funcao": "exp(x)", "ponto": "∞"},
        {"funcao": "(x**3 - 8)/(x - 2)", "ponto": "2"},
        {"funcao": "1/x", "ponto": "0"}
    ]
    exemplo = random.choice(exemplos)
    entrada_funcao.delete(0, tk.END)
    entrada_funcao.insert(0, exemplo["funcao"])
    entrada_ponto.delete(0, tk.END)
    entrada_ponto.insert(0, exemplo["ponto"])

janela = tk.Tk()
janela.title("Calculadora de Limites e Gráficos")

frame_principal = tk.Frame(janela)
frame_principal.pack(padx=10, pady=10)

rotulo_instrucao = tk.Label(frame_principal, text="Digite a função (em termos de x)")
rotulo_instrucao.grid(row=0, column=0, columnspan=2, pady=5)

entrada_funcao = tk.Entry(frame_principal, width=40)
entrada_funcao.grid(row=1, column=0, columnspan=2, pady=5)

rotulo_ponto = tk.Label(frame_principal, text="Digite o ponto para calcular o limite")
rotulo_ponto.grid(row=2, column=0, columnspan=2, pady=5)

entrada_ponto = tk.Entry(frame_principal, width=40)
entrada_ponto.grid(row=3, column=0, columnspan=2, pady=5)

rotulo_escala = tk.Label(frame_principal, text="Defina a escala do gráfico (limites)")
rotulo_escala.grid(row=4, column=0, columnspan=2, pady=5)

rotulo_limite_esquerdo = tk.Label(frame_principal, text="Domínio: esquerdo (x)")
rotulo_limite_esquerdo.grid(row=5, column=0, pady=5)

entrada_limite_esquerdo = tk.Entry(frame_principal, width=10)
entrada_limite_esquerdo.grid(row=5, column=1, pady=5)
entrada_limite_esquerdo.insert(0, "-10")

rotulo_limite_direito = tk.Label(frame_principal, text="Domínio: direito (x)")
rotulo_limite_direito.grid(row=6, column=0, pady=5)

entrada_limite_direito = tk.Entry(frame_principal, width=10)
entrada_limite_direito.grid(row=6, column=1, pady=5)
entrada_limite_direito.insert(0, "10")

botao_calcular = tk.Button(frame_principal, text="Calcular Limite", command=calcular_limite, bg="lightgray")
botao_calcular.grid(row=9, column=0, pady=10)

botao_grafico = tk.Button(frame_principal, text="Gerar Gráfico", command=gerar_grafico, bg="lightgray")
botao_grafico.grid(row=9, column=1, pady=10)

botao_exemplo = tk.Button(frame_principal, text="Mostrar Exemplo", command=mostrar_exemplo, bg="lightgray")
botao_exemplo.grid(row=10, column=0, columnspan=2, pady=10)

resultado = tk.Label(frame_principal, text="Limite: ", font=("Arial", 12))
resultado.grid(row=11, column=0, columnspan=2, pady=10)

janela.mainloop()
