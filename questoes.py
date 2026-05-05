# questoes.py

# IMPORTANTE: Este arquivo não deve ter nenhum "import" para o app.py 
# para evitar o erro de importação circular (ImportError).

BANCO_QUESTOES = [
    # --- QUESTÕES EXISTENTES NO SEU CÓDIGO ---
    {
        "id": 11,
        "modulo": "Mercado de Capitais",
        "pergunta": "Qual é o prazo de liquidação física e financeira para operações com ações no mercado à vista da B3?",
        "opcoes": {
            "A": "D+0",
            "B": "D+1",
            "C": "D+2",
            "D": "D+3"
        },
        "resposta_correta": "C",
        "explicacao": "Atualmente, a liquidação das operações no mercado à vista de ações ocorre em dois dias úteis (D+2) após a negociação."
    },
    {
        "id": 12,
        "modulo": "Administração de Risco",
        "pergunta": "O concept de 'VaR' (Value at Risk) é utilizado para medir:",
        "opcoes": {
            "A": "A perda máxima esperada em um determinado horizonte de tempo e nível de confiança",
            "B": "O lucro médio de uma carteira no longo prazo",
            "C": "A probabilidade de uma empresa falir (Default)",
            "D": "A variação do fluxo de caixa operacional"
        },
        "resposta_correta": "A",
        "explicacao": "O VaR quantifica o risco de mercado, indicando a perda potencial máxima sob condições normais."
    },
    {
        "id": 13,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Qual o prazo que as instituições financeiras têm para comunicar ao COAF operações suspeitas de lavagem de dinheiro?",
        "opcoes": {
            "A": "Até o final do mês corrente",
            "B": "24 horas após a decisão de que a operação é suspeita",
            "C": "48 horas úteis após a ocorrência",
            "D": "7 dias corridos"
        },
        "resposta_correta": "B",
        "explicacao": "A comunicação de operações suspeitas deve ser feita sem dar ciência ao cliente, no prazo de 24 horas após a análise interna concluir pela suspeição."
    },
    {
        "id": 14,
        "modulo": "Economia",
        "pergunta": "Em um cenário de apreciação do Real (Dólar em queda), espera-se que ocorra:",
        "opcoes": {
            "A": "Aumento das exportações e queda das importações",
            "B": "Estímulo às importações e maior pressão deflacionária em produtos transacionáveis",
            "C": "Aumento imediato da inflação de custos",
            "D": "Melhora no saldo da balança comercial"
        },
        "resposta_correta": "B",
        "explicacao": "Com o real mais forte, produtos importados ficam mais baratos, o que ajuda a segurar a inflação, mas prejudica a competitividade dos exportadores."
    },
    {
        "id": 15,
        "modulo": "Atividade do AAI",
        "pergunta": "O Assessor de Investimentos pode receber ordens de seus clientes por quais meios?",
        "opcoes": {
            "A": "Apenas por escrito",
            "B": "Apenas verbalmente",
            "C": "Por qualquer meio de comunicação, desde que a instituição contratante possa registrar e arquivar",
            "D": "Somente através de procuração pública"
        },
        "resposta_correta": "C",
        "explicacao": "A regulamentação exige que as ordens sejam passíveis de registro e guarda pela instituição intermediária para fins de auditoria."
    },
    {
        "id": 16,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Qual é a principal função do Conselho Monetário Nacional (CMN)?",
        "opcoes": {
            "A": "Fiscalizar as bolsas de valores",
            "B": "Executar a política monetária",
            "C": "Fixar as diretrizes e normas gerais das políticas monetária, cambial e creditícia",
            "D": "Emitir papel-moeda"
        },
        "resposta_correta": "C",
        "explicacao": "O CMN é o órgão deliberativo máximo do SFN, responsável por estabelecer as diretrizes que outros órgãos devem executar."
    },
    {
        "id": 17,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "A etapa da Lavagem de Dinheiro que visa introduzir o dinheiro 'limpo' no sistema econômico com aparência lícita é:",
        "opcoes": {
            "A": "Colocação",
            "B": "Ocultação",
            "C": "Integração",
            "D": "Fracionamento"
        },
        "resposta_correta": "C",
        "explicacao": "A integração é a última fase, onde o dinheiro retorna à economia formal com aparência de lucro legítimo."
    },
    {
        "id": 18,
        "modulo": "Administração de Risco",
        "pergunta": "O risco de crédito está associado a:",
        "opcoes": {
            "A": "Variação nos preços dos ativos",
            "B": "Possibilidade de não recebimento de juros ou principal por inadimplência do emissor",
            "C": "Dificuldade de vender um ativo pelo seu preço justo",
            "D": "Falhas em processos internos ou sistemas"
        },
        "resposta_correta": "B",
        "explicacao": "Risco de crédito é o risco de contraparte, ou seja, o emissor não honrar o compromisso financeiro assumido."
    },
    {
        "id": 19,
        "modulo": "Mercado de Capitais",
        "pergunta": "As ações que dão direito a voto nas assembleias de uma companhia são as:",
        "opcoes": {
            "A": "Ações Preferenciais (PN)",
            "B": "Ações Ordinárias (ON)",
            "C": "Debêntures",
            "D": "Commercial Papers"
        },
        "resposta_correta": "B",
        "explicacao": "As ações ordinárias conferem ao acionista o direito de voto e participação nas decisões da companhia."
    },
    {
        "id": 20,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Um fundo de investimento que possui a política de aplicar no mínimo 67% do seu patrimônio líquido em ações é classificado como:",
        "opcoes": {
            "A": "Fundo de Renda Fixa",
            "B": "Fundo Multimercado",
            "C": "Fundo de Ações",
            "D": "Fundo Cambial"
        },
        "resposta_correta": "C",
        "explicacao": "De acordo com a CVM, fundos de ações devem manter no mínimo 67% da carteira em ações ou ativos equiparados."
    },
    {
        "id": 21,
        "modulo": "Derivativos",
        "pergunta": "No mercado de opções, o investidor que adquire o direito de comprar um ativo por um preço determinado é o:",
        "opcoes": {
            "A": "Titular de uma opção de compra (Call)",
            "B": "Lançador de uma opção de compra (Call)",
            "C": "Titular de uma opção de venda (Put)",
            "D": "Lançador de uma opção de venda (Put)"
        },
        "resposta_correta": "A",
        "explicacao": "O titular de uma Call paga um prêmio para ter o direito de comprar o ativo objeto."
    },
    {
        "id": 22,
        "modulo": "Mercado Financeiro",
        "pergunta": "Qual a alíquota de Imposto de Renda para operações de Day Trade com ações para pessoas físicas?",
        "opcoes": {
            "A": "15%",
            "B": "20%",
            "C": "22,5%",
            "D": "Isento até R$ 20.000,00"
        },
        "resposta_correta": "B",
        "explicacao": "Diferente das operações comuns (15%), o Day Trade é tributado em 20% e não possui faixa de isenção."
    },
    {
        "id": 23,
        "modulo": "Mercado Financeiro",
        "pergunta": "O plano de previdência onde o Imposto de Renda incide apenas sobre os rendimentos no momento do resgate é o:",
        "opcoes": {
            "A": "PGBL",
            "B": "VGBL",
            "C": "Fundo de Pensão",
            "D": "Tesouro Direto"
        },
        "resposta_correta": "B",
        "explicacao": "O VGBL tributa apenas o ganho de capital, sendo ideal para quem faz declaração simplificada de IR."
    },
    {
        "id": 24,
        "modulo": "Atividade do AAI",
        "pergunta": "O 'Front Running' é uma prática ilícita que consiste em:",
        "opcoes": {
            "A": "Divulgar informações falsas para manipular preços",
            "B": "Operar à frente de uma ordem de um cliente que o profissional sabe que influenciará o preço",
            "C": "Vender ativos sem tê-los em custódia",
            "D": "Atrasar o envio de ordens propositalmente"
        },
        "resposta_correta": "B",
        "explicacao": "Front Running é o uso indevido de informação privilegiada sobre ordens de clientes para benefício próprio."
    },
    {
        "id": 25,
        "modulo": "Economia",
        "pergunta": "O índice de inflação que mede a variação de preços para o consumidor final e é a meta oficial do governo é o:",
        "opcoes": {
            "A": "IGP-M",
            "B": "IPCA",
            "C": "INPC",
            "D": "IPA"
        },
        "resposta_correta": "B",
        "explicacao": "O IPCA é calculado pelo IBGE e serve de referência para o regime de metas de inflação."
    },
    {
        "id": 26,
        "modulo": "Atividade do AAI",
        "pergunta": "É vedado ao Assessor de Investimentos, no exercício de sua atividade:",
        "opcoes": {
            "A": "Entregar material técnico aos clientes",
            "B": "Receber ordens de clientes",
            "C": "Garantir rentabilidade futura aos seus clientes",
            "D": "Prospectar novos investidores"
        },
        "resposta_correta": "C",
        "explicacao": "Garantir rentabilidade é uma prática vedada no mercado financeiro."
    },
    {
        "id": 27,
        "modulo": "Securitização e Recebíveis",
        "pergunta": "Uma debênture incentivada possui como principal característica para a Pessoa Física:",
        "opcoes": {
            "A": "Garantia do FGC",
            "B": "Isenção de Imposto de Renda sobre os rendimentos",
            "C": "Vencimento em até 30 dias",
            "D": "Participação nos lucros da empresa"
        },
        "resposta_correta": "B",
        "explicacao": "Debêntures incentivadas (infraestrutura) oferecem isenção de IR para atrair investidores Pessoa Física."
    },
    {
        "id": 28,
        "modulo": "Administração de Risco",
        "pergunta": "A diversificação de uma carteira de investimentos visa reduzir principalmente o:",
        "opcoes": {
            "A": "Risco Sistemático (Risco de Mercado)",
            "B": "Risco Não Sistemático (Risco Específico)",
            "C": "Risco de Liquidez",
            "D": "Risco Legal"
        },
        "resposta_correta": "B",
        "explicacao": "A diversificação dilui riscos específicos de ativos individuais, mas não elimina o risco do mercado (sistemático)."
    },
    {
        "id": 29,
        "modulo": "Matemática Financeira",
        "pergunta": "O IOF em aplicações de renda fixa incide apenas se o resgate ocorrer em um prazo inferior a:",
        "opcoes": {
            "A": "15 dias",
            "B": "30 dias",
            "C": "60 dias",
            "D": "180 dias"
        },
        "resposta_correta": "B",
        "explicacao": "O IOF segue uma tabela regressiva que chega a zero no 30º dia de aplicação."
    },
    {
        "id": 30,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Em um fundo de investimento, quem é o responsável legal pela guarda dos ativos da carteira?",
        "opcoes": {
            "A": "O Administrador",
            "B": "O Gestor",
            "C": "O Custodiante",
            "D": "O Auditor Independente"
        },
        "resposta_correta": "C",
        "explicacao": "O custodiante é a instituição responsável por guardar e processar os ativos do fundo."
    },
    {
        "id": 31,
        "modulo": "Derivativos",
        "pergunta": "O contrato com liquidação diária de ganhos e perdas é o:",
        "opcoes": {
            "A": "Contrato a Termo",
            "B": "Contrato Futuro",
            "C": "Opção de Compra",
            "D": "Swap"
        },
        "resposta_correta": "B",
        "explicacao": "A existência do ajuste diário é a marca registrada dos contratos futuros na Bolsa."
    },
    {
        "id": 32,
        "modulo": "Mercado Financeiro",
        "pergunta": "No regime regressivo da previdência, a alíquota de 10% é aplicada após:",
        "opcoes": {
            "A": "4 anos",
            "B": "6 anos",
            "C": "8 anos",
            "D": "10 anos"
        },
        "resposta_correta": "D",
        "explicacao": "A tabela regressiva atinge a alíquota mínima de 10% após 10 anos de acumulação."
    },
    {
        "id": 33,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "O crime de lavagem de dinheiro no Brasil é punível com:",
        "opcoes": {
            "A": "Apenas multa administrativa",
            "B": "Reclusão e multa",
            "C": "Perda do registro profissional apenas",
            "D": "Trabalhos comunitários"
        },
        "resposta_correta": "B",
        "explicacao": "A Lei 9.613/98 estabelece penas de reclusão de 3 a 10 anos e multa."
    },
    {
        "id": 34,
        "modulo": "Economia",
        "pergunta": "Para reduzir a liquidez da economia, o Banco Central deve:",
        "opcoes": {
            "A": "Comprar títulos públicos",
            "B": "Reduzir o compulsório",
            "C": "Vender títulos públicos no Open Market",
            "D": "Diminuir a SELIC"
        },
        "resposta_correta": "C",
        "explicacao": "Ao vender títulos, o BC retira dinheiro do sistema e entrega papéis, reduzindo a liquidez."
    },
    {
        "id": 35,
        "modulo": "Atividade do AAI",
        "pergunta": "O Assessor de Investimentos PF pode atuar como preposto de quantas instituições?",
        "opcoes": {
            "A": "Apenas uma (exclusividade)",
            "B": "Até duas",
            "C": "Quantas ele desejar",
            "D": "Apenas instituições do mesmo grupo"
        },
        "resposta_correta": "A",
        "explicacao": "O regime de exclusividade é regra para o AI pessoa física vinculado a uma corretora."
    },
    {
        "id": 36,
        "modulo": "Mercado de Capitais",
        "pergunta": "O 'Tag Along' de 80% para ações ordinárias é garantido por lei para:",
        "opcoes": {
            "A": "Apenas Novo Mercado",
            "B": "Todas as companhias abertas",
            "C": "Apenas estatais",
            "D": "Apenas empresas com lucro"
        },
        "resposta_correta": "B",
        "explicacao": "A Lei das S.A. garante o Tag Along mínimo de 80% para ONs de todas as companhias abertas."
    },
    {
        "id": 37,
        "modulo": "Instituições Financeiras",
        "pergunta": "As Letras de Crédito Imobiliário (LCI) são isentas de IR para:",
        "opcoes": {
            "A": "Pessoas Jurídicas",
            "B": "Pessoas Físicas apenas",
            "C": "Ambos",
            "D": "Ninguém"
        },
        "resposta_correta": "B",
        "explicacao": "A isenção de IR em LCI e LCA é um incentivo exclusivo para Pessoa Física."
    },
    {
        "id": 38,
        "modulo": "Outros Fundos",
        "pergunta": "A portabilidade de um plano de previdência permite:",
        "opcoes": {
            "A": "Resgate isento",
            "B": "Transferir para outro plano sem incidência de IR",
            "C": "Trocar PGBL por VGBL",
            "D": "Sacar rendimentos"
        },
        "resposta_correta": "B",
        "explicacao": "A portabilidade mantém o diferimento fiscal, mas não permite trocar a categoria do plano."
    },
    {
        "id": 39,
        "modulo": "Fundos de Investimentos",
        "pergunta": "O documento que contém as regras e taxas de um fundo é o:",
        "opcoes": {
            "A": "Prospecto",
            "B": "Regulamento",
            "C": "Lâmina",
            "D": "Termo de Adesão"
        },
        "resposta_correta": "B",
        "explicacao": "O regulamento é o contrato principal entre o fundo e os cotistas."
    },
    {
        "id": 40,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Um indivíduo praticou o crime de lavagem de dinheiro através de organização criminosa. Nesse caso, esse indivíduo terá a sua pena:",
        "opcoes": {
            "A": "Aumentada em até 2/3",
            "B": "Reduzida em até 2/3",
            "C": "Aumentada em até 1/3",
            "D": "Aumentada em até 3 anos"
        },
        "resposta_correta": "A",
        "explicacao": "A Lei 9.613/98 prevê aumento de pena de um a dois terços se os crimes forem praticados de forma reiterada ou por intermédio de organização criminosa."
    },
    {
        "id": 41,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Sobre as etapas de lavagem de dinheiro, assinale a alternativa correta:\nI) Aquisição de obras de arte com recursos ilícitos é integração.\nII) Múltiplas transferências e vendas de ativos representa a ocultação.\nIII) Compra de empresas com o saldo das operações é colocação.\nIV) O primeiro depósito em conta é a colocação.",
        "opcoes": {
            "A": "V, F, F, V",
            "B": "F, F, V, F",
            "C": "F, V, F, V",
            "D": "V, F, V, F"
        },
        "resposta_correta": "C",
        "explicacao": "A fase de ocultação (layering) visa dificultar o rastreamento através de múltiplas operações, enquanto o primeiro depósito é a colocação."
    },
    {
        "id": 42,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Segundo a regulamentação, são consideradas Pessoas Expostas Politicamente (PPE), EXCETO:",
        "opcoes": {
            "A": "Presidente de Partido Político",
            "B": "Chefe do Executivo que teve seu mandato finalizado há 7 anos",
            "C": "Chefe do Executivo que teve seu mandato finalizado há 4 anos",
            "D": "Enteada de senador"
        },
        "resposta_correta": "B",
        "explicacao": "A condição de PPE perdura por 5 anos após a data em que a pessoa deixou de exercer o cargo ou função."
    },
    {
        "id": 43,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "As instituições financeiras devem manter os registros das operações dos clientes identificados pelo prazo mínimo de:",
        "opcoes": {
            "A": "5 anos",
            "B": "2 anos",
            "C": "10 anos",
            "D": "20 anos"
        },
        "resposta_correta": "C",
        "explicacao": "Conforme a circular do BACEN e normas da CVM, o prazo de guarda de registros e documentos é de no mínimo 10 anos."
    },
    {
        "id": 44,
        "modulo": "Atividade do Assessor de Investimentos",
        "pergunta": "É requisito mínimo para ser cadastrado como Assessor de Investimentos (AI):",
        "opcoes": {
            "A": "Efetuar o recolhimento de taxa mensal de Assessor",
            "B": "Ter curso superior completo",
            "C": "Ter sido aprovado em exame de qualificação técnica (Ancord)",
            "D": "Possuir certificação CFP"
        },
        "resposta_correta": "C",
        "explicacao": "A aprovação no exame da Ancord é o requisito técnico fundamental para o credenciamento e posterior registro na CVM."
    },
    {
        "id": 45,
        "modulo": "Atividade do Assessor de Investimentos",
        "pergunta": "O Assessor de Investimentos que decide começar a trabalhar com 'Carteira Administrada' ou 'Consultoria' deve:",
        "opcoes": {
            "A": "Manter os dois registros ativos",
            "B": "Solicitar a suspensão temporária",
            "C": "Solicitar o cancelamento do seu registro de AI",
            "D": "Apenas informar à corretora contratante"
        },
        "resposta_correta": "C",
        "explicacao": "As atividades de AI e consultor/gestor são inconfundíveis e a regulação veda o exercício simultâneo, exigindo o cancelamento do registro anterior."
    },
    {
        "id": 46,
        "modulo": "Atividade do Assessor de Investimentos",
        "pergunta": "Sobre a remuneração do Assessor de Investimentos (AI), é correto afirmar:",
        "opcoes": {
            "A": "Recebe salário fixo da corretora",
            "B": "Pode cobrar consultoria diretamente do cliente",
            "C": "A remuneração provém das operações realizadas pelos clientes de sua carteira (comissionamento)",
            "D": "É proibido de receber qualquer tipo de rebate"
        },
        "resposta_correta": "C",
        "explicacao": "O AI é remunerado pela instituição contratante com base na distribuição de produtos e corretagem gerada."
    },
    {
        "id": 47,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Qual o valor máximo da multa pecuniária que pode ser aplicada pelo descumprimento das normas de prevenção à lavagem de dinheiro?",
        "opcoes": {
            "A": "R$ 2.000.000,00",
            "B": "R$ 500.000,00",
            "C": "R$ 20.000.000,00",
            "D": "R$ 1.000.000,00"
        },
        "resposta_correta": "C",
        "explicacao": "A Lei 12.683/12 aumentou o teto da multa para 20 milhões de reais."
    },
    {
        "id": 48,
        "modulo": "Atividade do Assessor de Investimentos",
        "pergunta": "O AI pode utilizar senha e assinatura eletrônica do cliente para realizar investimentos em seu nome, desde que tenha autorização por escrito?",
        "opcoes": {
            "A": "Sim, se for familiar próximo",
            "B": "Sim, com procuração pública",
            "C": "Não, é uma prática vedada em todos os casos",
            "D": "Sim, se o cliente residir no exterior"
        },
        "resposta_correta": "C",
        "explicacao": "É expressamente vedado ao AI a custódia ou o uso de senhas e assinaturas eletrônicas de uso pessoal do cliente."
    },
    {
        "id": 49,
        "modulo": "Lavagem de Dinheiro",
        "pergunta": "Operações em espécie (dinheiro vivo) devem ser obrigatoriamente comunicadas ao COAF a partir de qual valor?",
        "opcoes": {
            "A": "R$ 10.000,00",
            "B": "R$ 50.000,00",
            "C": "R$ 100.000,00",
            "D": "Qualquer valor"
        },
        "resposta_correta": "B",
        "explicacao": "Depósitos, saques ou pagamentos em espécie de valor igual ou superior a R$ 50 mil devem ser comunicados independentemente de suspeita."
    },

    # --- NOVAS QUESTÕES ADICIONADAS (LUCAS SILVA) ---
    {
        "id": 50,
        "modulo": "Securitização de Recebíveis",
        "pergunta": "Em um processo de securitização de recebíveis o pagamento do fluxo financeiro originário é pago para o (a):",
        "opcoes": {
            "A": "Investidor",
            "B": "Securitizadora",
            "C": "Emissor da Dívida",
            "D": "Devedor"
        },
        "resposta_correta": "B",
        "explicacao": "O devedor paga à securitizadora, que então repassa os fluxos aos investidores dos títulos emitidos."
    },
    {
        "id": 51,
        "modulo": "Securitização de Recebíveis",
        "pergunta": "Em uma operação de securitização de recebíveis, uma Sociedade de Propósito Específico (SPE):",
        "opcoes": {
            "A": "Capta recursos por meio da emissão de cotas-parte, com o objetivo de adquirir direitos creditórios",
            "B": "Segrega o risco de crédito dos originadores",
            "C": "Vende recebíveis para comprar debêntures",
            "D": "Capta recurso, por meio da emissão de títulos de crédito, visando adquirir direitos creditórios"
        },
        "resposta_correta": "D",
        "explicacao": "A SPE é o veículo que emite os títulos para o mercado para financiar a compra dos créditos do originador."
    },
    {
        "id": 52,
        "modulo": "Mercado de Capitais",
        "pergunta": "Quanto ao prazo máximo de emissão das Notas Promissórias (Commercial Papers) para S.A. Fechadas e Abertas, respectivamente:",
        "opcoes": {
            "A": "180 dias e 360 dias",
            "B": "360 dias para ambas",
            "C": "180 dias para ambas",
            "D": "360 dias e 180 dias"
        },
        "resposta_correta": "B",
        "explicacao": "Atualmente, o prazo máximo para Notas Promissórias de oferta pública é de 360 dias, independente se a S.A é aberta ou fechada."
    },
    {
        "id": 53,
        "modulo": "Mercado de Capitais",
        "pergunta": "Ordem discricionária é aquela que:",
        "opcoes": {
            "A": "Estabelece um limite ao preço de negociação",
            "B": "Envolve obrigatoriamente compra e venda",
            "C": "Não possui qualquer limitação quanto a preço",
            "D": "É gerada por administradores de carteira ou representantes de mais de um investidor"
        },
        "resposta_correta": "D",
        "explicacao": "A ordem discricionária permite que o profissional decida o momento e preço da execução em nome do cliente."
    },
    {
        "id": 54,
        "modulo": "Mercado de Capitais",
        "pergunta": "Uma empresa deseja emitir títulos na bolsa da Alemanha (Europa). Essa empresa deveria optar por:",
        "opcoes": {
            "A": "ADR",
            "B": "BDR",
            "C": "GDR",
            "D": "Debêntures"
        },
        "resposta_correta": "C",
        "explicacao": "GDR (Global Depositary Receipts) são recibos de ações emitidos em mercados fora do país de origem e dos EUA."
    },
    {
        "id": 55,
        "modulo": "Mercado de Capitais",
        "pergunta": "O período de uma oferta pública em que se coleta as intenções de aquisição e o preço que os interessados estão dispostos a pagar é o:",
        "opcoes": {
            "A": "Front Runner",
            "B": "Chinese Wall",
            "C": "Bookbuilding",
            "D": "Churning"
        },
        "resposta_correta": "C",
        "explicacao": "O Bookbuilding serve para 'sentir' o mercado e definir o preço final de uma emissão."
    },
    {
        "id": 56,
        "modulo": "Mercado de Capitais",
        "pergunta": "Sobre o Juros Sobre Capital Próprio (JSCP), assinale a alternativa correta:",
        "opcoes": {
            "A": "São isentos de IR para pessoa física",
            "B": "Possuem IR conforme tabela regressiva",
            "C": "São os lucros da companhia isentos de IR",
            "D": "Originam-se de lucros retidos e possuem IR com alíquota única de 15%"
        },
        "resposta_correta": "D",
        "explicacao": "Diferente dos dividendos, o JSCP é tributado na fonte em 15% para o investidor pessoa física."
    },
    {
        "id": 57,
        "modulo": "Mercado de Capitais",
        "pergunta": "Uma ordem de venda que será executada somente se o ativo atingir um determinado preço (para limitar perdas) é chamada de:",
        "opcoes": {
            "A": "Stop",
            "B": "A Mercado",
            "C": "Tudo Ou Nada",
            "D": "Europeia"
        },
        "resposta_correta": "A",
        "explicacao": "Ordens Stop são gatilhos de segurança usados para proteção de capital ou garantia de lucro."
    },
    {
        "id": 58,
        "modulo": "Mercado de Capitais",
        "pergunta": "Em uma Bonificação de Ações:",
        "opcoes": {
            "A": "O acionista tem o direito de comprar novas ações",
            "B": "O acionista recebe gratuitamente um número de novas ações",
            "C": "A empresa capta novos recursos financeiros",
            "D": "O valor nominal das ações é reduzido"
        },
        "resposta_correta": "B",
        "explicacao": "Bonificação é a distribuição gratuita de ações resultante da capitalização de reservas de lucros."
    },
    {
        "id": 59,
        "modulo": "Mercado de Capitais",
        "pergunta": "Qual a diferença básica entre um bônus de subscrição e o direito de subscrição?",
        "opcoes": {
            "A": "O bônus tem validade e o direito não",
            "B": "O direito é dado a qualquer investidor e o bônus não",
            "C": "O direito é exclusivo do acionista, o bônus pode ser emitido para terceiros",
            "D": "Ambos não possuem prazo de validade"
        },
        "resposta_correta": "C",
        "explicacao": "Direitos de subscrição nascem do aumento de capital para acionistas atuais. Bônus são títulos negociáveis emitidos pela companhia."
    },
    {
        "id": 60,
        "modulo": "Mercado de Capitais",
        "pergunta": "Nas operações de Day Trade com ações, as alíquotas de IR total e retido na fonte (dedo-duro) são, respectivamente:",
        "opcoes": {
            "A": "20% e 0,005%",
            "B": "15% e 0,005%",
            "C": "15% e 1%",
            "D": "20% e 1%"
        },
        "resposta_correta": "D",
        "explicacao": "No Day Trade, o IR total é 20% e a retenção na fonte (dedo-duro) é de 1% sobre o lucro."
    }
]
