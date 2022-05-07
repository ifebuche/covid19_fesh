@echo off

<<<<<<< HEAD
set "VIRTUAL_ENV=C:\Users\fesh\Documents\covid\covid_env"
=======
set "VIRTUAL_ENV=C:\Users\USER\Desktop\PYFESH~1\NOTEBO~1\covid\COVID1~1"
>>>>>>> 27dd9875f98c51b82553091a9dbcf027191524ef

if defined _OLD_VIRTUAL_PROMPT (
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
) else (
    if not defined PROMPT (
        set "PROMPT=$P$G"
    )
    if not defined VIRTUAL_ENV_DISABLE_PROMPT (
        set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
    )
)
if not defined VIRTUAL_ENV_DISABLE_PROMPT (
<<<<<<< HEAD
    set "ENV_PROMPT="
    if NOT DEFINED ENV_PROMPT (
        for %%d in ("%VIRTUAL_ENV%") do set "ENV_PROMPT=(%%~nxd) "
    )
    )
    set "PROMPT=%ENV_PROMPT%%PROMPT%"
=======
    set "PROMPT=(COVID1~1) %PROMPT%"
>>>>>>> 27dd9875f98c51b82553091a9dbcf027191524ef
)

REM Don't use () to avoid problems with them in %PATH%
if defined _OLD_VIRTUAL_PYTHONHOME goto ENDIFVHOME
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
:ENDIFVHOME

set PYTHONHOME=

REM if defined _OLD_VIRTUAL_PATH (
if not defined _OLD_VIRTUAL_PATH goto ENDIFVPATH1
    set "PATH=%_OLD_VIRTUAL_PATH%"
:ENDIFVPATH1
REM ) else (
if defined _OLD_VIRTUAL_PATH goto ENDIFVPATH2
    set "_OLD_VIRTUAL_PATH=%PATH%"
:ENDIFVPATH2

set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
