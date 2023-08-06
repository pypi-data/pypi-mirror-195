# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdyna']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1', 'scipy>=1.9.3']

setup_kwargs = {
    'name': 'xdyna',
    'version': '0.1.1',
    'description': 'Xsuite dynamics package',
    'long_description': "# xdyna\n\nTools to study beam dynamics in xtrack simulations, like dynamic aperture calculations, PYTHIA integration, dynamic indicators, ...\n\n## Dynamic aperture studies\n\nThe `xdyna` package provides the `DA` class which serves as a simple front-end for setting up and running dynamic aperture studies.\n\nTo start, a `xtrack.line` object is required.\nThe following code then sets up the study and launches the tracking\n\n```python\n\nimport xdyna as xd\n\nda = xd.DA(\n    name='name_of_your_study', # used to generate a directory where files are stored\n    normalised_emittance=[1,1], # provide normalized emittance for particle initialization in [m]\n    max_turns=1e5, # number of turns to track\n    use_files=False \n    # in case DA studies should run on HTC condor, files are used to collect the information\n    # if the tracking is performed locally, no files are needed\n)\n    \n# initialize a grid of particles using 5 angles in x-y space, in a range from 0 to 20 sigmas in steps of 5 sigma.\nda.generate_initial_radial(angles=5, r_min=0, r_max=20, r_step=5, delta=0.) \n\nda.line = line # associate prev. created line, holding the lattice and context, with DA object\n\nda.track_job() # start the tracking\n\nda.survival_data # returns a dataframe with the number of survived turns for the initial position of each particle\n\n```\n\nTo use on a platform like HTCondor, perform the same setup as before but using `use_files=True`.\nEach HTCondor job then only requires the following lines\n\n```python\nimport xdyna as xd\n# This will load the existing DA based on the meta file with the same name found in the working directory.\n# If the script is ran somewhere else, the path to the metafile can be passed with 'path=...'.\nDA = xd.DA(name=study, use_files=True)\n\n# Do the tracking, here for 100 particles.\n# The code will automatically look for particles that are not-submitted yet and use these.\nDA.track_job(npart=100)\n```\n",
    'author': 'Frederik F. Van der Veken',
    'author_email': 'frederik@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xsuite/xdyna',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
