# PV Basics Course

Lecture and hands-on tutorial materials for an introduction to semiconductor devices and p–n junction solar cells. The course combines the underlying physics with a practical, learn-by-doing approach to scientific programming.

## Course overview

Students are introduced to:

- semiconductor conductivity, carrier concentration, and interfaces;
- the role of interfaces in semiconductor devices, using MOSFETs as an example;
- p–n junction diode operation in the dark and under illumination;
- photovoltaic current, voltage, power, recombination, and efficiency losses;
- Python programming fundamentals in Google Colab; and
- numerical semiconductor-device simulation using DEVSIM.

The lecture/tutorial sequence is built around three exercises:

1. Explore how interface charge and capacitance affect MOSFET threshold voltage.
2. Investigate MOSFET transfer curves and operational regimes.
3. Reproduce a solar-cell J–V curve and extend the model to include surface-recombination losses.

## Repository contents

| File | Purpose |
| --- | --- |
| [`programming_basics.ipynb`](programming_basics.ipynb) | Beginner-friendly Python notebook covering variables, data types, expressions, functions, methods, conditionals, loops, collections, modules/libraries, and debugging. |
| [`solar_cell_simulation.ipynb`](solar_cell_simulation.ipynb) | Guided silicon p–n junction simulation: mesh creation, material and doping definitions, equilibrium solution, drift–diffusion equations, energy-band diagrams, dark and illuminated J–V curves, and solar-cell performance metrics. |
| [`diode_common.py`](diode_common.py) | Reusable DEVSIM helper functions for meshes, silicon parameters, doping, initial solutions, and drift–diffusion setup. |
| [`LICENSE`](LICENSE) | GNU General Public License, version 3. |

The wider teaching folder also contains the lecture slide decks and the introductory Colab guide:

- `2026_PV_principles_full_v1.pptx` — full lecture/tutorial deck, including semiconductor devices, interfaces, MOSFETs, p–n junction solar cells, and exercises.
- `2026_PV_principles_vid_v1.pptx` — video-oriented version of the lecture deck.
- `Introduction to programming with Colab.docx` — getting-started guide for Google Colab, including account setup and introductory programming videos.

These three teaching assets are currently outside this GitHub repository. Copy them into the repository if students should download them directly from GitHub.

## Suggested learning path

1. Read the lecture material on semiconductors, interfaces, and p–n junction solar cells.
2. Work through `programming_basics.ipynb` in Google Colab. Run each cell, change the examples, and complete the small tasks.
3. Use the lecture exercises to connect the equations to plots and device behaviour.
4. Study `solar_cell_simulation.ipynb` to see how a physical model is translated into a numerical device simulation.
5. Compare dark and illuminated J–V characteristics and calculate $J_{SC}$, $V_{OC}$, the maximum-power point, fill factor, and conversion efficiency.

## Running the notebooks

### Python basics

Open [`programming_basics.ipynb`](programming_basics.ipynb) in [Google Colab](https://colab.research.google.com/) and run the cells from top to bottom. No local Python installation is required for this introductory notebook.

### Solar-cell simulation

`solar_cell_simulation.ipynb` imports `devsim`, DEVSIM's Python packages, NumPy, Matplotlib, Pandas, and the local `diode_common.py` module. It is configured with a `tcad_env` notebook kernel and therefore requires a Python environment in which DEVSIM is installed and discoverable.

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

## Intended audience

The material is aimed at students who are new to semiconductor device physics and scientific programming. Prior Python experience is not assumed; the programming notebook is designed to be used alongside the lecture and tutorial activities.

## Contributing and extending the course

Useful student extensions include:

- changing doping, temperature, mobility, or generation parameters;
- testing how recombination changes the J–V curve;
- adding series-resistance or shunt-resistance effects;
- comparing numerical results with an analytical diode model; and
- improving plots, comments, or explanations in the notebooks.

When sharing modified notebooks, keep the explanatory text with the code and record the assumptions and parameter values used to generate the results.

## Licence

See [`LICENSE`](LICENSE) for the licensing terms.
