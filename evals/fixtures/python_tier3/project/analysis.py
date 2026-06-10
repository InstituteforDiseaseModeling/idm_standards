import numpy as np
import matplotlib.pyplot as plt

# Tier 3 one-off analysis script: simulate an SIR outbreak and plot the curve.

def run_sir(beta, gamma, S0, I0, R0, days):
    np.random.seed(42)
    S=[S0]; I=[I0]; R=[R0]
    N=S0+I0+R0
    for d in range(days):
        new_inf=beta*S[-1]*I[-1]/N
        new_rec=gamma*I[-1]
        S.append(S[-1]-new_inf)
        I.append(I[-1]+new_inf-new_rec)
        R.append(R[-1]+new_rec)
    return np.array(S),np.array(I),np.array(R)

def run_sir_noisy(beta, gamma, S0, I0, R0, days):
    np.random.seed(42)
    S=[S0]; I=[I0]; R=[R0]
    N=S0+I0+R0
    for d in range(days):
        new_inf=beta*S[-1]*I[-1]/N*(1+np.random.normal(0,0.05))
        new_rec=gamma*I[-1]
        S.append(S[-1]-new_inf)
        I.append(I[-1]+new_inf-new_rec)
        R.append(R[-1]+new_rec)
    return np.array(S),np.array(I),np.array(R)

if __name__=='__main__':
    S,I,R=run_sir(0.3,0.1,990,10,0,160)
    plt.plot(S,label='S'); plt.plot(I,label='I'); plt.plot(R,label='R')
    plt.legend(); plt.xlabel('day'); plt.ylabel('count')
    plt.savefig('sir.png')
