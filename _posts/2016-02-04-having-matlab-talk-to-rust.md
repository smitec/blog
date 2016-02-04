---
layout: post
title:  "Having Matlab Talk to Rust"
date:   4-2-2016 14:42:31
categories: rust matlab mex
---
As part of my PhD I write a lot of Matlab. 
I am not particularly fond of Matlab but because I need to collaborate and work
on older code bases I don't have much choice in the matter.
All that aside sometimes in Matlab you'll find that things can get a little slow.
In my field of computational electrodynamics this is typically around the time
we need to calculate a matrix of inductance contributions with 100 million elements.
Because code like this is hard to vectorise we tend to write code in other languages
like C to speed up that section of code. In Matlab land this is typically referred
to as writing a Mex file. Mex files can be written in C, C++, Fortran and possibly
others. As a fan of Rust I wanted to see what I could do to get Rust and Matlab
talking to one another. It took some time to work out how it could all fit together
but I have ported one of the older C Mex files to Rust and successfully linked them
to Matlab. While I can't share the specifics of that code here I will work through
a working example of sending data from Matlab to Rust and back again. Let's get 
started.

## My Setup
Just in case something falls apart with updates this is my current setup:

- Matlab R2015b
- Mac OSX 10.11.3
- rustc 1.5.0
- cargo 0.7.0

## Step 1 - Writing a static library in Rust
This step is fairly well documented but for completeness I will start from the 
beginning. I assume you have all of the components above installed and Matlab 
knows what C compiler you will be using.

So let's create an empty Rust project.

{% highlight bash %}
cargo new rustlab
cd rustlab
{% endhighlight %}

Open up your `Cargo.toml` file and add the following lines to the end.

```
[dependencies]
libc="0.2.4"

[lib]
name="rustlab"
crate-type=["staticlib"]
```

We ask for `libc` so we can send data between Matlab and Rust, we also declare this project as a library and say we want to build a static library. As it stands we need to create a static library which will be linked to a C file which wraps the Matlab Mex calling interface, more on that later.

Now to write our functions. In this example we will be writing a function which takes two vectors and does an element wise multiplication on their elements. Something Matlab already does, and does quickly, but enough of an example to show the process of getting data sent both ways.

In our Rust code we will be writing two functions. 
One, which we will call `multiply_safe` is where we will use only Rust variables and do the actual computation. 
The other `multiply` will be a wrapper, and our interface to C which takes C types, populates Rust variables with them, calls our `multiply_safe` function and then passes the result back as a C type. 
This way we keep our Rust code and glue separate as much as possible. 
Allowing us to test our Rust code on it's own without having to set up all the glue each time.

## Step 2 - A simple function

So let's get going with implementing `multiply_safe` and writing a simple test to ensure it is doing what we want.

First open up lib.rs and add the following function to the file:

{% highlight rust %}

fn multiply_safe(a : Vec<f64>, b : Vec<f64>) -> Vec<f64> {
    if a.len() != b.len() {
        panic!("The two vectors differ in length!");
    }

    let mut result : Vec<f64> = vec![0f64; a.len()];
    
    for i in 0..a.len() {
        result[i] = a[i]*b[i];
    }

    return result;
}

{% endhighlight %}

Nice and simple, there should be no surprises here. Because it is good practice we will also write a test to ensure the results are indeed what we expect. Edit the default `it_works` test to look like the following:

{% highlight rust %}
#[test]
fn it_works() {
    let a : Vec<f64> = vec![1f64, 2f64, 3f64];
    let b : Vec<f64> = vec![3f64, 2f64, 1f64];
    let c : Vec<f64> = multiply_safe(a, b);
    let expected : Vec<f64> = vec![3f64, 4f64, 3f64];

    assert!(c.len() == expected.len());
    
    for i in 0..c.len() {
        assert!(c[i] == expected[i]);
    }
}

{% endhighlight %}

Now if you run `cargo test` you should see our test passing. The other thing we now have is a file called `librustlab.a` in the `target/debug` folder. It wont do anything right now because we haven't written the `multiply` function but this is were our library will end up.

## Step 3 - A C wrapper

Now let's look at the function that makes the link between C and Rust. As I mentioned before we will be writing a C file which acts as a middleman between Matlab and Rust. This is clearly not ideal but in currently it appears to be the most straightforward way to get things working.

Before we write this new function lets add the `libc` requirements to the top of the file.

{% highlight rust %}
extern crate libc;
use libc::{c_double, c_long};
{% endhighlight %}

The C function will be passing us double pointers so we use rust's c_double
type and c_long to pass the length of the two arrays. Next to create our exported function add the following.

{% highlight rust %}
#[no_mangle]
pub extern fn multiply(a_double : *mut c_double, 
                    b_double : *mut c_double, 
                    c_double : *mut c_double,
                    elements : c_long) {
    
    let size : usize = elements as usize;
    let mut a : Vec<f64> = vec![0f64; size];
    let mut b : Vec<f64> = vec![0f64; size];

    for i in 0..size {
        unsafe {
            a[i] = *(a_double.offset(i as isize)) as f64;
            b[i] = *(b_double.offset(i as isize)) as f64;
        }
    }

    let c : Vec<f64> = multiply_safe(a, b);

    for i in 0..size {
        unsafe {
            *c_double.offset(i as isize) = c[i];
        }
    }
}
{% endhighlight %}

Some things to note here. First up `#[no_mangle]` this tells rust to keep the 
function name the same so we can link to it, typically it gets mangled to 
reduce the risk of two things having the same name. Next `pub extern` is needed
to make sure the function is publicly exported. The last thing worth noting is
the `unsafe` block. We use one of these to mark where potentially unsafe things
might happen (like dereferencing pointers). Hopefully the rest of the function
is clear enough. Build the code again and we will move on to writing the final
piece of the puzzle.

## Part 4 - Some C code
Create a new file `rustlab.c` and add the following code. If you have used the
mex interface before it should be pretty straightforward.

{% highlight c %}
#include "mex.h"

// Multiplies a and b element wise, and puts the result in c
extern void multiply(double* a, double* b, double* c, long elements);

void mexFunction(int nlhs, mxArray *plhs[], 
        int nrhs, const mxArray *prhs[]) {
    double* a;
    double* b;
    double* c;

    mwSize elements;

    if (nrhs != 2) {
        mexErrMsgTxt("Wrong number of input args");
    }

    if (nlhs != 1) {
        mexErrMsgTxt("Wrong number of output args");
    }

    a = mxGetPr(prhs[0]);
    b = mxGetPr(prhs[1]);
    elements = mxGetM(prhs[0]);

    plhs[0] = mxCreateDoubleMatrix(elements, 1, mxREAL);
    c = mxGetPr(plhs[0]);

    multiply(a, b, c, elements);
}
{% endhighlight %}

Now that both of these are done, open up Matlab and move to a folder that 
contains both `librustlab.a` and `rustlab.c`. While in Matlab run the following.

{% highlight matlab %}
mex rustlab.c librustlab.a
a = 1:10;
c = rustlab(a', a');
disp(c);
{% endhighlight %}

Woohoo! You did it. Hopefully this made things clear and helps in some way. 
While I am probably not considered an expert in rust I am happy to help out
if you get in touch with me via twitter [@smitec][tw].

I plan over time to move more of my mex files to Rust. It offers a lot in terms
of safety and high level concepts that can be more difficult to achieve in C.

All of the code related to this post is available on Github: [rustlab][rl] and
so if things are broken on your system feel free to post an issue or pull request.


[tw]: https://twitter.com/smitec
[rl]: https://github.com/smitec/rustlab
