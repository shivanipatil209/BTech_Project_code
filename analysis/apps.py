from django.apps import AppConfig
from django.conf import settings
import os
import pickle

from tensorflow.keras.models import load_model

class DemoAppConfig(AppConfig):
    name = 'analysis'
    # create path to models
    model_path = os.path.join(settings.MODELS,'texual')
    numeric_model_path =  os.path.join(settings.MODELS,'numeric')
    transformer_path =  os.path.join(settings.MODELS, 'texual\\transformer.pkl')
    # load models into separate variables
    # these will be accessible via this class
    cv_transformer = pickle.load(open(transformer_path,'rb'))
    logistic_regression = pickle.load(open(model_path+'\\lr_classifier.sav','rb'))
    adaboost = pickle.load(open(model_path+'\\adaboost_classifier.sav','rb'))
    bernoulliNB = pickle.load(open(model_path+'\\BernoulliNB_classifier.sav','rb'))
    complementNB = pickle.load(open(model_path+'\\ComplementNB_classifier.sav','rb'))
    dtree = pickle.load(open(model_path+'\\dtree_classifier.sav','rb'))
    gradient_boosting = pickle.load(open(model_path+'\\gradient_boosting.sav','rb'))
    Kneighbors = pickle.load(open(model_path+'\\Kneighbors_classifier.sav','rb'))
    linear_svc = pickle.load(open(model_path+'\\linear_svc.sav','rb'))
    multinomialNB = pickle.load(open(model_path+'\\MultinomialNB_classifier.sav','rb'))
    perceptron = pickle.load(open(model_path+'\\perceptron.sav','rb'))
    random_forest = pickle.load(open(model_path+'\\rf_classifier.sav','rb'))
    sgd_classifier = pickle.load(open(model_path+'\\SGD_classifier.sav','rb'))
    svm = pickle.load(open(model_path+'\\svm.sav','rb'))

    shallow_rnn = load_model(model_path+'\\Shallow_RNN.h5',compile = False)
    deep_rnn = load_model(model_path+'\\Deep_RNN.h5',compile = False)
    #cnn = load_model(model_path+'\\CNN.h5',compile = False)
    

    bidirectional_rnn = load_model(model_path+'\\Bidirectional_RNN.h5',compile = False)
    lstm = load_model(model_path+'\\LSTM.h5',compile = False)


    AAPL_LSTM = load_model(numeric_model_path+'\\AAPL_LSTM.h5',compile = False)
    AAPL_scalar =  pickle.load(open(numeric_model_path+'\\scalar_AAPL.pkl','rb'))

    AMZN_LSTM = load_model(numeric_model_path+'\\AMZN_LSTM.h5',compile = False)
    AMZN_scalar =  pickle.load(open(numeric_model_path+'\\scalar_AMZN.pkl','rb'))