---
layout: post
title: "Matrix Derivatives"
date: 2025-12-3
categories: blog
---

Recently, I've been finding myself trying to calculate the derivative a functions with respect to a matrix. Many papers I've passed by include matrix derivatives that seem to have come out of thin air, without any justification or proof at all! This made me think: I must have missed this all-important class in my undergrad or early graduate life that's left me without this basic tools for solving matrix derivatives.

It turns out, I was around 30% correct. This doesn't seem to be something that people universally get taught in a class. Instead, people derive them with such ease that they don't feel the need to write out their process, they use a wonderful collection of rules called the [Matrix Cookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf), or something similar. 

This blog will be dedicated to understanding matrix calculus better. For both you and me, I'd like to give some intuition on how these rules work (rather than simply stating the rule in the matrix cookbook). I'll then go into some of my own attempts at making a workable calculus of matrices that, importantly, makes the chain rule a simple operation to work with. With this, we will work through the derivatives of important functions, some simple, and others useful in the realm of machine learning.

I will expect a decent background in multivariate calculus.

## First Steps

Let's review some simple multivariate/vector calculus. Most commonly, we have functions $f:\mathbb{R}^n \rightarrow \mathbb{R}$. Partial derivatives can be taken of this function in any of the coordinate directions $x_1$:

$$
\partial_{x_i} f:\mathbb{R}^n \rightarrow \mathbb{R}.
$$

We can collect these into a vector called the gradient:

$$
\partial_x f^\top =: \nabla f:\mathbb{R}^n \rightarrow \mathbb{R}^n.
$$

This object gives us full knowledge of the first-order structure of $f$. 

More generally, we can have $f:\mathbb{R}^n \rightarrow \mathbb{R}^m$. We still can take partial derivatives, but now these will be vector valued:

$$
\partial_{x_i} f: \mathbb{R}^n \rightarrow \mathbb{R}^m.
$$

Collecting these into one object gives us a matrix:

$$
\partial_x f =: J_f: \mathbb{R}^n \rightarrow \mathbb{R}^{n,m}.
$$

where 

$$
(J_f)_{i,j} = \partial_{x_j}f_i.
$$ 

This again describes the complete first-order behavior of $f$.

For a very simple example, consider

$$
f(x) = Wx.
$$

The Jacobian is then the very simple

$$
J_f = W.
$$

There's also the beautiful property, the chain-rule, for taking the Jacobian of $f\circ g$. It says

$$
J_{f\circ g}(x) = J_{f}(g(x))J_{g}(x).
$$

This is arguably the most powerful of all of the differentiation rules since most applications involve nested function applications, many times deeper than just two. This, along with the other common rules in calculus, allow us to compute derivatives of much more complex functions without going all the way back to the definition of the derivative.

### Matrix Derivatives

Notice that everything until now works with the input being a scalar/vector and the output being a scalar/vector. However, there are just as many uses for functions which take matrices as input! 

For instance, we can have

$$
f(W) = Wx.
$$

It's the same function, just with a different choice of variable! Notice that this is a function that takes a matrix and outputs a vector. This will require a kind of 3-dimensional tensor of information to fully describe. Let's start simple with the cases that still only require 2-dimensions of information so they can be stores in a matrix.

The first of these cases will be a scalar-valued function with a matrix input. For example,

$$
f(X) = \text{Tr}(X).
$$

We can take partial derivatives w.r.t. each of the coordinates of $X$:

$$
\partial_{X_{i,j}}f = \delta_{i,j}.
$$

These can then be collected into a matrix as

$$
\partial_X f = I.
$$

It's a bit strange to call this the identity matrix though. It won't ever be used as an identity matrix, either by the chain-rule discussed later, or in finding first-order Taylor approximations. It should be thought of more as 1's on the diagonal, 0's elsewhere, and will be used with each coordinate separately.

The second case is some parametric matrix-valued function, like

$$
f(t) = tAB.
$$

For this, we can simply take the derivative w.r.t. the parameter $t$ and get a matrix of derivatives:

$$
\partial_t f = AB.
$$

