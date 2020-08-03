from correlationWilliam import correlationWilliam

class pump(correlationWilliam):

     def __init__(self, Q, fm, installed):
        correlationWilliam.__init__(self, fm, installed)
        self.Q = Q

     def calculate_cost_pump(self, Capital_factors):
         """Return centrifuge pump cost for a caudal between 0.2 and 126 L/s. Inputs:
             phase = 'Fluids', 'Fluids - Solids' or 'Solids'
             fm = material factor"""

         assert type(self.installed) == bool

         if self.Q < 0.2 or self.Q > 126:
             print(f"    - WARNING: pump caudal out of method bounds, 0.2 < Q (L/s) < 126. Results may not be accurate.")

         C = 6900 + 206 * self.Q ** 0.9

         return correlationWilliam.calculate_cost(self, C, Capital_factors)