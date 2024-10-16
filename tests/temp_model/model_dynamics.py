import sympy as sp

# Definire le variabili simboliche per le coordinate delle articolazioni
theta1, theta2, theta3, l1, l2 = sp.symbols('theta1 theta2 theta3 l1 l2')

# Definire le equazioni di cinematica diretta
x = l1 * sp.cos(theta1) * sp.sin(theta2) + l2 * (sp.cos(theta1) * sp.cos(theta2) * sp.cos(theta3) - sp.cos(theta1) * sp.sin(theta2) * sp.sin(theta3))
y = l1 * sp.sin(theta1) * sp.sin(theta2) + l2 * (sp.sin(theta1) * sp.cos(theta2) * sp.cos(theta3) - sp.sin(theta1) * sp.sin(theta2) * sp.sin(theta3))
z = -l1 * sp.cos(theta2) + l2 * (sp.sin(theta2) * sp.cos(theta3) + sp.cos(theta2) * sp.sin(theta3))

# Definire il vettore delle posizioni (cinematica diretta)
position_vector = sp.Matrix([x, y, z])

# Definire il vettore delle variabili articolari
joint_variables = sp.Matrix([theta1, theta2, theta3])

# Calcolare la Jacobiana
jacobian = position_vector.jacobian(joint_variables)

# Stampare la matrice Jacobiana
sp.pprint(jacobian)