Functions of this form won't be of much interest to us, and often has much simpler calculations since derivatives happen only to scalars outside of matrix operations (usually).

## Good Resources

Especially for these last two cases when trying to find matrix-related derivatives, I found a few good resources to lookup solutions to simple forms of the above.

### [The Matrix Cookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)

This is a wonderful reference for anyone using matrix derivatives. It provides a nicely detailed list of properties, many coming from [here](https://tminka.github.io/papers/matrix/minka-matrix.pdf), a paper describing the properties of differentials useful for statistics. Most of these focus on finding the derivative of a scalar function w.r.t. matrix. For example, let's take the derivative of 

$$
f(A) = \|AB\|_F^2,
$$

where the Frobenius norm squared takes all of the elements of $AB$, squares them, and sums them. Using the rules from the Matrix Cookbook (specifically rule 111), we have


$$
\begin{align}

\partial_A f &= \partial_A \text{Tr}(ABB^\top A^\top), \\
&= A(BB^\top)^\top + ABB^\top, \\
&= 2(AB)B^\top.

\end{align}
$$


That wasn't too bad! But it does show us something important: our typical intuition for chain-rule doesn't work with matrices. The constant factor next to $A$ comes out transposed. 

Similarly, we could calculate (with rule 110):

$$
\begin{align}

\partial_B f &= \partial_B \text{Tr}(ABB^\top A^\top), \\
&= \partial_B \text{Tr}(BB^\top A^\top A), \\
&= A^\top A B + (A^\top A)^\top B, \\
&= 2A^\top (AB).

\end{align}
$$


Now we can also see that the location of where the 'chain rule' factor appears depends on its location inside the inner function! 

<div class="red-box">
Be careful when trying to do things like chain rule with matrices! They have strange properties, partially from multiplication being non-commutative, that will make quick intuitions misleading.
</div>

This reference also contains lots of auxiliary information about matrices, and even investigates derivatives of other matrix objects, such as inverses and eigenvalues. At the time of writing this, I wasn't as interested in using these properties, so they won't be focused on, but I'm sure I'll be referencing this document at some point in the future.

To note, the Matrix Cookbook does include a section on the chain-rule, but in many ways I find it surprisingly short for something that would be so powerful. It's brevity also misses showing the reader how different that 4-tensor is from the other linear algebra in the cookbook. Hopefully I didn't miss something clever in their notation!

### [Wikipedia](https://en.wikipedia.org/wiki/Matrix_calculus)

While not always the best source of information, the page on matrix calculus seems pretty good! In many ways, it just summarizes the above cookbook and its related papers. I especially like their treatment of differentiating a matrix w.r.t. a scalar. They also describe derivatives in differential form notation, which I find more appealing, even though I won't be using it much here.

### [Sourya Dey's Notes](https://souryadey.github.io/teaching/material/Matrix_Calculus.pdf)

This one is very interesting, especially since it partially validated my belief that matrix calculus is taught in a class. Let's look at these notes and see what else they can tell us. 

Everything until page 5 are ideas we've already looked at a bit. What's new are the vector-matrix and matrix-vector derivatives. And what an insight they have! They write their derivatives as a vector of matrices, or a matrix of vectors! 

Again, I've probably missed this as a concept (except when used in quantum field theory, which I know about as well as anyone who doesn't study physics), but it's such a powerful one that I'm surprised I have. In many ways, it gives us a way to still use linear algebra when working with these very involved 4-tensors! 

Let's work out the one example from these notes. The way the matrix derivative works is each position in the derivative is a matrix, which is the partial derivative of the corresponding coordinate in $A$. 

What is $\partial_A A$? We can write this component-wise by

$$
(\partial_A A)_{i,j} = e_{j,i},
$$

where $e_{i,j}$ is the matrix with a 1 in the $i,j$ position and 0 elsewhere. It may seem weird that these indices are reversed, but they have to be for the Jacobian to make sense! Note that $\partial_x x$ is a row-vector, so to make a matrix, these have to be stacked vertically, hence the indices need to be flipped.

