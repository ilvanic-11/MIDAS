::Fresh Python Install 3.7.4
::For MIDAS
python -m pip install --upgrade pip --user
python -m pip install --upgrade wheel --user
python -m pip install --upgrade setuptools --user
python -m pip install --upgrade numpy --user
python -m pip install --upgrade numpy_indexed --user	
python -m pip install --upgrade music21 --user
python -m pip install --upgrade matlab --user
python -m pip install --upgrade plotly --user
python -m pip install --upgrade matplotlib --user
python -m pip install --upgrade pyqt5 --user
python -m pip install install pyface==7.0.1
::python -m pip install --upgrade pyface --user
python -m pip install --upgrade wxpython --user
::python -m pip install vtk==8.1.2 --user (LATEST Version is actuall 9.0.3, but it's not tested\patched yet)
python -m pip install vtk==9.0.1 --user  
::python -m pip install --upgrade vtk --user
python -m pip install --upgrade traits --user
python -m pip install --upgrade traitsui==7.0.1 --user
::python -m pip install --upgrade traitsui --user
python -m pip install --upgrade mayavi --user
python -m pip install --upgrade mlab --user
::python -m pip install mayavi=4.7.1 --user
python -m pip install --upgrade open3d-python --user
python -m pip install --upgrade pillow --user
python -m pip install --upgrade opencv-python --user
python -m pip install --upgrade pygame --user
python -m pip install --upgrade scipy --user
python -m pip install --upgrade sympy --user
python -m pip install --upgrade inspect --user
python -m pip install --upgrade mido --user
python -m pip install --upgrade pyo --user
python -m pip install --upgrade blender --user
python -m pip install --upgrade pyinstaller
::python -m pip install tensorflow==1.15 #This requires a downgrade to python 3.6.8.
::python -m pip install --upgrade wrapt --user
::python -m pip install --upgrade magenta -- user   ##Requires tensorflow which, above v1.15,requires AVX hardware support.

::NOTE: if vtk, mayavi, traits doesn't build correctly, uninstall and run this .bat again. (There is a package that creates an whole new python directory for installation, I think it's vtk.)
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
::python -m pip install --upgrade pip wheel setuptools
::python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
::python -m pip install kivy.deps.gstreamer
::python -m pip install kivy.deps.angle
::python -m pip install kivy
::python -m pip install kivy_examples