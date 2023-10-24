import numpy as np 
import pandas as pd 
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms,models
from torch.utils.data import Dataset, DataLoader
import cv2
import pandas as pd
import numpy as np
from PIL import Image
import math
from Customloss import CustomLoss

def train(train_loader,epochs,model=model, optimizer=optimizer,loss=loss):
   
    ep_count=0
    for epoch in range(epochs):
        
    # initialize the running loss and accuracy
        running_loss = 0.0
        mid_loss = 0.0
        # loop over the batches
        model.to(device)
        for i, (images, labels) in enumerate(train_loader):
            # move the images and labels to the device (CPU or GPU)
            images = images.to(device)
            labels = labels.to(device)
            lengths = torch.tensor(labels.size())
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward pass
            
            outputs = model.forward(images)
            
            #outputs = outputs.contiguous().cpu()
            #outputs = torch.nn.functional.log_softmax(outputs, 2)
            B,T, H = outputs.size()
            
            
            input_lengths = torch.full((B,),T, dtype=torch.long)
            

            target_lengths = torch.full((B,),16, dtype=torch.long)
            #labs=torch.reshape(labels,(B,20*28))
            
            lossb = loss.forward(outputs.log_softmax(dim=1).transpose(0,1), labels, input_lengths , target_lengths)
            ####outputs.log_softmax(dim=2).transpose(0,1)
            lossb.backward()
            optimizer.step()
            running_loss += lossb.item()
            #print(torch.squeeze(outputs,0))

        val_loss=validate(data_test,model,optimizer,loss)
        print(f'Epoch {epoch + 1}, Runn_Loss: {running_loss / 20:.4f}, val_loss: {val_loss / 20:.4f}')
        ep_count +=1
        wandb.log({"val_loss": (val_loss / 20), "loss": (running_loss / 20), "epoch":ep_count})
        if ep_count%20==0:
            save_checkpoint(model, optimizer, epoch, loss)

def main():
  # basic model running code
  cnet =CRNN(model.args)
  optim =optim.Adam(cnet.parameters(),lr=0.001)
  loss_fu = CustomLoss()
  ##Enter Data with data_loader module
  train(data,epochs)
