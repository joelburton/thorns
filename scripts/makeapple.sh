scp thorns.z3 lab:FictionTools/myproject.z3
ssh lab "cd FictionTools; source .punyrc; APPLE2_Z3_INFOCOM=true puny -b apple2"
scp lab:FictionTools/myproject_apple2.dsk /tmp
