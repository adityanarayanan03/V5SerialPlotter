from cx_Freeze import setup, Executable

setup(name = 'V5_Serial_Plotter',
    version = '0.1',
    description='Plot from V5 Brain',
    executables = [Executable("plotter.py")])