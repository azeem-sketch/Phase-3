const fetch = require('node-fetch');

async function createUser() {
    const email = 'test@example.com';
    const password = 'password123';
    const name = 'Test User';

    try {
        console.log('Creating user via Better Auth API...');

        const response = await fetch('http://localhost:3000/api/auth/sign-up/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
                name,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('✅ User created successfully!');
            console.log('');
            console.log('=== LOGIN CREDENTIALS ===');
            console.log('Email:    test@example.com');
            console.log('Password: password123');
            console.log('=========================');
        } else {
            if (data.error && data.error.includes('already exists')) {
                console.log('ℹ️  User already exists!');
                console.log('');
                console.log('=== LOGIN CREDENTIALS ===');
                console.log('Email:    test@example.com');
                console.log('Password: password123');
                console.log('=========================');
            } else {
                console.error('❌ Error:', data.error || data.message || 'Unknown error');
            }
        }
    } catch (error) {
        console.error('❌ Network error:', error.message);
        console.log('\nMake sure the frontend server is running on http://localhost:3000');
    }
}

createUser();
