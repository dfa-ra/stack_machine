;_import_
;    "lib/math.forth"

_data_
5 VAR var_a
9 VAR var_b

_text_

var_a var_b > IF
    var_a !tmp
    var_b !var_a
    tmp !var_b
ELSE
    var_a var_b + !var_b
THEN


HALT
