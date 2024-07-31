dv <- read.csv("dv.dat")


f1 <- dv[1,1]

gx <- 1
for (i in 2:30){
  x <- dv[i,1]
  gx <- gx + (9/29)*x
}

hx = 1-(f1/gx)^2

f2 <- gx*hx

obj1 <- f1
obj2 <- f2
obj1sd <- 0
obj2sd <- 0

output <- c(obj1,obj2, obj1sd, obj2sd, obj1, obj1)
write.csv(output, "hf_output.dat", quote = F, row.names = F)
