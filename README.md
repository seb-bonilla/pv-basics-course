# PV Basics Course

Lecture and hands-on tutorial materials for an introduction to semiconductor devices and p–n junction solar cells. The course combines the underlying physics with a practical, learn-by-doing approach to scientific programming.

## Learning to code in Python

The [`programming_basics.ipynb`](programming_basics.ipynb) notebook introduces the core ideas needed to begin scientific programming in Python. It covers variables, data types, expressions, functions, methods, conditional statements, loops, collections, modules and libraries, and debugging.

Students should work through the notebook by running the code cells, changing the examples, and completing the small tasks. It is designed for beginners and can be used directly in Google Colab without installing Python on a personal computer.

<a href="https://colab.research.google.com/github/seb-bonilla/pv-basics-course/blob/main/programming_basics.ipynb" target="_blank" rel="noopener noreferrer"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open programming basics in Google Colab"></a>

## Solar-cell simulation

The `solar_cell_simulation.ipynb` notebook is completed in the classroom with the lecturer while the contents of the lecture are being explained. The notebook connects the semiconductor physics of a silicon p–n junction diode with the numerical methods used to simulate its behaviour.

Students are introduced to:

- computational mesh creation for a one-dimensional silicon device;
- silicon material properties and an abrupt p–n doping profile;
- the equilibrium solution of Poisson's equation;
- the coupled drift–diffusion equations for electrons and holes;
- potential, carrier-density, electric-field, and energy-band diagrams;
- dark current–voltage (J–V) characteristics;
- optical generation and illuminated J–V characteristics; and
- solar-cell performance metrics, including $J_{SC}$, $V_{OC}$, maximum power, fill factor, and conversion efficiency.

The simulation notebook imports `devsim`, DEVSIM's Python packages, NumPy, Matplotlib, Pandas, and the local `diode_common.py` module. It is configured with a `tcad_env` notebook kernel and therefore requires a Python environment in which DEVSIM is installed and discoverable.

The notebook develops the simulation in stages:

- create a one-dimensional silicon device and computational mesh;
- define silicon material properties and an abrupt p–n doping profile;
- solve Poisson's equation at equilibrium;
- solve the coupled drift–diffusion equations;
- inspect potential, carrier-density, electric-field, and band-diagram results;
- sweep applied voltage to obtain the dark J–V curve;
- add a uniform optical-generation term to obtain the illuminated J–V curve; and
- calculate power, $J_{SC}$, $V_{OC}$, maximum power, fill factor, and efficiency.

Standard Google Colab does not include DEVSIM by default. Before using the simulation notebook in Colab, configure a compatible DEVSIM environment and make `diode_common.py` available in the notebook's working directory. Otherwise, run it in a prepared local or hosted TCAD environment.

<a href="https://colab.research.google.com/github/seb-bonilla/pv-basics-course/blob/main/solar_cell_simulation.ipynb" target="_blank" rel="noopener noreferrer"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open solar cell simulation in Google Colab"></a>

## Licence

See [`LICENSE`](LICENSE) for the licensing terms.
