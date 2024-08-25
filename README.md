# Slides SoftPython (in italiano)

Tratte dal libro it.softpython.org

## [VEDI LE SLIDE](https://davidleoni.github.io/softpython-it-slides)


## Per editare le slide

**How to build**

Slides built from jupyter notebooks for Python courses, with some quick and dirty integration between:

- [Jupman](https://github.com/DavidLeoni/jupman): jupyter notebook manager (modded 3.5.7 version), allows  to strip solutions from notebooks marked with special tags

- [Interactive Coding Playgrounds (ICP)](https://github.com/lucademenego99/icp-bundle) to allow students to run Python code in slides

- [Python Tutor](https://pythontutor.com/) (using the offline version integrated in jupman) for visualizing code runs

The process is the following:

1. Set up environment according to jupman [Local build with Sphinx setup instructions](https://jupman.softpython.org/en/latest/manual/quickstart.html#Local-build-with-Sphinx)
2. author a jupyter notebook ending in `-sol.ipynb` by using mostly markdown text, sometimes html (for i.e. tables) 
    - mark code you don't want students to see with special jupman tags
    - run Python code in Jupyter to produce HTML widgets for ICP and Python tutor, so the result is immediately visible while authoring
3. run [make_slides.py](make_slides.py) like `make_slides.py lists/lists1` which:
    1. calls jupman to take original `lists1-sol.ipynb` and generate a new `lists1.ipynb` file with stripped solutions 
    2. calls `nbconvert` to export to a reveal.js html presentation file  (a native functionality of Jupyter) 
    3. crudely processes html generated from nbconvert to inject various scripts and css


**Known issues**

- currently [my ICP adaptation is buggy](https://github.com/DavidLeoni/ssds-2023/issues/3)
- organizing cells in multicolumn layout still has to be done in html which may be cumbersome, in pandas notebooks there is [some example workaround](https://github.com/DavidLeoni/jupman/issues/148)

