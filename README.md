# ssds 2023 summerschool

Slides built from jupyter notebooks for Python courses, with some quick and dirty integration between:

- [Jupman](https://github.com/DavidLeoni/jupman): jupyter notebook manager (modded 3.5.7 version)

- [Interactive Coding Playgrounds (ICP)](https://github.com/lucademenego99/icp-bundle) to allow students to run Python code in slides

- [Python Tutor](https://pythontutor.com/) (using the offline version integrated in jupman) for visualizing code runs

The process is the following:

1. author in jupyter with mostly markdown text, sometimes html (for i.e. tables) 
    - run Python code in Jupyter to produce HTML widgets for ICP and Python tutor, so the result is immediately visible while authoring
2. run [make_slides.py](make_slides.py) which calls `nbconvert` to export to a reveal.js html presentation file  (a native functionality of Jupyter) 
3. make_slides crudely processes html generated from jupyter to inject various scripts and css


Downsides: organizing cells in multicolumn layout still has to be done in html which may be cumbersome
