import soccerdata as sd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sofascore = sd.Sofascore(seasons=2024)
leagues = sofascore.read_leagues()
print(leagues)