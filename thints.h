Constant HAS_HINTS;
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

Menu HintGeneral "General";

Option -> Hint_intro "Who are we, and what's our purpose?"
 class Hintobj
 with in_menu HintGeneral,
 the_hints
  "You're a novice monk at the priory Our Lady of Thorns."
  "A dramatic thing happens early in the game that will give you a sense
    of your purpose in the game."
  "If that hasn't happened yet, wander around the priory until that happens.";

Option -> Hint_commands "What are uncommon commands used by this game?"
  class Hintobj
  with in_menu HintGeneral,
  the_hints
    "MAP: see a map of the area.";

#IfDef DEBUG;
Option -> Hint_debug "What are secret debugging commands?"
  class Hintobj
  with in_menu HintGeneral,
  the_hints
    "There are others, but the most useful for alpha/beta testers:^
    ^GOTO location: jump to any area by name.
    ^GONEAR obj: jump to area that contains that object.
    ^PURLOIN obj: take this object from wherever it is.
    ^SCOPE: list all the objects you can see.
    ^TREE: show tree of objects in your room.
    ^ROOMS: get a list of all rooms in game.
    ^^Specific to this game:
    ^SETTIME h m: set time (eg: ~SETTIME 14 15~ sets to 2:15pm).
    ^TIME: set current time.
    ";
#EndIf;

Option Hint_dragon "How can I kill the red dragon?"
 class Hintobj
 with in_menu Hints,
 the_hints
  "He's allergic to cherries."
  "You could try THROW CHERRIES AT DRAGON."
  "Of course, there are no cherries."
  "There's also no dragon."
  "Don't read hints for problems you're not facing---they'll spoil the game."
  ;

Menu HintExChurch "Exploring the church";

Option Hint_chantry "What is the purpose of the FitzAlan Chantry?"
 class Hintobj
 with in_menu HintExChurch,
 the_hints
  "Wealthy families sometimes bought private chapels where prayers would be
    for them."
  "They would also often have the right to be buried in the crypt."
  "Or even have a private crypt."
  "There is an entrance hidden to their private crypt."
  "Have you examined the altar carefully?"
  "The gouges might have come from moving the altar."
  "Have you tried doing anything with the family arms?"
  "You might need to get closer to them."
  "CLIMB ON ALTAR. PUSH LION. GO DOWN."
  "PUSH ALTAR."
;
Option Hint_gate "How can I open the crypt gate?"
 class Hintobj
 with in_menu HintExChurch,
 the_hints
  "With a key, of course."
  "Brother Oswald carries that key."
  "But that's a red herring---you'll never get them from him."
  "There must be another way into the crypt."
  "There is, in fact, another, private, crypt with a secret entrance."
  "Have you encountered a place funded by a long-lost wealthy family?"
  "Solve the challenge of the FitzAlan Chantry."
;
Option Hint_silence "Why can't I talk to the monks?"
 class Hintobj
 with in_menu Hints
 the_hints
  "Many monasteries have strict vows of silence at many times and places."
  "There are many places you'll never be able to talk to them."
  "Have you discovered a room designed for conversation?"
  "Visit the locutory."
  "It can be tricky to get a monk to visit, but you can help them."
  "Wait in the cloister by the locutory and POINT TO LOCUTORY."
  "That said, talking to the monks is not a big part of the game."
  ;
Option Hint_not_suspicious "Why can't I search the cots/chests/other things?"
  class Hintobj
  with in_menu Hints,
  the_hints
    "You're just a novice monk---you can't just pry into things for no reason."
    "Once you've established that Aelred's death was suspicious, you can."
  ;
Option Hint_jude "What can I do in the St Jude chapel?"
 class Hintobj
 with in_menu HintExChurch,
 the_hints
  "If you're desperate, you could try praying---he is the saint of
    desperate causes."
  "Your prayer, however, won't be answered in the game."
  "There isn't anything you *need* to do here."
  "But it might be helpful to notice the offering given to the saint."
  "What kind of berries are those?"
  "You've studied herbalism with Brother Aelred;
    what could you do with them to try to figure out what they are?"
  "Try SMELL BERRIES or TASTE BERRIES."
  "Rosehips, hmm? The final stage of decline for a rose.
    That might be useful to think on."
  ;

[ HintSub;
  if (hint_dragon.hints_seen == hint_dragon.#the_hints / 2) remove hint_dragon;

  Hints.select();
];

Verb meta 'hint' 'hints' * -> Hint;

