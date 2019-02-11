# -*- coding: utf-8 -*-
"""
Created on Tue Feb 5 14:56:39 2019
@authors: Diego Eckhard and Emerson Boeira
"""
"""
Testing the vrft function on a example
"""
#%%Header: importing python libraries

import numpy as np #important package for scientific computing: it has important array features
from scipy import signal #signal processing librarie
import matplotlib.pyplot as plt #librarie to plot graphics
from vrft import teste # implementation of vrft and some filtering functions

#%% First step: defining the process model, the noise model, the reference model, and the controller class

# declaration of the transfer fuctions that compose the MIMO process G(z)
G11 = signal.TransferFunction([1],[1,-0.9],dt=1)
G12 = 0
G21 = 0
G22 = signal.TransferFunction([1],[1,-0.9],dt=1)
# organizing the MIMO system G(z) in a python list
G=[[G11,G12],[G21,G22]]
# IMPORTANT: if the numerator of the transfer function is 1, for example, define it as num=[1], instead of num=[0,1]. The latter generates a warning!!

# declaration of the transfer fuctions that compose the MIMO noise model process H(z)
H11 = signal.TransferFunction([1],[1],dt=1)
H12 = 0
H21 = 0
H22 = signal.TransferFunction([1],[1],dt=1)
# organizing the MIMO system H(z) in a python list
H=[[H11,H12],[H21,H22]]

# declaration of the transfer fuctions that compose the MIMO reference model Td(z)
Td11 = signal.TransferFunction([0.2],[1,-0.8],dt=1)
Td12 = 0
Td21 = 0
Td22 = signal.TransferFunction([0.2],[1,-0.8],dt=1)
# organizing the MIMO reference model T(z) in a python list
Td=[[Td11,Td12],[Td21,Td22]]

# choosing the VRFT method filter
L=Td
# defining the controller structure that will be used in the method
Cp=[[signal.TransferFunction([1],[1],dt=1)]] # proportional controller
Cpi=[[signal.TransferFunction([1, 0],[1, -1],dt=1)] , [signal.TransferFunction([1],[1, -1],dt=1)]] # PI controller
# assembling the MIMO controller structure
C = [[Cpi,[]],[[],Cpi]] # in this scenario, we choosed a descentralized PI controller

#%% Simulating the open loop system to obtain the data for the VRFT

# samples of the input signal
N=350
# discrete time vector of the simulation
t=np.linspace(0,N-1,N) #linspace(start,stop,numberofpoints)
# pushing the vector to have the specified dimensions
t.shape=(1,N)

# using a square wave for both inputs
# defining the period of the square wave
ts=N
fs=1/ts
# finally, defining the square wave using the function square
u1=0.5-0.5*signal.square(2*np.pi*fs*t).T
u2=0.5-0.5*signal.square(2*np.pi*fs*t-3*np.pi/2).T
## testing another arbitrary inputs: gaussian pulse
#u1=signal.gausspulse(t,fc=0.003).T
#u2=signal.gausspulse(t,fc=0.002).T
# concatenating the signals
u=np.concatenate((u1,u2),axis=1)
#IMPORTANT: in our toolbox, we decided to organize the input and output signals as an array (N,n), where N=number of data samples, n=number of inputs and outputs

# plotting the input signal
plt.figure()
plt.step(t.T,u)
plt.grid(True)
plt.xlabel('time (t)')
plt.ylabel('u(t)')
plt.show()

# calculating the output of the MIMO system
yu=teste.filtra(G,u)
# add noise to the output
# variance of the whie noise signals
sigma2_e1=0
sigma2_e2=0
# creating noise vectors
w1=np.random.normal(0,np.sqrt(sigma2_e1),N)
w2=np.random.normal(0,np.sqrt(sigma2_e2),N)
# pushing the dimensions to match our signals
w1.shape=(N,1)
w2.shape=(N,1)
# concatenating noise signals
w=np.concatenate((w1,w2),axis=1)
# filtering the white noise
v=teste.filtra(H,w)
# real output
y=yu+v;

# plotting the output signal
plt.figure()
plt.step(t.T,y)
plt.grid(True)
plt.xlabel('time (t)')
plt.ylabel('y(t)')
plt.show()

p=teste.vrft_mimo(u,y,y,Td,C,L)
print(p)