Include "extlib/menus";

class Hintobj
  with
    hints_seen 0,
    hint_done 0,
    the_hints "Hints go Here",
    description [; self.showhints(); rtrue; ],
    showhints [ max i k;
      max = (self.#the_hints / 2);

      for (i = 1: (i <= max): i++) {
        if ((i==1) && ((max > 1) && (self.hints_seen < max)))
          print
            "There are ", max, " hints: press H for next hint, or any other key to exit.^^^";
        print "(", i, "/", max, ") ";
        print (string) (self.&the_hints-->(i-1));
        new_line; new_line;

        ! How many times through this loop? That is the number of the current
        ! hint. Starting with 1 = 0 hints_seen.
        if (self.hints_seen == (i-1)) self.hints_seen = self.hints_seen + 1;

        ! Only call read_char if currently on the last hint seen and
        ! skip on the very last hint.
        if ((i < max) && (i == self.hints_seen)) {
          @read_char 1 0 0 k;
          if (k ~= 'H' or 'h') return;
        }
      }
    ];

[ HintReady h;
  h.hints_seen = 0;
  ! if ((h.hint_done == 0) && (h hasnt general)) {
  if (h hasnt general) {
     ! if this is first time we've seen this option, unlock it
     move h to h.in_menu;
     give h general;
     ! if this is first option in a submenu, unlock submenu
     if (h.in_menu hasnt general) {
      give h.in_menu general;
      move h.in_menu to Hints;
     }
  }
];

Menu Hints "Hints"
  has general;  ! important -- don't move the main menu to the main menu :)


[ HintSub;
  if (hint_dragon.hints_seen == hint_dragon.#the_hints / 2) remove hint_dragon;

  Hints.select();
];

Verb meta 'hint' 'hints' * -> Hint;

#IfDef DEBUG;
Verb meta 'hintcheck' * -> HintCheck;
[ HintCheckSub o;
  objectloop (o ofclass Option) {
    if (o ofclass Menu) continue;
    if (~~o ofclass Hintobj)
      print (name) o, " missing Hintobj class.^";
    if (~~o provides the_hints)
      print (name) o, " missing the_hints.^";
    if (~~o provides in_menu)
      print (name) o, " missing in_menu.^";
  }
  "Done.";
];
#EndIf;
