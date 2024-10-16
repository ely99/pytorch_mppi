import torch
from pytorch_mppi import MPPI

# Definizione del modello dinamico (esempio: pendolo o altro sistema)
def dynamics(state, control):
    # Definisci le equazioni di stato per il tuo sistema
    # state: vettore di stato (posizione, velocità)
    # control: input di controllo (esempio: coppia o forza)

    # Esempio semplificato: modello dinamico
    position = state[0]
    velocity = state[1]
    
    # Sistema dinamico (es. equazioni del moto)
    new_position = position + velocity * 0.01
    new_velocity = velocity + control[0] * 0.01
    
    return torch.stack([new_position, new_velocity])

# Parametri del modello
state_dim = 2  # Dimensione del vettore stato
control_dim = 1  # Dimensione del vettore di controllo
horizon = 15  # Orizzonte temporale
lambda_ = 1.0  # Parametro di costo per l'MPPI

# Crea l'oggetto MPPI
mppi = MPPI(dynamics, state_dim, control_dim, horizon, lambda_)

# Stato iniziale del sistema
state = torch.tensor([0.0, 0.0])

# Ciclo di controllo
for i in range(100):
    control = mppi.command(state)
    state = dynamics(state, control)
    print(f"Stato attuale: {state}, Controllo applicato: {control}")
