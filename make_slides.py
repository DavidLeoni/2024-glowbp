#/usr/bin/python3/tmp/lists/lists1-sol.slides.html


""" Given a number N, reads parteN-sol.ipynb and generates parteN.slides.html  (without the -sol!)

DIRTY script! 


June 2023: works fine with nbconvert 7.4.0  (6.5.0 didn't show alert boxes properly and added wrong <p><style></p>)
Installing collected packages: mistune, nbconvert
  Attempting uninstall: mistune
    Found existing installation: mistune 0.8.4
    Uninstalling mistune-0.8.4:
      Successfully uninstalled mistune-0.8.4
  Attempting uninstall: nbconvert
    Found existing installation: nbconvert 6.4.0
    Uninstalling nbconvert-6.4.0:
      Successfully uninstalled nbconvert-6.4.0
Successfully installed mistune-2.0.5 nbconvert-7.4.0

TO CHECK:  
    - commands like 
      jupyter nbconvert --to slides parte2-sol.ipynb --SlidesExporter.reveal_theme=sky --SlidesExporter.reveal_transition=fade     
      Current supported options are here:
      https://github.com/jupyter/nbconvert/blob/68b496b7fcf4cfbffe9e1656ac52400a24cacc45/nbconvert/exporters/slides.py
    - currently (oct 2022) this option is NOT supported: --SlidesExporter.reveal_navigationMode=linear
    - how to specify a custom made theme from command line   
    - offline browsing

"""


custom_css = ["../_static/css/softpython-slides.css",
              "../_static/css/ssds-slides.css"]


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('slide', metavar='N', type=str, nargs='?', default=-1,
                    help='a string for the slide number')
args = parser.parse_args()
print(args.slide)
sn = args.slide

if sn == -1:
    print("Please specify a slide number. Aborting.")
    exit(1)

prefix = f'{sn}'

import subprocess


import tempfile
import os

import shutil

tempdir = os.path.join(tempfile.gettempdir(), "jupman")

notebook_sol = f'{prefix}-sol.ipynb'
notebook = f'{prefix}.ipynb'
notebook_dir = os.path.dirname(notebook_sol)

print("notebook_dir=",notebook_dir)

raw_slides_html = os.path.join(tempdir, f'{prefix}-sol')

raw_slides_dir = os.path.dirname(raw_slides_html)
print("raw_slides_dir=",raw_slides_dir)

if not os.path.isdir(raw_slides_dir):
    os.makedirs(raw_slides_dir)



# some paranoid check
print('bn', os.path.basename(notebook))
print('dn', os.path.dirname(notebook))
if os.path.isfile(notebook_sol):
    if notebook.split('.ipynb')[0] + '-sol.ipynb' == notebook_sol:
        if os.path.dirname(notebook) == notebook_dir:
            if os.path.isfile(notebook):
                print('d')
                print(f"DELETING {notebook}    (temporary behoaviour, should be done by jupman)")
                os.remove(notebook)
    
print(f"MAKE_SLIDES: Generating {notebook} ....")

import jupman_tools as jmt

import conf
jmt.init(conf.jm, vars(conf))
conf.jm.generate_exercise(notebook_sol, notebook_dir)

print(f"MAKE_SLIDES: Creating {raw_slides_html} ....")

#NOTA: ho fissato la versione di reveal perchè altrimenti mi dava pagina bianca
cmd = ['jupyter', 'nbconvert', '--to', 'slides', notebook, '--output', raw_slides_html]
        #"--reveal-prefix", "./risorse/reveal"] #"https://unpkg.com/reveal.js@4.0.2"]

print(' '.join(cmd))
res = subprocess.check_output(cmd)

print(res)




dest = f'{prefix}.slides.html'

