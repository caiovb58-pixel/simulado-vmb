# questoes.py

# IMPORTANTE: Este arquivo não deve ter nenhum "import" para o app.py 
# para evitar o erro de importação circular (ImportError).

BANCO_QUESTOES = [
    # --- QUESTÕES ORIGINAIS DO SEU CÓDIGO ---
    {
        "id": 11,
        "modulo": "Mercado de Capitais",
        "pergunta": "Qual é o prazo de liquidação física e financeira para operações com ações no mercado à vista da B3?",
        "opcoes": {"A": "D+0", "B": "D+1", "C": "D+2", "D": "D+3"},
        "resposta_correta": "C",
        "explicacao": "Atualmente, a liquidação das operações no mercado à vista de ações ocorre em dois dias úteis (D+2) após a negociação."
    },
    {
        "id": 12,
        "modulo": "Administração de Risco",
        "pergunta": "O conceito de 'VaR' (Value at Risk) é utilizado para medir:",
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
        "opcoes": {"A": "Colocação", "B": "Ocultação", "C": "Integração", "D": "Fracionamento"},
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
        "opcoes": {"A": "15%", "B": "20%", "C": "22,5%", "D": "Isento até R$ 20.000,00"},
        "resposta_correta": "B",
        "explicacao": "Diferente das operações comuns (15%), o Day Trade é tributado em 20% e não possui faixa de isenção."
    },
    {
        "id": 23,
        "modulo": "Mercado Financeiro",
        "pergunta": "O plano de previdência onde o Imposto de Renda incide apenas sobre os rendimentos no momento do resgate é o:",
        "opcoes": {"A": "PGBL", "B": "VGBL", "C": "Fundo de Pensão", "D": "Tesouro Direto"},
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
        "opcoes": {"A": "IGP-M", "B": "IPCA", "C": "INPC", "D": "IPA"},
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
        "opcoes": {"A": "15 dias", "B": "30 dias", "C": "60 dias", "D": "180 dias"},
        "resposta_correta": "B",
        "explicacao": "O IOF segue uma tabela regressiva que chega a zero no 30º dia de aplicação."
    },
    {
        "id": 30,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Em um fundo de investimento, quem é o responsável legal pela guarda dos ativos da carteira?",
        "opcoes": {"A": "O Administrador", "B": "O Gestor", "C": "O Custodiante", "D": "O Auditor Independente"},
        "resposta_correta": "C",
        "explicacao": "O custodiante é a instituição responsável por guardar e processar os ativos do fundo."
    },
    {
        "id": 31,
        "modulo": "Derivativos",
        "pergunta": "O contrato com liquidação diária de ganhos e perdas é o:",
        "opcoes": {"A": "Contrato a Termo", "B": "Contrato Futuro", "C": "Opção de Compra", "D": "Swap"},
        "resposta_correta": "B",
        "explicacao": "A existência do ajuste diário é a marca registrada dos contratos futuros na Bolsa."
    },
    {
        "id": 32,
        "modulo": "Mercado Financeiro",
        "pergunta": "No regime regressivo da previdência, a alíquota de 10% é aplicada após:",
        "opcoes": {"A": "4 anos", "B": "6 anos", "C": "8 anos", "D": "10 anos"},
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
        "opcoes": {"A": "Pessoas Jurídicas", "B": "Pessoas Físicas apenas", "C": "Ambos", "D": "Ninguém"},
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
        "opcoes": {"A": "Prospecto", "B": "Regulamento", "C": "Lâmina", "D": "Termo de Adesão"},
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
        "opcoes": {"A": "V, F, F, V", "B": "F, F, V, F", "C": "F, V, F, V", "D": "V, F, V, F"},
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
        "opcoes": {"A": "5 anos", "B": "2 anos", "C": "10 anos", "D": "20 anos"},
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
        "opcoes": {"A": "R$ 2.000.000,00", "B": "R$ 500.000,00", "C": "R$ 20.000.000,00", "D": "R$ 1.000.000,00"},
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
        "opcoes": {"A": "R$ 10.000,00", "B": "R$ 50.000,00", "C": "R$ 100.000,00", "D": "Qualquer valor"},
        "resposta_correta": "B",
        "explicacao": "Depósitos, saques ou pagamentos em espécie de valor igual ou superior a R$ 50 mil devem ser comunicados independentemente de suspeita."
    },
    {
        "id": 50,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Com relação ao Fundo Multimercado, assinale a alternativa correta:",
        "opcoes": {
            "A": "Deve investir no mínimo 50% em crédito privado",
            "B": "Deve investir no mínimo 67% em ações",
            "C": "Investe em vários fatores de risco, sem o compromisso de alocação mínima em nenhum desses mercados",
            "D": "Investe em vários fatores de risco, porém, com concentração mínima em renda fixa"
        },
        "resposta_correta": "C",
        "explicacao": "Fundos Multimercado possuem política de investimento que envolve vários fatores de risco, sem obrigatoriedade de concentração em um mercado específico."
    },
    {
        "id": 51,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Um determinado fundo de investimento possui 75% em Renda Variável, 25% em Renda Fixa e até 40% em derivativos. Esse fundo:",
        "opcoes": {
            "A": "Deve ser indicado para um investidor que busca baixo risco",
            "B": "Deve ser indicado para um investidor que busca um fundo de renda fixa",
            "C": "Tem possibilidade de ter perdas superiores ao seu patrimônio líquido",
            "D": "É um fundo de Renda Fixa Simples"
        },
        "resposta_correta": "C",
        "explicacao": "O uso de derivativos para alavancagem permite que as perdas excedam o patrimônio líquido do fundo."
    },
    {
        "id": 52,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Sobre as operações ex-pit, é correto afirmar que:",
        "opcoes": {
            "A": "Reduzem a liquidez do mercado a termo",
            "B": "Não possibilitam a precificação de posições",
            "C": "São submetidas à interferência do mercado",
            "D": "Constituem negócios realizados fora do pit de negociação ou pregão, de uma bolsa"
        },
        "resposta_correta": "D",
        "explicacao": "Operações ex-pit são negócios fechados fora do ambiente de negociação centralizado da bolsa."
    },
    {
        "id": 53,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Um fundo de investimentos constituído sob a forma de condomínio fechado permite o resgate de cotas:",
        "opcoes": {
            "A": "De acordo com as regras do regulamento",
            "B": "Após o primeiro ano",
            "C": "Ao término do prazo de duração do fundo",
            "D": "Se houver concordância de 2/3 dos cotistas"
        },
        "resposta_correta": "C",
        "explicacao": "Em condomínios fechados, as cotas só são resgatadas ao término do prazo de duração do fundo."
    },
    {
        "id": 54,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Tipo de Fundo de Investimento que dispensa o Termo de Adesão e também o API:",
        "opcoes": {
            "A": "Fundo de Renda Fixa",
            "B": "Fundo de Renda Fixa Simples",
            "C": "Fundo Cambial",
            "D": "Fundo Referenciado"
        },
        "resposta_correta": "B",
        "explicacao": "O Fundo de Renda Fixa Simples é destinado a investidores iniciantes e dispensa esses documentos por sua política conservadora."
    },
    {
        "id": 55,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Para ser um Fundo de Curto Prazo (Receita Federal), o mesmo deve ter:",
        "opcoes": {
            "A": "Prazo médio da carteira de até 60 dias",
            "B": "Prazo médio da carteira de até 365 dias",
            "C": "Prazo médio da carteira de até 375 dias",
            "D": "Prazo médio da carteira de até 180 dias"
        },
        "resposta_correta": "B",
        "explicacao": "Para fins fiscais, fundos de curto prazo possuem carteira com títulos de prazo médio igual ou inferior a 365 dias."
    },
    {
        "id": 56,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Quem é o responsável pela definição da Política de Investimentos de um fundo?",
        "opcoes": {
            "A": "Diretor Administrativo",
            "B": "Cotistas",
            "C": "Gestor",
            "D": "Administrador"
        },
        "resposta_correta": "D",
        "explicacao": "A responsabilidade pela elaboração do regulamento e definição da política de investimento é do Administrador."
    },
    {
        "id": 57,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Metodologia utilizada para a cobrança da Taxa de Performance:",
        "opcoes": {
            "A": "Linha D'água",
            "B": "Chinese Wall",
            "C": "Day Trade",
            "D": "Taxa Over"
        },
        "resposta_correta": "A",
        "explicacao": "O método da Linha D'água garante que a taxa de performance só seja cobrada sobre o que exceder o valor máximo anterior da cota."
    },
    {
        "id": 58,
        "modulo": "Fundos de Investimentos",
        "pergunta": "São considerados investidores profissionais aqueles com investimentos financeiros superiores a:",
        "opcoes": {
            "A": "R$ 1.000.000,00",
            "B": "R$ 10.000.000,00",
            "C": "R$ 5.000.000,00",
            "D": "R$ 50.000.000,00"
        },
        "resposta_correta": "B",
        "explicacao": "Investidores profissionais são aqueles que atestam essa condição e possuem mais de R$ 10 milhões em investimentos."
    },
    {
        "id": 59,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Sobre a taxa de administração em um fundo de investimento:",
        "opcoes": {
            "A": "Cobrada apenas se houver lucro",
            "B": "É devolvida após um período",
            "C": "É um dos fatores que afeta o valor da cota",
            "D": "Cobrada apenas no resgate"
        },
        "resposta_correta": "C",
        "explicacao": "A taxa de administração é provisionada diariamente e reduz o valor da cota divulgado."
    },
    {
        "id": 60,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Um Fundo Cambial deve investir qual percentual mínimo em ativos ligados à variação de moeda estrangeira?",
        "opcoes": {"A": "67%", "B": "95%", "C": "80%", "D": "100%"},
        "resposta_correta": "C",
        "explicacao": "Conforme a CVM, fundos cambiais devem manter pelo menos 80% da carteira em ativos que busquem acompanhar a variação de moedas estrangeiras."
    },
    {
        "id": 61,
        "modulo": "Fundos de Investimentos",
        "pergunta": "É característica de um Fundo com Gestão Ativa:",
        "opcoes": {
            "A": "Replicar um benchmark",
            "B": "Superar a rentabilidade de um benchmark",
            "C": "Ser mais defensivo",
            "D": "Focar apenas em Hedge"
        },
        "resposta_correta": "B",
        "explicacao": "Na gestão ativa, o gestor busca retornos acima do índice de referência (benchmark)."
    },
    {
        "id": 62,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Sobre o Come-Cotas em Fundos de Renda Fixa de Longo Prazo, as alíquotas são:",
        "opcoes": {
            "A": "15% em maio e novembro",
            "B": "20% em maio e novembro",
            "C": "22,5% no resgate",
            "D": "10% semestralmente"
        },
        "resposta_correta": "A",
        "explicacao": "Para fundos de Longo Prazo, a antecipação semestral (come-cotas) ocorre em maio e novembro com alíquota de 15%."
    },
    {
        "id": 63,
        "modulo": "Fundos de Investimentos",
        "pergunta": "Responsável pela escolha dos ativos que serão adquiridos para a carteira do fundo:",
        "opcoes": {"A": "Administrador", "B": "Custodiante", "C": "Distribuidor", "D": "Gestor"},
        "resposta_correta": "D",
        "explicacao": "O gestor é quem toma as decisões de compra e venda dos ativos da carteira."
    },
    {
        "id": 64,
        "modulo": "Fundos de Investimentos",
        "pergunta": "O Come-Cotas provoca no investidor uma:",
        "opcoes": {
            "A": "Redução no número de cotas",
            "B": "Aumento no número de cotas",
            "C": "Redução no valor da cota",
            "D": "Alteração no benchmark"
        },
        "resposta_correta": "A",
        "explicacao": "O imposto é cobrado através da redução da quantidade de cotas detidas pelo investidor."
    },
    {
        "id": 65,
        "modulo": "Outros Fundos",
        "pergunta": "Sobre os Exchange Traded Funds (ETF), assinale a correta:",
        "opcoes": {
            "A": "Fundo negociado em bolsa que replica um índice",
            "B": "Fundo fechado com investimento mínimo de R$ 25 mil",
            "C": "Fundo atrelado exclusivamente ao mercado imobiliário",
            "D": "Fundo de mercado de balcão"
        },
        "resposta_correta": "A",
        "explicacao": "ETFs são fundos cujas cotas são negociadas em bolsa e visam replicar o desempenho de um índice de referência."
    },
    {
        "id": 66,
        "modulo": "Outros Fundos",
        "pergunta": "A alíquota de IR para rendimentos de FIIs para Pessoa Jurídica é de:",
        "opcoes": {"A": "15%", "B": "20%", "C": "22,5%", "D": "Isento"},
        "resposta_correta": "B",
        "explicacao": "Diferente da PF (que pode ser isenta), a PJ paga 20% de IR sobre os rendimentos distribuídos pelos FIIs."
    },
    {
        "id": 67,
        "modulo": "Outros Fundos",
        "pergunta": "O ganho de capital na venda de cotas de FII na bolsa para Pessoa Física é tributado em:",
        "opcoes": {"A": "15%", "B": "20%", "C": "Depende do prazo", "D": "Isento"},
        "resposta_correta": "B",
        "explicacao": "A venda de cotas de fundos imobiliários com lucro é tributada em 20%, sem isenção para PF."
    },
    {
        "id": 68,
        "modulo": "Outros Fundos",
        "pergunta": "Percentual mínimo do PL que um FIDC deve comprar em direitos creditórios:",
        "opcoes": {"A": "67%", "B": "80%", "C": "50%", "D": "95%"},
        "resposta_correta": "C",
        "explicacao": "Fundos de Investimento em Direitos Creditórios devem aplicar no mínimo 50% de seu PL em direitos creditórios."
    },
    {
        "id": 69,
        "modulo": "Outros Fundos",
        "pergunta": "Um FIP (Participações) deve investir em ativos que:",
        "opcoes": {
            "A": "Sejam apenas títulos públicos",
            "B": "Sejam empresas de capital aberto apenas",
            "C": "Permitam influenciar nas decisões da empresa",
            "D": "Garantam renda fixa mensal"
        },
        "resposta_correta": "D",
        "explicacao": "O FIP caracteriza-se pela participação no processo decisório da companhia investida."
    },
    {
        "id": "422025",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "A B3, empresa resultante da fusão entre BM&FBovespa e Cetip é uma empresa ____ que atua na infraestrutura do mercado financeiro, com atuação nos mercados de ____ e ____.",
        "opcoes": ["A) Pública; Bolsa; Balcão", "B) Privada; Bolsa; Balcão", "C) Sociedade Mista; Bolsa; Balcão", "D) Sociedade Mista; Primário; Secundário"],
        "resposta": "B"
    },
    {
        "id": "70",
        "tema": "Sistema Financeiro Nacional",
        "pergunta": "É o órgão responsável pela administração da dívida pública mobiliária e contratual, interna e externa, da União:",
        "opcoes": ["A) Tesouro Nacional", "B) Bacen", "C) CMN", "D) CVM"],
        "resposta": "A"
    },
    {
        "id": "71",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É uma definição correta sobre o Sistema de Pagamentos Brasileiro - SPB:",
        "opcoes": [
            "A) Sistema criado para transferir fundos entre bancos de um mesmo conglomerado",
            "B) Sistema criado para realização de DOC's para valores superiores a R$ 5 mil",
            "C) É a transferência de fundos próprio e de terceiros realizados entre bancos em tempo real, com o objetivo de reduzir o risco sistêmico",
            "D) Sistema criado para gerenciar o risco de crédito das instituições ao custodiar todos os CDB's emitidos por essas instituições"
        ],
        "resposta": "C"
    },
    {
        "id": "72",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Tipo de Sociedade que a Comissão de Valores Mobiliários (CVM) fiscaliza:",
        "opcoes": [
            "A) Sociedades de Economia Mista que sejam de propriedade privada",
            "B) Sociedades Anônimas que possuem ações negociadas em Bolsa de Valores e Mercado de Balcão",
            "C) Sociedades Anônimas que possuem ações negociadas em Bolsa de Valores e Mercado Primário",
            "D) Sociedades Limitadas que possuem ações negociadas em Bolsa de Valores"
        ],
        "resposta": "B"
    },
    {
        "id": "73",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "O Sistema de Pagamentos Brasileiro (SPB) é o conjunto de:",
        "opcoes": [
            "A) Entidades, sistemas e mecanismos relacionados com o processamento e a liquidação de operações de transferência de fundos, de operações com moeda estrangeira ou com ativo financeiros e valores mobiliários.",
            "B) Instituições financeiras, cooperativas de crédito e centrais depositárias de ações e de títulos de dívida corporativa.",
            "C) Sistemas eletrônicos disponibilizados pelo governo brasileiro para transferência de fundos e pagamentos de tributos",
            "D) Sistemas e mecanismos que possuem relação com a liquidação de câmbio entre as instituições financeiras"
        ],
        "resposta": "A"
    },
    {
        "id": "74",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São funções da CVM: I-Estimular a formação de poupança e sua aplicação em valores mobiliários; II-Proteger os investidores do mercado de capitais; III-Fiscalizar as S.A abertas, principalmente aquelas que apresentam falta de lucro contábil. Está correto:",
        "opcoes": ["A) I e II", "B) II e III", "C) Apenas I", "D) I, II e III"],
        "resposta": "A"
    },
    {
        "id": "75",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É a entidade responsável pelas diretrizes das operações dos 'Fundos de Pensão':",
        "opcoes": ["A) CNSP", "B) CNPC", "C) CMN", "D) PREVIC"],
        "resposta": "B"
    },
    {
        "id": "76",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "O Conselho Monetário Nacional (CMN) tem como função:",
        "opcoes": [
            "A) Exercer a fiscalização das instituições financeiras",
            "B) Conceder autorização para abertura de bancos estrangeiros no Brasil",
            "C) Realizar operações de redesconto junto às instituições financeiras",
            "D) Definir as diretrizes e normas referentes ao câmbio"
        ],
        "resposta": "D"
    },
    {
        "id": "77",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "De quem é a responsabilidade de fiscalizar um título de capitalização (como o Shark Cap)?",
        "opcoes": ["A) BACEN", "B) SUSEP", "C) CVM", "D) COAF"],
        "resposta": "B"
    },
    {
        "id": "78",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Assinale as funções que competem ao BACEN: I) Receber compulsórios; II) Fixar diretrizes cambiais; III) Emitir papel moeda; IV) Proteger titulares de valores mobiliários; V) Controle do crédito.",
        "opcoes": ["A) Todas", "B) I, II, V", "C) II, III, IV", "D) I, III, V"],
        "resposta": "D"
    },
    {
        "id": "79",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São funções do CNSP: I-Fixar diretrizes de seguros privados; II-Fiscalizar seguradoras; III-Fixar diretrizes cambiais. Está correto:",
        "opcoes": ["A) I e II", "B) II e III", "C) Apenas I", "D) Apenas III"],
        "resposta": "C"
    },
    {
        "id": "80",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "A BSM é responsável pela administração do ____ e possui personalidade jurídica e ____ para sua atuação.",
        "opcoes": ["A) SFN | Orçamento Próprio", "B) Orçamento Próprio | Subordinação ao BACEN", "C) MRP | Subordinação ao BACEN", "D) MRP | Orçamento Próprio"],
        "resposta": "D"
    },
    {
        "id": "81",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São considerados Índices Amplos da B3: I-IBRX-100 e IBRX-50; II-Ibovespa; III-ISE.",
        "opcoes": ["A) I e II", "B) II e III", "C) I e III", "D) I, II e III"],
        "resposta": "A"
    },
    {
        "id": "82",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Os sistemas que integram o SPB NÃO incluem o sistema:",
        "opcoes": ["A) Cetip", "B) SICAF", "C) STR", "D) Selic"],
        "resposta": "B"
    },
    {
        "id": "83",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Órgão máximo do Sistema Financeiro Nacional:",
        "opcoes": ["A) CNSP", "B) Bacen", "C) CMN", "D) Tesouro Nacional"],
        "resposta": "C"
    },
    {
        "id": "84",
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É uma função da CVM:",
        "opcoes": [
            "A) Fiscalizar instituições do ramo bancário",
            "B) Determinar diretrizes do mercado de câmbio",
            "C) Limitar comissões cobradas por instituições no mercado de distribuição de valores mobiliários",
            "D) Estimular investimentos em poupança"
        ],
        "resposta": "C"
    },
    {
        "id": "85",
        "modulo": "Mercado de Capitais",
        "pergunta": "Quanto ao prazo máximo de emissão das Notas Promissórias – Commercial Papers, assinale a correta:",
        "opcoes": ["A) 180 dias (Fechada) e 360 (Aberta)", "B) 360 dias (Fechada e Aberta)", "C) 180 dias (Fechada e Aberta)", "D) 180 dias (Aberta) e 360 (Fechada)"],
        "resposta": "B"
    },
    {
        "id": "86",
        "modulo": "Mercado de Capitais",
        "pergunta": "O que deve constar obrigatoriamente na escritura de uma debênture?",
        "opcoes": ["A) Intervenção de um Agente Fiduciário", "B) Rating de crédito", "C) Direitos iguais independente da série", "D) Garantia de pagamento pelo Agente Fiduciário"],
        "resposta": "A"
    },
    {
        "id": "87",
        "modulo": "Mercado de Capitais",
        "pergunta": "Sobre o Juros Sobre Capital Próprio – JSCP, assinale a correta:",
        "opcoes": [
            "A) Isentos de IR e originam-se em lucros retidos",
            "B) Originam-se de lucros retidos e IR regressivo",
            "C) Lucros distribuídos e isentos de IR",
            "D) Originam-se de lucros retidos e IR com alíquota única de 15%"
        ],
        "resposta": "D"
    },
    {
        "id": "88",
        "modulo": "Economia",
        "pergunta": "Sob a ótica do consumo, o PIB será a soma de: I- Consumo das famílias; II- Investimentos; III- Gastos Governamentais; IV - Exportações, deduzidas as importações. Está correto o que se afirma em:",
        "opcoes": ["A) Todas as alternativas", "B) I, II e III", "C) I, II e IV", "D) II e III"],
        "resposta": "A"
    },
    {
        "id": "89",
        "modulo": "Economia",
        "pergunta": "Uma política monetária é dita ____ quando injeta maior volume de recursos nos mercados, e quando age em sentido contrário, retraindo a atividade econômica, é chamada de ____.",
        "opcoes": ["A) Ativa / Passiva", "B) Agressiva / Expansionista", "C) Passiva / Ativa", "D) Expansionista / Restritiva"],
        "resposta": "D"
    },
    {
        "id": "90",
        "modulo": "Economia",
        "pergunta": "Com intenção de reduzir a demanda agregada da economia, o BACEN deveria realizar qual tipo de alteração na política monetária:",
        "opcoes": ["A) Diminuir o depósito compulsório", "B) Aumentar o depósito compulsório", "C) Reduzir a taxa do redesconto", "D) Realizar operações de 'open market' de compra de títulos"],
        "resposta": "B"
    },
    {
        "id": "91",
        "modulo": "Economia",
        "pergunta": "Em um regime cambial de taxa flutuante, com a conta corrente e a conta de capitais sendo superavitárias e sem intervenção, espera-se que:",
        "opcoes": ["A) Valorize a moeda local", "B) Desvalorize a moeda local", "C) O governo atue para reduzir a alta da moeda estrangeira", "D) O governo atue para aumentar a cotação da moeda estrangeira"],
        "resposta": "A"
    },
    {
        "id": "92",
        "modulo": "Economia",
        "pergunta": "Um investimento com rendimento nominal de 15% e inflação de 5% no mesmo período, teve uma taxa real de aproximadamente:",
        "opcoes": ["A) 5%", "B) 20%", "C) 15%", "D) 10%"],
        "resposta": "D"
    },
    {
        "id": "93",
        "modulo": "Economia",
        "pergunta": "Um Superávit Consolidado contempla as contas do(s):",
        "opcoes": ["A) Governo Federal, somente", "B) Governo Federal e Estados", "C) Governo Federal, Estados e Municípios", "D) Governo Federal, Estados, Municípios e Empresas Estatais"],
        "resposta": "D"
    },
    {
        "id": "94",
        "modulo": "Economia",
        "pergunta": "Assinale o item que contém somente medidas contracionistas: I-Redução da Selic; II-Aumento do compulsório; III-Redução do IPI; IV-Redução dos gastos governamentais.",
        "opcoes": ["A) I e III", "B) II e III", "C) II, III e IV", "D) II e IV"],
        "resposta": "D"
    },
    {
        "id": "95",
        "modulo": "Economia",
        "pergunta": "Assinale a alternativa correta sobre taxas e índices:",
        "opcoes": ["A) A T.R é usada pelo BNDES", "B) Taxa DI é lastreada em títulos públicos", "C) O IGP-M é mais afetado por preços no atacado", "D) O spread de crédito é livre de risco"],
        "resposta": "C"
    },
    {
        "id": "96",
        "modulo": "Economia",
        "pergunta": "Inflação de 6 meses: Jan(+0,16%), Fev(+0,35%), Mar(-0,16%), Abr(-0,02%), Mai(+0,05%), Jun(-0,02%). Qual a acumulada?",
        "opcoes": ["A) 0,3600%", "B) 0,3598%", "C) 0,3698%", "D) 0,3740%"],
        "resposta": "B"
    },
    {
        "id": "97",
        "modulo": "Economia",
        "pergunta": "Quando o BACEN reduz o compulsório, a liquidez ____, as taxas de juros ____ e o consumo ____.",
        "opcoes": ["A) aumente, caiam, aumente", "B) aumente, caiam, caia", "C) caia, aumentem, caia", "D) caia, caiam, aumente"],
        "resposta": "A"
    },
    {
        "id": "98",
        "modulo": "Economia",
        "pergunta": "A diferença entre Taxa Selic Meta e Selic Over é que:",
        "opcoes": ["A) Meta é mercado, Over é Copom", "B) Meta é títulos privados, Over é públicos", "C) Meta é anual, Over é semestral", "D) Meta é Copom, Over é mercado"],
        "resposta": "D"
    },
    {
        "id": "99",
        "modulo": "Economia",
        "pergunta": "O índice IPC-FIPE estima as variações do custo de vida das famílias de:",
        "opcoes": ["A) São Paulo", "B) Região Sudeste", "C) Região Sul", "D) IBGE"],
        "resposta": "A"
    },
    {
        "id": "100",
        "modulo": "Economia",
        "pergunta": "A taxa 'Selic Over' diária é obtida com juros ____ e métrica de ____ dias.",
        "opcoes": ["A) Compostos; 252", "B) Compostos; 360", "C) Simples; 252", "D) Simples; 360"],
        "resposta": "A"
    },
    {
        "id": "101",
        "modulo": "Economia",
        "pergunta": "Conforme a Lei dos Rendimentos Decrescentes:",
        "opcoes": ["A) Produção aumenta proporcionalmente ao fator", "B) Produção total é reduzida", "C) Mantendo fatores, produção total aumenta", "D) Aumentando um fator, a produção proporcional deste fator é reduzida"],
        "resposta": "D"
    },
    {
        "id": "102",
        "modulo": "Instituições Financeiras",
        "pergunta": "Qual quantidade mínima de associados necessários para que uma cooperativa de crédito seja constituída?",
        "opcoes": ["A) 20 associados", "B) 30 associados", "C) 50 associados", "D) Não tem quantidade mínima"],
        "resposta": "A"
    },
    {
        "id": "103",
        "modulo": "Instituições Financeiras",
        "pergunta": "São funções de uma SCTVM, EXCETO:",
        "opcoes": ["A) Administrar planos de capitalização", "B) Administrar clubes de investimentos", "C) Administrar fundos de investimentos", "D) Realizar operações de câmbio"],
        "resposta": "A"
    },
    {
        "id": "104",
        "modulo": "Instituições Financeiras",
        "pergunta": "Sobre os Bancos de Investimentos, assinale a correta:",
        "opcoes": ["A) Ofertam crédito de curto prazo (cheque especial)", "B) Realizam operações com dólar turismo", "C) Fiscalizam o mercado de distribuição", "D) Assessoram fusões, emissões de valores mobiliários e crédito de médio/longo prazo"],
        "resposta": "D"
    },
    {
        "id": "105",
        "modulo": "Instituições Financeiras",
        "pergunta": "Podem receber depósitos interfinanceiros (CDI): I-Caixas Econômicas; II-Sociedades de Crédito e Financiamento; III-SCTVM. Está correto:",
        "opcoes": ["A) I e II", "B) I e III", "C) Apenas I", "D) I, II e III"],
        "resposta": "A"
    },
    {
        "id": "106",
        "modulo": "Instituições Financeiras",
        "pergunta": "Sobre o BNDES, assinale a alternativa correta:",
        "opcoes": ["A) É um banco de desenvolvimento federal", "B) É sociedade de economia mista com ações em bolsa", "C) Fomenta apenas o mercado imobiliário", "D) É instrumento para fomentar setores estratégicos"],
        "resposta": "D"
    },
    {
        "id": "107",
        "modulo": "Instituições Financeiras",
        "pergunta": "Para ofertar leasing e crédito imobiliário em um único balanço, Júlio precisa de:",
        "opcoes": ["A) Banco com carteira de crédito e arrendamento", "B) Banco Múltiplo (Comercial ou Desenv.) + Arrendamento", "C) Banco Múltiplo (Comercial ou Invest.) + Desenv. e Imobiliário", "D) Banco Múltiplo (Comercial ou Invest.) + Arrendamento e Imobiliário"],
        "resposta": "D"
    },
    {
        "id": "108",
        "modulo": "Instituições Financeiras",
        "pergunta": "É uma carteira que deve estar presente em um Banco Múltiplo, obrigatoriamente (para ser considerado múltiplo):",
        "opcoes": ["A) Comercial ou de Investimento", "B) Crédito e Financiamento", "C) Crédito Imobiliário", "D) Desenvolvimento"],
        "resposta": "A"
    },
    {
        "id": "109",
        "modulo": "Instituições Financeiras",
        "pergunta": "Instituição Financeira autorizada a captar através de depósito à vista:",
        "opcoes": ["A) Banco Comercial", "B) Banco de Investimento", "C) Banco de Desenvolvimento", "D) Financeiras"],
        "resposta": "A"
    },
    {
        "id": "110",
        "modulo": "Instituições Financeiras",
        "pergunta": "As Financeiras são instituições ____ e tem como principal característica o financiamento para ____.",
        "opcoes": ["A) bancárias / atividade produtiva", "B) bancárias / capital fixo", "C) não bancárias / capital social", "D) não bancárias / capital de giro"],
        "resposta": "D"
    },
    {
        "id": "111",
        "modulo": "Instituições Financeiras",
        "pergunta": "Qual das opções abaixo configura um banco múltiplo?",
        "opcoes": ["A) Banco de Desenv. com carteira imobiliária", "B) Banco Comercial (apenas)", "C) Banco com carteira de financiamento e arrendamento", "D) Banco de investimento com carteira de arrendamento mercantil"],
        "resposta": "D"
    },
    {
    "id": "112",
    "modulo": "Matemática Financeira",
    "pergunta": "Germano resolveu trocar sua geladeira. Promoção à vista com 10% de desconto ou 10 vezes de R$ 280,00 sem desconto. Qual a taxa de juros embutida na operação?",
    "opcoes": [
        "26,27% a.a.",
        "1,86% a.m.",
        "Taxa zero, pois parcelamento foi sem juros.",
        "1,94% a.m."
    ],
    "resposta": "26,27% a.a."
},
{
    "id": "113",
    "modulo": "Matemática Financeira",
    "pergunta": "No conceito de taxa over, a equivalente diária é descapitalizada segundo o regime:",
    "opcoes": [
        "Composto, por 360 dias corridos.",
        "Composto, por 252 dias úteis.",
        "Simples, por 360 dias corridos.",
        "Simples, por 252 dias úteis."
    ],
    "resposta": "Composto, por 252 dias úteis."
},
{ 
    "id": "114",
    "modulo": "Matemática Financeira",
    "pergunta": "Investidor comprou LFT com prazo de 846 dias úteis, com ágio de 0.20% a.a., pagando PU de R$ 4.446. O preço par desse papel é:",
    "opcoes": ["4.256", "4.446", "4.416", "4.387"],
    "resposta": "4.416"
},
{
    "id": "115",
    "modulo": "Matemática Financeira",
    "pergunta": "Carro financiado em 24 parcelas de R$ 3.106,85, com a primeira no ato. Valor financiado: R$ 60 mil. Qual a taxa?",
    "opcoes": ["1,82% mês", "26,68% ano", "1,76% mês", "24,86% ano"],
    "resposta": "26,68% ano"
},
{
    "id": "116",
    "modulo": "Matemática Financeira",
    "pergunta": "Se o VPL de um projeto de investimento for positivo, isso indica que:",
    "opcoes": [
        "Não devemos investir, resultado indiferente.",
        "Podemos investir, o projeto é lucrativo para essa taxa.",
        "Podemos investir, resultado indiferente.",
        "Não devemos investir, o projeto não é lucrativo."
    ],
    "resposta": "Podemos investir, o projeto é lucrativo para essa taxa."
},
{
    "id": "117",
    "modulo": "Clubes de Investimentos",
    "pergunta": "Número máximo de participantes de um Clube de Ações:",
    "opcoes": ["50", "150", "3", "30"],
    "resposta": "50"
},
{
    "id": "118",
    "modulo": "Clubes de Investimentos",
    "pergunta": "Qual o percentual máximo do patrimônio que um Clube pode ter em Títulos Públicos Federais?",
    "opcoes": ["67%", "33%", "80%", "100%"],
    "resposta": "33%"
},
{
    "id": "119",
    "modulo": "Administração de Risco",
    "pergunta": "Sobre o conceito de Value At Risk (VaR), assinale a correta:",
    "opcoes": [
        "Pode ser reduzido com hedge cambial.",
        "Risco de crédito é a oscilação de valores na carteira.",
        "Risco sistemático é reduzido com diversificação.",
        "O VaR define a perda máxima potencial com um nível de confiança."
    ],
    "resposta": "O VaR define a perda máxima potencial com um nível de confiança."
},
{
    "id": "120",
    "modulo": "Administração de Risco",
    "pergunta": "Uma carteira 100% composta por ações possui os seguintes riscos, EXCETO:",
    "opcoes": ["Liquidez", "Mercado", "Crédito", "Sistemático"],
    "resposta": "Crédito"
},
{    
    "id": "121",
    "modulo": "Administração de Risco",
    "pergunta": "Para menor risco de crédito e menor risco de reinvestimento, qual a melhor escolha?",
    "opcoes": [
        "Tesouro IPCA 2028 com juros semestrais",
        "Debêntures incentivadas 2031",
        "NTN-B Principal 2028",
        "CDB pré-fixado com juros mensais"
    ],
    "resposta": "NTN-B Principal 2028"
    ]
