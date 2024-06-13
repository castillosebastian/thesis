import numpy as np

def sample_latent_space(mu, sigma):
    """
    Sample from the latent space using the reparameterization trick.

    Parameters:
    - mu: numpy array, mean vector
    - sigma: numpy array, standard deviation vector

    Returns:
    - z: numpy array, sampled latent vector
    """
    # Ensure that sigma is positive
    sigma = np.maximum(sigma, 1e-10)
    print("sigma:", sigma)

    # Sample epsilon from a standard normal distribution
    epsilon = np.random.normal(0, 1, size=mu.shape)
    print("epsilon:", epsilon)

    # Compute the sampled latent vector z
    z = mu + sigma * epsilon

    return z

# Example usage:
# Define mean and standard deviation vectors
mu = np.array([0.0, 0.0])
sigma = np.array([1.0, 1.0])

# Sample from the latent space
z = sample_latent_space(mu, sigma)

print("Sampled latent vector:", z)
