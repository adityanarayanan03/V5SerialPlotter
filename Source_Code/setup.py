from cx_Freeze import setup, Executable

packages = ['mpl_toolkits', 'matplotlib.backends.backend_tkagg', 'matplotlib.backends.backend_pdf']


setup(name = 'V5_Serial_Plotter',
    version = '0.1',
    description='Plot from V5 Brain',
    options = {'build_exe': {'packages':packages}},
    executables = [Executable("plotter.py")])