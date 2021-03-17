
class OptimalLocationModel:
    def CalculateOptimalLocation(knkod):
        if knkod == 0:
            optimal_city = "Sweden"
            optimal_loc  = '0:0:0:0:0'
        elif knkod == 1000:
            optimal_city = "Borlänge"
            optimal_loc  = '777:888:999:888:999'
        elif knkod == 1001:
            optimal_city = "Stockholm"
            optimal_loc  = '111:222:333:444:555'

        return optimal_city, optimal_loc


# Testing
print (OptimalLocationModel.CalculateOptimalLocation(0))
print (OptimalLocationModel.CalculateOptimalLocation(1001))