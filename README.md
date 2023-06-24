# IPyR

## Overview
This project descibes how to obtain **max flow rate** (defined as `q_max: NUMERIC (float | int)`) using several equations.

## Language Features
Since this repository was created, **Python 3.8.10** is used in this project.

## Program Features
- Calculate the `q_max` based on relations of variables
    - Reservoir pressure (`p_res: NUMERIC (float | int)`)
    - Wellbore pressure (`p: NUMERIC (float | int)`)<sup>[1]</sup>
    - Flow rate at current wellbore pressure (`q: NUMERIC (float | int)`)<sup>[1]</sup>
- Illustrate extensions of production data for graphic and charting purposes
    
<sup>[1]</sup> Notice that `p` and `q` are combined in single dictionary defined as `Dict[NUMERIC (float | int), NUMERIC (float | int)]`. For instance, for single data of `q` and `p`, it will be defined as `data = { "p": NUMERIC, "q": NUMERIC }`.

## Testing Files
- `main.py`: Testing for calculation of `q_max` in several wellbore pressures using **Vogel Equation**
- `fetkovitch.py`: Testing for calculation of `q_max` in several wellbore pressures using **Fetkocivh Equation**
- `graph.py`: Demonstrating graph correlation of wellbore pressures between flow rates based on **Vogel Equation**
- `main.py`: Demonstrating graph correlation of wellbore pressures between flow rates based on  **Fetkovich Equation**