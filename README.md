###  A Collection of Python Projects 

- **Data Analysis**
  - Tutorial on data analysis using python, Panda library and so forth
- **SAT Algorithms**
  - Examples of boolean satisfiability (SAT) Algorithms: Davis–Putnam–Logemann–Loveland (DPLL) algorithm, walk SAT, greedy SAT.
- **Search Algorithms**
  - Examples of Search Algorithms
- **Face Detection**
  - Project Face Detection from OpenCV
- **Keras Programming**
  - Projects on Keras that I'm applying to learn to use it
- **PyGame Project**
  - Project of PyGame to learn how to do a game using python


# ISR/Vislab servers - including IST server as well
## connect to IST server
```
ssh -i Downloads/Nuno.pem -4 ubuntu@nuno.gpccu.tp.vps.tecnico.ulisboa.pt
```
You need to have Nuno.pem file which is private key

## tensorboard remote (IST server)
open terminal (local machine) and open ip address
```
ssh -N -f -L localhost:16006:localhost:6006 -i Downloads/Nuno.pem -4 ubuntu@nuno.gpccu.tp.vps.tecnico.ulisboa.pt
```
open terminal (ist server)
```
tensorboard --logdir ./assets/log --port 6006
```
open browser at  ```http://localhost:16006/```
