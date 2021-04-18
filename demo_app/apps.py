from django.apps import AppConfig
from django.conf import settings
import os
import pickle

class DemoAppConfig(AppConfig):
    name = 'demo_app'
    # create path to models
    model_path = os.path.join(settings.MODELS, 'lr_classifier.sav')
    transformer_path =  os.path.join(settings.MODELS, 'transformer.pkl')
    # load models into separate variables
    # these will be accessible via this class
    logistic_regression = pickle.load(open(model_path,'rb'))
    cv_transformer = pickle.load(open(transformer_path,'rb'))

    