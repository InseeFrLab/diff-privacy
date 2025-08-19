import numpy as np
import matplotlib.pyplot as plt

# Définition de la fonction phi(U, L)
def phi(U, L):
    numerator = 2 * np.abs(U**2 - L**2) + 2 * U * L
    denominator = (U + L)**2
    return numerator / denominator

# Création de la grille
U_vals = np.linspace(-2, 2, 200)
L_vals = np.linspace(-2, 2, 200)
U, L = np.meshgrid(U_vals, L_vals)

# Évaluation de phi
Z = phi(U, L)

# ----------- Tracé 3D -----------
fig = plt.figure(figsize=(12, 5))

ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(U, L, Z, cmap='viridis', edgecolor='none')
ax1.set_xlabel('U')
ax1.set_ylabel('L')
ax1.set_zlabel('phi(U,L)')
ax1.set_title('Surface plot of phi(U,L)')
fig.colorbar(surf, ax=ax1, shrink=0.5)

# ----------- Heatmap -----------
ax2 = fig.add_subplot(1, 2, 2)
heatmap = ax2.imshow(Z, extent=[U_vals.min(), U_vals.max(), L_vals.min(), L_vals.max()],
                     origin='lower', cmap='viridis', aspect='auto')
ax2.set_xlabel('U')
ax2.set_ylabel('L')
ax2.set_title('Heatmap of phi(U,L)')
fig.colorbar(heatmap, ax=ax2)

plt.tight_layout()
plt.show()
