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

Standard Google Colab does not include the libraries used here for running semicondcutor device simulations (`DEVSIM`). Before using the simulation notebook in Colab, configure a compatible environment with the key packages and make `pv_cell_functions.py` available in the notebook's working directory. Let's start:

<a href="https://colab.research.google.com/github/seb-bonilla/pv-basics-course/blob/main/solar_cell_simulation.ipynb" target="_blank" rel="noopener noreferrer"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open solar cell simulation in Google Colab"></a>

## Licence

See [`LICENSE`](LICENSE) for the licensing terms.
