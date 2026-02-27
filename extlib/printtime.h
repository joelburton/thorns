[ SundialTime time hour min rounded_min;
    hour = (time / 60) % 12;
    min = time % 60;

    if (min < 8) rounded_min = 0;
    else if (min < 23) rounded_min = 15;
    else if (min < 38) rounded_min = 30;
    else if (min < 53) rounded_min = 45;
    else {
        rounded_min = 0;
        hour = (hour + 1) % 12;  ! Round up to next hour
    }

    ! Adjust hour for "til" times
    if (rounded_min == 45) hour = (hour + 1) % 12;

    switch (rounded_min) {
        0:  ; ! just use the hour
        15: print "quarter past ";
        30: print "half past ";
        45: print "quarter to ";
    }

    #IfDef OPTIONAL_LANGUAGE_NUMBER;
        if (hour == 0) hour = 12;
        LanguageNumber(hour);
    #IfNot;
        switch (hour) {
            0: print "twelve";
            1: print "one";
            2: print "two";
            3: print "three";
            4: print "four";
            5: print "five";
            6: print "six";
            7: print "seven";
            8: print "eight";
            9: print "nine";
            10: print "ten";
            11: print "eleven";
        }
    #Endif;
];