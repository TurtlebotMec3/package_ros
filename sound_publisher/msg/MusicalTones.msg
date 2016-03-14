# definition of Real musical tones
# the tone could be : 
#	do, do#
#	ré, réb, ré#
#	mi, mib
#	fa, fa#
#	sol, solb, sol#
#	la, lab, la#
#	si, sib
#
# /!\ They're in lowercase !! /!\

# the time_base is a time reference for the duration of the tone
# basiquely a black tone could be 500, or 1000
# they are no real time correspondance for now (need to be done)

string tone
uint8 octave
uint16 time_base
