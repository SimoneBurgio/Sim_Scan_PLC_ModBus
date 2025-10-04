# timers.py
import time

# ==============================================================================
# CLASSE TON (Timer On-Delay)
# ==============================================================================
class TON:
    """
    Timer On-Delay (TON) Function Block Simulation.
    """
    def __init__(self, preset_time: float):
        if preset_time < 0:
            raise ValueError("Il tempo preimpostato non può essere negativo.")
        self.PT = preset_time
        self.IN = False
        self.Q = False
        self.ET = 0.0
        self._start_time = None

    def __call__(self, IN: bool) -> bool:
        current_time = time.monotonic()
        if IN:
            if self._start_time is None:
                self._start_time = current_time
            self.ET = current_time - self._start_time
            if self.ET >= self.PT:
                self.Q = True
        else:
            self.Q = False
            self.ET = 0.0
            self._start_time = None
        self.IN = IN
        return self.Q

    def __repr__(self) -> str:
        return f"TON(PT={self.PT}s, IN={self.IN}, Q={self.Q}, ET={self.ET:.2f}s)"

# ==============================================================================
# CLASSE TOF (Timer Off-Delay)
# ==============================================================================
class TOF:
    """
    Timer Off-Delay (TOF) Function Block Simulation.
    """
    def __init__(self, preset_time: float):
        if preset_time < 0:
            raise ValueError("Il tempo preimpostato non può essere negativo.")
        self.PT = preset_time
        self.IN = False
        self.Q = False
        self.ET = 0.0
        self._start_time = None

    def __call__(self, IN: bool) -> bool:
        current_time = time.monotonic()
        if IN:
            self.Q = True
            self.ET = 0.0
            self._start_time = None
        else:
            if self.Q:
                if self._start_time is None:
                    self._start_time = current_time
                self.ET = current_time - self._start_time
                if self.ET >= self.PT:
                    self.Q = False
        self.IN = IN
        return self.Q

    def __repr__(self) -> str:
        return f"TOF(PT={self.PT}s, IN={self.IN}, Q={self.Q}, ET={self.ET:.2f}s)"


# ==============================================================================
# BLOCCO DI TEST ESEGUIBILE
# ==============================================================================
if __name__ == '__main__':
    
    # --- Test della classe TON ---
    print("--- Test della Libreria TON ---")
    timer_ton_test = TON(preset_time=3.0)
    print(f"Timer TON creato: {timer_ton_test}")
    start_sim_time = time.monotonic()
    while (time.monotonic() - start_sim_time) < 8:
        simulated_input = (time.monotonic() - start_sim_time) % 8 < 5
        timer_ton_test(IN=simulated_input)
        print(timer_ton_test)
        time.sleep(0.5)
    print("\n--- Fine Test TON ---\n")
    
    # --- Test della classe TOF ---
    print("--- Test della Libreria TOF ---")
    timer_tof_test = TOF(preset_time=3.0)
    print(f"Timer TOF creato: {timer_tof_test}")
    start_sim_time = time.monotonic()
    while (time.monotonic() - start_sim_time) < 10:
        simulated_input = (time.monotonic() - start_sim_time) < 4
        timer_tof_test(IN=simulated_input)
        print(timer_tof_test)
        time.sleep(0.5)
    print("\n--- Fine Test TOF ---")