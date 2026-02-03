[ SundialTime time hour min;
    hour = (time / 60) % 12;
    min = (time % 60) / 5 * 5; ! fuzz to nearest 5 mins

    if (min > 30) hour = (hour + 1) % 12; ! to print "til", need next hour

    switch (min) {
        5: print "five past";
        10: print "ten past";
        15: print "quarter past";
        20: print "twenty past";
        25: print "twenty-five past";
        30: print "half past";
        35: print "twenty-five til";
        40: print "twenty til";
        45: print "quarter til";
        50: print "ten til";
        55: print "five til";
    }
    print " ";
    #IfDef OPTIONAL_LANGUAGE_NUMBER;
        if (hour == 0) hour = 12;
        LanguageNumber(hour);
    #IfNot;
        switch (hour) {
            0: "twelve";
            1: "one";
            2: "two";
            3: "three";
            4: "four";
            5: "five";
            6: "six";
            7: "seven";
            8: "eight";
            9: "nine";
            10: "ten";
            11: "eleven";
        }
    #Endif;
];
