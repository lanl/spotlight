#! /usr/bin/env python
""" Create an HTML summary page for GSAS or GSAS-II analyses.
This script requires a particular setup for Spotlight.
"""

import argparse
import jinja2
import itertools
import matplotlib.pyplot as plt
import mpld3
import numpy
from mpld3 import plugins
from spotlight import filesystem
from spotlight import gsas
from spotlight.io import solution_file

class TopToolbar(plugins.PluginBase):
    """ Plugin for moving toolbar to top of figure.
    """

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("y", 2);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

def histogram_from_file(data_file):
    data = numpy.loadtxt(data_file, comments="#")
    x = data[:, 1]
    y_obs = data[:, 2]
    y_fit = data[:, 3]
    res = data[:, 4]
    ref = data[:, 5]
    return map(list, [x, y_obs, y_fit, res, ref])

def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

def phases_from_icode(val, n_phases, test_vals=None):
    phase_vals = [4]
    for n in range(n_phases):
        phase_vals.append(phase_vals[-1] * 2)
    test_vals = powerset(phase_vals) if test_vals == None else test_vals
    for powervals in powerset(phase_vals):
        if numpy.sum(powervals) == val:
            result = []
            for icode in powervals:
                result.append(phase_vals.index(icode))
            return result

def main():

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", default="solution.db")
    parser.add_argument("--setup-dir", default="tmp_minima")
    parser.add_argument("--output-file", default="out.html")
    parser.add_argument("--gsasii", action="store_true")
    opts = parser.parse_args()
    
    # special section names
    detectors_section = "detectors"
    phases_section = "phases"
    
    # read file
    config, _, _, best_x, best_y = solution_file.SolutionFile.read_data(opts.input_file)
    
    # get histograms and phases
    num_hists = 0
    num_phases = 0
    phase_files = []
    for section in config.cp.sections():
        if section.startswith(detectors_section):
            num_hists += 1
        elif section.startswith(phases_section):
            num_phases += 1
            phase_files.append(config.cp.get(section, "phase_file"))
    
    # change to setup dir
    filesystem.mkdir(opts.setup_dir, change=True)
    
    # get model diffraction pattern
    html_figs = []
    for j in range(num_hists):
    
        # write CSV file with histogram data, model, and reflection positions
        hist_file = "hist_{}.txt".format(j)
        if opts.gsasii:
            cmd = ["gsasii_write_csv",
                   "--input-file", "step_2.gpx",
                   "--output-file", hist_file,
                   "--histogram", j]
        else:
            cmd = ["gsas_write_csv", j + 1, "TRIAL", hist_file]
        gsas._external_call(cmd)
    
        # read results
        x, y_obs, y_fit, res, ref = histogram_from_file(hist_file)
    
        # create figure
        fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    
        # plot histograms
        axs[0].plot(x, y_obs, linewidth=0.5, c="red", label="Data")
        axs[0].plot(x, y_fit, linewidth=0.5, c="black", label="Fit")
        axs[0].set_xlabel(r"D-spacing ($\AA$)")
        axs[0].set_ylabel(r"Normalized Counts")
        axs[0].set_xlim(numpy.min(x), numpy.max(x))
    
        # loop over reflection data
        categories_in_order = phase_files
        categories_in_order.sort()
        x_ref = {}
        y_ref = {}
        for x_i, y_i in zip(x, ref):
    
            # find indices of phases for a given x-position
            phase_idxs = phases_from_icode(y_i, len(categories_in_order))
            if phase_idxs == None:
                continue
    
            # record all phases present at the given x-position
            for idx in phase_idxs:
                if idx not in x_ref.keys():
                    x_ref[idx] = []
                    y_ref[idx] = []
                x_ref[idx].append(x_i)
                y_ref[idx].append(idx)
    
        # plot reflections
        points = []
        for idx in x_ref.keys():
            p = axs[1].scatter(x_ref[idx], y_ref[idx], marker="|", linewidth=0.5, alpha=1.0, c="black")
            points.append(p)
        axs[1].set_yticks(range(len(categories_in_order)))
        axs[1].set_yticklabels(categories_in_order)
        axs[1].set_xlabel(r"D-spacing ($\AA$)")
        axs[1].set_ylim(-1, len(categories_in_order))
        axs[1].grid()
    
        # plot residual
        axs[2].plot(x, res, linewidth=0.5, c="black")
        axs[2].set_xlabel(r"D-spacing ($\AA$)")
        axs[2].set_ylabel(r"Residual Normalized Counts")
    
        # interactive legend
        lines = axs[0].get_lines()
        lines_labels = [l.get_label() for l in lines]
        lines = zip(axs[0].get_lines(), [None] + points, [None] + axs[2].get_lines())
        interactive_legend = plugins.InteractiveLegendPlugin(lines,
                                                             lines_labels,
                                                             alpha_unsel=0.0,
                                                             alpha_over=1.0,
                                                             start_visible=True)
        plugins.connect(fig, interactive_legend)
    
        # move toolbar
        plugins.connect(fig, TopToolbar())
    
        # formatting
        plt.subplots_adjust(top=0.99)
    
        # save HTML
        html_fig = mpld3.fig_to_html(fig)
        plt.close()
        html_figs += [html_fig]
    
    # HTML template
    HTML = """
    <html>
    <head>
    </head>
    <body>
    
    <h1>{{title}}</h1>
    
    {% for html_fig in html_figs %}
    <h1>Histogram {{loop.index}}</h1>
    {{html_fig}}
    {% endfor %}
    
    </body>
    </html>
    """
    
    # generate HTML
    e = jinja2.Environment()
    e.globals.update(zip=zip)
    html = e.from_string(HTML).render(
               title=opts.setup_dir,
               html_figs=html_figs)
    
    # write HTML
    with open(opts.output_file, "w") as fp:
        fp.write(html)

if __name__ == "__main__":
    main()
