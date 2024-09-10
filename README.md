# CRNN_wor2feat

## Artificial Dataset
Use generator module to generate synthetic dataset based on a csv files containing list of words. 
the images are augmented at random. Basic augmentations include rotations, blur, sharpness,colour
The data is sent to a dataset folder in working directory. A label.csv file is created in same directory mapping image names to labels


## Architecture
A covolution first Recurrent later, because we want the image features first :) 
CRNN, has 2 LSTM layer and not a lot of hidden_dimension (512)
There are not a whole lot to categorise perse
This keeps the model short and also leaves space to optimise relevant hyper-parameter like dropout,weight_decay,normalisation, CNN layers
CNN is single Channel, because there is not much to learn about words from colors.


## The Model Improvements
The model is extremely under_trained and under_optimised at the moment. 
Regularisation would be something great to implement, probably a larger model with more classes to sequenence difference, trained on similar images.
Model could generalise hidden features without getting overfit on loss
If we are talking about sequence semantics, one_hot_encoder sequence might also improve model. Though its just a spatial-sematic mapping.


## To Play around
If you want to check if it works on images or not, then probably better to hit Huggingspace where the model is hosted for now.

project_folder/
├── server.py
├── index.html
└── static/ 
