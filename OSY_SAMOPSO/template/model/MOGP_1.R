library(laGP)

#get training data points
training_data <- read.csv("./model/input/trainingdata.csv")

#set training data for objectives
X <- cbind(X1 = training_data$x1, X2 = training_data$x2, X3 = training_data$x3, X4 = training_data$x4, X5 = training_data$x5, X6 = training_data$x6)

Y1 <- training_data$obj_1
Y2 <- training_data$obj_2

G1 <- training_data$g1
G2 <- training_data$g2
G3 <- training_data$g3
G4 <- training_data$g4
G5 <- training_data$g5
G6 <- training_data$g6

#get untried location
dv <- read.csv("./model/input/dv.dat", header=T)
Xref_obj <- matrix(unlist(dv),nrow=1)

#laGP appoximation
OBJ1.alc <- laGP(Xref_obj, 10, 60, X, Y1, d=NULL, method = "alc")
OBJ2.alc <- laGP(Xref_obj, 10, 60, X, Y2, d=NULL, method = "alc")

Xref1 <- matrix(unlist(dv[1:2,]),nrow=1)
G1.alc <- laGP(Xref1, 20, 60, X[,1:2], G1, d=NULL, method = "alc")
G2.alc <- laGP(Xref1, 20, 60, X[,1:2], G2, d=NULL, method = "alc")
G3.alc <- laGP(Xref1, 20, 60, X[,1:2], G3, d=NULL, method = "alc")
G4.alc <- laGP(Xref1, 20, 60, X[,1:2], G4, d=NULL, method = "alc")

Xref5 <- matrix(unlist(dv[3:4,]),nrow=1)
G5.alc <- laGP(Xref5, 20, 60, X[,3:4], G5, d=NULL, method = "alc")

Xref6 <- matrix(unlist(dv[5:6,]),nrow=1)
G6.alc <- laGP(Xref6, 20, 60, X[,5:6], G6, d=NULL, method = "alc")

# G1_s <- G1.alc$mean+2*sqrt(G1.alc$s2)
# G2_s <- G2.alc$mean+2*sqrt(G2.alc$s2)
# G3_s <- G3.alc$mean+2*sqrt(G3.alc$s2)
# G4_s <- G4.alc$mean+2*sqrt(G4.alc$s2)
# G5_s <- G5.alc$mean+2*sqrt(G5.alc$s2)
# G6_s <- G6.alc$mean+2*sqrt(G6.alc$s2)

Pf_g1 <- 1-pnorm(-G1.alc$mean/sqrt(G1.alc$s2))
Pf_g2 <- 1-pnorm(-G2.alc$mean/sqrt(G2.alc$s2))
Pf_g3 <- 1-pnorm(-G3.alc$mean/sqrt(G3.alc$s2))
Pf_g4 <- 1-pnorm(-G4.alc$mean/sqrt(G4.alc$s2))
Pf_g5 <- 1-pnorm(-G5.alc$mean/sqrt(G5.alc$s2))
Pf_g6 <- 1-pnorm(-G6.alc$mean/sqrt(G6.alc$s2))

g1 <- dv[1,1] + dv[2,1] -2
g2 <- 6 - dv[1,1] -dv[2,1]
g3 <- 2 - dv[2,1] + dv[1,1]
g4 <- 2 - dv[1,1] + 3*dv[2,1]

#save results to pass to MOU
objective <- c(OBJ1.alc$mean, OBJ2.alc$mean, sqrt(OBJ1.alc$s2), sqrt(OBJ2.alc$s2), 
               G1.alc$mean, G2.alc$mean, G3.alc$mean, G4.alc$mean, G5.alc$mean, G6.alc$mean, 
               Pf_g1, Pf_g2, Pf_g3, Pf_g4, Pf_g5, Pf_g6)

write.csv(objective, "./model/output/gp_output.dat", quote = F, row.names = F)