To make this more concrete, imagine $A$ is a $2 \times 2$ matrix. Then,

$$
\partial_A A = \begin{bmatrix}
\begin{bmatrix}1 & 0 \\ 0 & 0 \end{bmatrix} & \begin{bmatrix} 0 & 0 \\ 1 & 0 \end{bmatrix} \\
\begin{bmatrix}0 & 1 \\ 0 & 0 \end{bmatrix} & \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix} \\
\end{bmatrix}.
$$

<div class="red-box">
Warning: This will not be the same derivative as described in the 4-tensor section.
</div>

What's the use of such a structure? Let's imagine we want to take a first-order approximation of $f(A) = A$ (kinda silly, but go with me). Then the first-order Taylor approximation would be

$$
f(A + E) \approx f(A) + \langle \partial_A f(A)^\top, E\rangle = A + E.
$$

This matrix $\partial_A A$ is an identity tensor! It seems weird where the 1's are placed intuitively, but it works out perfectly!

Wait, what's $\langle \cdot, \cdot\rangle$? This is the Frobenius inner product, where

$$
\langle A, B\rangle = \sum_{i,j} A_{i,j}B_{i,j}.
$$

It's the matrix version of the inner-product we see in the vector-valued Taylor expansion.

Something is a bit off about this though, as was already pointed out. It has all of the gradient information, but to do anything more complex with it (such as chain rule), you'll find that everything is Kronecker products and Frobenius inner products. There also will be some weird sums that hang around.

## 4-Tensor Linear Algebra

This form of a matrix of scalar derivatives works, but might there be a different, cleaner form? Something where chain-rule becomes a familiar operation?

#### Notation

Before we begin, some pieces of notation should be mentioned. Let $M$ be a matrix. 

The vector $M_i$ will be the $i$-th column of $M$ rather than the $i$-th row. If the row needs to be identified, that will be identified with $M_{i,:}$, to clean up notation.

The matrix can be tensored into $M_T$, where 

$$
(M_T)_{1,J,1,j} := M_{j,J}.
$$ 

There also will be an associated matrixing operation of a tensor $T$ with shape $(1,n,1,m)$, denoted as $T_M$ where 

$$
(T_M)_{j,J} = T_{1,J,1,j}.
$$ 

Clearly these operations are inverses:

$$
(A_T)_M = A \qquad (A_M)_T = A.
$$

This will be such a natural operation that many times the subscript denoting that we are performing one of these operations will be omitted. This is especially true in cases where we multiply a tensor by a matrix. For example, if $T$ is a tensor and $M$ is a matrix, their product is defined as

$$
TM := T(M_T).
$$

At any time, if the phrase "in matrix form" is used, it means to make the tensor into a matrix. For example, the matrix form of $TM$ above is $(TM)_M$. 

These two operators will let us move to and from tensor space to do some multi-linear algebra before converting back into a matrix.

#### Chain Rule

So, is there a nice form for 4-tensors? It turns out, yes there is! Let 

<div class="green-box">
$$
(\partial_{A} f)_{I,J,i,j} = \partial_{A_{j,J}}f_{i,I}
$$
</div>

This will be so important that it deserves it's own green background. In this form, we can define a (fairly natural) notation of composition. Let $T,U$ be 4-tensors which are each a matrix of matrices. Their product is

$$
(TU)_{I,K} = \sum_J T_{I,J}U_{J,K}
$$

where each of these components is a matrix and the elements of the sum are matrix multiplications. Written in sub-coordinates, we have

$$
(TU)_{I,K,i,k} = \sum_{J,j} T_{I,J,i,j}U_{J,K,j,k},
$$

It's nested matrix multiplication! Now, applying the chain-rule, we have


$$
\begin{align}

(\partial_{A} (f \circ g))_{I,K,i,k} &= \partial_{A_{k,K}} (f \circ g)_{i,I}, \\
&= \sum_{J,j} (\partial_{A_{j,J}} f)_{i,I}(g(A)) (\partial_{A_{k,K}} g)_{j,J}(A), \\
&= \sum_{J,j} (\partial_{A} f)_{I,J,i,j}(g(A)) (\partial_{A} g)_{J,K,j,k}(A),

