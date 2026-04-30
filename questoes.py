# questoes.py
BANCO_QUESTOES = [
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
# Adicione estas questões à lista simulado_ancord no seu arquivo questoes.py

novas_questoes = [
    {
        "id": 6,
        "tema": "Mercado de Derivativos",
        "pergunta": "Um investidor que possui uma carteira de ações e teme uma queda no mercado no curto prazo deseja fazer um 'Hedge'. Qual estratégia em derivativos seria a mais adequada?",
        "opcoes": {
            "A": "Comprar opções de compra (Calls)",
            "B": "Vender opções de venda (Puts)",
            "C": "Comprar opções de venda (Puts)",
            "D": "Vender o ativo objeto no mercado à vista"
        },
        "resposta_correta": "C",
        "explicacao": "A compra de uma Put dá ao investidor o direito de vender suas ações por um preço fixado (strike), protegendo-o caso o preço de mercado caia abaixo desse valor."
    },
    {
        "id": 7,
        "tema": "Fundos de Investimento",
        "pergunta": "No que se refere à cobrança de taxa de performance em fundos destinados ao público em geral, é correto afirmar que:",
        "opcoes": {
            "A": "Pode ser cobrada mensalmente, desde que prevista em regulamento",
            "B": "Deve ser cobrada apenas após a dedução de todas as despesas, inclusive impostos",
            "C": "É calculada sobre o que exceder o índice de referência (benchmark), observando o princípio da 'linha d'água'",
            "D": "É proibida para fundos de ações"
        },
        "resposta_correta": "C",
        "explicacao": "A taxa de performance só pode ser cobrada se o valor da cota superar o seu recorde histórico anterior (linha d'água) e após a dedução de todas as taxas (mas antes dos impostos)[cite: 7]."
    },
    {
        "id": 8,
        "tema": "Mercado de Câmbio",
        "pergunta": "O regime cambial adotado atualmente no Brasil, onde o Banco Central intervém ocasionalmente para conter a volatilidade excessiva sem definir uma meta fixa, é o de:",
        "opcoes": {
            "A": "Câmbio Fixo",
            "B": "Flutuação Suja (Dirty Floating)",
            "C": "Bandas Cambiais",
            "D": "Currency Board"
        },
        "resposta_correta": "B",
        "explicacao": "No Brasil vigora o câmbio flutuante, mas com intervenções pontuais do BACEN para manter a funcionalidade do mercado, caracterizando a 'flutuação suja'[cite: 1]."
    },
    {
        "id": 9,
        "tema": "Tributação em Fundos",
        "pergunta": "O mecanismo de 'come-cotas' ocorre nos meses de maio e novembro em quais tipos de fundos?",
        "opcoes": {
            "A": "Fundos de Ações e Fundos de Renda Fixa",
            "B": "Apenas Fundos de Curto Prazo",
            "C": "Fundos de Renda Fixa, Cambiais e Multimercados",
            "D": "Fundos Imobiliários e Fundos de Ações"
        },
        "resposta_correta": "C",
        "explicacao": "O come-cotas é a antecipação semestral do IR. Fundos de Ações e FIIs não sofrem essa incidência antecipada."
    },
    {
        "id": 10,
        "tema": "Atividade do Assessor",
        "pergunta": "De acordo com a Resolução CVM 178, a remuneração recebida pelo Assessor de Investimentos deve ser:",
        "opcoes": {
            "A": "Mantida em sigilo absoluto para evitar conflitos",
            "B": "Divulgada ao cliente de forma transparente, incluindo a forma e o arranjo de remuneração",
            "C": "Cobrada diretamente do cliente via boleto bancário",
            "D": "Fixa e independente do volume de produtos vendidos"
        },
        "resposta_correta": "B",
        "explicacao": "A transparência sobre a remuneração e potenciais conflitos de interesse é uma exigência central da nova regulamentação para proteger o investidor[cite: 2]."
    }
]
