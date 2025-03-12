import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

def contar_colaboracoes(arquivo, saida):
    # Dicionários para armazenar contagens e colaboradores
    producoes = defaultdict(list)
    contagem_docentes = defaultdict(int)
    colaboradores_docentes = defaultdict(list)
    detalhes_producoes = defaultdict(list)

    # Ler e processar o arquivo
    with open(arquivo, 'r', encoding='utf-8') as f:
        cabecalho = next(f)  # Ignorar cabeçalho
        
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            
            dados = linha.split('\t')
            if len(dados) != 3:
                continue  # Ignorar linhas inválidas
            
            # Extrair dados formatados
            producao = dados[0].strip()
            autor = dados[1].strip()
            categoria = dados[2].strip()
            
            producoes[producao].append((autor, categoria))

    # Processar cada produção
    for producao, autores in producoes.items():
        categorias = {categoria for _, categoria in autores}
        
        # Verificar se há Docente e colaboradores relevantes
        if 'Docente' in categorias:
            categorias_alvo = {'Discente', 'Egresso', 'Pós-Doc'}
            colaboradores = [
                (autor, categoria) 
                for autor, categoria in autores 
                if categoria in categorias_alvo
            ]
            
            if colaboradores:
                # Listar todos os docentes da produção
                docentes = [
                    autor 
                    for autor, categoria in autores 
                    if categoria == 'Docente'
                ]
                
                # Atualizar contagens e colaboradores para cada docente
                for docente in docentes:
                    contagem_docentes[docente] += 1
                    colaboradores_docentes[docente].extend(colaboradores)
                    
                    # Detalhar cada produção
                    detalhes_producoes[docente].append({
                        'producao': producao,
                        'colaboradores': colaboradores
                    })

    # Gerar saída formatada
    with open(saida, 'w', encoding='utf-8') as f:
        for docente, total in contagem_docentes.items():
            colaboradores = colaboradores_docentes[docente]
            producoes_detalhadas = detalhes_producoes[docente]
            
            # Formatar lista de colaboradores
            lista_colaboradores = [
                f"{nome} ({categoria})" 
                for nome, categoria in colaboradores
            ]
            
            # Juntar itens em uma string
            colaboradores_str = "\n- ".join(lista_colaboradores) or "Nenhum colaborador listado"
            
            f.write(f"\n{docente} (Docente) tem {total} produção(ões) com:\n")
            f.write(f"- {colaboradores_str}\n")
            
            # Detalhar cada produção
            f.write("\nDetalhes das produções:\n")
            for producao in producoes_detalhadas:
                producao_nome = producao['producao']
                producao_colaboradores = producao['colaboradores']
                
                colaboradores_producao_str = "\n- ".join(
                    f"{nome} ({categoria})" 
                    for nome, categoria in producao_colaboradores
                )
                
                f.write(f"\nProdução: {producao_nome}\n")
                f.write(f"Colaboradores: \n- {colaboradores_producao_str}\n")

def buscar_arquivo():
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo de entrada", filetypes=[("Arquivos de texto", "*.txt")])
    entrada.delete(0, tk.END)
    entrada.insert(0, arquivo)

def selecionar_saida():
    saida = filedialog.asksaveasfilename(title="Selecionar arquivo de saída", defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt")])
    saida_entrada.delete(0, tk.END)
    saida_entrada.insert(0, saida)

def executar():
    arquivo = entrada.get()
    saida = saida_entrada.get()
    if arquivo and saida:
        contar_colaboracoes(arquivo, saida)
        resultado_label.config(text="Execução concluída com sucesso!")
    else:
        resultado_label.config(text="Por favor, selecione os arquivos de entrada e saída!")

# Criar janela principal
janela = tk.Tk()
janela.title("Contador de Colaborações")

# Criar botões e entradas
entrada_label = tk.Label(janela, text="Arquivo de entrada:")
entrada_label.pack()
entrada = tk.Entry(janela, width=50)
entrada.pack()
buscar_button = tk.Button(janela, text="Buscar", command=buscar_arquivo)
buscar_button.pack()

saida_label = tk.Label(janela, text="Arquivo de saída:")
saida_label.pack()
saida_entrada = tk.Entry(janela, width=50)
saida_entrada.pack()
selecionar_saida_button = tk.Button(janela, text="Selecionar", command=selecionar_saida)
selecionar_saida_button.pack()

executar_button = tk.Button(janela, text="Executar", command=executar)
executar_button.pack()

resultado_label = tk.Label(janela, text="")
resultado_label.pack()

janela.mainloop()