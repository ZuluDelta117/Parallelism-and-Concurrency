#include <cstdlib>
#include <iostream>
#include <pthread.h>
#include <stdio.h>
#include <sys/unistd.h>

#define NUM_THREADS 5

using namespace std;

struct thread_args
{
    int a;
    double b;
};

struct thread_result
{
    long x;
    double y;
};

void *thread_func(void *args_void)
{
    struct thread_args *args = (thread_args *)args_void;
    // The thread cannot return a pointer to a local variable
    struct thread_result *res = new thread_result;

    // C version of this:
    //struct thread_result *res = (thread_result *)malloc(sizeof *res);

    res->x  = 10 + args->a;
    res->y = args->a * args->b;
    return res;
}

void example2()
{
    cout << "*****************************************\n";
    cout << "Example 2 - returning values from threads\n";

    pthread_t threadL;
    struct thread_args in = { .a = 10, .b = 3.141592653 };
    void *out_void;
    struct thread_result *out;

    pthread_create(&threadL, NULL, thread_func, &in);
    pthread_join(threadL, &out_void);
    out = (struct thread_result *)out_void;
    cout << "x = " << out->x << "\ty = " << out->y << endl;
    free(out);

    cout << "Example 2 completed\n";
}

int main(void)
{
    example2();

    return 0;
}