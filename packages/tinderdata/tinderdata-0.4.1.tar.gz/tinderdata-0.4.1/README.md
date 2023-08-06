<h1 align="center">
  <b>tinderdata</b>
</h1>

A very simple package to get insight on your Tinder usage.

## Install

This code is compatible with `Python 3.6+`.
If for some reason you have a need for it, you can simply install it in your virtual enrivonment with:
```bash
pip install tinderdata
```

## Usage

This utility requires that you export your data from the Tinder platform, as described [here](https://www.help.tinder.com/hc/en-us/articles/115005626726-How-do-I-request-a-copy-of-my-personal-data-).
You should obtain a single `tinderdata.json` file, which is the input required for this script.

With this package installed in the activated enrivonment, it can be called through `python -m tinderdata` or through a newly created `tinderdata` command.

Detailed usage goes as follows:
```
Usage: tinderdata [OPTIONS] [DATA_PATH]

  Get insight on your Tinder usage.

Arguments:
  [DATA_PATH]  Location, relative or absolute, of the exported JSON file with
               your user data.


Options:
  --show-figures / --no-show-figures
                                  Whether or not to show figures when plotting
                                  insights.  [default: False]

  --save-figures / --no-save-figures
                                  Whether or not to save figures when plotting
                                  insights.  [default: False]

  --log-level TEXT                The base console logging level. Can be
                                  'debug', 'info', 'warning' and 'error'.
                                  [default: info]

  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

An example command is then:
```
python -m tinderdata path_to_tinderdata.json --save-figures --log-level debug
```

The script print out a number of insight statements, and finally the text you should paste to get a Sankey diagram.
It will then create a `plots` folder and populate it with visuals.

You can otherwise import the high-level object from the package, and use at your convenience:
```python
from tinderdata import TinderData

tinder = TinderData("path/to/tinderdata.json")
tinder.output_sankey_string()
tinder.plot_messages_loyalty(showfig=True, savefig=False)
```

## Output example

Here are examples of the script's outputs:

![Example_1](plots/messages_monthly_stats.png)

![Example_2](plots/swipes_weekdays_stats.png)

---

<div align="center">
  <sub><strong>Made with ♥︎ by fsoubelet</strong></sub>
  <br>
  <sub><strong>MIT &copy 2019 Felix Soubelet</strong></sub>
</div>



[license]: https://github.com/fsoubelet/Tinder_Data/blob/master/LICENSE
