// auth.js - Authentication flow utilities
export async function fetchProfile(token) {
  const resp = await fetch('/api/me', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return resp.json();
}

export async function login(usernameOrEmail, password) {
  const resp = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username_or_email: usernameOrEmail, password })
  });
  return resp.json();
}

export async function register(userInfo) {
  const resp = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userInfo)
  });
  return resp.json();
}

export async function validatePassport(provider, apiKey) {
  const resp = await fetch('/api/validate_passport', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ provider, api_key: apiKey })
  });
  return resp.json();
}

export async function forgotPassword(email) {
  const resp = await fetch('/api/forgot_password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });
  return resp.json();
}

export async function resetPassword(email, code, newPassword) {
  const resp = await fetch('/api/reset_password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, code, new_password: newPassword })
  });
  return resp.json();
}
