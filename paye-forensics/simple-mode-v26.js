// PAYE Forensics v26 - Explain It Like I'm Five mode
// Plain-language presentation layer only. It never changes tax calculations.

const money = n => `£${Number(n || 0).toLocaleString('en-GB', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

export function buildSimpleExplanation(input = {}) {
  const code = String(input.taxCode || '').toUpperCase().replace(/\s+/g,'');
  const iya = Number(input.iyaAmount || 0);
  const underpayment = Number(input.underpayment || 0);
  const personalAllowance = Number(input.personalAllowance || 12570);
  const reasons = Array.isArray(input.reasons) ? input.reasons : [];
  const isK = /^(S|C)?K\d+/.test(code);
  const nonCum = /(W1|M1|X|NONCUM)$/.test(code);

  const cards = [];

  cards.push({
    emoji:'🪣',
    title:'Think of your tax-free allowance like one bucket',
    text:`You start with one tax-free bucket. In this example it is ${money(personalAllowance)} for the year. Different things can use up space in that bucket.`
  });

  if (reasons.length) {
    cards.push({
      emoji:'🥄',
      title:'Some things can use up the bucket',
      text:'HMRC may take account of things like State Pension, taxable benefits, savings interest or earlier tax owed. Each one can reduce how much tax-free space is left.',
      items: reasons.map(r => `${r.title}${Number(r.amount||0) ? `: ${money(r.amount)}` : ''}`)
    });
  }

  if (isK) {
    cards.push({
      emoji:'🔁',
      title:'A K code means the bucket has run out',
      text:'When the deductions used in your code are bigger than the tax-free allowance, the code can flip into a K code. A K code is not a fine or punishment. It tells payroll to collect more tax through your pay or pension.'
    });
  } else if (code) {
    cards.push({
      emoji:'🏷️',
      title:`Your tax code is ${code}`,
      text:'Think of the tax code as an instruction label sent to payroll. It helps payroll decide how much tax to take from this pay or pension.'
    });
  }

  if (iya > 0) {
    cards.push({
      emoji:'🧮',
      title:'An IYA means HMRC found extra tax during this tax year',
      text:`The IYA amount you entered is ${money(iya)}. Think of it as HMRC saying: “We think more tax needs to be collected before the tax year ends.” The code may then be adjusted to help collect it.`
    });
  }

  if (nonCum) {
    cards.push({
      emoji:'📅',
      title:'M1 / W1 / X means “look at this pay period on its own”',
      text:'Instead of re-checking everything from the start of the tax year, payroll treats this pay period separately while using that code.'
    });
  }

  if (underpayment > 0) {
    cards.push({
      emoji:'🧩',
      title:'The underpayment is the missing piece',
      text:`The underpayment you entered is ${money(underpayment)}. It means that, after comparing the tax due with the tax already collected, HMRC believes some tax is still missing. Our job is to explain how that may have happened.`
    });
  }

  cards.push({
    emoji:'🛑',
    title:'Three different things',
    text:'Tax code = the instruction. IYA = extra tax HMRC wants to collect during this year. Underpayment = the amount still not collected. They are connected, but they are not the same thing.'
  });

  return {
    version:'26',
    mode:'EXPLAIN_LIKE_FIVE',
    cards,
    oneLine: isK
      ? 'Your normal tax-free allowance has been used up by coding deductions, so payroll has been given a K code to collect more tax.'
      : 'Your tax code is the instruction payroll follows; any IYA or underpayment explains why HMRC may have changed that instruction.',
    guardrail:'Simple Mode changes the words, not the tax calculation. It is an explanation of possible PAYE mechanics from confirmed information, not proof of fault or a replacement HMRC calculation.'
  };
}
