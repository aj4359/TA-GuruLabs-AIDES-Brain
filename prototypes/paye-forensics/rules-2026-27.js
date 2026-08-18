window.PAYE_RULES_2026_27 = {
  id: 'UK-2026-27-v1',
  taxYear: '2026/27',
  personalAllowance: 12570,
  personalAllowanceTaperStart: 100000,
  personalAllowanceZeroAt: 125140,
  startingRateSavingsLimit: 5000,
  personalSavingsAllowance: { basic: 1000, higher: 500, additional: 0 },
  dividendAllowance: 500,
  ukSavingsBands: [
    { id: 'UK-SAV-BASIC-2026-27', upper: 37700, rate: 0.20 },
    { id: 'UK-SAV-HIGHER-2026-27', upper: 125140, rate: 0.40 },
    { id: 'UK-SAV-ADDITIONAL-2026-27', upper: Infinity, rate: 0.45 }
  ],
  ukDividendBands: [
    { id: 'UK-DIV-BASIC-2026-27', upper: 37700, rate: 0.1075 },
    { id: 'UK-DIV-HIGHER-2026-27', upper: 125140, rate: 0.3575 },
    { id: 'UK-DIV-ADDITIONAL-2026-27', upper: Infinity, rate: 0.3935 }
  ],
  mainNonSavingsBands: [
    { id: 'MAIN-BASIC-2026-27', width: 37700, rate: 0.20, label: 'Basic rate' },
    { id: 'MAIN-HIGHER-2026-27', width: 87440, rate: 0.40, label: 'Higher rate' },
    { id: 'MAIN-ADDITIONAL-2026-27', width: Infinity, rate: 0.45, label: 'Additional rate' }
  ],
  scotlandNonSavingsBands: [
    { id: 'SCOT-STARTER-2026-27', width: 3967, rate: 0.19, label: 'Starter rate' },
    { id: 'SCOT-BASIC-2026-27', width: 12989, rate: 0.20, label: 'Basic rate' },
    { id: 'SCOT-INTERMEDIATE-2026-27', width: 14136, rate: 0.21, label: 'Intermediate rate' },
    { id: 'SCOT-HIGHER-2026-27', width: 31338, rate: 0.42, label: 'Higher rate' },
    { id: 'SCOT-ADVANCED-2026-27', width: 62710, rate: 0.45, label: 'Advanced rate' },
    { id: 'SCOT-TOP-2026-27', width: Infinity, rate: 0.48, label: 'Top rate' }
  ],
  sources: [
    { title: 'Income Tax rates and allowances for current and previous tax years', authority: 'GOV.UK / HMRC' },
    { title: 'Income Tax in Scotland: current rates', authority: 'GOV.UK' },
    { title: 'Tax on savings interest', authority: 'GOV.UK' }
  ]
};
