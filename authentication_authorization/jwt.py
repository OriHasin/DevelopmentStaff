"""
JWT (JSON Web Token) is a secure, compact way to authenticate users without storing session data on the server (instead of using session cookies which makes the system stateful).
A JWT includes a header, payload, and signature, and is used by the client to prove its identity with each request, its provide the ability of being stateless.

**Symmetric vs. Asymmetric Signing**
    - **Symmetric (e.g., HS256)**: Uses a single shared **secret key** for both signing (by the server) and verifying (by the server).
    - **Asymmetric (e.g., RS256)**: Uses a **private key** to sign the JWT and a **public key** to verify it.
      - The private key is kept secure on the authentication server.
      - The public key can be shared with other services to allow distributed verification.

**JWT Authentication Flow (Login)**
    1. **Login Request**:
       - Client sends login credentials to the authentication server.

    2. **Token Creation**:
       - Server authenticates credentials and, if valid, creates a JWT.
       - **Symmetric**: Server signs the JWT with a secret key.
       - **Asymmetric**: Server signs the JWT with a private key, allowing other services to verify it with the public key.

    3. **Token Usage**:
       - The server sends the JWT to the client.
       - Client includes the JWT in subsequent requests (e.g., in an `Authorization` header).

    4. **Token Verification**:
       - The server (or other authorized services) verifies the JWT.
       - **Symmetric**: The server uses the same secret key to verify the signature.
       - **Asymmetric**: The server or services use the public key to verify the token, probably uses key set json tokens trough an endpoint. """
