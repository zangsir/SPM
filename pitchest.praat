#doing pitch analysis and interpolation: 1. to manipulation; 2. extract pitch tier; 3. interpolate quadratically. 4. write to file.


n=numberOfSelected ("Sound")
echo n='n'

printline List of Sound Files

for i to n
    sound'i' = selected ("Sound", i)
    printline sound'i'
endfor


for i to n
    select sound'i'
    label$=selected$ ("Sound")
    To Manipulation: 0.001, 50, 600
    Extract pitch tier
    Interpolate quadratically: 4, "Semitones"
    Write to text file... pitch/'label$'.pitch
    printline finished 'i'



endfor
