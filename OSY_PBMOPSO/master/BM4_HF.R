dv <- read.csv("dv.dat")


f1 <- -25*(dv[1,1]-2)^2 - (dv[2,1]-2)^2 - (dv[3,1]-1)^2 - (dv[4,1]-4)^2 - (dv[5,1]-1)^2
f2<-0
for (i in 1:6){
  f2 <- f2 + dv[i,1]^2
}

obj1 <- f1
obj2 <- f2

g1 <- dv[1,1] + dv[2,1] -2
g2 <- 6 - dv[1,1] -dv[2,1]
g3 <- 2 - dv[2,1] + dv[1,1]
g4 <- 2 - dv[1,1] + 3*dv[2,1]
g5 <- 4 - (dv[3,1]-3)^2 - dv[4,1]
g6 <- (dv[5,1]-3)^2 + dv[6,1] -4

obj1sd <- 1e-3
obj2sd <- 1e-3
Pf_g1 <- 1
Pf_g2 <- 1
Pf_g3 <- 1
Pf_g4 <- 1
Pf_g5 <- 1
Pf_g6 <- 1

output <- c(obj1,obj2,obj1sd, obj2sd, g1,g2,g3,g4,g5,g6, 
            Pf_g1, Pf_g2, Pf_g3, Pf_g4, Pf_g5, Pf_g6)
write.csv(output, "hf_output.dat", quote = F, row.names = F)
