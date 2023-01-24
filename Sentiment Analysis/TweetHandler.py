from random import random

#data structures
import pandas as pd
import numpy as np 
import queue

#sklearn & cleaning
from sklearn.feature_extraction.text import TfidfVectorizer # for vectorizing
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
from nltk.corpus import stopwords

#time
import time 
from timeit import default_timer as timer

#required imports for output model
import seaborn as sns
from matplotlib import pyplot as plt
import os
from numpy import linalg
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist

# Importing matplotlib for graphics.
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

# Importing seaborn to make nice plots.
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,rc={"lines.linewidth": 2.5})

class TWTHandler:
    #creates threadsafe queue
    def __init__(self):
        self.queue = queue.Queue()
    #pushes new tweet to threadsafe queue
    def pushNewTweet(self,tweet):
        self.queue.put(tweet)

    #defines layout of scatterplot
    def define_scatterplot(self, x, colors):
        palette = np.array(sns.color_palette("hls",3))
        f = plt.figure(figsize=(32,32))
        ax = plt.subplot(aspect='equal')
        sc = ax.scatter(x[:,0],x[:,1], lw=0, s=120, c=palette[colors.astype(np.int)])
        ax.axis('off')
        ax.axis('tight')
        txts = []
        for i in range(3):
            xtext, ytext = np.median(x[colors ==i, :], axis=0)
            txt = ax.text(xtext,ytext,str(i),fontsize=50)
            txt.set_path_effects([
                PathEffects.Stroke(linewidth=5, foreground='w'),
                PathEffects.Normal()])
            txts.append(txt)
        return f, ax, sc, txts

    #inf loop of tweet processing
    def handleTweets(self):
        redundancy_filter = stopwords.words("english")
        words_list = []
        time.sleep(1)
        print("Thread created.")
        while True:
            start_time = timer()
            #look up how many items in queue & store
            queue_size = self.queue._qsize()

            if queue_size != 0 and len(words_list)+queue_size>=3:
                #take that many items
                for i in range(queue_size):
                    words_list.append(''.join([w for w in self.queue.get().lower() if w not in redundancy_filter]))
                #apply them to TFIDF to get vectors
                tfidf_vectorizer = TfidfVectorizer()
                vectors = tfidf_vectorizer.fit_transform(words_list)
                feature_names = tfidf_vectorizer.get_feature_names_out()
                vectors = vectors.todense().tolist()
                vector_df = pd.DataFrame(vectors,columns=feature_names)

                #convert them into 2d for k-means
                k_means_model = KMeans(n_clusters=3)
                k_means_model.fit(vector_df)
                
                #grab the label 
                Y_labels = k_means_model.labels_
                #z = pd.Dataframe(Y_labels.toList())

                tsne_model = TSNE(random_state=12345).fit_transform(vector_df)
                sns.palplot(np.array(sns.color_palette('hls',3)))
                self.define_scatterplot(tsne_model, Y_labels)
                plt.savefig('scatterplot.png', dpi=120)
                plt.close()

            end_time = timer()
            elapsed_time = end_time - start_time
            #Sleep for 30 seconds - time spent on k-means
            if elapsed_time < 30:     
                time.sleep(30 - elapsed_time)
