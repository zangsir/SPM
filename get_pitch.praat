form Params
    real pitch_step 0.01
    real pitch_floor 50
    word interpolate no
    text sound_path /Users/zangsir/Desktop/speech-exp-diuss/
endform


writeInfoLine()
sound_files$=sound_path$ + "*.flac"
Create Strings as file list: "fileList", sound_files$
fileList = selected("Strings")
fileCount = Get number of strings

for curFile from 1 to fileCount
    #appendInfoLine: curFile
    select fileList
    soundname$ = Get string... curFile
    curSound=Read from file... 'sound_path$''soundname$'
    #sound'curFile' = selected ("Sound", curFile)
    #filename$ = selected$ ("Sound", curFile)
    
    #appendInfoLine: soundname$
    label$=selected$ ("Sound")
    mani=To Manipulation: pitch_step, pitch_floor, 600
    pt=Extract pitch tier
    if interpolate$="yes"
       Interpolate quadratically: 4, "Semitones"
       appendInfoLine: "interpolation done"
    endif
    Write to text file... pitch/pitc'label$'.pitch
    #appendInfoLine: "finished ", curFile
    removeObject:mani,pt,curSound



   
endfor
