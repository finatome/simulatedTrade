import unittest
from engine.analytics import calculate_metrics

class TestAnalytics(unittest.TestCase):
    def test_empty_history(self):
        history = []
        metrics = calculate_metrics(history)
        self.assertEqual(metrics['trade_count'], 0)
        self.assertEqual(metrics['total_pnl'], 0)
        self.assertEqual(metrics['win_rate'], 0)
        self.assertEqual(metrics['profit_factor'], 0)

    def test_calculate_metrics_mixed_results(self):
        history = [
            {'pnl': 100},
            {'pnl': -50},
            {'pnl': 200},
            {'pnl': -50}
        ]
        metrics = calculate_metrics(history)
        
        # 4 trades
        self.assertEqual(metrics['trade_count'], 4)
        
        # Total PnL: 100 - 50 + 200 - 50 = 200
        self.assertEqual(metrics['total_pnl'], 200)
        
        # Win rate: 2 wins / 4 total = 50%
        self.assertEqual(metrics['win_rate'], 50.0)
        
        # Profit factor: (100+200) / (50+50) = 300 / 100 = 3.0
        self.assertEqual(metrics['profit_factor'], 3.0)

    def test_calculate_metrics_all_wins(self):
        history = [{'pnl': 100}, {'pnl': 50}]
        metrics = calculate_metrics(history)
        self.assertEqual(metrics['win_rate'], 100.0)
        self.assertEqual(metrics['profit_factor'], 150) # Gross profits / 0 (handled as gross profits if losses 0) -> check impl logic
        # Impl: profit_factor = gross_profits / gross_losses if gross_losses > 0 else (gross_profits if gross_profits > 0 else 0)
        # So 150 / 0 -> 150

    def test_calculate_metrics_all_losses(self):
        history = [{'pnl': -100}, {'pnl': -50}]
        metrics = calculate_metrics(history)
        self.assertEqual(metrics['win_rate'], 0.0)
        self.assertEqual(metrics['profit_factor'], 0)

if __name__ == '__main__':
    unittest.main()
