var CONFIG = {
    PROPS: [
        { key: 'actual', label: '(Actual)' },
        { key: 'applied', label: '(Applied)' }
    ],
    PAGES: {
        home: [
            { chartId: 'summary', dataKey: 'home.summary', title: 'Sumário Geral' },
            { chartId: 'home-treasury', dataKey: 'home.homeTreasury', title: 'Sumário Tesouro Direto' },
            { chartId: 'fixed-income', dataKey: 'home.fixedIncome', title: 'Sumário Renda Fixa' },
            { chartId: 'funds', dataKey: 'home.funds', title: 'Sumário Fundos de Investimento' }
        ],
        treasury: [
            { chartId: 'home-treasury', dataKey: 'homeTreasury', title: 'Tesouro Direto' }
        ],
        fixedIncome: [
            { chartId: 'fixed-income', dataKey: 'fixedIncome', title: 'Renda Fixa' }
        ]
    }
}