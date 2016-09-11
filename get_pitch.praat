form Params
    real pitch_step
    real pitch_ceiling
    word interpolate
endform


writeInfoLine()
Create Strings as file list: "fileList", "/Users/zangsir/Desktop/speech-exp-diuss/test-small/*.flac"
fileList = selected("Strings")
fileCount = Get number of strings
soundDir$="/Users/zangsir/Desktop/speech-exp-diuss/test/"

for curFile from 1 to fileCount
    #appendInfoLine: curFile
    select fileList
    soundname$ = Get string... curFile
    curSound=Read from file... 'soundDir$''soundname$'
    #sound'curFile' = selected ("Sound", curFile)
    #filename$ = selected$ ("Sound", curFile)
    
    appendInfoLine: soundname$
    label$=selected$ ("Sound")
    To Manipulation: pitch_step, pitch_ceiling, 600
    Extract pitch tier
    if interpolate$="yes"
       Interpolate quadratically: 4, "Semitones"
       appendInfoLine: "interpolation done"
    endif
    Write to text file... pitch/pitc'label$'.pitch
    #appendInfoLine: "finished ", curFile


   
endfor
