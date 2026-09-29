import matplotlib.pyplot as plt
import control.matlab as control
import scipy
import numpy as np
import streamlit as st

# Ziegler Nicholas input
'''
tau = 160
L = 27
K = 0.65

R = K/tau
'''
'''
G1 = 0.65*control.tf([1], [27,1])*control.tf([1], [160, 1])
Q = []

for j in range(100):
    Q.append(control.tf([1], [27,1]))
t = np.linspace(0, 400, 1000)

y = np.zeros(1000)

for i in range (1000):
    y[i] = 2 * t[i]


t, y_Q = control.step(Q, t)

plt.plot(t,y, 'b', t, np.ones(1000), 'g-')
plt.xlabel('Times(s)')
plt.ylabel('Output (t^degreesC)')
plt.title('PID Step Response')
plt.show()

plt.plot(t, y_Q, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Power (%) input')
plt.grid()
plt.show()
'''


Gv = control.tf([1], [2, 1]) #1/(2s + 1)
Gp = control.tf([1], [5, 1]) #1/(5s + 1)
Gd = control.tf([1], [5, 1]) #1/(52 + 1)

print(Gv, Gp, Gd)

tdelay = 1
norder = 1

num,den = control.pade(tdelay,norder)

Gm = control.tf(num, den)
print(Gm)

Kc = 1
tauI = 100
'''
Gc = Kc*control.tf([tauI, 1], [tauI, 0])
print(Gc)
'''

def sim(Kc = 1, tauI = 1000):
    Gc = Kc*control.tf([tauI, 1], [tauI, 0])

    Hyr = Gp * Gv * Gc / (1 + Gp * Gv * Gc * Gm)
    Hyd = Gd / (1 + Gp * Gv * Gc * Gm)
    Hur = Gc / (1 + Gc * Gm * Gp * Gv)
    Hud = -Gc * Gm * Gd / (1 + Gc * Gm * Gp * Gv)

    t = np.linspace(0, 25, 1000)

    plt.figure(figsize=(12,6))

    plt.subplot(2, 2, 1)
    y, t = control.step(Hyr, t)
    plt.plot(t, y)
    plt.ylim(-0.5, 2.2)
    plt.title('output response from step to setpoint')
    plt.ylabel('y')

    plt.subplot(2, 2, 2)
    y, t = control.step(Hyd, t)
    plt.plot(t, y)
    plt.ylim(-0.5, 2.2)
    plt.title('output response due to step disturbance')
    plt.ylabel('y')

    plt.subplot(2,2,3)
    y, t = control.step(Hur, t)
    plt.plot(t, y)
    plt.ylim(-1.5, 1.5)
    plt.title('manipulated variable response from step setpoint')
    plt.ylabel('y')

    plt.subplot(2,2,4)
    y, t = control.step(Hud, t)
    plt.plot(t, y)
    plt.ylim(-1.5, 1.5)
    plt.title('manipulated variable response due to step distrubance')
    plt.ylabel('y')

    plt.tight_layout()

st.title("KC & TAUI Interactive")

#sliders

kc = st.slider("kc", min_value=0.0, max_value=10.0, value=1.0, step=1.0)
taui = st.slider("taui", min_value=0.1, max_value=25.0, value=25.0, step=1)

#function call
def simulate(Kc, tauI):
    st.write(f"Running simulation with Kc = {Kc} and tauI = {tauI}")
    sim(Kc, tauI)

simulate(Kc, taui)