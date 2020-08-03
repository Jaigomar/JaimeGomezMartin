from correlationWilliam import correlationWilliam

class steamTurbine(correlationWilliam):

    def __init__(self, kW, fm, installed):
        correlationWilliam.__init__(self, fm, installed)
        self.kW = kW

    def calculate_cost_turbine(self, Capital_factors):
        """Return steam turbine cost for a power between 100 and 20000 kW. Inputs:
        fm = material factor"""

        assert type(self.installed) == bool

        if self.kW < 100 or self.kW > 20000:
            print(
                f"    - WARNING: steam turbine power out of method bounds, 100 < kW < 20000. Results may not be accurate.")

        C = -12000 + 1630 * self.kW ** 0.75

        return correlationWilliam.calculate_cost(self, C, Capital_factors)