\end{align}
$$


so,

<div class="green-box">
$$
\partial_A (f \circ g) = (\partial_A f)(\partial_A g)
$$
</div>

as a 4-tensor product. 

<div class="blue-box">
The product of two tensors $TU$, denoted with no multiplication symbol, will be the nested matrix product of them, to make the notation of the chain-rule as clean as possible.
</div>

#### Taylor Approximation

How do we then use this tensor-derivative for first-order approximation now? We now need to do something special to our perturbation matrix $E$. Let $E_i$ denote the i-th column of $E$. 

Further, define $E_T$ as the tensor-ed version of $E$ by stacking the $E_i$ into on big column vector of column vectors. This will be such a common transformation to and from this form that the subscript $T$ for tensor will frequently be omitted. Look back at the **Notation** section for more information.

In this tensored form, a first order Taylor approximation will have the form

$$
f(A+E) \approx f(A) + (\partial_A f) E_T,
$$

where $\partial_A f$ is our new favorite 4-tensor derivative. Not quite as elegant as one might hope, but it's still pretty good!

#### Product Rule

With matrices, there are many notions of product. None is more versatile and wide-spread as the standard matrix product. It pops up everywhere in linear algebra.

What does it's tensor derivative look like? Let $g,h: \mathbb{R}^{n \times n} \rightarrow \mathbb{R}^{n\times n}$ and let $f(A) = g(A)h(A)$ where this is a standard matrix product. Using the definition of the tensor derivative, we find that


$$
\begin{align}

(\partial_{A}f)_{I,J,i,j} &= \partial_{A_{j,J}}f_{i,I}, \\
&= \partial_{A_{j,J}} \sum_\iota g_{i,\iota} h_{\iota, I}, \\
&= \sum_\iota (\partial_{A_{j,J}} g_{i,\iota}) h_{\iota, I} + g_{i,\iota} (\partial_{A_{j,J}} h_{\iota, I}), \\
&= \sum_\iota (\partial_{A} g)_{\iota,J,i,j} h_{\iota, I} + g_{i,\iota} (\partial_A h)_{I,J,\iota,j}. \\

\end{align}
$$


Great! This looks like a product rule! Except, there's something unfortunately weird about it... The left and the right terms are very, *very* different. The left term interacts with the output indices while the right term interacts with the inner indices. In hindsight, this isn't too surprising. Multiplying on the right and on the left by a matrix has very different forms. This does mean that we need two different notions of products of a matrix with a tensor. 

Let's first define the ***outside product***. For this product, imagine $T$ as a matrix, with coordinates $T_{i,j}$ all matrices. The outside product of a matrix and this tensor is

$$
(M\times_o T)_{I,K} = \sum_J M_{I,J} T_{J,K}.
$$

It's just a matrix product where the latter matrix has matrix coordinates. 

Now, for the ***inside product***, we look at each coordinate matrix separately. We write

$$
(M\times_i T)_{I,J} = MT_{I,J}.
$$

This feels more natural, since it's just standard matrix multiplication.

With these two nice products defined, we can simplify the product rule as 

<div class="green-box">
$$
\partial_A f = h^\top \times_o (\partial_A g) + g \times_i (\partial_A h)
$$
</div>

Wonderful! All it took was two new notions of products, both of which aren't that difficult to calculate! 

### Chain Rule for Different Shapes

We still will be interested in operations like those in the Matrix Cookbook. That is, we'll be interested in functions which take a matrix as input and a scalar as an output. What will the chain-rule look like when we have a composition $f(g(A))$, where $g$ is matrix valued and $f$ is scalar valued? 

First, we need to think of $f$ as a $1 \times 1$ matrix. The tensor derivative of $f$ will be

$$
(\partial_A f)_{1,J,1,j} = \partial_{A_{j,J}}f_{1,1}.
$$

