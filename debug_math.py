from trading_sim.engine.simulator import FuturesSimulator
sim = FuturesSimulator(initial_balance=10000)
sim.enter_trade('LONG', price=1000, tp_amount=150, sl_amount=200)
