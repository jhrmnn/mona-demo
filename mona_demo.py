from mona import Rule
from mona.files import File, add_source, file_collection
from mona.sci.aims import Aims, SpeciesDefaults, parse_aims
from mona.sci.tex import jinja_tex

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rc("font", family="serif", serif="STIXGeneral")
mpl.rc("mathtext", fontset="stix")

xc = "PBE"
conv_threshold = 2e-5


def add_radial_base(species_defs, kwargs):
    for spec in species_defs:
        spec["radial_base"]["number"] += kwargs.pop("radial_base_add")


aims = Aims()
SpeciesDefaults(add_radial_base)(aims)


@Rule
async def converged_energy(inp, enes):
    if len(enes) >= 2 and abs(enes[-1] - enes[-2]) < conv_threshold:
        return np.array(enes)
    if len(enes) > 0:
        inp["radial_base_add"] += 20
    label = f'/calcs/{inp["atoms"][0][0]}/{inp["radial_base_add"]}'
    ene = parse_aims(aims(**inp, label=label))["energy"]
    return converged_energy(inp, [*enes, ene])


@Rule
async def main():
    defaults = {
        "aims": "aims-mona-demo",
        "species_defaults": "light",
        "tags": {
            "xc": xc.lower(),
            "relativistic": "atomic_zora scalar",
            "sc_accuracy_eev": 1e-4,
            "sc_accuracy_rho": 1e-6,
            "sc_accuracy_etot": 1e-7,
            "sc_iter_limit": 100,
            "xml_file": "results.xml",
        },
    }
    return {
        elem: converged_energy(
            {**defaults, "atoms": [[elem, [0, 0, 0]]], "radial_base_add": 0}, []
        )
        for elem in "He Ne Ar Kr".split()
    }


@Rule
async def pub():
    energies = main()
    fig = figure_file(energies["Kr"])
    tex = tex_file("krypton", energies["Kr"], fig)
    return file_collection([tex, fig], label="/pub")


@Rule
async def figure_file(energies):
    offset = int(np.round(energies[-1]))
    plt.figure(figsize=(3, 2))
    plt.plot(np.arange(len(energies)) + 1, (energies - offset) / 1e-3)
    plt.xlabel("Step")
    plt.ylabel(r"$(\mathrm{Energy}/E_\mathrm{h}+%s)/10^{-3}$" % -offset)
    plt.ticklabel_format(useOffset=False)
    filename = "conv.pdf"
    plt.savefig(filename, bbox_inches="tight")
    return File.from_path(filename, keep=False)


@add_source("paper.tex.in")
@Rule
async def tex_file(elem, energies, figfile, template):
    tex = jinja_tex(
        template.read_text(),
        {
            "element": elem,
            "xc": xc,
            "energies": energies,
            "offset": int(np.round(energies[-1])),
            "conv_figure": figfile.name,
            "threshold": conv_threshold,
        },
    )
    texfile = template.stem
    with open(texfile, "w") as f:
        f.write(tex)
    return File.from_path(texfile, keep=False)
