# modified from https://towardsdatascience.com/how-to-cluster-images-based-on-visual-similarity-cd6e7209fe34

# for loading/processing the images  
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array 
from keras.applications.vgg16 import preprocess_input 

# models 
from keras.applications.vgg16 import VGG16 
from keras.models import Model

# clustering and dimension reduction
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# for everything else
import os
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import pickle
import csv

def main():
    path = r"/Users/cimendoz/bus-sim/images/sankey/"

    # change the working directory to the path where the images are located
    os.chdir(path)

    # this list holds all the image filename
    sankeys = []

    # creates a ScandirIterator aliased as files
    with os.scandir(path) as files:
    # loops through each file in the directory
        for file in files:
            if file.name.endswith('.png'):
            # adds only the image files to the sankeys list
                sankeys.append(file.name)
                
                
                
    model = VGG16()
    model = Model(inputs = model.inputs, outputs = model.layers[-2].output)

    def extract_features(file, model):
        # load the image as a 224x224 array
        img = load_img(file, target_size=(224,224))
        # convert from 'PIL.Image.Image' to numpy array
        img = np.array(img) 
        # reshape the data for the model reshape(num_of_samples, dim 1, dim 2, channels)
        reshaped_img = img.reshape(1,224,224,3) 
        # prepare image for model
        imgx = preprocess_input(reshaped_img)
        # get the feature vector
        features = model.predict(imgx)
        return features
    
    data = {}
    p = r"/Users/cimendoz/bus-sim/vectors/sankey/sankey_labels.csv"

    # lop through each image in the dataset
    for sankey in sankeys:
        feat = extract_features(sankey,model)
        data[sankey] = feat
        # # try to extract the features and update the dictionary
        # try:
        #     feat = extract_features(sankey,model)
        #     data[sankey] = feat
        # # if something fails, save the extracted features as a pickle file (optional)
        # except:
        #     with open(p,'wb') as file:
        #         pickle.dump(data,file)
            
    
    # get a list of the filenames
    filenames = np.array(list(data.keys()))

    # get a list of just the features
    feat = np.array(list(data.values()))

    # reshape so that there are 210 samples of 4096 vectors
    feat = feat.reshape(-1,4096)

    # get the unique labels (from the sankey_labels.csv)
    df = pd.read_csv('/Users/cimendoz/bus-sim/cluster_labels.csv')
    label = df['label'].tolist()
    unique_labels = list(set(label))

    # reduce the amount of dimensions in the feature vector
    pca = PCA(n_components=97, random_state=22)
    pca.fit(feat)
    x = pca.transform(feat)

    # cluster feature vectors
    kmeans = KMeans(n_clusters=len(unique_labels), random_state=22)
    kmeans.fit(x)

    # holds the cluster id and the images { id: [images] }
    groups = {}
    for file, cluster in zip(filenames,kmeans.labels_):
        if cluster not in groups.keys():
            groups[cluster] = []
            groups[cluster].append(file)
        else:
            groups[cluster].append(file)

    # reshape groups for file
    file_groups = []
    for key in groups:
        for curr_file in groups[key]:
            file_groups.append({
                "cluster": str(key),
                "file": str(curr_file)
            })
    print(file_groups)

    # write to file
    with open('sankey_clusters.csv', 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = ["cluster", "file"]) 
        writer.writeheader() 
        writer.writerows(file_groups)

    # function that lets you view a cluster (based on identifier)        
    def view_cluster(cluster):
        plt.figure(figsize = (11,11))
        # gets the list of filenames for a cluster
        files = groups[cluster]
        # only allow up to 30 images to be shown at a time
        if len(files) > 30:
            print(f"Clipping cluster size from {len(files)} to 30")
            files = files[:29]
        # plot each image in the cluster
        for index, file in enumerate(files):
            plt.subplot(10,10,index+1)
            img = load_img(file)
            img = np.array(img)
            plt.imshow(img)
            plt.axis('off')

    for label in unique_labels:
        view_cluster(label)     
    
    # this is just incase you want to see which value for k might be the best 
    sse = []
    list_k = list(range(3, 50))

    for k in list_k:
        km = KMeans(n_clusters=k, random_state=22)
        km.fit(x)
        
        sse.append(km.inertia_)

    # Plot sse against k
    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sse)
    plt.xlabel(r'Number of clusters *k*')
    plt.ylabel('Sum of squared distance')
    plt.show()

if __name__ == "__main__":
    main()