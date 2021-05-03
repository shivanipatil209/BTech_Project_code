from django.shortcuts import render


# Create your views here.

from analysis.forms import SearchForm

from .forms import SearchForm
from django.template import loader
from django.http import HttpResponse
from .services import collect_tweets
from django.shortcuts import render
from .apps import DemoAppConfig
from django.http import JsonResponse
import MySQLdb
import pymysql
from sqlalchemy import create_engine
import os 
import pandas as pd
from .models import usersignup
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def search(request):
   if request.method == "POST":
      #Get the posted form
      MySearchForm = SearchForm(request.POST)
      

      if MySearchForm.is_valid():
         search_words = MySearchForm.cleaned_data['search_words']

         context = {
            'search_words' : search_words
            }

         #calling function from other .py file
         collect_tweets(search_words)

         template = loader.get_template('analysis/predict.html')
        
         return HttpResponse(template.render(context, request))
   else:
      MySearchForm = SearchForm()

   return render(request,'analysis/home1.html',{'form': MySearchForm})


def predict(request):
       return render(request,"analysis/predict.html")

def model(request):
   
   # create sqlalchemy engine
   engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 

   table_rows = engine.execute('SELECT preprocessed_text FROM tweets_table').fetchall()
   df = pd.DataFrame(table_rows, columns=['text'])
   print(len(df))

  
   test_set = DemoAppConfig.cv_transformer.transform(df['text'])
   predictions = DemoAppConfig.logistic_regression.predict(test_set)

   positive_count = predictions.tolist().count(1)
   negative_count = predictions.tolist().count(0)
   
   #print(prediction)
   labels = ['positive','negative']
   data=[positive_count,negative_count]
   print(data)
   
   return render(request, 'analysis/results.html', {
        'labels': labels,
        'data': data,
    })


   
      

    

