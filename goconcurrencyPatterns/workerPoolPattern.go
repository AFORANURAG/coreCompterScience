package main

import ("fmt")
func main(){
fmt.Println("Hello world in golang")
jobs:=make(chan int ,100)
results:=make(chan int,100)
for i:=0;i<5;i++{
	go worker(jobs,results)
}
for i:=0;i<100;i++{
	jobs <- i
}
close(jobs)

for result:= range results{
	fmt.Println(result)
}
}

func worker(jobs <-chan int,results chan<- int){
	for n:=range jobs{
      results<-doFib(n)
	}
}
func doFib(n int)int {
	if n<=1 {
		return n
	}

	return doFib(n-1)+doFib(n-2)
}