""" This module loads the entire VTK library into its namespace.  It
also allows one to use specific packages inside the vtk directory.."""

from __future__ import absolute_import

# --------------------------------------
from .vtkCommonCore import *
from .vtkCommonMath import *
from .vtkCommonTransforms import *
from .vtkCommonDataModel import *
from .vtkCommonExecutionModel import *
from .vtkCommonMisc import *
from .vtkFiltersCore import *
from .vtkRenderingCore import *
from .vtkInteractionStyle import *
from .vtkRenderingContext2D import *
from .vtkFiltersGeneral import *
from .vtkFiltersSources import *
from .vtkInteractionWidgets import *
from .vtkViewsCore import *
from .vtkViewsInfovis import *
from .vtkCommonColor import *
from .vtkViewsContext2D import *
from .vtkTestingRendering import *
from .vtkPythonContext2D import *
from .vtkImagingCore import *
from .vtkImagingMath import *
from .vtkRenderingUI import *
from .vtkRenderingOpenGL2 import *
from .vtkRenderingVolume import *
from .vtkRenderingVolumeOpenGL2 import *
from .vtkRenderingFreeType import *
from .vtkRenderingLabel import *
from .vtkRenderingLOD import *
from .vtkRenderingImage import *
from .vtkIOVeraOut import *
from .vtkIOTecplotTable import *
from .vtkIOImage import *
from .vtkIOSegY import *
from .vtkIOXMLParser import *
from .vtkIOXML import *
from .vtkIOParallelXML import *
from .vtkIOCore import *
from .vtkIOLegacy import *
from .vtkIOGeometry import *
from .vtkIOParallel import *
from .vtkIOPLY import *
from .vtkIOMovie import *
from .vtkIOOggTheora import *
from .vtkIONetCDF import *
from .vtkIOMINC import *
from .vtkIOLSDyna import *
from .vtkIOInfovis import *
from .vtkIOImport import *
from .vtkIOVideo import *
from .vtkRenderingSceneGraph import *
from .vtkRenderingVtkJS import *
from .vtkIOExport import *
from .vtkIOExportPDF import *
from .vtkRenderingGL2PSOpenGL2 import *
from .vtkIOExportGL2PS import *
from .vtkIOExodus import *
from .vtkIOEnSight import *
from .vtkIOCityGML import *
from .vtkIOAsynchronous import *
from .vtkIOAMR import *
from .vtkInteractionImage import *
from .vtkImagingStencil import *
from .vtkImagingStatistics import *
from .vtkImagingGeneral import *
from .vtkImagingMorphological import *
from .vtkIOSQL import *
from .vtkImagingSources import *
from .vtkInfovisCore import *
from .vtkGeovisCore import *
from .vtkInfovisLayout import *
from .vtkRenderingAnnotation import *
from .vtkImagingHybrid import *
from .vtkImagingColor import *
from .vtkFiltersTopology import *
from .vtkFiltersSelection import *
from .vtkFiltersSMP import *
from .vtkFiltersPython import *
from .vtkFiltersProgrammable import *
from .vtkFiltersModeling import *
from .vtkFiltersPoints import *
from .vtkFiltersVerdict import *
from .vtkFiltersStatistics import *
from .vtkFiltersImaging import *
from .vtkFiltersExtraction import *
from .vtkFiltersGeometry import *
from .vtkFiltersHybrid import *
from .vtkFiltersTexture import *
from .vtkFiltersParallel import *
from .vtkFiltersParallelImaging import *
from .vtkFiltersHyperTree import *
from .vtkFiltersGeneric import *
from .vtkCommonComputationalGeometry import *
from .vtkFiltersFlowPaths import *
from .vtkFiltersAMR import *
from .vtkDomainsChemistry import *
from .vtkCommonPython import *
from .vtkChartsCore import *
from .vtkParallelCore import *
from .vtkImagingFourier import *
from .vtkCommonSystem import *


# useful macro for getting type names
from .util.vtkConstants import vtkImageScalarTypeNameMacro

# import convenience decorators
from .util.misc import calldata_type

# import the vtkVariant helpers
from .util.vtkVariant import *
