dv <- read.csv("dv.dat")

x1 <- dv[1,1]
x2 <- dv[2,1]
x3 <- dv[3,1]

obj1<- 0
for (i in 1:2){
  obj <- -10*exp(-0.2*sqrt(dv[i,1]^2+dv[i+1,1]^2))
  obj1 <- obj1 + obj
}

obj2<- 0
for (i in 1:3){
  obj <- abs(dv[i,1])^0.8 + 5*sin((dv[i,1]^3))
  obj2 <- obj2 + obj
}

output <- c(obj1,obj2)
write.csv(output, "hf_output.dat", quote = F, row.names = F)
