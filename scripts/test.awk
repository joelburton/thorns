/chose justice/{justice++}
/chose mercy/{mercy++}
/chose inaction/{inaction++}
/ran out of time/{time++}
/You have died/{died++}
/55 total/{score++}

END {
    if(justice==1 && mercy==1 && inaction==1 && time==1 && died==1 && score==1)
        print "OK";
    else {
        print "FAIL ",
            " justice", justice,
            ", mercy", mercy,
            ", inaction", inaction,
            ", time", time,
            ", died", died,
            ", score", score ;
            exit 1
        }
}
