"""Night Shift V1: deterministic, synthetic-data research sandbox. NO LIVE TRADING."""
import json, math, random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COST_PER_TURN = 0.001  # illustrative friction, not a broker quote

def synthetic_prices(seed=42, n=400):
    rng = random.Random(seed)
    p = 100.0
    out = []
    for i in range(n):
        drift = 0.00035 if i < 200 else -0.00010
        p *= math.exp(drift + rng.gauss(0, 0.012))
        out.append(p)
    return out

def backtest(prices, fast=10, slow=35):
    """Long/flat, next-bar execution proxy; signal from past observations only."""
    if not 2 <= fast < slow or len(prices) < slow + 30:
        raise ValueError("Invalid windows or too little data")
    curve = [1.0]; positions = []; trades = 0; previous = 0
    for t in range(slow, len(prices) - 1):
        short_avg = sum(prices[t-fast+1:t+1]) / fast
        long_avg = sum(prices[t-slow+1:t+1]) / slow
        position = int(short_avg > long_avg)
        if position != previous: trades += 1
        next_return = prices[t+1] / prices[t] - 1
        curve.append(curve[-1] * (1 + position * next_return - COST_PER_TURN * abs(position-previous)))
        positions.append(position)
        previous = position
    returns = [curve[i] / curve[i-1]-1 for i in range(1,len(curve))]
    avg = sum(returns)/len(returns)
    variance = sum((x-avg)**2 for x in returns)/max(1, len(returns)-1)
    sharpe = avg/math.sqrt(variance)*math.sqrt(252) if variance > 0 else 0
    peak = curve[0]; drawdown = 0
    for value in curve:
        peak = max(peak,value)
        drawdown = max(drawdown,1-value/peak)
    return {"return_pct":round((curve[-1]-1)*100,3),
            "sharpe":round(sharpe,3),"max_drawdown_pct":round(drawdown*100,3),
            "trades":trades,"observations":len(returns)}

def evaluate():
    prices = synthetic_prices()
    # Compare candidates on training segment, independently inspect later segment.
    candidates = []
    for fast,slow in [(5,20),(10,35),(15,50)]:
        training = backtest(prices[:260],fast,slow)
        holdout = backtest(prices[220:],fast,slow)
        candidates.append({"fast":fast,"slow":slow,"training":training,"holdout":holdout})
    chosen = max(candidates,key=lambda x:x["training"]["sharpe"])
    hold = chosen["holdout"]
    # These are research gates, NOT proof of tradable alpha.
    passed = hold["sharpe"]>1.5 and hold["max_drawdown_pct"]<15 and hold["trades"]>=5
    return {"timestamp_utc":datetime.now(timezone.utc).isoformat(),
            "mode":"SYNTHETIC_PAPER_ONLY","data_source":"seeded simulated prices; not market data",
            "risk":{"live_trading_enabled":False,"broker_connected":False,
                    "auto_spend_enabled":False,"approval_required":True},
            "agents":{"scout":"generate labeled synthetic scenario",
                      "sigma":"compare training hypotheses and evaluate holdout",
                      "codex":"execute reproducible pipeline",
                      "onyx":"gate result and log exceptions"},
            "candidates":candidates,"selected":chosen,
            "decision":"RESEARCH_ONLY" if passed else "REJECT",
            "warnings":["Synthetic results cannot establish real-world profitability.",
                        "Holdout overlaps training prices by design for indicator warm-up; trade periods are disjoint.",
                        "No execution, slippage or market microstructure calibration."]}

def main():
    result=evaluate()
    output=ROOT/"runs"; output.mkdir(exist_ok=True)
    filename=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")+".json"
    (output/filename).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"report":str(output/filename),"decision":result["decision"],
                      "mode":result["mode"]}))
if __name__=="__main__":
    main()
