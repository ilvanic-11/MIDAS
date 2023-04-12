::Fresh Python Install 3.7.4
::For MIDAS
python -m pip install --upgrade pip --user   
:: PIP LICENSE: MIT License (MIT) 
python -m pip install --upgrade wheel --user
:: WHEEL LICENSE: MIT License (MIT)
python -m pip install --upgrade setuptools --user
:: SETUPTOOLS LICENSE: MIT License
python -m pip install --upgrade numpy --user
:: NUMPY LICENSE: BSD License (BSD)
python -m pip install --upgrade numpy_indexed --user	
:: NUMPY_INDEXED LICENSE: Freely Distributable
python -m pip install --upgrade music21 --user
::python -m pip install music21==5.7.0
:: MUSIC21 LICENSE: BSD License

::python -m pip install --upgrade matlab --user
:: MATLAB LICENSE: Unknown
:: Matlab License is pylab and numpy license.

python -m pip install --upgrade plotly --user
:: PLOTLY LICENSE: MIT
python -m pip install --upgrade matplotlib --user
:: MATPLOTLIB LICENSE: OSI Approved :: Python Software Foundation License
::python -m pip install --upgrade pyqt6 --user
:: PYQT6 LICENSE: GPL v3
::python -m pip install --upgrade itertools --user
::python -m pip install --upgrade more-itertools --user
::python -m pip install --upgrade generator_tools --user
python -m pip install --upgrade pyopengl --user
:: PYOPENGL LICENSE: OSI Approved :: BSD License
python -m pip install install pyface==7.0.1
:: PYFACE LICENSE: BSD License (BSD)
::python -m pip install --upgrade pyface --user
python -m pip install --upgrade wxpython --user
:: WXPYTHON LICENSE: OSI Approved :: wxWindows Library Licence
::python -m pip install vtk==8.1.2 --user (LATEST Version is actually 9.0.3, but it's not tested\patched yet for MIDAS)
python -m pip install vtk==9.0.1 --user  
:: VTK LICENSE: OSI Approved :: BSD License
::python -m pip install --upgrade vtk --user
python -m pip install --upgrade traits --user
python -m pip install --upgrade traitsui==7.0.1 --user
:: TRAITS LICENSE: BSD License (BSD)
::python -m pip install --upgrade traitsui --user
python -m pip install --upgrade mayavi --user
python -m pip install --upgrade mlab --user
:: MAYAVI LICENSE: BSD License
::python -m pip install mayavi=4.7.1 --user
python -m pip install --upgrade open3d-python --user
:: OPEN3D LICENSE: MIT License (MIT)
python -m pip install --upgrade pillow --user
:: PILLOW LICENSE: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)
python -m pip install --upgrade opencv-python --user
:: OPEN-CV LICENSE: MIT License (MIT)
python -m pip install --upgrade pygame --user
:: PYGAME LICENSE: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
python -m pip install --upgrade scipy --user
:: SCIPY LICENSE: BSD License (BSD)
python -m pip install --upgrade sympy --user
:: SYMPY LICENSE: BSD License (BSD)
python -m pip install --upgrade inspect --user
:: INSPECT LICENSE: OSI Approved :: Python Software Foundation License
python -m pip install --upgrade mido --user
:: MIDO LICENSE: OSI Approved :: MIT License
python -m pip install --upgrade pyo --user
:: PYO LICENSE: GNU General Public License v3
python -m pip install --upgrade blender --user
:: BLENDER LICENSE: GNU General Public License
python -m pip install --upgrade pyinstaller
:: PYINSTALLER LICENSE: GNU General Public License v2 (GPLv2) (GPLv2-or-later with a special exception which allows to use PyInstaller to build and distribute non-free programs (including commercial ones))


python -m pip install --upgrade flask
:: FLASK LICENSE: BSD License (BSD-3-Clause)
python -m pip install --upgrade requests
:: REQUESTS LICENSE: Apache Software License (Apache 2.0)


::python -m pip install tensorflow==1.15 #This requires a downgrade to python 3.6.8.
:: TENSORFLOW LICENSE: OSI Approved :: Apache Software License

::python -m pip install --upgrade wrapt --user

::python -m pip install --upgrade magenta -- user   ##Requires tensorflow which, above v1.15,requires AVX hardware support.

::NOTE: if vtk, mayavi, traits doesn't build correctly, uninstall and run this .bat again. (There is a package that creates a whole new python directory for installation, I think it's vtk.)
::NOTE: Traits builds from vtk, so packages that use traits need to be installed after vtk.


::pip install py3d
::pip install ipython
::pip install numpy-stl
::pip install pyoints
::pip install pyproj
::pip install GDAL-2.4.1-cp37-cp37m-win_amd64.whl
	::Download .whl here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal 
::pip install Rtree-0.8.3-cp37-cp37m-win_amd64.whl   
	::Download .whl here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree
::pip install pymesh
::pip install pymesh2
::pip install pymesh2-0.1.14-cp35-cp35m-macosx_10_11_x86_64.whl 
	:: Download .whl here: https://pypi.org/project/pymesh2/#files
	:: pymesh2 is a better version.
::pip install pyntcloud 
	:: Unable to pip install: Hard install by downloading this: https://github.com/daavoo/pyntcloud and copying the folder in the zip "pyntcloud" to your python installation's "site-packages" folder.
::pip install pywavefront
::pip install mne
::pip install pyvoro

::pip install python_pcl-XXX.whl
:: Must have appropriate python_pcl wheel. Download here (version not yet python 3.7): https://ci.appveyor.com/project/Sirokujira/python-pcl-iju42/builds/23107177/job/7nh98y6bmft7a42a/artifacts

::pip install mock
::pip install iTerm2
::pip install resource
::pip install naming

::Kivi Install
::python -m pip install kivymd==0.104.2
::python -m pip install --upgrade pip wheel setuptools --user 
::python -m pip install --upgrade docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
::python -m pip install --upgrade kivy.deps.gstreamer --user
::python -m pip install --upgrade kivy.deps.angle --user
::python -m pip install --upgrade kivy --user
::python -m pip install --upgrade kivy_examples --user                                              