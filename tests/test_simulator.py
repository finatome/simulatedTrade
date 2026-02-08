import unittest
import pandas as pd
from engine.simulator import FuturesSimulator

class TestFuturesSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = FuturesSimulator(initial_balance=10000, leverage=10)

    def test_initialization(self):
        self.assertEqual(self.sim.balance, 10000)
        self.assertEqual(self.sim.leverage, 10)
        self.assertIsNone(self.sim.current_pos)
        self.assertEqual(self.sim.current_step, 0)

    def test_enter_long(self):
        self.sim.enter_trade('LONG', 1000, tp_points=10, sl_points=5)
        self.assertEqual(self.sim.current_pos, 'LONG')
        self.assertEqual(self.sim.entry_price, 1000)
        self.assertEqual(self.sim.tp_price, 1010)
        self.assertEqual(self.sim.sl_price, 995)

    def test_enter_short(self):
        self.sim.enter_trade('SHORT', 1000, tp_points=10, sl_points=5)
        self.assertEqual(self.sim.current_pos, 'SHORT')
        self.assertEqual(self.sim.entry_price, 1000)
        self.assertEqual(self.sim.tp_price, 990) # Short TP is lower
        self.assertEqual(self.sim.sl_price, 1005) # Short SL is higher

    def test_check_exit_tp_long(self):
        self.sim.enter_trade('LONG', 1000, tp_points=10, sl_points=10)
        # Candle hits TP (High >= 1010)
        candle = {'High': 1012, 'Low': 1000, 'Open': 1000, 'Close': 1005}
        triggered, reason, price = self.sim.check_exit(candle)
        self.assertTrue(triggered)
        self.assertEqual(reason, 'TP')
        self.assertEqual(price, 1010)

    def test_check_exit_sl_long(self):
        self.sim.enter_trade('LONG', 1000, tp_points=10, sl_points=10)
        # Candle hits SL (Low <= 990)
        candle = {'High': 1005, 'Low': 985, 'Open': 1000, 'Close': 995}
        triggered, reason, price = self.sim.check_exit(candle)
        self.assertTrue(triggered)
        self.assertEqual(reason, 'SL')
        self.assertEqual(price, 990)

    def test_check_exit_tp_short(self):
        self.sim.enter_trade('SHORT', 1000, tp_points=10, sl_points=10)
        # Candle hits TP (Low <= 990)
        candle = {'High': 1000, 'Low': 988, 'Open': 1000, 'Close': 995}
        triggered, reason, price = self.sim.check_exit(candle)
        self.assertTrue(triggered)
        self.assertEqual(reason, 'TP')
        self.assertEqual(price, 990)

    def test_check_exit_sl_short(self):
        self.sim.enter_trade('SHORT', 1000, tp_points=10, sl_points=10)
        # Candle hits SL (High >= 1010)
        candle = {'High': 1015, 'Low': 1000, 'Open': 1000, 'Close': 1005}
        triggered, reason, price = self.sim.check_exit(candle)
        self.assertTrue(triggered)
        self.assertEqual(reason, 'SL')
        self.assertEqual(price, 1010)

    def test_close_trade_long_profit(self):
        self.sim.enter_trade('LONG', 1000)
        # Exit at 1010 (1% move)
        # Leverage 10 -> 10% return
        # Balance 10000 -> Profit 1000
        pnl = self.sim.close_trade(1010)
        self.assertAlmostEqual(pnl, 1000)
        self.assertEqual(self.sim.balance, 11000)
        self.assertIsNone(self.sim.current_pos)
        self.assertEqual(len(self.sim.scenario_history), 1)
        self.assertEqual(self.sim.scenario_history[0]['pnl'], 1000)

    def test_close_trade_short_profit(self):
        self.sim.enter_trade('SHORT', 1000)
        # Exit at 990 (1% move down -> Profit for short)
        # Leverage 10 -> 10% return
        # Balance 10000 -> Profit 1000
        pnl = self.sim.close_trade(990)
        self.assertAlmostEqual(pnl, 1000)
        self.assertEqual(self.sim.balance, 11000)
        
    def test_reset(self):
        self.sim.enter_trade('LONG', 1000)
        self.sim.current_step = 50
        self.sim.reset()
        self.assertIsNone(self.sim.current_pos)
        self.assertEqual(self.sim.entry_price, 0)
        self.assertEqual(self.sim.current_step, 0)
        # Balance should NOT reset
        self.assertEqual(self.sim.balance, 10000)

if __name__ == '__main__':
    unittest.main()
