import pandas as pd
import numpy as np
class regression_selection():
    def __init__(self,nome = "default", path = './', df = None):
        """
        ## Classe para instanciar data frames

        ---

        Exemplo:

        path = "./data/datasets.csv"

        nome = "Minha Analise"

        Reg_sel = regression_selection(path, nome)

        """
        print("Instanciando Classe")
        self.nome = nome

        if (df != None):
            self.df = df
        else:
            try:
                self.df = pd.read_csv(path)
            except:
                print("Erro ao carregar dataframe")

    def count_records(self):
        """
        ## Método para contar registros do data frame
     
        count = Reg_sel.count_records() 

        """
        print("Executando método")
        return len(self.df)
