;_import_
;    "lib/math.forth"

_data_
0 VAR var_a

_text_

LOOP
    1 !i 4 <= 1
    WHILE
        LOOP
            1 !j 4 <= 1
            WHILE
                i j <= IF
                    var_a j + !var_a
                ELSE
                THEN
            REPEAT
    REPEAT
HALT
