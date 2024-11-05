import json
from datetime import datetime, timedelta

# Função para verificar conflitos de horários
def verificar_conflito(aulas, nova_aula):
    for aula in aulas:
        if (aula['inicio'] < nova_aula['fim']) and (nova_aula['inicio'] < aula['fim']):
            return True
    return False

# Função para calcular horas trabalhadas e renda
def calcular_renda(aulas, valor_hora):
    total_horas = 0
    total_renda = 0
    for aula in aulas:
        horas = (aula['fim'] - aula['inicio']).total_seconds() / 3600
        total_horas += horas
        total_renda += horas * valor_hora
    return total_horas, total_renda

# Função para calcular eficiência (renda por hora)
def calcular_eficiencia(total_renda, total_horas):
    if total_horas > 0:
        return total_renda / total_horas
    return 0

# Função para exibir os resultados em formato estruturado
def exibir_resultados(tipo, aulas, valor_hora):
    print(f"\n{tipo} - Detalhamento:")
    total_horas, total_renda = calcular_renda(aulas, valor_hora)
    for aula in aulas:
        nome = aula['nome']
        inicio = aula['inicio'].strftime("%Y-%m-%d %H:%M")
        fim = aula['fim'].strftime("%Y-%m-%d %H:%M")
        horas = (aula['fim'] - aula['inicio']).total_seconds() / 3600
        renda = horas * valor_hora
        print(f"  - {nome}: {inicio} às {fim} ({horas:.2f} horas) - R$ {renda:.2f}")
    print(f"Total de horas: {total_horas:.2f} horas")
    print(f"Renda total: R$ {total_renda:.2f}")
    return total_horas, total_renda

# Função para ajustes de horas (acréscimos ou descontos)
def ajustar_horas(aulas, nome_aula, horas_ajustadas, motivo):
    for aula in aulas:
        if aula['nome'] == nome_aula:
            aula['fim'] += timedelta(hours=horas_ajustadas)
            aula['ajustes'].append({
                'motivo': motivo,
                'ajuste': horas_ajustadas,
                'data': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            return aula
    return None

# Carregar ou criar dados de JSON
def carregar_dados_json(arquivo='professor_dados.json'):
    try:
        with open(arquivo, 'r') as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {
            'nome_professor': '',
            'valor_hora': 0,
            'cursos': [],
            'supermodulos': [],
            'workshops': [],
            'ajustes': []
        }
    return dados

def salvar_dados_json(dados, arquivo='professor_dados.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

# Função principal
def main():
    dados = carregar_dados_json()
    
    # Entrada dos dados do professor
    if not dados['nome_professor']:
        dados['nome_professor'] = input("Digite o nome do professor: ")
    if dados['valor_hora'] == 0:
        dados['valor_hora'] = float(input("Digite o valor da hora/aula: "))

    # Entrada de novas aulas
    while True:
        tipo_aula = input("Digite o tipo de aula (curso, supermodulo, workshop) ou 'sair' para terminar: ").lower()
        if tipo_aula == 'sair':
            break

        nome = input("Digite o nome da aula: ")
        inicio = datetime.strptime(input("Digite a data e hora de início (AAAA-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
        fim = inicio
        
        if tipo_aula == 'curso':
            fim += timedelta(hours=3.5)
            if not verificar_conflito(dados['cursos'], {'inicio': inicio, 'fim': fim}):
                dados['cursos'].append({'nome': nome, 'inicio': inicio, 'fim': fim, 'ajustes': []})
            else:
                print("Conflito de horários detectado!")
        elif tipo_aula == 'supermodulo':
            fim += timedelta(hours=3)
            if not verificar_conflito(dados['supermodulos'], {'inicio': inicio, 'fim': fim}):
                dados['supermodulos'].append({'nome': nome, 'inicio': inicio, 'fim': fim, 'ajustes': []})
            else:
                print("Conflito de horários detectado!")
        elif tipo_aula == 'workshop':
            fim += timedelta(hours=2)
            if not verificar_conflito(dados['workshops'], {'inicio': inicio, 'fim': fim}):
                dados['workshops'].append({'nome': nome, 'inicio': inicio, 'fim': fim, 'ajustes': []})
            else:
                print("Conflito de horários detectado!")
        else:
            print("Tipo de aula inválido!")

    # Exibir resultados
    total_horas_cursos, total_renda_cursos = exibir_resultados("Cursos", dados['cursos'], dados['valor_hora'])
    total_horas_supermodulos, total_renda_supermodulos = exibir_resultados("Supermódulos", dados['supermodulos'], dados['valor_hora'])
    total_horas_workshops, total_renda_workshops = exibir_resultados("Workshops", dados['workshops'], dados['valor_hora'])

    # Comparativo de rentabilidade
    print("\nComparativo de Rentabilidade:")
    eficiencia_cursos = calcular_eficiencia(total_renda_cursos, total_horas_cursos)
    eficiencia_supermodulos = calcular_eficiencia(total_renda_supermodulos, total_horas_supermodulos)
    eficiencia_workshops = calcular_eficiencia(total_renda_workshops, total_horas_workshops)
    print(f"Cursos: R$ {total_renda_cursos:.2f} - {total_horas_cursos:.2f} horas - Eficiência: R$ {eficiencia_cursos:.2f}/hora")
    print(f"Supermódulos: R$ {total_renda_supermodulos:.2f} - {total_horas_supermodulos:.2f} horas - Eficiência: R$ {eficiencia_supermodulos:.2f}/hora")
    print(f"Workshops: R$ {total_renda_workshops:.2f} - {total_horas_workshops:.2f} horas - Eficiência: R$ {eficiencia_workshops:.2f}/hora")

    # Salvar dados e ajustes
    salvar_dados_json(dados)

if __name__ == "__main__":
    main()
