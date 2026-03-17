Global mm_needs_new_line = false;   ! keeps track of if anything printed

! Move all monks one step, using prop_name
!   (walk_office or walk_home)
! Returns true if all movement is done
!
! Arrays are like
!    walk_to (e_to) (Bedroom) (Bed) 0 (Bedroom) (d_to)
!
! meaning
!   - e_to         : walk east
!   - Bedroom      : go to bedroom (useful for skipping doors)
!   - Bed          : sit on bed (checks if thing is enterable)
!   - Bedroom      : get up from bed to Bedroom (if was in enterable)
!   - d_to         : go down
!
! If anything is printed, follows by a blank line.

! [ MoveAllMonks _m _count _dir _moved;
!   mm_needs_new_line = false;

!   objectloop(_m ofclass Monk) MoveAMonk(_m, walk_home);

!   if (mm_needs_new_line) new_line;
!   return (_count == 0);
! ];

[ MoveAMonk prop_name m hush _dir _res ;
  ! print "---", (the) m, " index=", m.walk_index,
  !     " prop_len=", m.#(prop_name) / 2, "^";
  if (m.walk_index >= m.#(prop_name) / 2) rfalse;
  _dir = m.&(prop_name)-->m.walk_index++;
  _res = MovePerson(m, _dir, hush);
  if (SceneGoHome has active && parent(m) == m.home) {
    m.went_home();
  }
  return _res;
];



[ DirName _dir ;
  switch(_dir) {
    n_to: print "north";
    s_to: print "south";
    w_to: print "west";
    e_to: print "east";
    u_to: print "up";
    d_to: print "down";
    #IfDef OPTIONAL_FULL_DIRECTIONS;
      ne_to: print "northeast";
      se_to: print "southeast";
      nw_to: print "northwest";
      sw_to: print "southwest";
    #EndIf;
    #IfDef DEBUG;
      default: print "*** OppDirName REPORT BUG";
    #EndIf;
  }
];

[ OppDirName _dir ;
  switch (_dir) {
    s_to: print "the north";
    n_to: print "the south";
    w_to: print "the east";
    e_to: print "the west";
    d_to: print "upstairs";
    u_to: print "downstairs";
    #IfDef OPTIONAL_FULL_DIRECTIONS;
      ne_to: print "the southwest";
      se_to: print "the northwest";
      nw_to: print "the southeast";
      sw_to: print "the northeast";
    #EndIf;
    #IfDef DEBUG;
      default: print "*** OppDirName REPORT BUG";
    #EndIf;
  }
];

! Report departure
!   m = monk
!   dir = direction or new room
!   fakedir = true if dir is not a direction
!
! Prints message regardless of whether player is there; any "if"
! condition should be in the caller

[ ReportDepartures m dir fakedir ;
    mm_needs_new_line = true;
    print "^", (The) m;

    ! Custom messages for custom departures (not needed)
    ! if (dir == EastRoom) {
    !     print " opens the door to the east room and heads in.";
    !     return;
    ! }

    if (fakedir) {
      if (dir has enterable) print " sits in ", (the) dir;
      else print " goes to ", (the) dir;
    } else print " heads ", (DirName) dir;
    print ".";
];

! Report arrival
!   m = monk
!   dir = direction or NEW room
!   fakedir = true if dir is not a direction
!
! Prints message regardless of whether player is there; any "if"
! condition should be in the caller

[ ReportArrivals m dir fakedir ;
    mm_needs_new_line = true;
    print "^", (The) m;

    ! Custom messages for custom arrivals (not needed)
    ! if (dir == NorthRoom && parent(m) == EastRoom) {
    !       print " arrives here through the door from the east room.";
    !       return;
    ! }

    if (fakedir) {
      if (parent(m) has enterable ) print " gets up from ", (the) parent(m);
      else print " comes from ", (the) parent(m);
    }
    else print " arrives from ", (OppDirName) dir;
    print ".";
];

! Move a single monk one step
!
!   m = the monk
!   dir = direction to go or absolute room/enterable
!
! If dir=0, they're pausing and don't move (& nothing printed).
! Prints notification messages if player is room unless hush is true

[ MovePerson m dir hush _from _to _fakedir ;
  if (dir == 0) rtrue;  ! not done moving, but pausing at loc

  _from = parent(m);
  _fakedir = (dir ~= n_to or s_to or w_to or e_to or u_to or d_to);

  if (~~_fakedir) _to = _from.(dir);
  else _to = dir;

  ! print "*** m=", (the) m, " dir=", dir, " to=", (name) _to, "^";

  if (~~hush) {
    if (_from == location) ReportDepartures(m, dir, _fakedir);
    else if (_to == location) ReportArrivals(m, dir, _fakedir);
  }

  move m to _to;
  if (_to == PriorsSolar) give PriorDoor locked;
];
