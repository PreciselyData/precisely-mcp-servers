@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
set "ENV_FILE=%REPO_ROOT%\.env"
set "JAVA17_HOME=C:\Program Files\Java\jdk-17.0.17+10"
set "JAR_PATH="

if not "%~1"=="" (
    set "ENV_FILE=%~1"
    shift
)

if not exist "%ENV_FILE%" (
    >&2 echo Environment file not found: "%ENV_FILE%"
    exit /b 1
)

for %%F in ("%REPO_ROOT%\tss-mcp-server-*.jar") do (
    if /I not "%%~nxF"=="tss-mcp-server-*.jar" (
        set "JAR_PATH=%%~fF"
        goto jar_found
    )
)

:jar_not_found
>&2 echo Packaged jar not found under "%REPO_ROOT%\".
>&2 echo Build it first with "scripts\run-mvnw-java17.cmd -B -ntp package".
exit /b 1

:jar_found
if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" goto java_ready
)

if exist "%JAVA17_HOME%\bin\java.exe" (
    set "JAVA_HOME=%JAVA17_HOME%"
    set "PATH=%JAVA_HOME%\bin;%PATH%"
    goto java_ready
)

>&2 echo Java runtime not found. Set JAVA_HOME or install Java 17 at "%JAVA17_HOME%".
exit /b 1

:java_ready
for /f "usebackq tokens=* delims=" %%A in ("%ENV_FILE%") do (
    set "LINE=%%A"
    if not "!LINE!"=="" (
        if not "!LINE:~0,1!"=="#" (
            for /f "tokens=1* delims==" %%B in ("!LINE!") do (
                if not "%%B"=="" set "%%B=%%C"
            )
        )
    )
)

>&2 echo Launching TSS MCP server with environment from "%ENV_FILE%".
::"%JAVA_HOME%\bin\java.exe" -jar "%JAR_PATH%" %*
"%JAVA_HOME%\bin\java.exe" -Dspring.http.client.factory=apache -jar "%JAR_PATH%" %*
exit /b %ERRORLEVEL%