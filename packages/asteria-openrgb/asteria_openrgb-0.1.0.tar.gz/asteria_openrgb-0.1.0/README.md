# Asteria - a simple [OpenRGB](https://openrgb.org/) driver

OpenRGB is a great tool for controlling your LEDs, but if you want something more than a static pattern, you'll probably
outgrow its GUI relatively quickly. Fortunately, OpenRGB also offers an SDK that allows programmatic access to your
LEDs. **Asteria is a framework to faciliate automatically updating your LEDs (via OpenRGB) in response to various
conditions.** To make that more concrete, let's look at an example.

## Visual Example

My current PC case is a be quiet! Pure Base 500DX, which features a nice big LED strip down the front. I configured
Asteria to show the following information on those LEDs:

1. GPU temperature (blue = cold, red = hot)
2. CPU temperature (blue = cold, red = hot)
3. Memory usage (all lights off = 0%, all lights on = 100%)

Here's what that looks like all together (&hellip;in pitch dark to show off the LEDs, not because I live in the
sewers&hellip;):

![](asteria_example.jpg)

Asteria automatically scales the configured instruments to fit the available LEDs, and periodically updates them (every
500ms by default). Of course, this is only scratching the surface of what's possible&mdash;what will you come up with?

## Usage

Invoke the main Asteria driver with `python -m asteria CONFIG_FILE`. Add `--help` for further options.

**TODO: expand on this; add systemd user unit**

## Concepts

Here are the key concepts in Astoria:

- The `Driver` is the core Asteria application loop. It's responsible for polling the configured `Instrument`s to get
  their desired LED outputs, and making the OpenRGB SDK calls to set them accordingly. **Note:** generally, users should
not need to interact with this directly.

- `Instrument`s tell the driver how they would like their LEDs illuminated. As part of doing so, they might check the
  value of some `Metric` (e.g., the current CPU temperature), but they aren't required to do so.

- `Metric`s represent any variable of interest (e.g., the current CPU temperature, or % of memory used).

- `Scale`s map a `Metric` to a convenient range for `Instrument`s to work with.

- Finally, two OpenRGB terms: a "device" is anything with addressable LEDs. Every device has one or more "zones," which
  are regions of independently-addressable LEDs. You can explore your devices and their zones using the OpenRGB GUI;
you'll need the device/zone names to write an Asteria [config file](#configuration).

To see how these all fit together, have a look at the [configuration example](#example).

## Configuration
_(This section uses terminology explained in the [Concepts section](#concepts))_

An Asteria configuration file is a [TOML](https://toml.io/) file. At the top level, it should contain an array of
tables, where each header starts with two parts: 1) the OpenRGB device and 2) zone (within that device) to which this instrument should be applied.
Note that it is perfectly valid to assign multiple instruments to a single zone; Asteria will fill all available LEDs,
and assign a (roughly) equal quantity to each instrument.

There are three possible subsections for each config entry. They are described below.

### `instrument`

This section is always required.

Required keys

- `type` (string): the name of the Instrument class to use (see `instruments.py`).

Optional keys

- `args` (table): other arguments to be passed to the `__init__` of your instrument. (Note: Asteria will take care of passing
  the corresponding `metric` for this instrument&mdash;if any&mdash;to the `__init__` call; you do not need to do so.)

### `metric`

This section is only required if the corresponding `instrument` requires a metric.

Required keys

- `type` (string): the name of the metric function to use (see `metrics.py`).

Optional keys

- `args` (table): other arguments to be passed to the metric function. (Note: Asteria will [partially
  apply](https://en.wikipedia.org/wiki/Partial_application) the metric function with these arguments, and pass the
resulting zero-argument function to your instrument (after also applying the scale, if any).)

### `scale`

This section is always optional, but providing a scale without a corresponding metric is not permitted.

Required keys

- `type` (string): the name of the scale function to use (see `scales.py`).

Optional keys

- `args` (table): other arguments to be passed to the scale function.

### Example

Consider the CPU temperature example from earlier: we want our LEDs to be blue when the CPU is cool, and red when it
heats up.  Clearly our `metric` of interest is the CPU temperature. Looking in the `instruments` module, we see that
`LinearHueRange` offers the lighting effect we're interested in (gradually switching from one colour to another).
There's just one problem: when we read our CPU temperature, we'll probably get a value like `42` (degrees Celsius), but
`LinearHueRange` expects a value in the range [0, 1]. Fortunately, `scales.linear` handles that type of
conversion&mdash;we'll just need to tell it what our low and high temperatures thresholds are. Here's what that would
look like in a config file:

```toml
# The header has two levels: the OpenRGB device and zone
# to which this instrument should be applied
# Note: each zone could have multiple effects, so the double
# brackets are required (this is a TOML array of tables)
[["MSI PRO B550M-VC WIFI (MS-7C95)"."JRAINBOW1"]]

# First, our instrument...
["MSI PRO B550M-VC WIFI (MS-7C95)"."JRAINBOW1".instrument]
type = "LinearHueRange"
# That's hue as in "HSV hue"
args = { lower_hue = 180, upper_hue = 360 }

# ...next, our metric...
["MSI PRO B550M-VC WIFI (MS-7C95)"."JRAINBOW1".metric]
type = "get_sensor"
# Path to my CPU temperature--see metrics.get_sensor for details
args = { keys = ["k10temp-pci-00c3", "Tctl", "temp1_input"] }

# ...and finally, our scale.
["MSI PRO B550M-VC WIFI (MS-7C95)"."JRAINBOW1".scale]
type = "linear"
args = { lower = 40, upper = 100 }
```
