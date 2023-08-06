@echo off
:: Check for the validity of the input
if [%1]==[] goto USAGE
if [%2]==[] goto USAGE
echo.
echo MITSU Fast Video Processing Script
echo ******************************************************************
echo.
:: Notice the user what is neccessary to use the script
echo CAUTION: In order to use the script, make sure that "ffmpeg" and "ffprobe" are in your PATH environment variable!
echo CAUTION: When giving the path to the folder with video files, remember to end it with the '\' sign!
echo CAUTION: If you are using the files or paths containing spaces please enclose them between the double qutation marks!
echo.
:: Create the directory for storing the results
:: set DIR="VQIs-results-%YYYY%-%MM%-%DD%"
set DIR="VQIs-results-1111-11-11"
echo Creating the %DIR% directory for storing the results
echo.
mkdir %DIR%
echo.
echo Going into %DIR%...
cd %DIR%
echo.
:: Read the folder path
set FOLDER=%1
echo.
:: Read the binary file path
set EXECUTABLE=%2
echo Binary file at: %EXECUTABLE%
echo.
:: Read which VQIs run
set VQIS=%3
echo VQIs to run: %VQIS%
echo.
:: Calculate the metrics for each file in the folder:
echo Calculating the metrics for %FOLDER% file...
echo.
echo.
:: for %%f in (%FOLDER%*) do call :calculateMetrics "%%f"
call :calculateMetrics %FOLDER%
echo.
cd ..
echo ******************************************************************
goto :END
::
:: calculateMetrics function:
::
:calculateMetrics
:: Extract the sole file name from the video file
set FILENAME="%~n1"
:: Save the path to the video file
set VIDEOFILE=%1
echo The sole video file name: %FILENAME%
echo Full path to the video file: %VIDEOFILE%
:: Read the dimensions of the video frame and the FPS
ffprobe -v error -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 %VIDEOFILE% > widthTempFile
ffprobe -v error -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 %VIDEOFILE% > heightTempFile
ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 %VIDEOFILE% > fpsTempFile
set /p WIDTH= < widthTempFile
set /p HEIGHT= < heightTempFile
set /p FPS= < fpsTempFile
:: Calculate the FPS value:
:: Multiply by 1000 not to lose precision when performing integer arithmetic
for /f "tokens=1,2 delims=/ " %%a in ("%FPS%") do set /a NUM=%%a*1000&set DEN=%%b
set /a FPS="NUM/DEN"
:: Inser the dot in the result
set FPS=%FPS:~0,2%.%FPS:~2,2%
del /Q widthTempFile
del /Q heightTempFile
del /Q fpsTempFile
echo Width: %WIDTH%
echo Height: %HEIGHT%
echo FPS: %FPS%
echo.
:: Convert the video into the yuv format an store the ffmpeg log file
set YUV=%FILENAME%.yuv
set LOGFILE=ffmpeglog-%FILENAME%.txt
echo Uncompressing the video using the ffmpeg...
:: ffmpeg -i %VIDEOFILE% -pix_fmt yuv420p -hide_banner %YUV% > %LOGFILE% 2>&1
ffmpeg -i %VIDEOFILE% -pix_fmt yuv420p -nostdin -v info %YUV% > %LOGFILE% 2>&1
echo Done!
echo.
:: Calculate the metrics on the file and save the output in the proper file
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"

set RESULTS=results-%FILENAME%.csv
set OUTPUT=output.txt
echo Calculating the metrics on the uncompressed video stream...
%EXECUTABLE% %YUV% %WIDTH% %HEIGHT% %VQIS% %FPS% > %OUTPUT%
echo Done!
echo.
findstr /C:"Calculation time:" %OUTPUT%
findstr /C:"milliseconds per frame" %OUTPUT%
echo.
move /Y metricsResultsCSV.csv %RESULTS% > NUL
echo Results saved in the %RESULTS% file
echo.
:: Remove the output.csv file
del /Q %OUTPUT%
:: remove ffmpeg logfile
del /Q %LOGFILE%
:: Remove the YUV file
echo Removing the %YUV% file...
del /Q %YUV%
echo.
EXIT /B
goto :eof
::
:: end of the calculateMetrics function
::
:USAGE
echo.
echo WARNING: Missing argument.
echo.
echo Proper usage of the script:
echo.
echo %0 FullPathToTheFolderWithVideos FullPathToTheBinaryFile VQIsToRun
echo.
:END
