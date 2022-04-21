try:
    from . import _lib as lib
    from . import nutFiles as fl
    from . import nutDate as dat
    from . import nutOther as oth
except:
    import _lib as lib
    import nutFiles as fl
    import nutDate as dat
    import nutOther as oth
os  = lib.os()
pd  = lib.pandas()
db  = lib.pyodbc()
lite = lib.sqlite3()


#---------------------------------------------------------------
#------------- CLASS DB management -----------------------------
#---------------------------------------------------------------




