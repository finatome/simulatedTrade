import numpy as np

def calculate_metrics(history):
    if not history:
        return {
            "win_rate": 0, 
            "profit_factor": 0, 
            "total_pnl": 0, 
            "trade_count": 0
        }
    
    pnls = [t['pnl'] for t in history]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    
    win_rate = (len(wins) / len(pnls)) * 100 if pnls else 0
    gross_profits = sum(wins)
    gross_losses = abs(sum(losses))
    
    profit_factor = gross_profits / gross_losses if gross_losses > 0 else (gross_profits if gross_profits > 0 else 0)
    
    return {
        "win_rate": round(win_rate, 1),
        "profit_factor": round(profit_factor, 2),
        "total_pnl": round(sum(pnls), 2),
        "trade_count": len(pnls)
    }
