# PAYE Forensics verified rule notes — 2026/27

Prototype reference only. These rules must remain tax-year and jurisdiction versioned, with authoritative source metadata retained in the calculation audit.

Verified against GOV.UK on 14 August 2026:

- Standard Personal Allowance: £12,570. Personal Allowance tapers by £1 for every £2 of adjusted net income above £100,000 and reaches zero at £125,140.
- England, Northern Ireland and Wales non-savings bands: 20% basic rate to £37,700 taxable income; 40% higher rate from £37,701 to £125,140; 45% additional rate above that.
- Starting rate for savings: up to £5,000 at 0%, reduced as non-savings/non-dividend income rises above the Personal Allowance.
- Personal Savings Allowance: up to £1,000 for basic-rate taxpayers, £500 for higher-rate taxpayers and £0 for additional-rate taxpayers.
- Dividend Allowance: £500.
- 2026/27 dividend rates above the allowance: 10.75% basic, 35.75% higher, 39.35% additional.
- ISA income is not included as ordinary taxable savings/dividend income.
- Scotland 2026/27 non-savings bands after allowances: 19% to £3,967; 20% £3,968–£16,956; 21% £16,957–£31,092; 42% £31,093–£62,430; 45% £62,431–£125,140; 48% above £125,140. Savings and dividend taxation remains UK-wide.

Authoritative sources:
- GOV.UK: Income Tax rates and Personal Allowances, current rates and allowances.
- GOV.UK/HMRC: Income Tax rates and allowances for current and previous tax years.
- GOV.UK: Tax on dividends.
- GOV.UK/HMRC: Check how much tax you pay on dividends and interest from savings.

Engineering note: do not infer an HMRC reason solely because the reconstructed number is close. The UI must retain the wording “possible reconstruction” and distinguish HMRC stated amounts from PAYE Forensics estimates.