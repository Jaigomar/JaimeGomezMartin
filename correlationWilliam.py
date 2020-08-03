class correlationWilliam:

    def __init__(self, fm, installed):
        self.fm = fm
        self.installed = installed

    def calculate_cost(self, C, Capital_factors):
        """
        Return estimated cost
        """
        if self.installed:
            C *= ((1 + Capital_factors.loc["fp"]["Fluids"]) * self.fm + (
                    Capital_factors.loc["fer"]["Fluids"] + Capital_factors.loc["fel"]["Fluids"]
                    + Capital_factors.loc["fi"]["Fluids"] + Capital_factors.loc["fc"]["Fluids"]
                    + Capital_factors.loc["fs"]["Fluids"] + Capital_factors.loc["fl"]["Fluids"]))
        return C