This is like the tensoring operation $A_T$ above, but it's double-transposed, once on the inner coordinates and once on the outer coordinates. To make a simple notation for this, define 

$$
((A_T)^\top)_{1,J,1,j} = A_{j,J},
$$

so that

$$
(\partial_A f)_{1,J,1,j} = ((\partial_{A_{j,J}}f)_T)^\top.
$$

This object will be a row vector of row vectors, with each sub-vector being the transpose of a column of the original matrix.

## Some Simple Applications

#### Identity

Just to check that everything works somewhat as expected, let's first take the derivative of the identity:

$$
f(A)=A.
$$

It's derivative will be

$$
(\partial_A f)_{I,J,i,j} = \partial_{A_{j,J}}A_{i,I} = \delta_{ij}\delta_{IJ}.
$$

In matrix notation,

$$
\partial_A f = \begin{bmatrix}
I & 0 & \dots & 0 \\
0 & I & \dots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \dots & I \\
\end{bmatrix}.
$$

That sure looks like the identity! In fact, it will be tensor identity under the nested matrix product.

#### Transposition

What if

$$
f(A) = A^\top?
$$

Then the derivative will be

$$
(\partial_A f)_{I,J, i, j} = \partial_{A_{j,J}}A^\top_{i,I} = \delta_{iJ}\delta_{Ij}.
$$

This isn't as nice... In fact, we can write it in coordinates as

$$
(\partial_A f)_{I,J} = e_{J,I} = e_J e_I^\top.
$$

This means that every element of $\partial_A f$ is a non-zero matrix. Unfortunately, we'll have to accept this form for the chain-rule to behave nicely. Thankfully, it will only be used here in a single case.

#### Left Matrix Multiplication

How about something more complex, like

$$
f(A) = WA"
$$

The derivative will be

$$
\partial_A f = \begin{bmatrix}
W & 0 & \dots & 0 \\
0 & W & \dots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \dots & W \\
\end{bmatrix}.
$$

Beautiful! 

#### Right Matrix Multiplication

How about the uglier

$$
f(A) = AW?
$$

Each coordinate matrix will be

$$
(\partial_A f)_{I,J} = W_{J,I} I,
$$

where that last $I$ is the identity matrix. For the identity tensor $I_t$, it's possible to write this as

$$
\partial_A f = W^\top \times_i I_t.
$$

Still pretty cool! Even though it's not as clean.

#### Column-wise Operations

What if 

$$
f(A)_i = h(A_i),
$$

where subscripts denote the different columns of $f(A)$ and $A$? The coordinate matrices will be

$$
(\partial_A f)_{I,J} = \delta_{IJ} J_h(A_i),
$$

where $J_h(A_i)$ is the standard Jacobian of $h$! So this is a diagonal matrix with diagonal elements equal to the Jacobian of the column-wise operation. 

#### The Trace

How about a scalar valued function! Let

$$
g(A) = \text{Tr}(A) = \sum_i A_{i,i}.
$$

The derivative will be

$$
(\partial_A g)_{1,J} = e_J^\top,
$$

where $e_J$ is the standard basis element. If we put this in matrix form, we get back the standard matrix derivative $\frac{\partial g}{\partial A} = I$.

#### A Matrix Squared

For something a bit more involved, let 

$$
f(A) = A^2.
$$

Let's try and use the product rule here! This would mean that


$$
\begin{align}

\partial_A f &= A^\top \times_o \partial_A A + A \times_i \partial_A A, \\
&= A^\top \times_o I + A \times_i I.

\end{align}
$$


Looking at this coordinate-wise,

$$
(\partial_A f)_{I,J} = A_{J,I}I + \delta_{IJ} A.
$$

It's an interesting form no doubt! What's a good way to check that this agrees with what others have found before?

In the matrix cookbook, rule 106 states that $\frac{d}{dX}\text{Tr}(X^2) = 2X^\top$. Let's see if we can recover that!

We can write this as the composition of the two above functions:

$$
g(f(X)).
$$

By the chain-rule,


$$
\begin{align}

