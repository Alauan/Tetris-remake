import cx_Freeze

executables = [cx_Freeze.Executable("main.py", base="Win32GUI")]
cx_Freeze.setup(name="Tetris",
                options={"build_exe": {'packages': ['pygame', 'numpy'], 'include_files': ['Data/']}},
                executables=executables
                )