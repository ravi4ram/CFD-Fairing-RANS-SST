import numpy as np
import gmsh

# packages
model = gmsh.model
geo = model.geo
mesh = model.mesh
# init
gmsh.initialize()
model.add("pslv")
gmsh.option.setNumber("General.Terminal", 1)
gmsh.option.setNumber("Mesh.Smoothing", 0)
gmsh.option.setNumber("Mesh.Algorithm", 5) # delquad
gmsh.option.setNumber("Mesh.RecombineAll", 1)
# fairing diameter
fairing_dia = 4
# fairing mesh size
h = 100
# farfield size
H = 5
F = 20 * fairing_dia
# fairing size ratios
R = 0.5 * fairing_dia    # fairing radius
rn = 0.294 * fairing_dia # nose radius
Lc = 1.5 * fairing_dia   # cylinder length
Lf = 0.153 * fairing_dia # frustum length
Re = 0.7 * fairing_dia/2 # frustum end radius
# angles
theta_nose = np.radians(15)
# cone length
Lo = R / np.tan(theta_nose)
# tangency point (circle meets cone)
xt = (Lo**2 / R) * np.sqrt( (rn)**2 / (R**2 + Lo**2) )
yt = xt * (R / Lo)
xo = xt + np.sqrt( rn**2 - yt**2)
xa = xo - rn

# z co-ordinate
z = 0
# sphere section	
geo.addPoint( xo, 0, z, h * 0.01, 201 )
geo.addPoint( xa, 0, z, h * 0.01, 1 )
x = xt; y1 = yt; y2 = -yt
geo.addPoint( x, y1, z, h * 0.01, 2 )
geo.addPoint( x, y2, z, h * 0.01, 3 )
geo.addCircleArc( 2, 201, 1, 21 )
geo.addCircleArc( 1, 201, 3, 22 )

# cone section
x = Lo; y1 = R; y2 = -R
geo.addPoint( x, y1, z, h * 0.01, 11 )
geo.addPoint( x, y2, z, h * 0.01, 4 )
geo.addLine( 3, 4, 31 )
geo.addLine( 11, 2, 40 )

# cylinder section
x = (Lo+Lc); y1 = R; y2 = -R;
geo.addPoint( x, y1, z, h * 0.01, 10 )
geo.addPoint( x, y2, z, h * 0.01, 5 )
geo.addLine( 4, 5, 32 )
geo.addLine( 10, 11, 39 )

# frustum section
x = (Lo+Lc+Lf); y1 = Re; y2 = -Re;
geo.addPoint( x, y1, z, h * 0.01, 9 )
geo.addPoint( x, y2, z, h * 0.01, 6 )
geo.addLine( 5, 6, 33 )
geo.addLine( 9, 10, 38 )

# booster section
Le = 2.0 * fairing_dia;
x = (Lo+Lc+Lf+Le); y1 = Re; y2 = -Re;
geo.addPoint( x, 0, 0, h * 0.01, 203 )
geo.addPoint( x, y1, z, h * 0.01, 8 )
geo.addPoint( x, y2, z, h * 0.01, 7 )
geo.addLine( 6, 7, 34 )
geo.addLine( 8, 9, 37 )
geo.addLine( 7, 203, 35 )
geo.addLine( 203, 8, 36)

# farfield section
geo.addPoint( Lo, 0, 0, H, 202 )
geo.addPoint( -F+Lo, 0, 0, H, 15 )
geo.addPoint( Lo, -F, 0, H, 16 )
geo.addPoint( F+Lo, 0, 0, H, 17 )
geo.addPoint( Lo, F, 0, H, 18 )
geo.addCircleArc( 15, 202, 16, 23 )
geo.addCircleArc( 16, 202, 17, 24 )
geo.addCircleArc( 17, 202, 18, 25 )
geo.addCircleArc( 18, 202, 15, 26 )

# connecting lines
geo.addLine(1, 15, 41)
geo.addLine(4, 16, 42)
geo.addLine(203, 17, 43)
geo.addLine(11, 18, 44)

# loop & surfaces
geo.addCurveLoop([23, -42, -31, -22, 41], 51) 
geo.addPlaneSurface([51], 101)
geo.addCurveLoop([24, -43, -35, -34, -33, -32, 42], 52)
geo.addPlaneSurface([52], 102)
geo.addCurveLoop([25, -44, -39, -38, -37, -36, 43], 53)
geo.addPlaneSurface([53], 103)
geo.addCurveLoop([26, -41, -21, -40, 44], 54) 
geo.addPlaneSurface([54], 104)

# synchronize
geo.synchronize()

# structured mesh
numCellsX = 25; numCellsX_1 = 13; numCellsX_2 = 13; numCellsY = 60;
gradingX = 1.0; gradingY = 1.1;

# 1st section 
mesh.setTransfiniteCurve(23, numCellsX, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(31, numCellsX_1, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(22, numCellsX_2, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(41, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteCurve(42, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteSurface(101, cornerTags=[1, 15, 16, 4]) 

# 4th section
mesh.setTransfiniteCurve(26, numCellsX, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(21, numCellsX_1, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(40, numCellsX_2, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(44, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteCurve(41, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteSurface(104, cornerTags=[11, 18, 15, 1]) 

numCellsX = 25; numCellsX_1 = 7; numCellsX_2 = 7; numCellsX_3 = 7; numCellsX_4 = 7; numCellsY = 60;
gradingX = 1.0; gradingY = 1.1;
# 2nd section
mesh.setTransfiniteCurve(24, numCellsX, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(35, numCellsX_1, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(34, numCellsX_2, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(33, numCellsX_3, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(32, numCellsX_4, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(42, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteCurve(43, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteSurface(102, cornerTags=[4, 16, 17, 203]) 

# 3rd section
mesh.setTransfiniteCurve(25, numCellsX, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(36, numCellsX_1, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(37, numCellsX_2, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(38, numCellsX_3, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(39, numCellsX_4, meshType="Progression", coef=gradingX)
mesh.setTransfiniteCurve(43, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteCurve(44, numCellsY, meshType="Progression", coef=gradingY)
mesh.setTransfiniteSurface(103, cornerTags=[203, 17, 18, 11]) 

# boundaries
dim = 2
gmsh.model.addPhysicalGroup(dim, [101, 102, 103, 104], 501)
gmsh.model.setPhysicalName(dim, 501, "Plane surface")
dim = 1
gmsh.model.addPhysicalGroup(dim, [22, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 21], 1001)
gmsh.model.setPhysicalName(dim, 1001, "FAIRING")
gmsh.model.addPhysicalGroup(dim, [23, 24, 25, 26], 1002)
gmsh.model.setPhysicalName(dim, 1002, "FARFIELD")
# generate mesh
mesh.recombine()
mesh.generate(2)
gmsh.write('turb_pslv_cgrid.su2')
gmsh.fltk.run()
gmsh.finalize()