(\partial_A (g \circ f))_{1,K}(X) &= \sum_{J} (\partial_A g)_{1,J}(X^2) (\partial_A f)_{J,K}(X), \\
&= \sum_J X_{K,J} e_J^\top I + \delta_{JK} e_J^\top X, \\
&= \sum_J X_{K,J} e_J^\top + \delta_{JK} e_J^\top X, \\
&= X_K + X_K.

\end{align}
$$


So, each row vector component will be $2X_K$. In matrix form,

$$
\partial_A (g \circ f) = 2X.
$$

What happened to the transposition? Well, even in matrix form, $\partial_A f \not = \frac{\partial f}{\partial A}$. In fact, it's only wrong up to transposition, i.e.

$$
\frac{\partial f}{\partial A} = (\partial_A f)^\top.
$$

Why is this? Recall that

$$
(\partial_A f)_{1,J,1,j} = \partial_{A_{j,J}} f_{1,1},
$$

so in matrix form,

$$
(\partial_A f)_{J,j} = \partial_{A_{j,J}} f.
$$

The indices flipped! So, for the output we get of these tensor derivatives, when put into matrix form, they will be the transpose of the standard matrix derivative.

This was also true with the trace above, but since $I^\top = I$, we didn't see this behavior.

## More Interesting Applications

Let's now look at something much more interesting to machine-learning/language-modeling: Attention.

Denote attention as:

$$
f(X,W_V,W_Q,W_K) = W_V X \text{softmax}(X^\top W_Q^\top W_V X).
$$

This is much more complicated than all of the functions considered so far. Let's break it into pieces.

First, what is the derivative of softmax? Well, it's a column-wise operation so it will be matrix diagonal. For some input vector $x$, what is $\partial_x \text{softmax}(x)$? 

This has been calculated time and time again, but for completeness:


$$
\begin{align}

\partial_{x_j} \text{softmax}(x)_i &= \partial_{x_j} \frac{e^{x_i}}{\sum_k e^{x_k}}, \\
&= \delta_{ij} \frac{e^{x_i}}{\sum_k e^{x_k}} - \frac{e^{x_i}}{(\sum_k e^{x_k})^2}\partial_{x_j}(\sum_k e^{x_k}), \\
&= \delta_{ij} \frac{e^{x_i}}{\sum_k e^{x_k}} - \frac{e^{x_i}e^{x_j}}{(\sum_k e^{x_k})^2}. \\

\end{align}
$$


In matrix form, if we let $y = \text{softmax}(x)$, then

$$
\partial_x \text{softmax}(x) = \text{diag}(y) - yy^\top.
$$

Let's now look into the input of the softmax:

$$
g(X) = X^\top W_Q^\top W_V X.
$$

Using the product rule, 


$$
\begin{align}

\partial_A g &= (X^\top W_V^\top W_Q) \times_o (\partial_X X^\top) + X^\top \times_i (\partial_X W_Q^\top W_K X).

\end{align}
$$


In coordinates,


$$
\begin{align}

(\partial_A g)_{I,K} &= [\sum_J (X^\top W_V^\top W_Q)_{I,J} (\partial_X X^\top)_{J,K}] + [X^\top (\partial_X W_Q^\top W_K X)_{I,K}], \\
&= [\sum_J (X^\top W_V^\top W_Q)_{I,J} e_K e_J^\top] + [X^\top W_Q^\top W_K \delta_{I,K}I], \\
&= e_K [\sum_J (X^\top W_V^\top W_Q)_{I,J}  e_J^\top] + \delta_{I,K} X^\top W_Q^\top W_K, \\
&= e_K ((W_Q^\top W_K X)_I)^\top + \delta_{I,K} X^\top W_Q^\top W_K. \\

\end{align}
$$


Just to check, what is the associated first-order change of this? That will be


$$
\begin{align}

\sum_J (\partial_A g)_{IJ} E_J &= \sum_J e_J ((W_Q^\top W_K X)_I)^\top E_J + \sum_J \delta_{I,J} X^\top W_Q^\top W_K E_J, \\
&= \sum_J e_J E_J^\top (W_Q^\top W_K X)_I + X^\top W_Q^\top W_K E_I, \\
&= E^\top (W_Q^\top W_K X)_I + X^\top W_Q^\top W_K E_I. \\

