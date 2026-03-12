| Action        | #  | Example               | Notes                         |
|---------------|----|-----------------------|-------------------------------|
| **All**       |                                                            |
| Drop          | 2  | DROP *n*              |                               |
| Examine       | 2  | EXAMINE *n*           |                               |
| Search        | 2  | SEARCH *n*            |                               |
| Take          | 2  | TAKE *n*              |                               |
| **Books**                                                                  |
| Consult       | 3  | CONSULT *n* ABOUT *t* |                               |
| **Change**                                                                 |
| Attack        | 3  | ATTACK *n*            | Life                          |
| Burn          | 3! | BURN *n*              |                               |
| Cut           | 3  | CUT *n*               |                               |
| Pull          | 3! | PULL *n*              |                               |
| Push          | 3  | PUSH *n*              |                               |
| Rub           | 3  | RUB *n*               |                               |
| Swing         | 3! | SWING *n*             |                               |
| Squeeze       | 3! | SQUEEZE *n*           |                               |
| ThrowAt       | 3  | THROW *n* AT *s*      | Life for s, Takes noun        |
| Tie           | 3  | TIE *n* TO *s*        |                               |
| Turn          | 3  | TURN *n*              |                               |
| **Clothes**                                                                |
| Disrobe       | 2  | TAKE OFF *n*          |                               |
| Wear          | 2  | WEAR *n*              |                               |
| **Communicate**                                                            |
| Ask           | 3  | ASK *n* ABOUT *t*     | Life                          |
| Answer        | 3  | SAY *t* TO *n*        | Life                          |
| Give          | 3  | GIVE *n* TO *s*       | Life                          |
| Kiss          | 3! | KISS *n*              | Life                          |
| Shout         | 3  | SHOUT *t*             |                               |
| ShoutAt       | 3  | SHOUT AT *n*          |                               |
| Show          | 3  | SHOW *n* TO *s*       | Life                          |
| Tell          | 3  | TELL *n* ABOUT *t*    | Life                          |
| WaveHands     | 3! | WAVE                  |                               |
| **Containers**                                                             |
| Close         | 2  | CLOSE *n*             |                               |
| Empty         | 2! | EMPTY *n*             |                               |
| EmptyT        | 2! | EMPTY *n* INTO *s*    |                               |
| Enter         | 2  | ENTER *n*             |                               |
| Exit          | 2  | EXIT *n*              |                               |
| Fill          | 2  | FILL *n*              |                               |
| GetOff        | 2  | GET OFF *n*           | Then tries Exit               |
| Insert        | 2  | INSERT *n* INTO *s*   | First, takes                  |
| Open          | 2  | OPEN *n*              |                               |
| PutOn         | 2  | PUT *n* ON *s*        |                               |
| Remove        | 2  | REMOVE *n* FROM *s*   |                               |
| Transfer      | 2  | TRANSFER *n* TO *s*   |                               |
| **Doors**                                                                  |
| Lock          | 2  | LOCK *n* WITH *s*     |                               |
| Unlock        | 2  | UNLOCK *n* WITH *s*   |                               |
| **Edible**                                                                 |
| Drink         | 3  | DRINK *n*             |                               |
| Eat           | 2  | EAT *n*               |                               |
| **General**                                                                |
| Inv           | 2  | INVENTORY             |                               |
| Look          | 2  | LOOK                  |                               |
| Wait          | 2  | WAIT                  |                               |
| **Movement**                                                               |
| Climb         | 3  | CLIMB *n*             | Does not get on supporter     |
| Enter         | 2  | ENTER *n*             |                               |
| Exit          | 2  | EXIT                  |                               |
| GoIn          | 2! | IN                    |                               |
| Jump          | 3  | JUMP                  |                               |
| JumpOver      | 3  | JUMP OVER *n*         |                               |
| Go            | 2  | GO NORTH              |                               |
| PushDir       | 3  | PUSH *n* NORTH        | Don't need to check           |
| **On/Off**                                                                 |
| Set           | 3! | SET *n*               |                               |
| SetTo         | 3! | SET *n* TO *s*        |                               |
| SwitchOn      | 2  | SWITCH ON *n*         |                               |
| SwitchOff     | 2  | SWITCH OFF *n*        |                               |
| **Orders**                                                                 |
| AskFor        | 3  | ASK *n* FOR *s*       | orders then life. No before.  |
| AskTo         | 3  | ASK *n* TO *t*        | orders then life. No before.  |
| **Senses**                                                                 |
| Listen        | 3  | LISTEN                |                               |
| Smell         | 3  | SMELL *n*             |                               |
| Taste         | 3! | TASTE *n*             |                               |
| Touch         | 3  | TOUCH *n*             |                               |
| **Sleep**                                                                  |
| Sleep         | 3! | SLEEP                 |                               |
| Wake          | 3! | WAKE                  |                               |
| WakeOther     | 3! | WAKE *n*              | Life                          |
| **Misc**                                                                   |
| Blow          | 3! | BLOW *n*              | Takes first                   |
| Buy           | 3! | BUY *n*               |                               |
| Dig           | 3  | DIG *n*               |                               |
| Pray          | 3! | PRAY                  |                               |
| Sing          | 3! | SING                  |                               |
| Swim          | 3! | SWIM                  |                               |
| Wave          | 3! | WAVE *n*              |                               |
| **Misc Solo**                                                              |
| Sorry         | 3! | SORRY                 |                               |
| Think         | 3! | THINK                 |                               |
| Yes           | 3! | YES                   |                               |
| No            | 3! | NO                    |                               |
| Mild          | 3! | BOTHER                |                               |
| Strong        | 3! | DAMN                  |                               |

Orders, like `bob, wave` use `orders` and `life` (no `pre` or `before`)

### Fake Actions

| Fake Action   | Sent to                                                    |
|---------------|------------------------------------------------------------|
| Going         | before to room: player about to enter                      |
| LetGo         | container/supporter: player takes from it                  |
| NotUnderstood | creature's orders: player issued incomprehensible order    |
| Order         | creature's life: order given but not handled in orders     |
| PluralFound   |                                                            |
| Receive       | container/supporter: player tries to put in/on             |
| ThrownAt      | target noun: player tried to throw at it                   |
