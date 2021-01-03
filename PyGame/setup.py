# we want to let our friends to play our game without asking them to get python or pygame

import cx_Freeze

executables = [cx_Freeze.Executable('testpyGame.py')]

cx_Freeze.setup(
    name='A bit Racey',
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['racecar.png']}},
    executables = executables
    
    )

# to run this file:
#   go to the directory of the game
#   python3 setup.py bdist_dmg
#   (this will create a build folder with hopefully an executable)
#    cd A bit racey.app
#    cd Contents/MacOS
#   ./testpyGame