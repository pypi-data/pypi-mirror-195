# Orange3 System Dynamics Add-on

This is an add-on for [Orange3](https://orangedatamining.com/) allowing to
perform simulation using _System Dynamic Modeling_ (SDM) mechanism.

## Orange Data Mining
**ODM** (_Orange Data Mining_) is an open source machine learning and data
visualization tool. It allows to build data analysis workflows visually, with a
large, diverse toolbox.

We develop a list of widgets to be used in ODM, each widget has a functionality
to be mainly applied for _System Dynamic Modeling_. 

## Installation
_Orange3_ and the _SDM_ Addon must be installed in the same
_Python_ environment.

### Orange 3
```shell
pip install pyQt5 PyQtWebEngine
pip install orange3
```

### System Dynamics Addon
```shell
pip install orange-system-dynamics
```

## Usage
Orange3 can be run using the following command:
```shell
orange-canvas
```
or
```shell
python -m orange.canvas
```
New widgets should appear in the toolbox bar under the __System Dynamics__
section.


## Widgets Description
![](screenshots/Workflow_Example.png)

### Load Model Widget
`Load Model` widget is used to load simulation models in .mdl or .xmile format,
it outputs the model for Simulation.

![](screenshots/Load.png)

### Simulation Widget
Once the model is loaded, the `Simulation` Widget is updated to show model's
variables grouped by:
- Time Controls: contains the initial time, the final time and defined time
step
- Stocks: contains all model’s stocks, can be used to change any stock’s
initial value
- Auxiliary Values: contains  all the auxiliary values, can also be changed

![](screenshots/Simulation.png)

Once the Run Simulation button’s hit, the model is run, the widget outputs an
Orange Data Table, we use the `Line Chart` Widget to visualize results of
simulation: 

![](screenshots/Line_Chart.png)

Other widgets have been used to perform step by step execution of simulation, by simply running the 
results through `As Timeseries` while indicating Time as the index variable:

![](screenshots/As_Timeseries.png)

Next, using `Time Slice` which was adapted to commit a cumulative step by step simulation 
to the Line Chart:

![](screenshots/Time_Slice.png)

In another example; we run the simulation in two different regions: 

- Paris (France)

- Algiers(Algeria) and Casablanca (Morocco)

with different simulation parameters each time, we variate the total population, 
contact infectivity and the stocks (infectious, recovered, susceptible).
We simply add the results together using Concatenate:

![](screenshots/Simulation_Workflow.png)

We can also show the results in Geo Map, after adding Latitude and Longitude information: 

![](screenshots/Geo_Map.png)