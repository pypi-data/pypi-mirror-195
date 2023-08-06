# VisNet1D

A simple visualisation tool for 1D networks. 

![An image of visnet1d](visnet1d.png)

## Installation

### Use in your project

Python Package Index (PIP):
```
pip install visnet1d
```

Poetry:
```
poetry add visnet1d
```

### Use the development version

Git:
```
git clone git@gitlab.com:abdrysdale/visnet1d.git
nix-shell
poetry install
poetry shell
```

Installation instructions for `nix` can be obtained from [here](https://nixos.org/download.html).
If you don't have and don't want to install nix, it is sufficient to just install poetry and skip the `nix-shell` command.
Poetry installation instructions can be obtained from [here](https://python-poetry.org/).

### Just want to run the examples?

If you just want to run one of the examples, such as the vessel network example:
```
pip install visnet1d
git clone git@gitlab.com:abdrysdale/visnet1d.git
cd visnet1d
```

The run the desired example script with:
```
python examples/vessel_network.py
```
Naturally replacing `vessel_network.py` with any of the other examples.
Next, go to `http://127.0.0.1:8050` in your browser and start exploring!


## Usage

VisNet1D is intended to be used to visualise signals across a 1-dimensional network at potentially multiple locations.
It can either be used to explore an output of an other function, viewing signal(s) at different locations and comparing the results or it can be used to visualise the change in a function output due to a change in inputs.

An example usage is shown below:

First import the library:
```python
import visnet1d
```


Now we define a simple function that takes a spatial argument along with other keyword arguments.
This function returns y as a function of t at some spatial point x.
It must return two vectors to be compatible with the default plotting function.
But don't worry! You can define your own plotting functions - we'll get to that later.
```python
def foobar(x, tmax=1, a=2, b=3):
    t = np.linspace(0, tmax, 100)
    y = a * np.sin(x + 2 * np.pi * t / b)
    return y, t
```

Here we define a list for the function input arguments.
These are used to display the inputs on the web-page and pass the results to the function `foobar`.
```python
input_dict_list = [
    {
        "name" : "Amplitude",   # Name to be displayed on the web app.
        "id" : "a",             # Internal id and keyword argument for the function (foobar).
        "value" : 1,            # Initial value.
        "type" : "number",      # Used by Dash to determine the input type.
    },
    {
        "name" : "Period",
        "id" : "b",
        "value" : 2,
        "type" : "number",
    },
    {
        "name" : "Maximum t",
        "id" : "tmax",
        "value": 1,
        "type" : "number",
    },
]
```
The allowed types that dash input accepts can be found [here](https://dash.plotly.com/dash-core-components/input).

Next we need to define the boundaries that separate locations.
To illustrate this, let's consider two vessels connected in series:
```python
boundaries = {     # Locations can be selected from a drop-down menu
        "Vessel 1" : [0, np.pi],          # [Start, End]
        "Vessel 2" : [np.pi, 3 * np.pi],  
}
```

Now we create a site object and run the site.
```python
site = visnet1d.Site(
        foobar,             # Function to plot.
        boundaries,         # Locations to select.
        input_dict_list,    # List of function inputs (each input has it's own dictionary).
        xlab="Time (s)",    # X-axis label
        ylab="Response",    # Y-axis label
        title="My title",   # Title
)

# Runs the server with the default arguments - same as site.run()
site.run(host="127.0.0.1", port="8050", debug=False)
```
Go to `127.0.0.1:8050` on your web browser view the webapp.

### Custom plots

Custom plot functions can be utilised using the `plot` keyword argument for the visnet1d.Site class.
E.g.

```python
site = visnet.Site(
    my_function,
    my_boundaries,
    my_input_dictionary_list,
    plot=my_custom_plot_function, # <- This is how you pass your custom plot function.
)
```

A few things to note about writing custom plotting functions:

- The function must take the Site object as the **only** input argument.
- The function must return a plotly figure.

A few notable attributes of the Site class:

- `site.function_kwargs` : Is a list of dictionaries of the inputs defined by the `input_dict_list` argument.
    These are the values that you can change in the inputs section in the webapp.
- `site.boundaries` : The boundaries defined by the `boundaries` argument.
- `site.loc_slider_vals` : A dictionary of all of the slider positions for all of the previously selected locations.
    The dictionary is of the format `location` : `value`. Where location is the location key used in the `boundaries` argument and `value` is the value of the slider.
- `site.loc_keys` : A list of the locations currently selected. Where each location is the key used in the `boundaries argument.`
- `site.x` : The current position of the active slider.

### Exploring a static output

By default, VisNet1D evaluates the function each time an input is changed.
For a very expensive function this isn't ideal.
Moreover, there might be use case whereby the outputs of very complicated network have been produced by some other expensive function and you just wish to use VisNet1D to explore the output.

Here's how you'd do something like that:
```python
my_outputs = visnet1d.get_static_function(out_mat, t, axis=0)
```
First use the inbuilt function `get_static_function()` to handle static outputs.
This function needs to be passed the 2D output matrix and the value for the x-axis.
The output matrix might be something like a signal as a function of space and time.

Moreover, as the outputs are static there are no function inputs so we can do away with the `input_dict_list` argument.
This is done like so:
```python
site = visnet.Site(
    my_outputs,
    my_boundaries,
    input_dict_list=None,
)
```

### Customising plots

By default all the plots are editable and you can pass the x axis label, y axis label and title into the site object with the following:
```python
site = visnet.Site(
    my_function,
    my_boundaries,
    my_input_dictionary_list,
    xlab=my_x_label,
    ylab=my_y_label,
    title=my_title,
)
```

Moreover, the width of the graph itself can be controlled by using:
```python
site = visnet.Site(
    my_function,
    my_boundaries,
    my_input_dictionary_list,
    gwidth=80, # This sets the width of the graph to be 80% of the screen width.
)

```

It is also possible to display an optional image underneath the input section to aid network visualisation:
```python
site = visnet.Site(
    my_function,
    my_boundaries,
    my_input_dictionary_list,
    image='path/to/my/image.png'    # Any Pillow supported image format can be used
    iheight=80,                     # Adjusts the image height to be 80% of the screen height.
)
```

## Examples

For full examples see the [examples/](examples/) directory.

## Contributing

- For contributing guidelines see [CONTRIBUTING](CONTRIBUTING.md).
