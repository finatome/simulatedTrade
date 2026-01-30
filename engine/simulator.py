class FuturesSimulator:
    def __init__(self, initial_balance=10000, leverage=10):
        self.balance = initial_balance
        self.leverage = leverage
        self.current_pos = None  # None, 'LONG', or 'SHORT'
        self.entry_price = 0
        self.tp_price = 0
        self.sl_price = 0
        self.scenario_history = [] # Stores result of each of the 100 runs
        self.candles = None
        self.current_step = 0

    def enter_trade(self, side, price, tp_points=10, sl_points=10):
        self.current_pos = side
        self.entry_price = price
        
        # Inputs are Price Points (absolute price change)
        # e.g. price=1000, tp_points=10 -> tp_price=1010 (Long)
        
        if side == 'LONG':
            self.tp_price = price + tp_points
            self.sl_price = price - sl_points
        else:
            self.tp_price = price - tp_points
            self.sl_price = price + sl_points
            
        print(f"DEBUG: Trade {side} @ {price}. TP={self.tp_price} (+{tp_points}), SL={self.sl_price} (-{sl_points})")

    def check_exit(self, candle):
        """
        Checks if the candle High/Low hit TP or SL.
        Returns (triggered, reason, price)
        reason: 'TP', 'SL', or None
        """
        if not self.current_pos:
            return False, None, 0
        
        # Logic: Check if price HIT the level during the candle.
        # For LONG: High >= TP -> Trigger TP. Low <= SL -> Trigger SL.
        # For SHORT: Low <= TP -> Trigger TP. High >= SL -> Trigger SL.
        # Conflict: If both hit (big candle), traditionally SL is considered hit first for safety,
        # or we check open to see which is closer? 
        # Simpler: Check worst case first (SL).
        
        high = candle['High']
        low = candle['Low']
        
        if self.current_pos == 'LONG':
            if low <= self.sl_price:
                return True, 'SL', self.sl_price
            if high >= self.tp_price:
                return True, 'TP', self.tp_price
                
        elif self.current_pos == 'SHORT':
            if high >= self.sl_price:
                return True, 'SL', self.sl_price
            if low <= self.tp_price:
                return True, 'TP', self.tp_price
                
        return False, None, 0

    def close_trade(self, exit_price, reason='MANUAL'):
        if self.current_pos is None:
            return 0
        
        multiplier = 1 if self.current_pos == 'LONG' else -1
        raw_pnl = (exit_price - self.entry_price) / self.entry_price
        realized_pnl = raw_pnl * self.balance * self.leverage * multiplier
        
        self.balance += realized_pnl
        
        self.scenario_history.append({
            'side': self.current_pos,
            'pnl': realized_pnl,
            'return_pct': raw_pnl * self.leverage * 100 * multiplier,
            'exit_price': exit_price,
            'entry_price': self.entry_price,
            'reason': reason
        })
        
        self.current_pos = None
        self.tp_price = 0
        self.sl_price = 0
        return realized_pnl

    def get_unrealized_pnl(self, current_price):
        if not self.current_pos: return 0
        multiplier = 1 if self.current_pos == 'LONG' else -1
        return ((current_price - self.entry_price) / self.entry_price) * self.balance * self.leverage * multiplier

    def load_data(self, df):
        """
        Loads the market data for the current scenario.
        """
        self.candles = df
        self.current_step = 0

    def step(self):
        """
        Advances the simulation step.
        """
        self.current_step += 1

    def get_visible_slice(self):
        """
        Returns the data visible up to the current step (plus minimal history).
        """
        if self.candles is None:
            return None
        # In app.py logic, state['idx'] tracks the view index.
        # This method might be helper or unused if app handles slicing.
        # But app.py calls sim.candles directly.
        pass

    def reset(self):
        """
        Resets the trade state for a new scenario.
        Does NOT reset balance or history (that's global).
        """
        self.current_pos = None
        self.entry_price = 0
        self.tp_price = 0
        self.sl_price = 0
        self.current_step = 0

