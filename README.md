<p align="center">
  <h1 align="center">DTE Calculator</h1>
  <p align="center">
    <a href="https://github.com/jiuguangw/dte_calculator/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
    <a href="https://travis-ci.com/jiuguangw/dte_calculator">
    <img src="https://travis-ci.com/jiuguangw/dte_calculator.svg?branch=master">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/dte_calculator">
    <img src="https://img.shields.io/codeclimate/maintainability/jiuguangw/dte_calculator">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/dte_calculator/issues">
    <img src="https://img.shields.io/codeclimate/issues/jiuguangw/dte_calculator">
    </a>
    <a href="https://codeclimate.com/github/jiuguangw/dte_calculator/code">
    <img src="https://img.shields.io/codeclimate/coverage/jiuguangw/dte_calculator">
    </a>
  </p>
</p>

## Overview

DTE Calculator is a Python based utility to compare electric service plans based on past consumption data.

I was recently trying to compare two electric service plans from DTE Energy - the Residential Electric Service plan (a flat rate plan) vs the Time of Day plan (which has specific rates based on the season and time of day). However, other than publishing the rates, DTE does not provide an utility for determining whether or not switching to the ToD plan would actually save me money, as well as requiring a 12-month commitment.

I decided to instead to do my own analysis using the Energy Usage Report, which contains hours energy usage data for the previous 13 months. As it turns out, I do stand to save money by switching to the ToD plan.

![DTE Calculator](docs/doc.png?raw=true "DTE Calculator")

## Getting Started

### Installing Anaconda Python (Recommended)

All perquisites are installed as a part of [Anaconda Python](https://www.anaconda.com/distribution/#download-section).

Supported Configurations:

| OS      | Python version |
| ------- | -------------- |
| MacOS   | 3.7  |
| Ubuntu  | 3.7  |
| Windows | 3.7  |


### (Optional) Create a virtual environment

I strongly recommend using a virtual environment to ensure dependencies are  installed safely. This is an optional setup, but if you have trouble running the scripts, try this first.

The instructions below assume you are using Conda, though Virtualenv is essentially interchangeable. To create a new Python 3.7 environment, run:

```bash
conda create --name dte python=3.7
conda activate dte
```

The shell should now look like `(dte) $`. To deactivate the environment, run:

```bash
(dte)$ conda deactivate
```

The prompt will return back to `$ ` or `(base)$`.

Note: Older versions of conda may use `source activate dte` and `source
deactivate` (`activate dte` and `deactivate` on Windows).

### Installing dependencies

All of the required packages should have been installed via Anaconda. If you are using another distribution of Python, then you might need to run
```bash
(dte)$ pip install -r requirements.txt
```
To install the required packages.

### Cloning the repo

To checkout the repo:

```bash
git clone git@github.com:jiuguangw/dte_calculator.git
```

### Running the script
The hourly energy usage data can be downloaded from the DTE website, by going to newlook.dteenergy.com and "Energy Usage Data" on the left navigation menu. Pick a start date as far back as possible (the limit is 13 months) and use "CSV" as the file type.

I renamed the resulting file to "dte.csv" and placed it under "data". I can then generate the plot by
```bash
(dte)$ python dte_calculator.py data/dte.csv
```

### Development
The unit tests can be run by first installing the package, then running pytest:
```bash
(dte)$ python install .
(dte)$ pytest
```

## License

### License terms

The Python scripts and the data in CSV are released under the MIT license. The full license details can be found in [LICENSE](LICENSE).

### Technical contributions

I welcome bug fixes, feature additions, and other ways to improve the project. If you'd like to contribute your data, I'm happy to host it here, assuming it is in the same format and anonymized (DTE account number removed).

Please send me pull requests, issues, etc, and contact me if you'd like to be added as a collaborator to the repo.

For others without the time or skills to contribute, I'd also appreciate your help in spreading the word via Facebook, Twitter, etc.

### Donation

Please support the project by making a donation via PayPal or crypto:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N49BVZZLEXU4G&source=url)

![Bitcoin](https://img.shields.io/badge/Bitcoin-367dGyWPSfSjiP6Nh8oSmdCG9MPkMB58Ad-orange.svg?style=flat-square)
![Ethereum](https://img.shields.io/badge/Ethereum-0x4617f57f8b0e3D09Be50CcB32451A2CD20651262-orange.svg?style=flat-square)
![Bitcoin Cash](https://img.shields.io/badge/Bitcoin%20Cash-qrz4e6n3g7e2q6gqz4wetxlgk5eztskxag7tss982j-orange.svg?style=flat-square)
![Litecoin](https://img.shields.io/badge/Litecoin-MVdpa3uXnqoLkZFoarqNnGB9KHr6TL8xst-orange.svg?style=flat-square)

## Contact

- Jiuguang Wang
- [jw@robo.guru](mailto:jw@robo.guru?subject=DTE)
- [www.robo.guru](https://www.robo.guru)

Please drop me a line!
