from django.apps import AppConfig
from .predictor.compose import Compose
import pandas as pd
import warnings

compose = Compose()


def init_predictor():
    warnings.filterwarnings('ignore')
    random_state = 50

    bundes = pd.read_csv('futbik/predictor/data/shots_bundes_extended.csv').dropna(axis=0)
    apl = pd.read_csv('futbik/predictor/data/shots_apl_extended.csv').dropna(axis=0)
    x_train = pd.concat([bundes, apl])
    compose.fit(x_train)


class FutbikConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'futbik'

    def ready(self):
        init_predictor()