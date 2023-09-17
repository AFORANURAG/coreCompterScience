#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#define INITIAL_CAPACITY 10
struct Stack {
    int *arr;
    int top;
    int capacity;
};

void initialize(struct Stack *stack){
    stack->top = -1;
    stack->capacity = INITIAL_CAPACITY;
    stack->arr = (int *)malloc((stack->capacity)*sizeof(int));
    if(stack->arr==NULL){
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
}

bool isEmpty(struct Stack *stack){
    return (stack->top==-1);
}

void push(struct Stack *stack,int value){
if(stack->top==stack->capacity-1){
    stack->capacity*=2;
    stack->arr = (int*)realloc(stack->arr,stack->capacity*(sizeof(int)));
      if (stack->arr == NULL) {
            fprintf(stderr, "Memory reallocation failed\n");
            exit(1);
    }
}
stack->arr[++stack->top]=value;
}

int pop(struct Stack *stack){
    if(isEmpty(stack)){
 printf("Stack is empty\n");
        return -1; // Return an error value
    }
    return stack->arr[stack->top--];
}

int peek(struct Stack *stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty\n");
        return -1; // Return an error value
    }
    return stack->arr[stack->top];
}

void freeStack(struct Stack *stack){
    free(stack->arr);
    stack->arr = NULL;
}

int main(){
    struct Stack stack;
    initialize(&stack);
     for (int i = 1; i <= 20; i++) {
        push(&stack, i);
    }

    printf("Popping elements from the stack: ");
    while (!isEmpty(&stack)) {
        printf("%d ", pop(&stack));
    }
    printf("\n");

    freeStack(&stack);

    return 0;

}