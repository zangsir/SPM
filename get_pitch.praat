form Params
    real pitch_step
    real pitch_ceiling
    word interpolate
    text sound_path
endform


writeInfoLine()
sound_files$=sound_path$ + "*.flac"
Create Strings as file list: "fileList", sound_files$
fileList = selected("Strings")
fileCount = Get number of strings
#soundDir$="/Users/zangsir/Desktop/speech-exp-diuss/test/"

for curFile from 1 to fileCount
    #appendInfoLine: curFile
    select fileList
    soundname$ = Get string... curFile
    curSound=Read from file... 'sound_path$''soundname$'
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
