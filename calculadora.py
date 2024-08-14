import tkinter as tk
from tkinter import messagebox

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")

        self.resultado = None
        self.operacao = None
        self.entrada_atual = ""
        self.porcentagem = False
        
        self.setup_ui()
        self.root.bind('<Key>', self.teclado)

    def setup_ui(self):
        # Tela de entrada
        self.tela = tk.Entry(self.root, font=("Arial", 14), borderwidth=2, relief="solid", justify="right")
        self.tela.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.tela.focus_set()

        # Configuração dos botões
        botoes = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0, 2), (',', 4, 2), ('+', 4, 3),
            ('%', 5, 0), ('C', 5, 1), ('Del', 5, 2), ('<--', 5, 3), ('=', 6, 0, 4)
        ]
        
        for item in botoes:
            texto = item[0]
            linha = item[1]
            coluna = item[2]
            colspan = item[3] if len(item) == 4 else 1
            tk.Button(self.root, text=texto, font=("Arial", 14), command=lambda t=texto: self.acao(t), width=4).grid(row=linha, column=coluna, columnspan=colspan, padx=5, pady=5)

    def acao(self, valor):
        if valor.isdigit() or valor == ',':
            self.entrada_atual += valor
            self.tela.delete(0, tk.END)
            self.tela.insert(tk.END, self.entrada_atual)
            self.porcentagem = False
        elif valor in "+-*/":
            if self.entrada_atual or self.resultado is not None:
                if self.resultado is not None and self.entrada_atual:
                    self.calcular()
                elif self.resultado is None:
                    self.resultado = float(self.entrada_atual.replace(',', '.')) if self.entrada_atual else 0
                self.operacao = valor
                self.entrada_atual = ""
                self.porcentagem = False
            else:
                messagebox.showerror("Erro", "Insira um número antes de selecionar uma operação.")
        elif valor == "=":
            if self.operacao and self.entrada_atual:
                if self.porcentagem:
                    self.calcular_porcentagem()
                else:
                    self.calcular()
                self.operacao = None
                self.entrada_atual = self.formatar_resultado(self.resultado)
                self.tela.delete(0, tk.END)
                self.tela.insert(tk.END, self.entrada_atual)
                self.resultado = float(self.entrada_atual.replace(',', '.'))
                self.entrada_atual = ""
            else:
                messagebox.showerror("Erro", "Complete a operação antes de pressionar '='.")
        elif valor == "C":
            self.tela.delete(0, tk.END)
            self.resultado = None
            self.operacao = None
            self.entrada_atual = ""
            self.porcentagem = False
        elif valor == "Del":
            self.tela.delete(0, tk.END)
            self.resultado = None
            self.operacao = None
            self.entrada_atual = ""
        elif valor == "<--":
            self.entrada_atual = self.entrada_atual[:-1]
            self.tela.delete(0, tk.END)
            self.tela.insert(tk.END, self.entrada_atual)
        elif valor == "%":
            if self.entrada_atual:
                if self.resultado is not None:
                    self.porcentagem = True
                    self.entrada_atual = str(float(self.entrada_atual.replace(',', '.')))
                    self.tela.delete(0, tk.END)
                    self.tela.insert(tk.END, self.entrada_atual + "%")
                else:
                    messagebox.showerror("Erro", "Nenhum valor para calcular porcentagem.")
            else:
                messagebox.showerror("Erro", "Insira um número para calcular porcentagem.")

    def calcular(self):
        try:
            valor_atual = float(self.entrada_atual.replace(',', '.'))
            if self.operacao:
                if self.operacao == "+":
                    self.resultado += valor_atual
                elif self.operacao == "-":
                    self.resultado -= valor_atual
                elif self.operacao == "*":
                    self.resultado *= valor_atual
                elif self.operacao == "/":
                    if valor_atual != 0:
                        self.resultado /= valor_atual
                    else:
                        messagebox.showerror("Erro", "Divisão por zero!")
                        self.resultado = None
                        return
            self.entrada_atual = self.formatar_resultado(self.resultado)
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida!")
            self.resultado = None
            self.entrada_atual = ""

    def calcular_porcentagem(self):
        try:
            porcentagem = float(self.entrada_atual.replace(',', '.')) / 100
            if self.operacao:
                if self.operacao == "+":
                    self.resultado += self.resultado * porcentagem
                elif self.operacao == "-":
                    self.resultado -= self.resultado * porcentagem
                elif self.operacao == "*":
                    self.resultado *= porcentagem
                elif self.operacao == "/":
                    if porcentagem != 0:
                        self.resultado /= porcentagem
                    else:
                        messagebox.showerror("Erro", "Divisão por zero!")
                        self.resultado = None
                        return
            self.entrada_atual = self.formatar_resultado(self.resultado)
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida!")
            self.resultado = None
            self.entrada_atual = ""

    def formatar_resultado(self, resultado):
        if resultado is not None:
            resultado_str = str(int(resultado))  # Remove casas decimais desnecessárias
            return resultado_str.replace('.', ',')
        return "0"

    def teclado(self, evento):
        tecla = evento.keysym
        
        if tecla in '0123456789':
            self.acao(tecla)
        elif tecla == 'Return':  # Enter
            self.acao('=')
        elif tecla == 'Escape':  # Esc
            self.acao('C')
        elif tecla == 'Delete':  # Delete
            self.acao('Del')
        elif tecla == 'BackSpace':  # Backspace
            self.acao('<--')
        elif tecla == 'plus':  # +
            self.acao('+')
        elif tecla == 'minus':  # -
            self.acao('-')
        elif tecla == 'asterisk':  # *
            self.acao('*')
        elif tecla == 'slash':  # /
            self.acao('/')
        elif tecla == 'percent':  # %
            self.acao('%')
        elif tecla in ['period', 'comma']:  # . ou ,
            self.acao(',')
        else:
            print(f"Tecla '{tecla}' não está mapeada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
