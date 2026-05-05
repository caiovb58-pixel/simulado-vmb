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
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "A B3, empresa resultante da fusão entre BM&FBovespa e Cetip é uma empresa ____ que atua na infraestrutura do mercado financeiro, com atuação nos mercados de ____ e ____.",
        "opcoes": {"A": "Pública; Bolsa; Balcão", "B": "Privada; Bolsa; Balcão", "C": "Sociedade Mista; Bolsa; Balcão", "D": "Sociedade Mista; Primário; Secundário"},
        "resposta_correta": "B",
        "explicacao": "A B3 é uma entidade privada de capital aberto que administra mercados organizados de bolsa e balcão."
    },
    {
        "id": 70,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É o órgão responsável pela administração da dívida pública mobiliária e contratual, interna e externa, da União:",
        "opcoes": {"A": "Tesouro Nacional", "B": "Bacen", "C": "CMN", "D": "CVM"},
        "resposta_correta": "A",
        "explicacao": "O Tesouro Nacional é o órgão responsável pela gestão da dívida pública e do caixa da União."
    },
    {
        "id": 71,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É uma definição correta sobre o Sistema de Pagamentos Brasileiro - SPB:",
        "opcoes": {
            "A": "Sistema criado para transferir fundos entre bancos de um mesmo conglomerado",
            "B": "Sistema criado para realização de DOC's para valores superiores a R$ 5 mil",
            "C": "É a transferência de fundos próprio e de terceiros realizados entre bancos em tempo real, com o objetivo de reduzir o risco sistêmico",
            "D": "Sistema criado para gerenciar o risco de crédito das instituições ao custodiar todos os CDB's emitidos por essas instituições"
        },
        "resposta_correta": "C",
        "explicacao": "O SPB permite a liquidação em tempo real (STR), mitigando o risco de quebra em cadeia (risco sistêmico)."
    },
    {
        "id": 72,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Tipo de Sociedade que a Comissão de Valores Mobiliários (CVM) fiscaliza:",
        "opcoes": {
            "A": "Sociedades de Economia Mista que sejam de propriedade privada",
            "B": "Sociedades Anônimas que possuem ações negociadas em Bolsa de Valores e Mercado de Balcão",
            "C": "Sociedades Anônimas que possuem ações negociadas em Bolsa de Valores e Mercado Primário",
            "D": "Sociedades Limitadas que possuem ações negociadas em Bolsa de Valores"
        },
        "resposta_correta": "B",
        "explicacao": "A CVM fiscaliza as companhias abertas (S.A.) que captam recursos junto ao público no mercado de capitais."
    },
    {
        "id": 73,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "O Sistema de Pagamentos Brasileiro (SPB) é o conjunto de:",
        "opcoes": {
            "A": "Entidades, sistemas e mecanismos relacionados com o processamento e a liquidação de operações de transferência de fundos, de operações com moeda estrangeira ou com ativo financeiros e valores mobiliários.",
            "B": "Instituições financeiras, cooperativas de crédito e centrais depositárias de ações e de títulos de dívida corporativa.",
            "C": "Sistemas eletrônicos disponibilizados pelo governo brasileiro para transferência de fundos e pagamentos de tributos",
            "D": "Sistemas e mecanismos que possuem relação com a liquidação de câmbio entre as instituições financeiras"
        },
        "resposta_correta": "A",
        "explicacao": "Definição formal do SPB, abrangendo toda a infraestrutura de liquidação financeira do país."
    },
    {
        "id": 74,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São funções da CVM: I-Estimular a formação de poupança e sua aplicação em valores mobiliários; II-Proteger os investidores do mercado de capitais; III-Fiscalizar as S.A abertas, principalmente aquelas que apresentam falta de lucro contábil. Está correto:",
        "opcoes": {"A": "I e II", "B": "II e III", "C": "Apenas I", "D": "I, II e III"},
        "resposta_correta": "A",
        "explicacao": "A fiscalização da CVM não depende de lucro contábil, mas sim do cumprimento das normas do mercado de capitais."
    },
    {
        "id": 75,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É a entidade responsável pelas diretrizes das operações dos 'Fundos de Pensão':",
        "opcoes": {"A": "CNSP", "B": "CNPC", "C": "CMN", "D": "PREVIC"},
        "resposta_correta": "B",
        "explicacao": "O CNPC dita as normas (órgão normativo) e a PREVIC fiscaliza (órgão executor) as Entidades Fechadas de Previdência Complementar."
    },
    {
        "id": 76,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "O Conselho Monetário Nacional (CMN) tem como função:",
        "opcoes": {
            "A": "Exercer a fiscalização das instituições financeiras",
            "B": "Conceder autorização para abertura de bancos estrangeiros no Brasil",
            "C": "Realizar operações de redesconto junto às instituições financeiras",
            "D": "Definir as diretrizes e normas referentes ao câmbio"
        },
        "resposta_correta": "D",
        "explicacao": "O CMN é um órgão normativo; definir diretrizes de câmbio e moeda é sua competência principal."
    },
    {
        "id": 77,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "De quem é a responsabilidade de fiscalizar um título de capitalização?",
        "opcoes": {"A": "BACEN", "B": "SUSEP", "C": "CVM", "D": "COAF"},
        "resposta_correta": "B",
        "explicacao": "Títulos de capitalização são produtos da área de seguros, logo, sob supervisão da SUSEP."
    },
    {
        "id": 78,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Assinale as funções que competem ao BACEN: I) Receber compulsórios; II) Fixar diretrizes cambiais; III) Emitir papel moeda; IV) Proteger titulares de valores mobiliários; V) Controle do crédito.",
        "opcoes": {"A": "Todas", "B": "I, II, V", "C": "II, III, IV", "D": "I, III, V"},
        "resposta_correta": "D",
        "explicacao": "Fixar diretrizes cambiais é função do CMN, e proteger titulares de valores mobiliários é função da CVM."
    },
    {
        "id": 79,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São funções do CNSP: I-Fixar diretrizes de seguros privados; II-Fiscalizar seguradoras; III-Fixar diretrizes cambiais. Está correto:",
        "opcoes": {"A": "I e II", "B": "II e III", "C": "Apenas I", "D": "Apenas III"},
        "resposta_correta": "C",
        "explicacao": "O CNSP fixa diretrizes (normativo). A fiscalização (II) cabe à SUSEP e as diretrizes cambiais (III) ao CMN."
    },
    {
        "id": 80,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "A BSM é responsável pela administração do ____ e possui personalidade jurídica e ____ para sua atuação.",
        "opcoes": {"A": "SFN | Orçamento Próprio", "B": "Orçamento Próprio | Subordinação ao BACEN", "C": "MRP | Subordinação ao BACEN", "D": "MRP | Orçamento Próprio"},
        "resposta_correta": "D",
        "explicacao": "A BSM Supervisão de Mercados administra o Mecanismo de Ressarcimento de Prejuízos (MRP) com autonomia e orçamento próprio."
    },
    {
        "id": 81,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "São considerados Índices Amplos da B3: I-IBRX-100 e IBRX-50; II-Ibovespa; III-ISE.",
        "opcoes": {"A": "I e II", "B": "II e III", "C": "I e III", "D": "I, II e III"},
        "resposta_correta": "A",
        "explicacao": "IBRX e Ibovespa são índices amplos. O ISE (Índice de Sustentabilidade Empresarial) é um índice de segmento/sustentabilidade."
    },
    {
        "id": 82,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Os sistemas que integram o SPB NÃO incluem o sistema:",
        "opcoes": {"A": "Cetip", "B": "SICAF", "C": "STR", "D": "Selic"},
        "resposta_correta": "B",
        "explicacao": "O SICAF é um sistema de cadastro de fornecedores do governo, não integra a liquidação financeira do SPB."
    },
    {
        "id": 83,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "Órgão máximo do Sistema Financeiro Nacional:",
        "opcoes": {"A": "CNSP", "B": "Bacen", "C": "CMN", "D": "Tesouro Nacional"},
        "resposta_correta": "C",
        "explicacao": "O CMN é o órgão deliberativo máximo do SFN."
    },
    {
        "id": 84,
        "modulo": "Sistema Financeiro Nacional",
        "pergunta": "É uma função da CVM:",
        "opcoes": {
            "A": "Fiscalizar instituições do ramo bancário",
            "B": "Determinar diretrizes do mercado de câmbio",
            "C": "Limitar comissões cobradas por instituições no mercado de distribuição de valores mobiliários",
            "D": "Estimular investimentos em poupança"
        },
        "resposta_correta": "C",
        "explicacao": "A CVM tem poder para regular e limitar custos de intermediação no mercado de capitais para proteger o investidor."
    },
    {
        "id": 85,
        "modulo": "Mercado de Capitais",
        "pergunta": "Quanto ao prazo máximo de emissão das Notas Promissórias – Commercial Papers, assinale a correta:",
        "opcoes": {"A": "180 dias (Fechada) e 360 (Aberta)", "B": "360 dias (Fechada e Aberta)", "C": "180 dias (Fechada e Aberta)", "D": "180 dias (Aberta) e 360 (Fechada)"},
        "resposta_correta": "B",
        "explicacao": "Pela regra atual (Resolução CVM), o prazo máximo para Notas Promissórias é de 360 dias, independentemente de ser S.A. aberta ou fechada."
    },
    {
        "id": 86,
        "modulo": "Mercado de Capitais",
        "pergunta": "O que deve constar obrigatoriamente na escritura de uma debênture?",
        "opcoes": {"A": "Intervenção de um Agente Fiduciário", "B": "Rating de crédito", "C": "Direitos iguais independente da série", "D": "Garantia de pagamento pelo Agente Fiduciário"},
        "resposta_correta": "A",
        "explicacao": "A nomeação de um Agente Fiduciário é obrigatória para proteger os interesses dos debenturistas."
    },
    {
        "id": 87,
        "modulo": "Mercado de Capitais",
        "pergunta": "Sobre o Juros Sobre Capital Próprio – JSCP, assinale a correta:",
        "opcoes": {
            "A": "Isentos de IR e originam-se em lucros retidos",
            "B": "Originam-se de lucros retidos e IR regressivo",
            "C": "Lucros distribuídos e isentos de IR",
            "D": "Originam-se de lucros retidos e IR com alíquota única de 15%"
        },
        "resposta_correta": "D",
        "explicacao": "Diferente dos dividendos (isentos), o JSCP é tributado em 15% na fonte para o investidor pessoa física."
    },
    {
        "id": 88,
        "modulo": "Economia",
        "pergunta": "Sob a ótica do consumo, o PIB será a soma de: I- Consumo das famílias; II- Investimentos; III- Gastos Governamentais; IV - Exportações, deduzidas as importações. Está correto o que se afirma em:",
        "opcoes": {"A": "Todas as alternativas", "B": "I, II e III", "C": "I, II e IV", "D": "II e III"},
        "resposta_correta": "A",
        "explicacao": "A fórmula do PIB pela ótica da despesa é C + I + G + (X - M)."
    },
    {
        "id": 89,
        "modulo": "Economia",
        "pergunta": "Uma política monetária é dita ____ quando injeta maior volume de recursos nos mercados, e quando age em sentido contrário, retraindo a atividade econômica, é chamada de ____.",
        "opcoes": {"A": "Ativa / Passiva", "B": "Agressiva / Expansionista", "C": "Passiva / Ativa", "D": "Expansionista / Restritiva"},
        "resposta_correta": "D",
        "explicacao": "Expansionista estimula a economia (mais moeda); Restritiva freia a inflação (menos moeda)."
    },
    {
        "id": 90,
        "modulo": "Economia",
        "pergunta": "Com intenção de reduzir a demanda agregada da economia, o BACEN deveria realizar qual tipo de alteração na política monetária:",
        "opcoes": {"A": "Diminuir o depósito compulsório", "B": "Aumentar o depósito compulsório", "C": "Reduzir a taxa do redesconto", "D": "Realizar operações de 'open market' de compra de títulos"},
        "resposta_correta": "B",
        "explicacao": "Aumentar o compulsório retira dinheiro dos bancos, reduzindo a oferta de crédito e a demanda."
    },
    {
        "id": 91,
        "modulo": "Economia",
        "pergunta": "Em um regime cambial de taxa flutuante, com a conta corrente e a conta de capitais sendo superavitárias e sem intervenção, espera-se que:",
        "opcoes": {"A": "Valorize a moeda local", "B": "Desvalorize a moeda local", "C": "O governo atue para reduzir a alta da moeda estrangeira", "D": "O governo atue para aumentar a cotação da moeda estrangeira"},
        "resposta_correta": "A",
        "explicacao": "Superávit significa entrada de dólares; excesso de oferta de dólar faz a moeda local valorizar."
    },
    {
        "id": 92,
        "modulo": "Economia",
        "pergunta": "Um investimento com rendimento nominal de 15% e inflação de 5% no mesmo período, teve uma taxa real de aproximadamente:",
        "opcoes": {"A": "5%", "B": "20%", "C": "15%", "D": "10%"},
        "resposta_correta": "D",
        "explicacao": "A taxa real é a taxa nominal descontada a inflação. A conta exata usa divisão, mas a subtração é uma aproximação aceita em questões teóricas."
    },
    {
        "id": 93,
        "modulo": "Economia",
        "pergunta": "Um Superávit Consolidado contempla as contas do(s):",
        "opcoes": {"A": "Governo Federal, somente", "B": "Governo Federal e Estados", "C": "Governo Federal, Estados e Municípios", "D": "Governo Federal, Estados, Municípios e Empresas Estatais"},
        "resposta_correta": "D",
        "explicacao": "O resultado consolidado do setor público abrange todas as esferas de governo e as empresas estatais."
    },
    {
        "id": 94,
        "modulo": "Economia",
        "pergunta": "Assinale o item que contém somente medidas contracionistas: I-Redução da Selic; II-Aumento do compulsório; III-Redução do IPI; IV-Redução dos gastos governamentais.",
        "opcoes": {"A": "I e III", "B": "II e III", "C": "II, III e IV", "D": "II e IV"},
        "resposta_correta": "D",
        "explicacao": "Aumento do compulsório e redução de gastos (fiscal) são medidas para contrair a economia."
    },
    {
        "id": 95,
        "modulo": "Economia",
        "pergunta": "Assinale a alternativa correta sobre taxas e índices:",
        "opcoes": {"A": "A T.R é usada pelo BNDES", "B": "Taxa DI é lastreada em títulos públicos", "C": "O IGP-M é mais afetado por preços no atacado", "D": "O spread de crédito é livre de risco"},
        "resposta_correta": "C",
        "explicacao": "O IGP-M é composto por 60% do IPA (Índice de Preços ao Produtor Amplo), que mede preços no atacado."
    },
    {
        "id": 96,
        "modulo": "Economia",
        "pergunta": "Inflação de 6 meses: Jan(+0,16%), Fev(+0,35%), Mar(-0,16%), Abr(-0,02%), Mai(+0,05%), Jun(-0,02%). Qual a acumulada?",
        "opcoes": {"A": "0,3600%", "B": "0,3598%", "C": "0,3698%", "D": "0,3740%"},
        "resposta_correta": "B",
        "explicacao": "A inflação acumulada é o produto dos fatores (1+i) de cada mês."
    },
    {
        "id": 97,
        "modulo": "Economia",
        "pergunta": "Quando o BACEN reduz o compulsório, a liquidez ____, as taxas de juros ____ e o consumo ____.",
        "opcoes": {"A": "aumenta, caiam, aumente", "B": "aumenta, caiam, caia", "C": "caia, aumentem, caia", "D": "caia, caiam, aumente"},
        "resposta_correta": "A",
        "explicacao": "Menos compulsório = mais dinheiro nos bancos (liquidez) = juros menores = mais consumo."
    },
    {
        "id": 98,
        "modulo": "Economia",
        "pergunta": "A diferença entre Taxa Selic Meta e Selic Over é que:",
        "opcoes": {"A": "Meta é mercado, Over é Copom", "B": "Meta é títulos privados, Over é públicos", "C": "Meta é anual, Over é semestral", "D": "Meta é Copom, Over é mercado"},
        "resposta_correta": "D",
        "explicacao": "A Meta é definida pelo COPOM; a Over é a taxa efetiva praticada no mercado interbancário (Selic)."
    },
    {
        "id": 99,
        "modulo": "Economia",
        "pergunta": "O índice IPC-FIPE estima as variações do custo de vida das famílias de:",
        "opcoes": {"A": "São Paulo", "B": "Região Sudeste", "C": "Região Sul", "D": "IBGE"},
        "resposta_correta": "A",
        "explicacao": "O IPC-FIPE é um índice regionalizado que foca no custo de vida na cidade de São Paulo."
    },
    {
        "id": 100,
        "modulo": "Economia",
        "pergunta": "A taxa 'Selic Over' diária é obtida com juros ____ e métrica de ____ dias.",
        "opcoes": {"A": "Compostos; 252", "B": "Compostos; 360", "C": "Simples; 252", "D": "Simples; 360"},
        "resposta_correta": "A",
        "explicacao": "No mercado brasileiro, as taxas são expressas em juros compostos com base em 252 dias úteis."
    },
    {
        "id": 101,
        "modulo": "Economia",
        "pergunta": "Conforme a Lei dos Rendimentos Decrescentes:",
        "opcoes": {"A": "Produção aumenta proporcionalmente ao fator", "B": "Produção total é reduzida", "C": "Mantendo fatores, produção total aumenta", "D": "Aumentando um fator, a produção proporcional deste fator é reduzida"},
        "resposta_correta": "D",
        "explicacao": "Ao adicionar mais de um fator produtivo enquanto outros ficam fixos, o ganho marginal de produção tende a diminuir."
    },
    {
        "id": 102,
        "modulo": "Instituições Financeiras",
        "pergunta": "Qual quantidade mínima de associados necessários para que uma cooperativa de crédito seja constituída?",
        "opcoes": {"A": "20 associados", "B": "30 associados", "C": "50 associados", "D": "Não tem quantidade mínima"},
        "resposta_correta": "A",
        "explicacao": "A legislação exige o mínimo de 20 pessoas físicas para constituir uma cooperativa de crédito."
    },
    {
        "id": 103,
        "modulo": "Instituições Financeiras",
        "pergunta": "São funções de uma SCTVM, EXCETO:",
        "opcoes": {"A": "Administrar planos de capitalização", "B": "Administrar clubes de investimentos", "C": "Administrar fundos de investimentos", "D": "Realizar operações de câmbio"},
        "resposta_correta": "A",
        "explicacao": "Corretoras (SCTVM) não administram capitalização; isso é exclusividade de sociedades de capitalização autorizadas pela SUSEP."
    },
    {
        "id": 104,
        "modulo": "Instituições Financeiras",
        "pergunta": "Sobre os Bancos de Investimentos, assinale a correta:",
        "opcoes": {"A": "Ofertam crédito de curto prazo (cheque especial)", "B": "Realizam operações com dólar turismo", "C": "Fiscalizam o mercado de distribuição", "D": "Assessoram fusões, emissões de valores mobiliários e crédito de médio/longo prazo"},
        "resposta_correta": "D",
        "explicacao": "Bancos de investimento focam no médio/longo prazo e em mercado de capitais (Underwriting)."
    },
    {
        "id": 105,
        "modulo": "Instituições Financeiras",
        "pergunta": "Podem receber depósitos interfinanceiros (CDI): I-Caixas Econômicas; II-Sociedades de Crédito e Financiamento; III-SCTVM. Está correto:",
        "opcoes": {"A": "I e II", "B": "I e III", "C": "Apenas I", "D": "I, II e III"},
        "resposta_correta": "A",
        "explicacao": "Caixas e Financeiras operam CDI. Corretoras (SCTVM) não captam via depósitos interfinanceiros no mesmo molde bancário."
    },
    {
        "id": 106,
        "modulo": "Instituições Financeiras",
        "pergunta": "Sobre o BNDES, assinale a alternativa correta:",
        "opcoes": {"A": "É um banco de desenvolvimento federal", "B": "É sociedade de economia mista com ações em bolsa", "C": "Fomenta apenas o mercado imobiliário", "D": "É instrumento para fomentar setores estratégicos"},
        "resposta_correta": "D",
        "explicacao": "O BNDES é uma empresa pública federal usada como braço de fomento de longo prazo do governo."
    },
    {
        "id": 107,
        "modulo": "Instituições Financeiras",
        "pergunta": "Para ofertar leasing e crédito imobiliário em um único balanço, Júlio precisa de:",
        "opcoes": {"A": "Banco com carteira de crédito e arrendamento", "B": "Banco Múltiplo (Comercial ou Desenv.) + Arrendamento", "C": "Banco Múltiplo (Comercial ou Invest.) + Desenv. e Imobiliário", "D": "Banco Múltiplo (Comercial ou Invest.) + Arrendamento e Imobiliário"},
        "resposta_correta": "D",
        "explicacao": "Um banco múltiplo precisa das carteiras específicas para operar cada produto sob o mesmo CNPJ."
    },
    {
        "id": 108,
        "modulo": "Instituições Financeiras",
        "pergunta": "É uma carteira que deve estar presente em um Banco Múltiplo, obrigatoriamente (para ser considerado múltiplo):",
        "opcoes": {"A": "Comercial ou de Investimento", "B": "Crédito e Financiamento", "C": "Crédito Imobiliário", "D": "Desenvolvimento"},
        "resposta_correta": "A",
        "explicacao": "Para ser banco múltiplo, a instituição deve possuir pelo menos duas carteiras, sendo uma delas Comercial ou de Investimento."
    },
    {
        "id": 109,
        "modulo": "Instituições Financeiras",
        "pergunta": "Instituição Financeira autorizada a captar através de depósito à vista:",
        "opcoes": {"A": "Banco Comercial", "B": "Banco de Investimento", "C": "Banco de Desenvolvimento", "D": "Financeiras"},
        "resposta_correta": "A",
        "explicacao": "A captação de depósitos à vista é a característica principal dos bancos comerciais."
    },
    {
        "id": 110,
        "modulo": "Instituições Financeiras",
        "pergunta": "As Financeiras são instituições ____ e tem como principal característica o financiamento para ____.",
        "opcoes": {"A": "bancárias / atividade produtiva", "B": "bancárias / capital fixo", "C": "não bancárias / capital social", "D": "não bancárias / capital de giro"},
        "resposta_correta": "D",
        "explicacao": "Financeiras não são bancárias (não captam depósito à vista) e focam em crédito ao consumidor e capital de giro."
    },
    {
        "id": 111,
        "modulo": "Instituições Financeiras",
        "pergunta": "Qual das opções abaixo configura um banco múltiplo?",
        "opcoes": {"A": "Banco de Desenv. com carteira imobiliária", "B": "Banco Comercial (apenas)", "C": "Banco com carteira de financiamento e arrendamento", "D": "Banco de investimento com carteira de arrendamento mercantil"},
        "resposta_correta": "D",
        "explicacao": "Contém a carteira de Investimento (obrigatória para ser múltiplo neste caso) + uma carteira adicional."
    },
    {
        "id": 112,
        "modulo": "Matemática Financeira",
        "pergunta": "Germano resolveu trocar sua geladeira. Promoção à vista com 10% de desconto ou 10 vezes de R$ 280,00 sem desconto. Qual a taxa de juros embutida na operação?",
        "opcoes": {"A": "26,27% a.a.", "B": "1,86% a.m.", "C": "Taxa zero", "D": "1,94% a.m."},
        "resposta_correta": "A",
        "explicacao": "Considerando PV = 2520 (90% de 2800) e PMT = 280 em 10 meses. A taxa mensal é ~1,94%, que anualizada dá 26,27%."
    },
    {
        "id": 113,
        "modulo": "Matemática Financeira",
        "pergunta": "No conceito de taxa over, a equivalente diária é descapitalizada segundo o regime:",
        "opcoes": {"A": "Composto, por 360 dias corridos.", "B": "Composto, por 252 dias úteis.", "C": "Simples, por 360 dias corridos.", "D": "Simples, por 252 dias úteis."},
        "resposta_correta": "B",
        "explicacao": "Taxas 'Over' no Brasil sempre utilizam juros compostos e a base de 252 dias úteis."
    },
    {
        "id": 114,
        "modulo": "Matemática Financeira",
        "pergunta": "Investidor comprou LFT com prazo de 846 dias úteis, com ágio de 0.20% a.a., pagando PU de R$ 4.446. O preço par desse papel é:",
        "opcoes": {"A": "4.256", "B": "4.446", "C": "4.416", "D": "4.387"},
        "resposta_correta": "C",
        "explicacao": "O PU par é o valor nominal sem o ágio/deságio. No caso, o PU pago está acima do par devido ao ágio."
    },
    {
        "id": 115,
        "modulo": "Matemática Financeira",
        "pergunta": "Carro financiado em 24 parcelas de R$ 3.106,85, com a primeira no ato. Valor financiado: R$ 60 mil. Qual a taxa?",
        "opcoes": {"A": "1,82% mês", "B": "26,68% ano", "C": "1,76% mês", "D": "24,86% ano"},
        "resposta_correta": "B",
        "explicacao": "Cálculo de taxa em regime de antecipação (Begin mode na HP12c). A taxa mensal resultante anualizada é 26,68%."
    },
    {
        "id": 116,
        "modulo": "Matemática Financeira",
        "pergunta": "Se o VPL de um projeto de investimento for positivo, isso indica que:",
        "opcoes": {
            "A": "Não devemos investir, resultado indiferente.",
            "B": "Podemos investir, o projeto é lucrativo para essa taxa.",
            "C": "Podemos investir, resultado indiferente.",
            "D": "Não devemos investir, o projeto não é lucrativo."
        },
        "resposta_correta": "B",
        "explicacao": "VPL > 0 significa que o retorno do projeto supera a taxa mínima de atratividade definida."
    },
    {
        "id": 117,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Número máximo de participantes de um Clube de Ações:",
        "opcoes": {"A": "50", "B": "150", "C": "3", "D": "30"},
        "resposta_correta": "A",
        "explicacao": "Clubes de investimento têm limite mínimo de 3 e máximo de 50 participantes."
    },
    {
        "id": 118,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Qual o percentual máximo do patrimônio que um Clube pode ter em Títulos Públicos Federais?",
        "opcoes": {"A": "67%", "B": "33%", "C": "80%", "D": "100%"},
        "resposta_correta": "B",
        "explicacao": "Pelo menos 67% deve ser em ações. Logo, o limite para outros ativos (como TPF) é de 33%."
    },
    {
        "id": 119,
        "modulo": "Administração de Risco",
        "pergunta": "Sobre o conceito de Value At Risk (VaR), assinale a correta:",
        "opcoes": {
            "A": "Pode ser reduzido com hedge cambial.",
            "B": "Risco de crédito é a oscilação de valores na carteira.",
            "C": "Risco sistemático é reduzido com diversificação.",
            "D": "O VaR define a perda máxima potencial com um nível de confiança."
        },
        "resposta_correta": "D",
        "explicacao": "VaR é uma medida estatística que indica a perda máxima esperada para um dado horizonte e confiança."
    },
    {
        "id": 120,
        "modulo": "Administração de Risco",
        "pergunta": "Uma carteira 100% composta por ações possui os seguintes riscos, EXCETO:",
        "opcoes": {"A": "Liquidez", "B": "Mercado", "C": "Crédito", "D": "Sistemático"},
        "resposta_correta": "C",
        "explicacao": "Ações não possuem risco de crédito (promessa de pagamento), mas sim risco de mercado (oscilação de preço)."
    },
    {
        "id": 121,
        "modulo": "Administração de Risco",
        "pergunta": "Para menor risco de crédito e menor risco de reinvestimento, qual a melhor escolha?",
        "opcoes": {
            "A": "Tesouro IPCA 2028 com juros semestrais",
            "B": "Debêntures incentivadas 2031",
            "C": "NTN-B Principal 2028",
            "D": "CDB pré-fixado com juros mensais"
        },
        "resposta_correta": "C",
        "explicacao": "NTN-B Principal é garantida pelo governo (baixo crédito) e não paga cupons (zero risco de reinvestimento)."
    },
    {
        "id": 122,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Trata-se de uma descrição da atividade de Assessor de Investimentos (AI):",
        "opcoes": {
            "A": "Distribuir cotas de fundos de investimento sob a responsabilidade e como preposto de instituição integrante do sistema de distribuição",
            "B": "Entregar numerário (dinheiro em espécie) aos clientes da sua carteira",
            "C": "Atuar como representante de uma instituição e simultaneamente como consultor de investimentos",
            "D": "Terceirizar o serviço pelo qual foi contratado pela instituição integrante do sistema de distribuição"
        },
        "resposta_correta": "A",
        "explicacao": "O AI atua como preposto da instituição contratante, sendo vedado o manuseio de numerário ou a atuação simultânea como consultor[cite: 16]."
    },
    {
        "id": 123,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "São requisitos mínimos para ser cadastrado como Assessor de Investimentos, EXCETO:",
        "opcoes": {
            "A": "Efetuar o recolhimento da taxa mensal de fiscalização da CVM",
            "B": "Aderir ao Código de Conduta Profissional da entidade credenciadora",
            "C": "Ter sido aprovado em exame de qualificação técnica (Ancord)",
            "D": "Ter ensino médio completo no país ou equivalente no exterior"
        },
        "resposta_correta": "A",
        "explicacao": "O recolhimento de taxas é uma obrigação de manutenção, não um requisito técnico ou educacional para o cadastramento inicial[cite: 16]."
    },
    {
        "id": 124,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Qual o prazo para que a instituição contratante avise à Ancord sobre a extinção de contrato com o AI?",
        "opcoes": {
            "A": "Em até 10 dias úteis",
            "B": "Imediatamente",
            "C": "Em até 24 horas",
            "D": "Em até 30 dias corridos"
        },
        "resposta_correta": "B",
        "explicacao": "Conforme a regulamentação, a comunicação de quebra de vínculo deve ser imediata para fins de atualização cadastral[cite: 16]."
    },
    {
        "id": 125,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Sobre o vínculo de escritórios de AI (Pessoa Jurídica) com intermediários, é correto afirmar que:",
        "opcoes": {
            "A": "O escritório pode se vincular a diversas Corretoras ou Distribuidoras",
            "B": "O escritório deve ser exclusivo a apenas uma Corretora ou Distribuidora",
            "C": "O escritório deve, obrigatoriamente, ser vinculado a pelo menos duas instituições",
            "D": "A pluralidade de vínculos só é permitida para escritórios com custódia acima de R$ 10 milhões"
        },
        "resposta_correta": "A",
        "explicacao": "A Resolução CVM 178 extinguiu a exclusividade obrigatória, permitindo o modelo de 'multivínculo' para as PJs[cite: 16]."
    },
    {
        "id": 126,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Um Assessor de Investimentos decide migrar para a atividade de Gestor de Carteira Administrada. Nesse caso, ele deve:",
        "opcoes": {
            "A": "Solicitar o cancelamento do seu registro de AI",
            "B": "Solicitar a suspensão temporária por até 3 anos",
            "C": "Manter os dois registros ativos simultaneamente",
            "D": "Apenas alterar sua classificação no site da Ancord"
        },
        "resposta_correta": "A",
        "explicacao": "As atividades de AI e Gestor/Consultor são inacumuláveis; o profissional deve optar por uma delas e cancelar a outra[cite: 16]."
    },
    {
        "id": 127,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "As regras de uso de logotipos do AI em materiais publicitários aplicam-se a: I. Apostilas e Treinamentos; II. E-mails; III. Sites e Redes Sociais. Está(ão) correto(s):",
        "opcoes": {
            "A": "Apenas I e III",
            "B": "Apenas II e III",
            "C": "Apenas I e II",
            "D": "I, II e III"
        },
        "resposta_correta": "D",
        "explicacao": "Toda e qualquer comunicação do AI, seja física ou digital, deve seguir as normas de identificação visual da CVM[cite: 16]."
    },
    {
        "id": 128,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Sobre a estrutura societária de um escritório de AI (PJ), marque a alternativa INCORRETA:",
        "opcoes": {
            "A": "O escritório poderá ser uma Sociedade Limitada (Ltda)",
            "B": "O escritório poderá ser uma Sociedade Anônima (S/A)",
            "C": "O escritório não poderá ser uma Sociedade Simples",
            "D": "O escritório não precisa de uma classificação específica de sociedade (pode ser qualquer tipo)"
        },
        "resposta_correta": "D",
        "explicacao": "A norma exige tipos societários específicos que permitam a fiscalização e a responsabilidade técnica adequada[cite: 16]."
    },
    {
        "id": 129,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "O descumprimento do Programa de Educação Continuada (PEC) da Ancord resulta em:",
        "opcoes": {
            "A": "Advertência por escrito",
            "B": "Suspensão temporária de 180 dias",
            "C": "Cancelamento do credenciamento",
            "D": "Multa pecuniária fixa de R$ 5.000,00"
        },
        "resposta_correta": "C",
        "explicacao": "A manutenção da capacidade técnica via PEC é obrigatória; a falha resulta na perda da credencial[cite: 16]."
    },
    {
        "id": 130,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "É vedado ao Assessor de Investimentos, mesmo com autorização do cliente:",
        "opcoes": {
            "A": "Prospectar novos clientes para a corretora",
            "B": "Prestar informações sobre os produtos da instituição contratante",
            "C": "Utilizar a senha ou assinatura eletrônica do cliente para transmitir ordens",
            "D": "Transmitir ordens verbais recebidas do cliente para a mesa de operações"
        },
        "resposta_correta": "C",
        "explicacao": "O uso de senhas de clientes é uma infração grave e vedada em qualquer circunstância para garantir a segurança[cite: 16]."
    },
    {
        "id": 131,
        "modulo": "A Atividade do Assessor de Investimentos (AI)",
        "pergunta": "Sobre a remuneração do AI, assinale a alternativa correta:",
        "opcoes": {
            "A": "Possui um salário fixo mensal acrescido de bônus por metas",
            "B": "É exclusivamente composta por salário fixo garantido pela corretora",
            "C": "Não possui valor fixo mensal; provém do rateio de comissões das operações dos clientes",
            "D": "É tabelada pela CVM para evitar concorrência desleal entre escritórios"
        },
        "resposta_correta": "C",
        "explicacao": "A remuneração do AI é baseada na receita gerada pela sua carteira de clientes junto à instituição contratante[cite: 16]."
    },
    {
        "id": 132,
        "modulo": "Administração de Risco",
        "pergunta": "Com relação ao risco operacional, assinale a alternativa correta:",
        "opcoes": {
            "A": "É o risco de perdas (diretas ou indiretas) determinadas por erros humanos, falhas nos sistemas de informações e computadores",
            "B": "É o risco de perdas (diretas ou indiretas) determinadas por oscilações nos valores dos ativos presentes na carteira de uma instituição financeira",
            "C": "Com o objetivo de reduzir o risco operacional, é indicado que as instituições financeiras mantenham sempre a tecnologia atual sem melhorias de processos",
            "D": "É o risco de perdas (diretas ou indiretas) determinadas por oscilações de valores de dívidas lastreadas em moeda estrangeira"
        },
        "resposta_correta": "A",
        "explicacao": "O risco operacional deriva de falhas em processos internos, pessoas, sistemas ou eventos externos[cite: 17]."
    },
    {
        "id": 133,
        "modulo": "Administração de Risco",
        "pergunta": "Sobre riscos, analise as afirmações: I) Risco de crédito está associado ao não pagamento do compromisso pelo emissor (CDB, ações e debêntures); II) Risco de liquidez está associado à dificuldade de converter ativo em dinheiro; III) Risco de mercado pode ser sistemático ou não sistemático e ambos podem ser neutralizados.",
        "opcoes": {
            "A": "Todas são verdadeiras",
            "B": "Todas são falsas",
            "C": "Somente I e III são verdadeiras",
            "D": "Somente III é falsa"
        },
        "resposta_correta": "B",
        "explicacao": "A afirmação I está incorreta porque ações não possuem risco de crédito (o acionista é sócio). A III está incorreta pois o risco sistemático não pode ser neutralizado/eliminado[cite: 17]."
    },
    {
        "id": 134,
        "modulo": "Administração de Risco",
        "pergunta": "Com relação a risco, assinale a alternativa correta:",
        "opcoes": {
            "A": "O risco de mercado pode ser reduzido com operações de hedge, já o risco de liquidez é aquele decorrente da variação ligado à moeda estrangeira",
            "B": "Risco de crédito é a possibilidade de perdas decorrentes por falta de pagamento dos emissores, já o risco operacional é decorrente das oscilações dos valores dos títulos",
            "C": "O risco Sistemático pode ser reduzido através da diversificação",
            "D": "O Value At Risk define a perda máxima potencial de uma carteira, com um determinado nível de confiança"
        },
        "resposta_correta": "D",
        "explicacao": "O VaR é uma métrica estatística que estima a perda máxima esperada para um portfólio em um dado horizonte de tempo e nível de confiança[cite: 17]."
    },
    {
        "id": 135,
        "modulo": "Administração de Risco",
        "pergunta": "Com relação aos conceitos de Duration e Duration Modificada: I - A Duration é o prazo médio de um título; II - A Duration Modificada representa o quanto oscila um título; III - A Duration Modificada sempre será duas vezes superior à Duration.",
        "opcoes": {
            "A": "I e II estão corretas",
            "B": "I e III estão corretas",
            "C": "II e III estão corretas",
            "D": "I, II e III estão corretas"
        },
        "resposta_correta": "A",
        "explicacao": "A Duration mede o tempo médio de recuperação do capital, e a Modificada mede a sensibilidade do preço do título às variações na taxa de juros[cite: 17]."
    },
    {
        "id": 136,
        "modulo": "Administração de Risco",
        "pergunta": "Dois ativos (A e B) de mesmo emissor possuem prazo de 1 e 10 anos, respectivamente. O título B terá:",
        "opcoes": {
            "A": "Maior risco e menor rentabilidade que o ativo A",
            "B": "Maior risco e maior rentabilidade que o ativo A",
            "C": "Menor risco e maior rentabilidade que o ativo A",
            "D": "Menor risco e menor rentabilidade que o ativo A"
        },
        "resposta_correta": "B",
        "explicacao": "Prazos mais longos aumentam a exposição às oscilações de mercado (risco), exigindo maior prêmio de retorno (rentabilidade)[cite: 17]."
    },
    {
        "id": 137,
        "modulo": "Administração de Risco",
        "pergunta": "Ao realizar um aporte em um fundo de ações do tipo Small Caps, quais os principais riscos presentes:",
        "opcoes": {
            "A": "Operacional e Crédito",
            "B": "Operacional e Liquidez",
            "C": "Mercado e Crédito",
            "D": "Mercado e Liquidez"
        },
        "resposta_correta": "D",
        "explicacao": "Small Caps possuem alta volatilidade (mercado) e menor volume de negociação comparado às Blue Chips (liquidez)[cite: 17]."
    },
    {
        "id": 138,
        "modulo": "Administração de Risco",
        "pergunta": "O risco de liquidez presente em um título refere-se a:",
        "opcoes": {
            "A": "Impossibilidade de se comercializar um ativo por seu preço justo",
            "B": "Oscilações naturais no preço do ativo",
            "C": "Não pagamento das obrigações por parte do emissor do ativo",
            "D": "Excesso de recursos em um determinado mercado"
        },
        "resposta_correta": "A",
        "explicacao": "Liquidez é a facilidade de converter o ativo em caixa sem perda significativa de valor (preço justo)[cite: 17]."
    },
    {
        "id": 139,
        "modulo": "Administração de Risco",
        "pergunta": "Um investidor que deseja reduzir o seu risco de oscilação de taxa de juros de uma carteira de renda fixa pós-fixada, poderia:",
        "opcoes": {
            "A": "Vender contratos futuros de índice DI",
            "B": "Fazer um contrato de SWAP com ponta ativa em Juros-DI e ponta passiva em Pré-Fixado",
            "C": "Comprar contratos futuros de índice DI",
            "D": "Vender contratos futuros de Ibovespa"
        },
        "resposta_correta": "A",
        "explicacao": "A venda de contratos futuros de DI permite travar a taxa e proteger contra oscilações indesejadas[cite: 17]."
    },
    {
        "id": 140,
        "modulo": "Administração de Risco",
        "pergunta": "Um ativo com maior risco de crédito é aquele que tem:",
        "opcoes": {
            "A": "Maior prazo",
            "B": "Maior chance de inadimplência",
            "C": "Menor juros",
            "D": "Menor liquidez"
        },
        "resposta_correta": "B",
        "explicacao": "O risco de crédito é diretamente a probabilidade de o emissor não cumprir com suas obrigações financeiras[cite: 17]."
    },
    {
        "id": 141,
        "modulo": "Administração de Risco",
        "pergunta": "Seu cliente está montando uma carteira 100% composta com ações. Essa carteira possui os seguintes riscos, COM EXCEÇÃO DE:",
        "opcoes": {
            "A": "Liquidez",
            "B": "Mercado",
            "C": "Crédito",
            "D": "Sistemático"
        },
        "resposta_correta": "C",
        "explicacao": "Ações não possuem risco de crédito, pois o investidor torna-se sócio da empresa, não credor[cite: 17]."
    },
    {
        "id": 142,
        "modulo": "Administração de Risco",
        "pergunta": "Um investidor comprou uma ação por R$ 20,00. Na venda, a melhor oferta foi de R$ 13,00. Qual risco estava presente principalmente?",
        "opcoes": {
            "A": "Mercado",
            "B": "Crédito",
            "C": "Liquidez",
            "D": "Legal"
        },
        "resposta_correta": "A",
        "explicacao": "A queda no preço do ativo devido às condições de oferta e demanda caracteriza o risco de mercado[cite: 17]."
    },
    {
        "id": 143,
        "modulo": "Administração de Risco",
        "pergunta": "Tipo de risco que pode ser reduzido com a diversificação:",
        "opcoes": {
            "A": "Sistemático",
            "B": "Não Sistemático",
            "C": "Não Específico",
            "D": "De Conjuntura"
        },
        "resposta_correta": "B",
        "explicacao": "O risco não sistemático (específico) é aquele restrito a um setor ou empresa e pode ser diluído em uma carteira diversificada[cite: 17]."
    },
    {
        "id": 144,
        "modulo": "Administração de Risco",
        "pergunta": "Um investidor possui uma carteira com Duration = 900 dias. Para diminuir essa Duration, ele deverá:",
        "opcoes": {
            "A": "Comprar ativos com mais risco",
            "B": "Comprar ativos com prazo maior que 900 dias",
            "C": "Comprar ativos com prazo inferior a 900 dias",
            "D": "Comprar ativos mais defensivos"
        },
        "resposta_correta": "C",
        "explicacao": "A Duration é o prazo médio; adicionar ativos com prazos menores reduz a média ponderada da carteira[cite: 17]."
    },
    {
        "id": 145,
        "modulo": "Administração de Risco",
        "pergunta": "Sobre o sistema de Custódia Fungível, é correto afirmar:",
        "opcoes": {
            "A": "Não há vínculo entre o proprietário do ativo e o seu depositante",
            "B": "O ativo original depositado é o que deve ser devolvido",
            "C": "Um ativo com características idênticas ao depositado pode ser devolvido, sem necessidade de ser o original",
            "D": "A devolução somente pode ser feita ao proprietário original"
        },
        "resposta_correta": "C",
        "explicacao": "Bens fungíveis são aqueles que podem ser substituídos por outros da mesma espécie, qualidade e quantidade[cite: 17]."
    },
    {
        "id": 146,
        "modulo": "Administração de Risco",
        "pergunta": "Um investidor busca menor risco de crédito e menor risco de reinvestimento. Qual a melhor escolha?",
        "opcoes": {
            "A": "Tesouro IPCA+ com juros semestrais",
            "B": "Debêntures incentivadas com juros anuais",
            "C": "Tesouro IPCA+ Principal (sem juros semestrais)",
            "D": "CDB pré-fixado com juros mensais"
        },
        "resposta_correta": "C",
        "explicacao": "Títulos públicos têm o menor risco de crédito do país. Títulos 'Principal' eliminam o risco de reinvestimento dos cupons antes do vencimento[cite: 17]."
    },
    {
        "id": 147,
        "modulo": "Clubes de Investimentos",
        "pergunta": "O montante que exceder 67% do patrimônio líquido do Clube de Investimento pode ser aplicado em outros valores mobiliários de emissão de companhias abertas, sendo vedado o lançamento de:",
        "opcoes": {
            "A": "Cotas de Fundos de Investimento Referenciado.",
            "B": "Compra de opções.",
            "C": "Opções a descoberto.",
            "D": "Títulos de responsabilidade de instituição financeira."
        },
        "resposta_correta": "C",
        "explicacao": "É expressamente vedado aos Clubes de Investimento realizar operações com opções a descoberto[cite: 18]."
    },
    {
        "id": 148,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Número máximo de participantes de um Clube de Investimento:",
        "opcoes": {
            "A": "50",
            "B": "150",
            "C": "3",
            "D": "30"
        },
        "resposta_correta": "A",
        "explicacao": "Conforme a regulamentação da CVM, um Clube de Investimento deve ter no máximo 50 cotistas[cite: 18]."
    },
    {
        "id": 149,
        "modulo": "Clubes de Investimentos",
        "pergunta": "O 'Clube Shark de Ações' poderá ser administrado, conforme instrução CVM, por: I- Corretora ou Distribuidora; II - Banco de Investimento ou Múltiplo com essa carteira; III - Pelos próprios participantes. Está correto o que se afirma em:",
        "opcoes": {
            "A": "Apenas I",
            "B": "Apenas I e II",
            "C": "Apenas II e III",
            "D": "I, II e III"
        },
        "resposta_correta": "B",
        "explicacao": "A administração deve ser feita por instituição autorizada (Corretoras, Distribuidoras ou Bancos com carteira de investimento); os participantes não podem administrar o próprio clube[cite: 18]."
    },
    {
        "id": 150,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Com relação ao estatuto de um clube, o mesmo pode ser alterado para exclusão ou redução de Taxa de Administração ou Performance, mesmo sem a convocação de:",
        "opcoes": {
            "A": "Estatuto",
            "B": "Cotistas Seniores",
            "C": "Assembleia Extraordinária",
            "D": "Assembleia Geral"
        },
        "resposta_correta": "D",
        "explicacao": "Alterações que beneficiem o cotista (como redução de taxas) podem ser feitas sem a necessidade de convocação de Assembleia Geral[cite: 18]."
    },
  {
        "id": 151,
        "modulo": "Clubes de Investimentos",
        "pergunta": "O percentual máximo do patrimônio que um Clube de Investimento pode ter aplicado em Títulos Públicos Federais é de:",
        "opcoes": {
            "A": "67%",
            "B": "33%",
            "C": "80%",
            "D": "100%"
        },
        "resposta_correta": "B",
        "explicacao": "Como no mínimo 67% deve estar em ações e outros ativos variáveis, o máximo permitido para outros ativos (como Títulos Públicos) é de 33%."
    },
    {
        "id": 152,
        "modulo": "Clubes de Investimentos",
        "pergunta": "A qualidade de cotista de um Clube de Investimento caracteriza-se pela:",
        "opcoes": {
            "A": "Pelo cadastramento do cotista no Clube",
            "B": "Inscrição do nome do titular no registro de cotistas do clube",
            "C": "Pelo envio da documentação do cotista para o clube",
            "D": "Pelo aporte financeiro no clube"
        },
        "resposta_correta": "B",
        "explicacao": "O investidor torna-se formalmente cotista com a devida inscrição de seu nome no registro oficial de cotistas mantido pelo clube[cite: 18]."
    },
    {
        "id": 153,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Percentual mínimo da carteira de um Clube que deve ser direcionado para a compra de ações:",
        "opcoes": {
            "A": "67%",
            "B": "95%",
            "C": "80%",
            "D": "50%"
        },
        "resposta_correta": "A",
        "explicacao": "A regulamentação exige que pelo menos 67% do patrimônio líquido seja aplicado em ações e ativos correlatos[cite: 18]."
    },
    {
        "id": 154,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Em situação de atraso no pagamento do resgate das cotas de um Clube de Investimento, é devida multa por dia de atraso igual a:",
        "opcoes": {
            "A": "0,1% do valor da carteira, a ser paga pelo administrador do Clube.",
            "B": "0,1% do valor da carteira, a ser paga por cada cotista.",
            "C": "0,5% do valor de resgate, a ser paga por cada cotista.",
            "D": "0,5% do valor de resgate, a ser paga pelo administrador do Clube."
        },
        "resposta_correta": "D",
        "explicacao": "O administrador é o responsável pelo pagamento da multa de 0,5% sobre o valor do resgate por dia de atraso[cite: 18]."
    },
    {
        "id": 155,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Sobre o lote padrão de ativos em aplicações de ETF (Exchange Traded Funds):",
        "opcoes": {
            "A": "O lote padrão é de 10 unidades",
            "B": "Não existe lote padrão",
            "C": "O lote padrão é de 100 unidades",
            "D": "O lote padrão é de 15 unidades"
        },
        "resposta_correta": "B",
        "explicacao": "Atualmente, para negociação de cotas de ETFs, não existe a exigência de um lote padrão mínimo[cite: 18]."
    },
    {
        "id": 156,
        "modulo": "Clubes de Investimentos",
        "pergunta": "As demonstrações contábeis dos Clubes de Investimentos devem obedecer às normas contábeis da(o):",
        "opcoes": {
            "A": "Conselho Regional de Contabilidade",
            "B": "BACEN",
            "C": "CVM",
            "D": "CMN"
        },
        "resposta_correta": "C",
        "explicacao": "A Comissão de Valores Mobiliários (CVM) é o órgão responsável por ditar as normas contábeis para esses veículos de investimento[cite: 18]."
    },
    {
        "id": 157,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Conforme a instrução CVM 494/2011 (atualizada), um Clube de Investimento deve ter no mínimo _____ e no máximo _____ cotistas:",
        "opcoes": {
            "A": "3 e 150",
            "B": "3 e 50",
            "C": "10 e 50",
            "D": "10 e 150"
        },
        "resposta_correta": "B",
        "explicacao": "A regra de constituição estabelece o intervalo entre 3 (mínimo) e 50 (máximo) participantes[cite: 18]."
    },
    {
        "id": 158,
        "modulo": "Clubes de Investimentos",
        "pergunta": "Percentual máximo do total do Clube de Investimento que um único cotista pode deter:",
        "opcoes": {
            "A": "30%",
            "B": "67%",
            "C": "25%",
            "D": "40%"
        },
        "resposta_correta": "D",
        "explicacao": "Nenhum cotista pode ser detentor de mais de 40% das cotas emitidas pelo clube[cite: 18]."
    },
    {
        "id": 159,
        "modulo": "Fundos de Investimento",
        "pergunta": "Com relação à taxa de performance em fundos de investimento, é correto afirmar:",
        "opcoes": {
            "A": "É cobrada sobre o patrimônio líquido total do fundo",
            "B": "É cobrada sempre que o fundo apresenta rentabilidade positiva",
            "C": "É cobrada apenas quando o fundo excede a variação de um índice de referência (benchmark)",
            "D": "É obrigatória em todos os fundos de renda fixa"
        },
        "resposta_correta": "C",
        "explicacao": "A taxa de performance é um prêmio pago ao gestor quando o resultado do fundo supera o benchmark estabelecido."
    },
    {
        "id": 160,
        "modulo": "Fundos de Investimento",
        "pergunta": "O documento que contém as informações essenciais sobre o fundo, de forma resumida e em linguagem clara, é o:",
        "opcoes": {
            "A": "Regulamento",
            "B": "Lâmina de Informações Essenciais",
            "C": "Formulário de Informações Complementares",
            "D": "Termo de Adesão"
        },
        "resposta_correta": "B",
        "explicacao": "A Lâmina é o documento de leitura obrigatória que resume os principais riscos e características do fundo."
    },
    {
        "id": 161,
        "modulo": "Fundos de Investimento",
        "pergunta": "Um fundo de investimento que possui a maior parte de sua carteira em títulos públicos federais ou títulos privados de baixo risco de crédito é classificado como:",
        "opcoes": {
            "A": "Renda Fixa Simples",
            "B": "Ações",
            "C": "Multimercado",
            "D": "Cambial"
        },
        "resposta_correta": "A",
        "explicacao": "Fundos de Renda Fixa Simples devem ter pelo menos 95% do patrimônio em títulos públicos ou privados de baixo risco."
    },
    {
        "id": 162,
        "modulo": "Fundos de Investimento",
        "pergunta": "O responsável pela guarda dos ativos que compõem a carteira do fundo é o:",
        "opcoes": {
            "A": "Gestor",
            "B": "Administrador",
            "C": "Custodiante",
            "D": "Auditor Independente"
        },
        "resposta_correta": "C",
        "explicacao": "O custodiante faz a guarda física e o controle dos ativos financeiros do fundo."
    },
    {
        "id": 163,
        "modulo": "Fundos de Investimento",
        "pergunta": "A marcação a mercado (MtM) em fundos de investimento tem como objetivo principal:",
        "opcoes": {
            "A": "Garantir rentabilidade fixa ao investidor",
            "B": "Evitar a transferência de riqueza entre os cotistas",
            "C": "Reduzir o risco de crédito da carteira",
            "D": "Isentar o fundo do pagamento de impostos"
        },
        "resposta_correta": "B",
        "explicacao": "Ao precificar os ativos pelo valor de saída diário, evita-se que cotistas que entram ou saem prejudiquem os demais."
    },
    {
        "id": 164,
        "modulo": "Fundos de Investimento",
        "pergunta": "Sobre o sistema de 'Come-Cotas', assinale a alternativa correta:",
        "opcoes": {
            "A": "Ocorre mensalmente em todos os fundos de investimento",
            "B": "É a antecipação do Imposto de Renda que ocorre nos meses de maio e novembro",
            "C": "Aplica-se apenas aos fundos de ações",
            "D": "É uma taxa cobrada pelo administrador para cobrir custos operacionais"
        },
        "resposta_correta": "B",
        "explicacao": "O Come-Cotas é a tributação semestral automática em fundos de renda fixa e multimercados."
    },
    {
        "id": 165,
        "modulo": "Fundos de Investimento",
        "pergunta": "Um fundo de investimento 'Fechado' é aquele em que:",
        "opcoes": {
            "A": "As cotas podem ser resgatadas a qualquer momento",
            "B": "O resgate das cotas só é permitido ao término do prazo de duração do fundo",
            "C": "Não há cobrança de taxa de administração",
            "D": "Apenas investidores qualificados podem participar"
        },
        "resposta_correta": "B",
        "explicacao": "Nos fundos fechados, o investidor que deseja sair antes do prazo deve vender suas cotas no mercado secundário."
    },
    {
        "id": 166,
        "modulo": "Fundos de Investimento",
        "pergunta": "A decisão de onde investir os recursos do fundo, escolhendo quais ativos comprar ou vender, cabe ao:",
        "opcoes": {
            "A": "Custodiante",
            "B": "Auditor",
            "C": "Gestor",
            "D": "Distribuidor"
        },
        "resposta_correta": "C",
        "explicacao": "O gestor é o profissional responsável pela estratégia e execução das operações de compra e venda dos ativos."
    }
]
