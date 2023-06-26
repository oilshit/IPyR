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
### Two-phase production
#### Vogel
- `main.py`: Testing for calculation of `q_max` in several wellbore pressures using **Vogel Equation**
- `graph.py`: Demonstrating graph correlation of wellbore pressures between flow rates based on **Vogel Equation**
- `graph-vogel.py`: Demonstrating graph of wellbore pressure (in this case, using `p_wf` = 1335 psia) comparing with real production data **Vogel Equation**

#### Fetkovich
- `fetkovitch.py`: Testing for calculation of `q_max` in several wellbore pressures using **Fetkocivh Equation**
- `graph-2.py`: Demonstrating graph correlation of wellbore pressures between flow rates based on  **Fetkovich Equation**

#### Production graph comparison
- `graph-2-phase-comparison.py`: Compare of production graph between `Vogel` and `Fetkovich` methods.

### Three-phase production
#### Wiggin
- `phase3.py`: Demonstrating graph correlation of wellbore pressures between flow rates based on **Vogel Equation**
- `graph-3`: Testing for calculation of `q_max` of oil and water (in this case, using `p_wf` = 1335 psia) using **Wiggin Equation**