# questoes.py

simulado_ancord = [
    {
        "id": 1,
        "tema": "Prevenção à Lavagem de Dinheiro",
        "pergunta": "Um cliente realiza depósitos em espécie de R$ 9.000,00 em cinco dias consecutivos para evitar a notificação automática de depósitos acima de R$ 50.000,00. Essa prática é conhecida como:",
        "opcoes": {
            "A": "Tipificação",
            "B": "Estruturação (Smurfing)",
            "C": "Integração",
            "D": "Ocultação"
        },
        "resposta_correta": "B",
        "explicacao": "A estruturação consiste em fracionar valores para burlar os limites de comunicação automática aos órgãos de controle."
    },
    {
        "id": 2,
        "tema": "Economia",
        "pergunta": "Quando o Comitê de Política Monetária (COPOM) decide elevar a taxa SELIC meta, o objetivo principal é:",
        "opcoes": {
            "A": "Aumentar a liquidez do mercado financeiro",
            "B": "Estimular o consumo das famílias",
            "C": "Combater a inflação através da contração da demanda agregada",
            "D": "Reduzir o custo da dívida pública"
        },
        "resposta_correta": "C",
        "explicacao": "A alta da SELIC encarece o crédito e incentiva a poupança, reduzindo a pressão sobre os preços[cite: 1]."
    },
    {
        "id": 3,
        "tema": "Ética e Conduta",
        "pergunta": "De acordo com as normas de conduta, o Assessor de Investimentos deve priorizar as ordens de quais clientes?",
        "opcoes": {
            "A": "Dos clientes que pagam as maiores taxas de corretagem",
            "B": "Dos clientes que possuem maior patrimônio investido",
            "C": "Não há prioridade; deve-se seguir o princípio da equidade e ordem de chegada",
            "D": "As ordens próprias do assessor devem ser executadas antes das dos clientes"
        },
        "resposta_correta": "C",
        "explicacao": "O AI deve agir com boa fé e transparência, tratando todos os clientes com equidade, sem privilégios baseados em receita."
    },
    {
        "id": 4,
        "tema": "Lavagem de Dinheiro",
        "pergunta": "Na lavagem de dinheiro, a etapa que consiste em dificultar o rastreamento dos recursos através de diversas transações financeiras complexas é a:",
        "opcoes": {
            "A": "Colocação",
            "B": "Ocultação (Camuflagem/Layering)",
            "C": "Integração",
            "D": "Peculato"
        },
        "resposta_correta": "B",
        "explicacao": "A ocultação é a segunda fase, onde se busca quebrar a cadeia de evidências sobre a origem do dinheiro."
    },
    {
        "id": 5,
        "tema": "Economia - Índices",
        "pergunta": "Qual índice de inflação é utilizado pelo Conselho Monetário Nacional (CMN) para o estabelecimento da meta de inflação no Brasil?",
        "opcoes": {
            "A": "IGP-M",
            "B": "IPA",
            "C": "IPCA",
            "D": "INPC"
        },
        "resposta_correta": "C",
        "explicacao": "O IPCA, calculado pelo IBGE, é o índice oficial para o regime de metas de inflação do país[cite: 1]."
    }
]

# Exemplo de uso simples:
if __name__ == "__main__":
    for q in simulado_ancord:
        print(f"Questão {q['id']} - {q['tema']}")
        print(q['pergunta'])
        for letra, opcao in q['opcoes'].items():
            print(f"{letra}) {opcao}")
        print("-" * 30)
