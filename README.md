# Cross-Entropy Loss is NOT What You Need

This is the GitHub repository for the paper "Harmonic Loss Trains Interpretable AI Models" [[arXiv]]() [[Twitter]]() [[Github]](https://github.com/KindXiaoming/grow-crystals).

![Harmonic Demo](./figures/weights_evolution.gif)

## What is Harmonic Loss?
- Harmonic logit $d_i$ is defined as the $l_2$ distance between the weight vector $\mathbf{w}_i$ and the input (query) $\mathbf{x}$:&nbsp; $d_i = \|\mathbf{w}_i - \mathbf{x}\|_2$.

- The probability $p_i$ is computed using the harmonic max function:
  $p_i = \text{HarmonicMax}(\mathbf{d})_i \equiv \frac{1/d_i^n}{\sum_{j} 1/d_j^n},$  where $n$ is the **harmonic exponent**—a hyperparameter that controls the heavy-tailedness of the probability distribution.

- Harmonic Loss achieves (1) **nonlinear separability**, (2)  **fast convergence**, (3) **scale invariance**, (4) **interpretability by design**, properties that are not available in cross-entropy loss.


## Reproducing results

Download the results from the following link: [Link](https://www.dropbox.com/scl/fi/9kj9aw1ymgsw0qya7sh8h/harmonic-data.zip?rlkey=6oc804x2r3ocmx3jidow4uqcp&st=e7i81esq&dl=0)

Figure 1: ``toy_points.ipynb``

Figure 2,3,7: ``notebooks/final_figures.ipynb``

Figure 4. ``notebooks/case_study_circle.ipynb``

Figure 5. ``notebooks/mnist.ipynb``

Figure 6. ``GPT2/function_vectors.ipynb``
