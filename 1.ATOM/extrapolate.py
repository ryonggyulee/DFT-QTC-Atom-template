import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, PchipInterpolator


# executable files
exec_gion = os.path.abspath('./input/gion.py')

# input files
input_fae = os.path.abspath('./input/FEPOT') 

# Define the parent directory containing Alpha_para_* folders
parent_dir = "output"

# Create directory for saving extrapolated data
output_dir = "output_predicted"
os.makedirs(output_dir, exist_ok=True)

# Get all Alpha_para_* folders
#subfolders = sorted([f for f in os.listdir(parent_dir) if f.startswith("occ=")])

subfolders = []

occs = np.arange(0.050, 1.00, 0.050)

for iocc in range(len(occs)):
    occ = occs[iocc]
    subfolders.append(f'occ={occ:3.2f}')

plt.figure(figsize=(8, 6))

# Store data for interpolation
occupation_numbers = []
potential_values = []
extra_values = []
radius_values = None

# Read all AEPOT data
for folder in subfolders:
    aepot_path = os.path.join(parent_dir, folder, "HEPOT")

    if not os.path.exists(aepot_path):
        print(f"Warning: HEPOT file missing in {folder}")
        continue  

    # Load AEPOT data (assuming three columns: radius, potential, extra)
    data = np.loadtxt(aepot_path)
    radius = data[:, 0]    # First column: radius
    potential = data[:, 1] # Second column: potential
    extra = data[:, 2]     # Third column: extra

    # Extract occupation number
    occ = float(folder.split("=")[-1])
    occupation_numbers.append(occ)

    # Store radius values (from the first valid file)
    if radius_values is None:
        radius_values = radius  # Save the first radius set
    elif not np.allclose(radius_values, radius):
        print(f"Warning: Radius mismatch at Occ {occ}, skipping this dataset.")
        continue

    potential_values.append(potential)
    extra_values.append(extra)

print(occupation_numbers)

# Convert to NumPy arrays
occupation_numbers = np.array(occupation_numbers)
potential_values = np.array(potential_values)  # Shape: (n_occ, n_radius)
extra_values = np.array(extra_values)          # Shape: (n_occ, n_radius)

# Interpolation model for extrapolation
#interp_potential = interp1d(occupation_numbers, potential_values, axis=0, kind='cubic', fill_value='extrapolate')
#interp_extra = interp1d(occupation_numbers, extra_values, axis=0, kind='cubic', fill_value='extrapolate')
interp_potential = PchipInterpolator(occupation_numbers, potential_values, axis=0, extrapolate = True)
interp_extra = PchipInterpolator(occupation_numbers, extra_values, axis=0, extrapolate = True)


# Define new occupations beyond the existing range
extra_occ = np.arange(0.35, 0.60, 0.050)  # Extrapolate every 0.050

# Predict new values using interpolation models
extrapolated_potentials = interp_potential(extra_occ)
extrapolated_extra = interp_extra(extra_occ)

# Plot original data
for i, occ in enumerate(occupation_numbers):
    plt.plot(radius_values, potential_values[i], label=f"Occ {occ:.3f}")

# Plot extrapolated data and save to files
for i, occ in enumerate(extra_occ):
    plt.plot(radius_values, extrapolated_potentials[i], linestyle="dashed", label=f"Extrapolated Occ {occ:.3f}")

   # Save each extrapolated data file with three columns

    path = os.path.join(output_dir,f'occ={occ:.2f}')
    os.makedirs(path, exist_ok =True)

    output_file = os.path.join(path,'HEPOT')
    np.savetxt(output_file, np.column_stack((radius_values, extrapolated_potentials[i], extrapolated_extra[i])), fmt="%.17f")


# Formatting
plt.xlabel("Radius")
plt.ylabel("Potential")
plt.title("AEPOT Data with Extrapolated Occupations")
plt.legend(fontsize=8, loc="best")
plt.grid(True)
plt.savefig("AEPOT_extrapolated_plot.png", dpi=300)
plt.show()

print(f"Extrapolated data saved in '{output_dir}'")

