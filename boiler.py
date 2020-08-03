from correlationWilliam import correlationWilliam

class boiler(correlationWilliam):

     def __init__(self, Q, p, fm, installed):
        correlationWilliam.__init__(self, fm, installed)
        self.Q = Q
        self.p = p

     def calculate_cost_boiler(self, Capital_factors):
         """Return boiler cost. Inputs:
         Vapor production (kg/h): 5000 < Q < 800000
         Pressure (bar): 			   10 < p < 70
         fm = material factor"""

         assert type(self.installed) == bool

         if self.Q < 5000 or self.Q > 800000:
             print(
                 f"    - WARNING: boiler vapor production out of method bounds, 5000 < Q < 800000. Results may not be accurate.")

         if self.p < 10 or self.p > 70:
             print(f"    - WARNING: boiler pressure out of method bounds, 10 < p < 70. Results may not be accurate.")

         if self.Q < 20000:
             C = 106000 + 8.7 * self.Q
         elif self.Q < 200000:
             if self.p < 15:
                 C = 110000 + 4.5 * self.Q ** 0.9
             elif self.p < 40:
                 C = 106000 + 8.7 * self.Q
             else:
                 C = 110000 + 4.5 * self.Q ** 0.9
         else:
             C = 110000 + 4.5 * self.Q ** 0.9

         return correlationWilliam.calculate_cost(self, C, Capital_factors)