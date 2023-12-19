from compileall import compile_file

compile_file("pytest_loop.py")

file = open("__pycache__//pytest_loop.cpython-312.pyc",'rb').read()
with open("pytest_loop_3t.pyc",'ab+') as f:
    f.write(file)