print("Reading", raw_slides_html)
with open(f'{raw_slides_html}.slides.html', encoding='utf8') as fr:
    s = fr.read()
    
    ps = s
    rev = '<div class="reveal">'    

    css_links = ''
    for css in custom_css:
        the_id = css.split('/')[-1][:-4]
        css_links += f'\n <link rel="stylesheet" href="{css}" id="{the_id}-theme">'
    print(css_links)

    ps = ps.replace(rev, rev + css_links)
                    
    
    ps = ps.replace('transition: "slide",',
    """
            transition: "fade",
            navigationMode: "linear",                
    """)
    
    ps = ps.replace('slideNumber: "",', 
                    'slideNumber: true,')
    

    manual_reveal = """
<script type="text/javascript" src="risorse/reveal/dist/reveal.js"></script>
<script type="text/javascript" src="risorse/reveal/plugin/notes/notes.js"></script>"""

    jupman = """
    <link rel="stylesheet" href="../_static/css/jupman.css">
    <script type="text/javascript" src="../_static/js/pytutor-embed.bundle.min.js"></script>    
    <script type="text/javascript" src="../_static/js/jupman.js"></script>            
    """
    icp = """
    <script type="text/javascript" src="../_static/js/python.iife.js"></script>    
    """
        
    ssds = """
    <link rel="stylesheet" href="../_static/css/ssds-slides.css">
    """


    #ps = ps.replace('</head>',  manual_reveal + '\n</head>')
    ps = ps.replace('</head>',  jupman + icp + ssds + '\n</head>')
    # useful for weird floating placements you don't want to show in jupyter but only in slides
    ps = ps.replace('data-jupman-style', 'style')  
    ps = ps.replace("Reveal.addEventListener('slidechanged', update);",
    """
    Reveal.addEventListener('slidechanged', update);
    
    let updateVizs = function (container){
    
        let viz_ids = $(container).find('.pytutorVisualizer')
            .map((i, el) => el.getAttribute('id')).get();
            
            
        console.log('jupman slides: viz ids', viz_ids);
        
        let cfg_ids = viz_ids.map(theid => 'pytut_cfg_' +
                                    theid.substring(3).replace('-','_'));                                
        
        console.log('jupman slides: cfg ids', cfg_ids);
        
        for (let i=0; i<cfg_ids.length;i++){
            let cfg_id = cfg_ids[i];
            let viz_id = viz_ids[i];
            let trace_id = 'trace-' + viz_id;
            let cfg = window[cfg_id];
            console.log('jupman slides:', cfg);
            let exViz = jmRenderPytut(trace_id, viz_id, cfg);
            console.log('Created executionVisualizer:', exViz);
        }
        
            
            
    }; 
    
    Reveal.on( 'ready', event => {
        // event.currentSlide, event.indexh, event.indexv
        console.log('jupman slides EVENT: ready', event);   
        //console.log('Skipping update...');
        // needed for pdfs
        updateVizs(document);
    } );
    Reveal.addEventListener('resize', event => {            
        console.log('jupman slides EVENT: resize', event);         
        console.log('Skipping update...');
        //updateVizs(document);    
    });
    Reveal.addEventListener('overviewshown', event => {            
        console.log('jupman slides EVENT: overviewshown', event);           
        updateVizs(document);    
    });    
    Reveal.addEventListener('overviewhidden', event => {            
        console.log('jupman slides EVENT: overviewshown', event);           
        updateVizs(event.currentSlide);    
    });
    Reveal.addEventListener('slidechanged', event => {
        console.log('jupman slides EVENT: slidechanged', event);  
        console.log("The event is", event);
        updateVizs(event.currentSlide);            
    });
    """)

    #ps = ps.replace('require(',  'console.log("DAV:About to run require..."); require(')
    #ps = ps.replace('</body>', '')
    #ps = ps.replace('</html>',  '<div>SGURIMPO</div></body></html>')
    #ps = ps.replace('<html>', '<html><script>console.log("DAV: after HTML"); </script>')

    #Fixes crap of nbconvert 6.5.0 I guess - WITHOUT THIS REQUIRE <script> AT THE BOTTOM DOESN'T RUN !!!!
   # ps = ps.replace('<p><style></p>','<p><style></style></p>')

    with open(dest, 'w', encoding='utf8') as fw:
        fw.write(ps)
        print()
        print("Done writing", f"Slides available at   file://{os.path.abspath(dest)}")
        print()


print("DONE.")
