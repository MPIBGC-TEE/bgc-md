# vim:set ff=unix expandtab ts=4 sw=4:
file_name="Hunt1991TreePhysiol.py"
global_vars=globals()
local_vars=locals()
with open(file_name) as f:
    code = compile(f.read(),file_name, 'exec')
    exec(code, global_vars, local_vars)
    print(x)