\end{align}
$$


In matrix form:

$$
(\partial_X g)E_T = E^\top W_Q^\top W_K X + X^\top W_Q^\top W_K E.
$$

That's exactly what we'd expect! So far things look really good.

Let's do some chain-rule now. Let $A = X^\top W_Q^\top W_V X$ and $Y = \text{softmax}(A)$. What is $\partial_X Y$? By the chain-rule,


$$
\begin{align}

(\partial_X Y)_{I,K} &= \sum_J (\partial_A Y)_{I,J} (\partial_X A)_{J,K}, \\
&= \sum_J \delta_{I,J}( \text{diag}(Y_I) - Y_IY_I^\top)(e_K ((W_Q^\top W_K X)_J)^\top + \delta_{J,K} X^\top W_Q^\top W_K), \\
&= (\text{diag}(Y_I) - Y_IY_I^\top)(e_K ((W_Q^\top W_K X)_I)^\top + \delta_{I,K} X^\top W_Q^\top W_K).

\end{align}
$$


Finally, let $f(X) = W_V X Y$. For this derivative,

$$
\partial_X f = Y^\top \times_o (\partial_X (W_V X)) + W_V X \times_i (\partial_X Y).
$$

In coordinates


$$
\begin{align}

(\partial_X f)_{I,K} &= \sum_J Y_{J,I} (\partial_X (W_V X))_{J,K} + W_V X(\partial_X Y)_{I,K}, \\
&= \sum_J Y_{J,I} (\delta_{J,K} W_V) + W_V X(\partial_X Y)_{I,K}, \\
&= Y_{K,I} W_V + W_V X(\text{diag}(Y_I) - Y_IY_I^\top)(e_K ((W_Q^\top W_K X)_I)^\top + \delta_{I,K} X^\top W_Q^\top W_K). \\

\end{align}
$$


What is then the resulting first order change?


$$
\begin{align}

\sum_J (\partial_X f)_{I,J} E_J =& \sum_J W_V E_J Y_{J,I} \\
&+ \sum_J W_V X(\text{diag}(Y_I) - Y_IY_I^\top)e_J ((W_Q^\top W_K X)_I)^\top E_J \\
&+ \sum_J W_V X(\text{diag}(Y_I) - Y_IY_I^\top)\delta_{I,J} X^\top W_Q^\top W_K E_J, \\
=& W_V E Y_I \\
&+ \sum_J W_V X(\text{diag}(Y_I) - Y_IY_I^\top)e_J E_J^\top (W_Q^\top W_K X)_I \\
&+ W_V X(\text{diag}(Y_I) - Y_IY_I^\top)X^\top W_Q^\top W_K E_I, \\
=& W_V E Y_I \\
&+ W_V X(\text{diag}(Y_I) - Y_IY_I^\top)E^\top (W_Q^\top W_K X)_I \\
&+ W_V X(\text{diag}(Y_I) - Y_IY_I^\top)X^\top W_Q^\top W_K E_I. \\

\end{align}
$$


It's again what we would expect from first order! Unfortunately, this won't admit a similar matrix form as the examples above, simply because there is another dependence on $I$ than just a the end.

<!---
## More Involved Notions

These all are really special cases of differential forms and vector-valued (or even matrix-valued) differential forms. 
-->

## Summary

Taking derivatives of functions is a very natural and useful operation. However, taking the derivative of a matrix valued function w.r.t. a matrix has more structure than just a matrix, it's a 4-tensor. 

This blog went into some common methods for calculating derivatives of matrices or w.r.t. matrices. It then went on to work through a different notation/mechanism for calculating these derivatives such that the chain-rule is a simple operation. 

Using this 4-tensor technique, the derivatives of operations such as the attention mechanism underpinning transformers could be easily worked out.

I hope you find this as useful and interesting as I do. Hope to see you soon for future posts!