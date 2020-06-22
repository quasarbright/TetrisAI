time challenges:
* DAS
* auto repeat rate
* entry delay (ARE)
* stack locking
  * reset on rotation/shift
* falling
  * (variable) gravity speed
---
* for time, have an advanceFrame method and a registerInput method
  * have an input buffer queue that gets cleared each frame
  * execute all moves pending in buffer
* for holding/DAS, you can keep track of how long each input has been held
  * have a map from action/input to frameCount, initialize to zero
  * when going from 0 to 1 or when count > DAS and count % something == 0, do the input
    * need modulo bc you don't want to move once per frame
    * maybe just use the gravity system if you can (probably won't work)
  * set count to zero if input isn't currently held