import pyomo.environ as pyo
from pyomo.environ import *
from sklearn.neighbors import DistanceMetric
import pandas as pd

###############################################
class OptimalLocationModel:

    def __init__(self, df_data, p=1):
        self.df = df_data
        self.p = p

    def find(self):
        df = self.df
        # Save rows with values greater than 900 to new dataframe Implemented the model on just the Population Grid data
        # nedf = df[df["FID_"] > 900]

        # A copy of the Borlange Municipality Populations Grids Data
        df_pickup = df[['X', 'Y']].copy()
        print(df.shape)
        # A Distance Metrics of the Borlange Municipality population Grids Data
        dist = DistanceMetric.get_metric('euclidean')
        dij = df_pickup[['X', 'Y']].to_numpy()
        dij = dist.pairwise(dij)
        pd.DataFrame(dij)

        # Create the Model
        modelo = pyo.ConcreteModel()

        # Índices:
        modelo.M = range(len(dij))
        modelo.N = range(len(dij))
        # Parâmetros
        modelo.d = pyo.Param(modelo.M, modelo.N, initialize=lambda modelo, i, j: dij[i][j])
        p = self.p
        # Sets the Model parameter
        modelo.y = pyo.Var(modelo.N, within=pyo.Binary)
        modelo.x = pyo.Var(modelo.M, modelo.N, within=pyo.Binary)
        print(modelo.N)


        # Model objective Function
        def f_obj(modelo):
            return sum(modelo.x[i, j] * modelo.d[i, j] for i in modelo.M for j in modelo.N)

        modelo.objective = pyo.Objective(rule=f_obj, sense=pyo.minimize)
        # Models Constraints_1
        modelo.restricao_a = pyo.Constraint(expr=sum(modelo.y[j] for j in modelo.N) == p)
        # Model Constraints_2
        modelo.restricao_b = pyo.ConstraintList()
        for i in modelo.M:
            modelo.restricao_b.add(sum(modelo.x[i, j] for j in modelo.N) == 1)
        # Model Constraints_3
        modelo.restricao_c = pyo.ConstraintList()
        for i in modelo.M:
            for j in modelo.N:
                modelo.restricao_c.add(modelo.x[i, j] <= modelo.y[j])
        result = pyo.SolverFactory('glpk').solve(modelo)
        print(result)

        # Print the Model.y
        modelo.y.pprint()

        # PRint the model y list
        list_y = list(modelo.y.keys())
        print([j for j in list_y if modelo.y[j]() == 1])
        # Checks if a neighborhood was chosen as the median or not
        data_model = df_pickup.copy()
        data_model['Median'] = [modelo.y[i]() for i in list_y]
        print(data_model.head(16))
        # Print out the allocations made
        list_x = list(modelo.x.keys())
        allocations = [i for i in list_x if modelo.x[i]() == 1]
        allocations.sort(key=lambda x: x[0])
        print(allocations)
        # insert the allocations in to a table of the i to the median j so you can see that neighborhood 8 was allocated to 59 and soforth
        medians = [allocation[1] for allocation in allocations]
        data_model['Allocation'] = medians
        print(data_model)
        # Table for which neighborhood were chosen as median and which store each neighborhoo was allocated to  and the data set for the distances between each neighborhood and their respective medians
        data_model['Distance'] = [dij[allocation[0], allocation[1]] for allocation in allocations]
        print(data_model)
        # Add The total distance by median

        data_modelo_resumo = data_model.copy()
        abstract = data_modelo_resumo.groupby('Allocation', as_index=False).agg({"Distance": "sum"})
        print(abstract)

        return abstract


#############################

if __name__ == '__main__':
    csv_path = 'C:\\OptimalLocation\\Dalarna.csv'
    # Load the Pandas Dataframe of the Borlange Population grid
    df = pd.read_csv(csv_path, delimiter=',')

    optLoc = OptimalLocationModel(df, p=1)
    location = optLoc.find()

    print('Optimal location(s) for store: ')
    print([df['NAMN_'][i] for i in location['Allocation']])

    del optLoc
