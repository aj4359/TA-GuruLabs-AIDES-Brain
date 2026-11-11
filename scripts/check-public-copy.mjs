#!/usr/bin/env node
// Advisory preflight for public-facing TA GuruLabs copy. No network or credentials.
import { readFileSync } from "node:fs";
const file = process.argv[2];
if (!file) {
  console.error("Usage: node scripts/check-public-copy.mjs <draft.txt>");
  process.exit(2);
}
let content;
try { content = readFileSync(file, "utf8"); }
catch (err) { console.error("Could not read draft:", err.message); process.exit(2); }
const text = content.replace(/https?:\/\/\S+/g, "");
const checks = [
  { name:"AIDES", pattern:/\bAIDEs?\b/gi, explain:/digital assistants?|digital helpers?/i, tip:"Explain AIDEs as specialist digital assistants." },
  { name:"GMCH", pattern:/\bGMCH\b/gi, explain:/music (creation|production|editing) (and |& )?(editing |creation |production )?(system|tool|engine)/i, tip:"Use 'our music creation and editing system' instead of unexplained GMCH." },
  { name:"agentic", pattern:/\bagentic\b/gi, explain:/digital assistants?|digital workers?/i, tip:"Use 'digital assistants working together'." },
  { name:"API", pattern:/\bAPI\b/g, explain:/software (services|systems).*?(talk|communicat|exchang|connect)/i, tip:"Explain as a way software systems exchange information." },
  { name:"MVP", pattern:/\bMVP\b/g, explain:/first working version|minimum viable product/i, tip:"Say 'first working version'." },
  { name:"HUNTR-X", pattern:/HUNTR-X/gi, explain:/recruitment (platform|technology|project|tool|system)/i, tip:"Say what HUNTR-X does before naming it." },
];
const flags=[];
if (/\bAIDS\b/.test(text)) flags.push("Use 'digital assistants', not 'AIDS'.");
for (const c of checks) {
  if (c.pattern.test(text) && !c.explain.test(text)) flags.push(c.name+": "+c.tip);
}
if (!/TA GuruLabs|JingWuMedia|Jingwu Media/i.test(text)) flags.push("No clear studio identity; confirm the intended audience knows who is speaking.");
if (flags.length) { console.log("Review required:\n"+flags.map(s=>"- "+s).join("\n")); process.exitCode=1; }
else console.log("Basic jargon scan passed. This does NOT confirm factual accuracy or publication readiness.");
